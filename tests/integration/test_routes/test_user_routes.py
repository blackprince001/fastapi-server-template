def test_create_user_via_api(client):
    response = client.post(
        "/api/v1/users/", json={"name": "API User", "email": "api@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "API User"
    assert "id" in data


# I havent added token authorization and authentication yet so cannot get users with this test
# def test_get_users_via_api(client):
#     client.post("/api/v1/users/", json={"name": "API User", "email": "api@example.com"})

#     response = client.get("/api/v1/users/")
#     assert response.status_code == 200
#     data = response.json()
#     assert len(data) == 1
#     assert data[0]["email"] == "api@example.com"
