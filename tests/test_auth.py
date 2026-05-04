def test_register_success(client):
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "123456"
    })

    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"


def test_register_duplicate(client):
    client.post("/auth/register", json={
        "email": "dup@example.com",
        "password": "123456"
    })

    response = client.post("/auth/register", json={
        "email": "dup@example.com",
        "password": "123456"
    })

    assert response.status_code == 400


def test_login_success(client):
    client.post("/auth/register", json={
        "email": "login@example.com",
        "password": "123456"
    })

    response = client.post("/auth/login", json={
        "email": "login@example.com",
        "password": "123456"
    })

    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "email": "wrong@example.com",
        "password": "123456"
    })

    response = client.post("/auth/login", json={
        "email": "wrong@example.com",
        "password": "wrongpass"
    })

    assert response.status_code == 401