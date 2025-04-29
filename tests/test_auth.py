import os

from fastapi.testclient import TestClient
from app.main import app
from app.core.config import DATABASE_PATH

client = TestClient(app)
headers = None


def __prepare_to_test():
    db_path = DATABASE_PATH
    if os.path.exists(db_path):
        os.remove(db_path)


def test_register():
    __prepare_to_test()
    data = {"username": "vanya", "password": "markin", "email": "ivan@mail.ru"}
    response = client.post("/auth/register", json=data)
    assert response.status_code == 200
    assert "id" in response.json()


def test_register_wrong():
    data = {"username": "vanya", "password": "markin", "email": "ivan@mail.ru"}
    response = client.post("/auth/register", json=data)
    assert response.status_code == 400


def test_authorize_wrong():
    data = {"username": "VANYA", "password": "MARKIN"}
    response = client.post("/auth/login", data=data)
    assert response.status_code == 401


def test_authorize():
    global headers
    data = {"username": "vanya", "password": "markin"}
    response = client.post("/auth/login", data=data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    headers = {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_add_auth_logs():
    global headers
    data = {"auth_at": 1682446412345}
    response = client.post("/user/auth_logs", json=data, headers=headers)
    assert response.status_code == 200
    data = {"auth_at": 1682890980952}
    response = client.post("/user/auth_logs", json=data, headers=headers)
    assert response.status_code == 200
    data = {"auth_at": 1699999402244}
    response = client.post("/user/auth_logs", json=data, headers=headers)
    assert response.status_code == 200


def test_add_auth_logs_wrong():
    response = client.post("/user/auth_logs")
    assert response.status_code == 401

    global headers
    data = {"Некорректно": "ABCDEFGH"}
    response = client.post("/user/auth_logs", json=data, headers=headers)
    assert response.status_code == 422

    data = {"auth_at": "ABCDEFGH"}
    response = client.post("/user/auth_logs", json=data, headers=headers)
    assert response.status_code == 422

    data = {"Incorrect": 1699999402244}
    response = client.post("/user/auth_logs", json=data, headers=headers)
    assert response.status_code == 422


def test_get_auth_logs():
    global headers
    response = client.get("/user/auth_logs", headers=headers)
    assert response.status_code == 200
    assert response.json() == [{"auth_at": 1682446412345},
                               {"auth_at": 1682890980952},
                               {"auth_at": 1699999402244}]


def test_get_auth_logs_wrong():
    response = client.get("/user/auth_logs")
    assert response.status_code == 401
