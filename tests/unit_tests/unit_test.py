import pytest


@pytest.mark.parametrize(
        "user_id, status_code, error, value",
        [
            (1, 200, False, "jack_niklson@gmail.com"),
            (2, 200, False, "mindi_star@mail.ru"),
            (999, 404, True, "Пользователя нет в базе!")
        ])
@pytest.mark.asyncio
async def test_get_user(client, add_data_to_db,
                        user_id: int, status_code: int, error: bool,
                        value: str) -> None:
    """Тестирование получения информации о пользователе."""
    response = await client.get(f"/user/get_user/{user_id}")
    data = response.json()
    assert data['status_code'] == status_code
    if error:
        assert data['message'] == value
    else:
        assert data['message']['email'] == value


@pytest.mark.parametrize(
        ("first_name, last_name, age, salary,"
         "email, status_code, error_num, value"),
        [
            ("Mikle", "Karlson", 27, 10000, "mikle_little_cat@gmail.com",
             200, 0, "Пользователь добавлен!"),
            ("Karl", "Nilson", 25, 20000, "karl_little_catcom",
             422, 2, "Value error, Неверный формат почты"),
            ("Ka", "Nilson", 25, 20000, "karl_little_catcom", 422, 2,
             "Value error, Длина имени должна быть не менее 3 символов"),
            ("Karl", "Ni", 25, 20000, "karl_little_catcom", 422, 2,
             "Value error, Длина фамилии должна быть не менее 3 символов"),
            ("Karl", "Nilson", '25', 20000, "karl_little_catcom",
             422, 2, "Value error, Возраст должен быть числом"),
            ("Karl", "Nilson", 125, 20000, "karl_little_catcom", 422, 2,
             "Value error, Возраст должен быть в пределах от 0 до 120"),
            ("Karl", "Nilson", 25, -1, "karl_little_catcom",
             422, 2, "Value error, Заработная плата должна быть от 0"),
            ("Karl", "Nilson", 25, "20000", "karl_little_catcom",
             422, 2, "Value error, Заработная плата должна быть числом"),
        ])
@pytest.mark.asyncio
async def test_add_user(client, add_data_to_db,
                        first_name: str, last_name: str, age: int,
                        salary: float | int, email: str,
                        status_code: int, error_num: int,
                        value: str) -> None:
    """Тестирование добавления пользователя."""
    data_request = {
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "salary": salary,
        "email": email
    }
    response = await client.post("/user/add_user", json=data_request)
    data = response.json()
    if error_num == 0:
        assert data['status_code'] == status_code
        assert data['message'] == value
    elif error_num == 2:
        assert response.status_code == 422
        assert data['detail'][0]["msg"] == value


@pytest.mark.parametrize(
        ("user_id, first_name, last_name, age, salary,"
         "email, status_code, error_num, value"),
        [
            (1, "Karl", "Nilson", 25, 20000, "karl_little_cat@gmail.com",
             200, 0, "no"),
            (999, "Karl", "Nilson", 25, 20000, "karl_little_cat@gmail.com",
             404, 1, "no"),
            (2, "Karl", "Nilson", 25, 20000, "karl_little_catcom",
             422, 2, "Value error, Неверный формат почты"),
            (2, "Ka", "Nilson", 25, 20000, "karl_little_catcom", 422, 2,
             "Value error, Длина имени должна быть не менее 3 символов"),
            (2, "Karl", "Ni", 25, 20000, "karl_little_catcom", 422, 2,
             "Value error, Длина фамилии должна быть не менее 3 символов"),
            (2, "Karl", "Nilson", '25', 20000, "karl_little_catcom",
             422, 2, "Value error, Возраст должен быть числом"),
            (2, "Karl", "Nilson", 125, 20000, "karl_little_catcom", 422, 2,
             "Value error, Возраст должен быть в пределах от 0 до 120"),
            (2, "Karl", "Nilson", 25, -1, "karl_little_catcom",
             422, 2, "Value error, Заработная плата должна быть от 0"),
            (2, "Karl", "Nilson", 25, "20000", "karl_little_catcom",
             422, 2, "Value error, Заработная плата должна быть числом"),
        ])
@pytest.mark.asyncio
async def test_update_user(client, add_data_to_db, user_id: int,
                           first_name: str, last_name: str, age: int,
                           salary: float | int, email: str,
                           status_code: int, error_num: int,
                           value: str | None) -> None:
    """Тестирование изменения информации о пользователе."""
    data_request = {
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "salary": salary,
        "email": email
    }
    response = await client.put(f"/user/update_user/{user_id}",
                                json=data_request)
    data = response.json()
    if error_num == 0:
        assert data['status_code'] == status_code
        assert data[
            'message'
            ] == f"Данные пользователя с ID: {user_id} изменены!"
    elif error_num == 1:
        assert data['status_code'] == status_code
        assert data['message'] == f"Пользователь с ID: {user_id} не найден!"
    elif error_num == 2:
        assert response.status_code == 422
        assert data['detail'][0]["msg"] == value


@pytest.mark.parametrize(
        "user_id, status_code, error",
        [
            (1, 200, False),
            (2, 200, False),
            (999, 404, True)
        ])
@pytest.mark.asyncio
async def test_delete_user(client, add_data_to_db,
                           user_id: int, status_code: int,
                           error: bool) -> None:
    """Тестирование удаления пользователя."""
    response = await client.delete(f"/user/delete_user/{user_id}")
    data = response.json()
    assert data['status_code'] == status_code
    if error:
        assert data['message'] == f"Пользователь с ID: {user_id} не найден!"
    else:
        assert data['message'] == f"Пользователь с ID: {user_id} удалён!"
