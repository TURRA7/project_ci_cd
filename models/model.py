"""
Модели валидации данных pydantic.

Classes:

    UserInfo: Пользователь
"""
from pydantic import BaseModel, EmailStr


class UserInfo(BaseModel):
    first_name: str
    last_name: str
    age: int
    salary: float
    email: EmailStr
