from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models.model import UserInfo
from database.FDataBase import (get_session, get_one_user,
                                add_one_user, update_user_info,
                                delete_one_user)


router_user = APIRouter(prefix="/user")


@router_user.get("/get_user/{user_id}")
async def get_user(user_id: int,
                   session: AsyncSession = Depends(get_session)
                   ) -> dict | str:
    """
    Получение информации о пользователе.

    Args:

        user_id: ID пользователя

    Returns:

        dict{
        'message': dict{инфо о пользователе} | str(ненахождение пользователя),
        'status_code': int(статус код)
        }
    """
    user = await get_one_user(user_id=user_id, session=session)
    return {"message": user['message'], "status_code": user["status_code"]}


@router_user.post("/add_user")
async def add_user(data: UserInfo,
                   session: AsyncSession = Depends(get_session)
                   ) -> str:
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

        dict{
        'message': str(добавление/ошибка добавления пользователя в базу),
        'status_code': int(статус код)
        }
    """
    new_user = await add_one_user(first_name=data.first_name,
                                  last_name=data.last_name, age=data.age,
                                  salary=data.salary, email=data.email,
                                  session=session)
    return {"message": new_user['message'],
            "status_code": new_user["status_code"]}


@router_user.put("/update_user/{user_id}")
async def update_user(user_id: int, data: UserInfo,
                      session: AsyncSession = Depends(get_session)
                      ) -> str:
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

        dict{
        'message': str(изменениие информации/ненахождение пользователя в базе),
        'status_code': int(статус код)
        }
    """
    new_info = await update_user_info(user_id=user_id,
                                      first_name=data.first_name,
                                      last_name=data.last_name, age=data.age,
                                      salary=data.salary, email=data.email,
                                      session=session)
    return {"message": new_info['message'],
            "status_code": new_info["status_code"]}


@router_user.delete("/delete_user/{user_id}")
async def delete_user(user_id: int,
                      session: AsyncSession = Depends(get_session)
                      ) -> str:
    """
    Удаление пользователя.

    Args:

        user_id: ID пользователя

    Returns:

        dict{
        'message': str(удаление/ненахождение пользователя в базе),
        'status_code': int(статус код)
        }
    """
    delete_user = await delete_one_user(user_id=user_id, session=session)
    return {"message": delete_user['message'],
            "status_code": delete_user["status_code"]}
