def test_health(client):
    response = client.get("/health")

    print(response.json())
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"