from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
headers = None


def __get_headers():
    global headers
    try:
        data = {"username": "mary", "password": "fun", "email": "mary@mail.ru"}
        response = client.post("/auth/register", json=data)
        assert response.status_code == 200
        assert "id" in response.json()
    except AssertionError:
        pass
    data = {"username": "mary", "password": "fun"}
    response = client.post("/auth/login", data=data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    headers = {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_parse():
    __get_headers()
    global headers

    text = """GND  XX-1 GG-22
*  DDC-12 D20-2
*  DD1-123 DD1-222
*  DD1-221 DD1-412
"""

    result = """GND 123
GND 222
GND 221
GND 412
"""

    data = {"text": text,
            "obj_name": "DD1"}
    response = client.post("/parse/netlist", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json()["result"] == result


def test_parse_wrong():
    text = """GND  XX-1 GG-22
*  DDC-12 D20-2
*  DD1-123 DD1-222
*  DD1-221 DD1-412
"""

    data = {"text": text,
            "obj_name": "DD1"}
    response = client.post("/parse/netlist", json=data)
    assert response.status_code == 401
