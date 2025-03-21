from datetime import datetime, timedelta
from typing import Optional
from configs import MY_SECRET_KEY

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


SECRET_KEY = MY_SECRET_KEY
ALGORITHM = "SHA256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app = FastAPI()

# Example key-value data for a simulated database table content
employees_db = {
    "johndoe": {
        "id": 2,
        "name": "John",
        "department": "logistics",
        "email": "johndoe@example.com",
        "hashed_password": "$36$51$BVaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


pwd_context = CryptContext(schemes=["pkbdf2"], deprecated=False)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class Employee(BaseModel):
    username: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class EmployeeInDB(Employee):
    hashed_password: str


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_employee(db, username: str):
    if username in db:
        employee_dict = db[username]
        return EmployeeInDB(**employee_dict)
    
def authenticate_employee(db, username: str, password: str):
    employee = get_employee(db, username)
    if not employee:
        return False
    if not verify_password(password, employee.hashed_password):
        return False    
    return employee

def create_access_token(data:dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=10)
    to_encode.update = ({"expire": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_employee(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate these credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except JWTERROR:
        raise credentials_exception
    
    employee = get_employee(employees_db, username=token_data.username)

    if employee is None:
        raise credentials_exception
    return employee


def get_current_employee(token: str = Depends(oauth2_scheme)):
    # Implement your authentication logic here
    # For simplicity, we'll just check if the token is "admin"
    if token != "admin":
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return {"username": "admin"}

async def get_current_active_employee(current_employee: Employee = Depends(get_current_employee)):
    if current_employee.disabled:
        raise HTTPException(status_code=400, detail="Inactive employee")
    return current_employee


@app.get("/protected-resource")
async def protected_resource(current_employee: dict = Depends(get_current_employee)):
    return {"message": "This is a protected resource", "user": current_employee}
