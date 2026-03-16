import pytest


@pytest.mark.asyncio
async def test_create_task(client, auth_headers):
    response = await client.post("/tasks/", json={
        "title": "Изучить FastAPI",
        "description": "Прочитать документацию",
        "priority": "high",
    }, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Изучить FastAPI"
    assert data["status"] == "todo"


@pytest.mark.asyncio
async def test_get_tasks(client, auth_headers):
    # Создаём несколько задач
    for i in range(3):
        await client.post("/tasks/", json={"title": f"Task {i}"}, headers=auth_headers)

    response = await client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.asyncio
async def test_update_task(client, auth_headers):
    create_resp = await client.post("/tasks/", json={"title": "Old title"}, headers=auth_headers)
    task_id = create_resp.json()["id"]

    response = await client.patch(f"/tasks/{task_id}", json={
        "title": "New title",
        "status": "in_progress",
    }, headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["title"] == "New title"
    assert response.json()["status"] == "in_progress"


@pytest.mark.asyncio
async def test_delete_task(client, auth_headers):
    create_resp = await client.post("/tasks/", json={"title": "To delete"}, headers=auth_headers)
    task_id = create_resp.json()["id"]

    delete_resp = await client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert delete_resp.status_code == 204

    get_resp = await client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_unauthorized_access(client):
    """Без токена — 403"""
    response = await client.get("/tasks/")
    assert response.status_code == 403