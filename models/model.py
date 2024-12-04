from pydantic import BaseModel, EmailStr


class User(BaseModel):
    first_name: str
    last_name: str
    age: int
    salary: float
    email: EmailStr
