import pytest


@pytest.mark.asyncio
async def test_register_success(client):
    response = await client.post("/auth/register", json={
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "securepass",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert "hashed_password" not in data  # пароль не должен утекать в ответ


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    payload = {"email": "dup@example.com", "username": "user1", "password": "pass1234"}
    await client.post("/auth/register", json=payload)

    response = await client.post("/auth/register", json={**payload, "username": "user2"})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_success(client):
    await client.post("/auth/register", json={
        "email": "logintest@example.com",
        "username": "loginuser",
        "password": "mypassword",
    })

    response = await client.post("/auth/login", params={
        "email": "logintest@example.com",
        "password": "mypassword",
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post("/auth/register", json={
        "email": "user@test.com", "username": "u", "password": "correctpass"
    })
    response = await client.post("/auth/login", params={
        "email": "user@test.com", "password": "wrongpass"
    })
    assert response.status_code == 401