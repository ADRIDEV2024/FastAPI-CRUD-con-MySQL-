from pydantic import BaseModel
from typing import Optional

class EmployeeSchema(BaseModel):
    id: Optional[str]
    name: str
    password: str
    age: int
    department: str
    position: str
    years_worked: str
    salary_month: int