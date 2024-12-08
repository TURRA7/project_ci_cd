"""
Модели валидации данных pydantic.

Classes:

    UserInfo: Пользователь
"""
import re
from pydantic import BaseModel, field_validator


class UserInfo(BaseModel):
    first_name: str
    last_name: str
    age: int
    salary: float
    email: str

    class Config:
        anystr_strip_whitespace = True

    @field_validator('email')
    def validate_email(cls, value: str) -> str:
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise ValueError('Неверный формат почты')
        return value

    @field_validator('first_name')
    def validate_first_name(cls, value: str) -> str:
        if len(value) < 3:
            raise ValueError(
                'Длина имени должна быть не менее 3 символов')
        return value

    @field_validator('last_name')
    def validate_last_name(cls, value: str) -> str:
        if len(value) < 3:
            raise ValueError(
                'Длина фамилии должна быть не менее 3 символов')
        return value
