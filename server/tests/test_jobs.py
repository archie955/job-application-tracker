import pytest
from models.datatypes import ApplicationStatus

def auth_headers(authenticated_user):
    return {
        "Authorization": f"Bearer {authenticated_user['access_token']}"
    }

def create_sample_job(client, authenticated_user, status=ApplicationStatus.NOT_APPLIED, unique: str = ""):
    job = {
        "employer": "TestCorp",
        "title": f"Test Job {unique}",
        "description": "Test description",
        "status": status,
        "location": "Remote",
        "deadline": "2030-01-01"
    }

    response = client.post("/jobs/create",
                           json=job,
                           headers=auth_headers(authenticated_user)
                           )
    
    assert response.status_code == 200
    return response.json()

def test_create_job(client, authenticated_user):
    job = create_sample_job(client, authenticated_user)

    assert job["employer"] == "TestCorp"
    assert job["title"] == "Test Job "
    assert "id" in job
    assert job["status"] == ApplicationStatus.NOT_APPLIED
    assert job["location"] == "Remote"
    assert job["description"] == "Test description"

def test_create_job_requires_auth(client):
    response = client.post("/jobs/create", json={})
    assert response.status_code == 401

def test_get_jobs(client, authenticated_user):
    create_sample_job(client, authenticated_user)

    response = client.get(
        "/jobs/get",
        headers=auth_headers(authenticated_user)
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["employer"] == "TestCorp"

def test_get_jobs_pagination(client, authenticated_user):
    for i in range(2):
        create_sample_job(client, authenticated_user, unique=str(i))

    newjob = {
        "employer": "NewTest",
        "title": "Test Job",
        "description": "Test description",
        "status": ApplicationStatus.NOT_APPLIED,
        "location": "Remote",
        "deadline": "2030-01-01"
    }

    client.post("/jobs/create", 
                json=newjob,
                headers=auth_headers(authenticated_user)
                )
    
    for i in range(2):
        create_sample_job(client, authenticated_user, unique=str(i+2))

    response = client.get(
        "/jobs/get?skip=2&limit=2",
        headers=auth_headers(authenticated_user)
    )
    data = response.json()
    print(data)

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["employer"] == "NewTest"
    assert data[1]["employer"] == "TestCorp"

def test_get_single_job(client, authenticated_user):
    job = create_sample_job(client, authenticated_user)

    response = client.get(
        f"/jobs/get/{job['id']}",
        headers=auth_headers(authenticated_user)
    )

    assert response.status_code == 200
    assert response.json()["id"] == job["id"]

def test_get_nonexistent_job(client, authenticated_user):
    response = client.get(
        "/jobs/get/9999",
        headers=auth_headers(authenticated_user)
    )

    assert response.status_code == 404

def test_update_job(client, authenticated_user):
    job = create_sample_job(client, authenticated_user)

    updated_data = {
        "employer": "UpdatedCorp",
        "title": "Senior Test Job",
        "description": "Updated description",
        "status": ApplicationStatus.APPLIED,
        "location": "London",
        "deadline": "2031-01-01"
    }

    response = client.put(
        f"/jobs/update/{job['id']}",
        json=updated_data,
        headers=auth_headers(authenticated_user)
    )

    assert response.status_code == 200
    data = response.json()
    assert data["employer"] == "UpdatedCorp"
    assert data["status"] == ApplicationStatus.APPLIED

def test_update_nonexistent_job(client, authenticated_user):
    updated_job = {
        "employer": "DoesntMatter",
        "title": "None",
        "description": "None",
        "status": ApplicationStatus.NOT_APPLIED,
        "location": "Nowhere",
        "deadline": "2030-01-01"
    }

    response = client.put(
        "/jobs/update/9999",
        json=updated_job,
        headers=auth_headers(authenticated_user)
    )

    assert response.status_code == 404

def test_delete_job(client, authenticated_user):
    job = create_sample_job(client, authenticated_user)

    response = client.delete(
        f"/jobs/delete/{job['id']}",
        headers=auth_headers(authenticated_user)
    )

    assert response.status_code == 204

    response = client.get(
        f"/jobs/get/{job['id']}",
        headers=auth_headers(authenticated_user)
    )

    assert response.status_code == 404

def test_delete_nonexistent_job(client, authenticated_user):
    response = client.delete(
        "/jobs/delete/9999",
        headers=auth_headers(authenticated_user)
    )

    assert response.status_code == 404

