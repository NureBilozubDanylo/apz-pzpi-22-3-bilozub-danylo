from pydantic import BaseModel

class EmployeeBase(BaseModel):
    shop_id: int
    position: str
    salary_without_percent: int

    model_config = {
        "from_attributes": True
    }

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    user_id: int
