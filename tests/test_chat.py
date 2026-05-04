def create_user_and_token(client):
    client.post("/auth/register", json={
        "email": "chat@example.com",
        "password": "123456"
    })

    res = client.post("/auth/login", json={
        "email": "chat@example.com",
        "password": "123456"
    })

    return res.json()["access_token"]


def test_chat_history_empty(client):
    token = create_user_and_token(client)

    response = client.get(
        "/chat/history",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_chat_stream(client):
    token = create_user_and_token(client)

    response = client.post(
        "/chat",
        json={"message": "Hello"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_get_thread_not_found(client):
    token = create_user_and_token(client)

    response = client.get(
        "/chat/999",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404