from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
headers = None


def __get_headers():
    global headers
    try:
        data = {"username": "leon", "password": "sun", "email": "leon@mail.ru"}
        response = client.post("/auth/register", json=data)
        assert response.status_code == 200
        assert "id" in response.json()
    except AssertionError:
        pass
    data = {"username": "leon", "password": "sun"}
    response = client.post("/auth/login", data=data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    headers = {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_get_user_info():
    __get_headers()
    global headers
    response = client.get("/user/me", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"username": "leon",
                               "email": "leon@mail.ru"}


def test_get_user_info_wrong():
    response = client.get("/user/me")
    assert response.status_code == 401


def test_add_history():
    global headers

    result = """GND 123
GND 222
GND 221
GND 412
"""

    data = {"data": result,
            "timestamp": 1682446400000}
    response = client.post("/user/results", json=data, headers=headers)
    assert response.status_code == 200


def test_add_history_wrong():
    result = """GND 123
GND 222
GND 221
GND 412
"""

    data = {"data": result,
            "timestamp": 1682446400000}
    response = client.post("/user/results", json=data)
    assert response.status_code == 401

    global headers
    data = {"Неверная структура": "передаваемых данных"}
    response = client.post("/user/results", json=data, headers=headers)
    assert response.status_code == 422


def test_get_history():
    global headers

    result = """GND 123
GND 222
GND 221
GND 412
"""

    response = client.get("/user/results", headers=headers)
    assert response.status_code == 200
    assert response.json() == [{"data": result,
                                "timestamp": 1682446400000}]


def test_get_history_wrong():
    result = """GND 123
GND 222
GND 221
GND 412
"""

    data = {"data": result,
            "timestamp": 1682446400000}
    response = client.post("/user/results", json=data)
    assert response.status_code == 401


def test_delete_history_wrong():
    response = client.delete("/user/delete_results")
    assert response.status_code == 401


def test_delete_history():
    global headers

    response = client.delete("/user/delete_results", headers=headers)
    assert response.status_code == 200

    response = client.get("/user/results", headers=headers)
    assert response.status_code == 200
    assert response.json() == []


def test_change_password():
    global headers

    passwords = {"old": "sun",
                 "new": "m_a_r_k_i_n"}
    response = client.put("/user/change_password", json=passwords, headers=headers)
    assert response.status_code == 200


def test_change_password_wrong():
    passwords = {"old": "sun",
                 "new": "m_a_r_k_i_n"}
    response = client.put("/user/change_password", json=passwords)
    assert response.status_code == 401

    global headers
    passwords = {"old": "sun"}
    response = client.put("/user/change_password", json=passwords, headers=headers)
    assert response.status_code == 422

    passwords = {"old": "неверный пароль",
                 "new": "m_a_r_k_i_n"}
    response = client.put("/user/change_password", json=passwords, headers=headers)
    assert response.status_code == 400

    passwords = {"old": "sun",
                 "неверная структура": 34243234}
    response = client.put("/user/change_password", json=passwords, headers=headers)
    assert response.status_code == 422

    passwords = {"new": "m_a_r_k_i_n"}
    response = client.put("/user/change_password", json=passwords, headers=headers)
    assert response.status_code == 422


def test_delete_account_wrong():
    response = client.delete("/user/delete_account")
    assert response.status_code == 401


def test_delete_account():
    global headers
    response = client.delete("/user/delete_account", headers=headers)
    assert response.status_code == 200
