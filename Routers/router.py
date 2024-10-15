from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED
from schema.employee_schema import EmployeeSchema
from config.db import engine
from models.employees import employees
from werkzeug.security import generate_password_hash, check_password_hash 
from typing import List

employee = APIRouter()

@employee.get("/employees")
async def get_users(page: int = 1, page_size: int = 20):
    offset = (page - 1) * page_size
    with engine.connect() as conn:
        result = conn.execute(employees.select().offset(offset).limit(page_size)).fetchall()
        total = conn.execute(employees.count()).scalar()
    return {"employees": result, "total": total, "page": page, "page_size": page_size}

@employee.get("/api/employees", response_model=List[EmployeeSchema], summary="Get all employees", description="Retrieve a list of all employees.")
async def get_employees():
    with engine.connect() as conn:
        result = conn.execute(employees.select()).fetchall()
        return result

@employee.get("/api/employees/{employee_id}", response_model=EmployeeSchema)
async def get_employee(employee_id:str):
   with engine.connect as conn:
      result = conn.execute(employees.select().where(employees.c.id == employee_id)).first()

      return result
   
@employee.get("/employees/{employee_name}")
async def search_employees(name: str | None):
    results = employees
    if name:
        results = [employee for employee in results if name.lower() in employee["name"].lower()]
        
@employee.get("/employees/{employee_department}")
async def search_by_deparment(department: str | None):
    results = employees
    if department:
        results = [employee for employee in results if department.lower() in employee["name"].lower()]
        

@employee.post("/api/employees", status_code=HTTP_201_CREATED)
async def create_employee(data_employee: EmployeeSchema):
    with engine.connect() as conn:
        new_employee = data_employee.dict()
        new_employee["password"] = generate_password_hash(data_employee.password, "pbkdf2:sha256:30", 50)
        conn.execute(employees.insert().values(new_employee))
    return {"message": "Employee created successfully"}


@employee.put("/api/employees/{employee_id}")
async def update_employee(data_update:EmployeeSchema, employee_id:str):
    encrypt_passw = generate_password_hash(data_update.password, "pbkdf2:sha256:30", 50)
    with engine.connect as conn:
         conn.execute(employees.update().values(name=data_update.name, salary=data_update.salary_month, password=encrypt_passw
         ).where(employees.c.id == employee_id))

         result = conn.execute(employees.select().where(employees.c.id == employee_id)).first()

         return result
                            


