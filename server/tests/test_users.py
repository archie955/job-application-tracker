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

    assert response.status_code == 400

def test_login(client):
    user = {
        "email": "login@example.com",
        "password": "loginpassword"
    }
    client.post("/users/register", json=user)

    response = client.post("/users/login", json=user)

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
                           json={
                               "email": "incorrect@example.com",
                               "password": "incorrectpassword"
                           }
                        )
    assert response.status_code == 401
    

def test_logout(client, authenticated_user):
    response = client.get("/users/logout",
                          headers={
                          "Authorization": f"Bearer {authenticated_user['access_token']}"
                          }
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
                             headers={
                                 "Authorization": f"Bearer {authenticated_user['access_token']}"
                             }
                             )
    assert response.status_code == 204
    
def test_update_email(client, authenticated_user):
    response = client.put("/users/me/email",
        json={"email": "newemail@example.com"},
        headers={
            "Authorization": f"Bearer {authenticated_user['access_token']}"
        }
        )

    assert response.status_code == 200
    assert response.json()["email"] == "newemail@example.com"

def test_update_same_email(client, authenticated_user):
    response = client.put("/users/me/email",
        json={"email": authenticated_user["email"]},
        headers={
            "Authorization": f"Bearer {authenticated_user['access_token']}"
        }
        )

    assert response.status_code == 400

def test_update_password(client, authenticated_user):
    response = client.put("/users/me/password",
        json={"password": "newsecurepassword"},
        headers={
            "Authorization": f"Bearer {authenticated_user['access_token']}"
        }
        )

    assert response.status_code == 200

def test_update_same_password(client, authenticated_user):
    response = client.put("/users/me/password",
        json={"password": "securepassword"},
        headers={
            "Authorization": f"Bearer {authenticated_user['access_token']}"
        }
    )

    assert response.status_code == 400