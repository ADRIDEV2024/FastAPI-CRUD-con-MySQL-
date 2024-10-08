from pydantic import BaseModel, Field

class EmployeeSchema(BaseModel):
    id: str
    name: str
    salary: float
    password: str = Field(..., min_length=8)
