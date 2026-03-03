import pytest

def auth_headers(authenticated_user):
    return {
        "Authorization": f"Bearer {authenticated_user['access_token']}"
    }

def test_registration(client):
    response = client.post(
        "/users/register",
        json={
            "email": "test@example.com",
            "password": "testpassword"
        }
    )

    assert response.status_code == 201

    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_duplicate_registration(client):
    user = {
        "email": "duplicate@example.com",
        "password": "duplicatepassword"
    } 

    client.post("/users/register", json=user)
    response = client.post("/users/register", json=user)

    assert response.status_code == 409

def test_login(client):
    user = {
        "email": "login@example.com",
        "password": "loginpassword"
    }
    client.post("/users/register", json=user)

    response = client.post("/users/login",
                           data={
                               "username": user["email"],
                               "password": user["password"]
                               },
                               headers={"Content-Type": "application/x-www-form-urlencoded"}
                               )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_incorrect_login(client):
    user = {
        "email": "incorrect@example.com",
        "password": "correctpassword"
    }

    client.post("/users/register", json=user)

    response = client.post("/users/login",
                           data={
                               "username": user["email"],
                               "password": "incorrectpassword"
                               },
                               headers={"Content-Type": "application/x-www-form-urlencoded"}
                               )
    assert response.status_code == 403
    

def test_logout(client, authenticated_user):
    response = client.get("/users/logout",
                          headers=auth_headers(authenticated_user)
                          )
    assert response.status_code == 200
    assert response.json()["message"] == "successfully logged out"

def test_refresh(client, authenticated_user):
    response = client.post("/users/refresh",
                           cookies={
                               "refresh_token": authenticated_user["refresh_token"]
                           }
                           )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "refresh_token" in response.cookies
    
def test_missing_refresh(client):
    response = client.post("/users/refresh")

    assert response.status_code == 401

def test_delete(client, authenticated_user):
    response = client.delete("/users/me",
                             headers=auth_headers(authenticated_user)
                             )
    assert response.status_code == 204
    
def test_update_email(client, authenticated_user):
    response = client.put("/users/me/email",
        json={"email": "newemail@example.com"},
        headers=auth_headers(authenticated_user)
        )

    assert response.status_code == 200
    assert response.json()["email"] == "newemail@example.com"

def test_update_same_email(client, authenticated_user):
    response = client.put("/users/me/email",
        json={"email": authenticated_user["email"]},
        headers=auth_headers(authenticated_user)
        )

    assert response.status_code == 400

def test_update_password(client, authenticated_user):
    response = client.put("/users/me/password",
        json={"password": "newsecurepassword"},
        headers=auth_headers(authenticated_user)
        )

    assert response.status_code == 200

def test_update_same_password(client, authenticated_user):
    response = client.put("/users/me/password",
        json={"password": authenticated_user["password"]},
        headers=auth_headers(authenticated_user)
        )

    assert response.status_code == 400