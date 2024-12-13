"""
Модели валидации данных pydantic.

Classes:

    UserInfo: Пользователь
"""
import re
from typing import Union
from pydantic import BaseModel, field_validator, ConfigDict


class UserInfo(BaseModel):
    model_config = ConfigDict(from_orm=True)
    first_name: str
    last_name: str
    age: int
    salary: Union[int, float]
    email: str

    @field_validator('first_name')
    def validate_first_name(cls, value: str) -> str:
        if len(value) < 3:
            raise ValueError('Длина имени должна быть не менее 3 символов')
        return value

    @field_validator('last_name')
    def validate_last_name(cls, value: str) -> str:
        if len(value) < 3:
            raise ValueError('Длина фамилии должна быть не менее 3 символов')
        return value

    @field_validator('age', mode="before")
    def validate_age_type(cls, value: Union[int, float]) -> Union[int, float]:
        if not isinstance(value, (int, float)):
            raise ValueError('Возраст должен быть числом')
        return value

    @field_validator('age', mode="after")
    def validate_age_range(cls, value: Union[int, float]) -> Union[int, float]:
        if value < 0 or value > 120:
            raise ValueError('Возраст должен быть в пределах от 0 до 120')
        return value

    @field_validator('salary', mode="before")
    def validate_salary_type(cls, value: Union[int, float]) -> Union[int,
                                                                     float]:
        if not isinstance(value, (int, float)):
            raise ValueError('Заработная плата должна быть числом')
        return value

    @field_validator('salary', mode="after")
    def validate_salary_range(cls, value: Union[int, float]) -> Union[int,
                                                                      float]:
        if value < 0:
            raise ValueError('Заработная плата должна быть от 0')
        return value

    @field_validator('email')
    def validate_email(cls, value: str) -> str:
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise ValueError('Неверный формат почты')
        return value
