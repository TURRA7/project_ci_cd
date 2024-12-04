from fastapi import APIRouter

from models.model import UserInfo


router_user = APIRouter(prefix="/user")


@router_user.get("/get_user/{user_id}")
async def get_user(item_id: int) -> dict:
    """
    Получение информации о пользователе.

    Args:
        user_id: ID пользователя

    Returns:
        ...
    """
    ...


@router_user.post("/add_user")
async def add_user(data: UserInfo) -> str:
    """
    Добавление пользователя в базу данных.

    Args:
        user_id: ID пользователя

        first_name: Имя пользователя
        last_name: Фамилия пользователя
        age: Количество полных лет пользователя
        salary: Заработная плата пользователя
        email: Электронная почта пользователя

    Returns:
        ...
    """
    ...


@router_user.put("/update_user/{user_id}")
async def update_user(user_id: int, data: UserInfo) -> str:
    """
    Обновление информации о пользователе в базе данных.

    Args:
        user_id: ID пользователя

        first_name: Имя пользователя
        last_name: Фамилия пользователя
        age: Количество полных лет пользователя
        salary: Заработная плата пользователя
        email: Электронная почта пользователя

    Returns:
        ...
    """
    ...


@router_user.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    """
    Удаление пользователя.

    Args:
        user_id: ID пользователя

    Returns:
        ...
    """
