from pydantic import BaseModel, ConfigDict


class EmployeeBase(BaseModel):
    full_name: str
    job_title: str
    country: str
    salary: float


class EmployeeCreate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
