def test_full_user_workflow(client):
    create_response = client.post(
        "/api/v1/users/", json={"name": "E2E User", "email": "e2e@example.com"}
    )
    assert create_response.status_code == 200

    get_response = client.get("/api/v1/users/")
    assert get_response.status_code == 200
    users = get_response.json()
    assert len(users) == 1
    assert users[0]["email"] == "e2e@example.com"
