import pytest
from models.datatypes import ApplicationStatus, AssessmentType

# Could use a decorator to immediately check every request for auth? consider

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

def create_sample_assessment(client, authenticated_user, job_id, type=AssessmentType.ONLINE_ASSESSMENT):
    assessment = {
        "job_id": job_id,
        "type": type,
        "description": "Test description",
        "completed": True,
        "deadline": "2030-01-01"
    }

    response = client.post(f"/jobs/create/{job_id}",
                           json=assessment,
                           headers=auth_headers(authenticated_user)
                           )
    
    assert response.status_code == 200
    return response.json()["assessments"][0]

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

def test_create_assessment(client, authenticated_user):
    job = create_sample_job(client, authenticated_user)

    assessment = create_sample_assessment(client, authenticated_user, job["id"])

    assert assessment["job_id"] == job["id"]
    assert assessment["type"] == AssessmentType.ONLINE_ASSESSMENT
    assert assessment["description"] == "Test description"
    assert assessment["completed"] == True

def test_create_assessment_requires_auth(client, authenticated_user):
    response = client.post("/jobs/create/1", json={})
    assert response.status_code == 401

def test_update_assessment(client, authenticated_user):
    job = create_sample_job(client, authenticated_user)

    assessment = create_sample_assessment(client, authenticated_user, job["id"])

    updated_assessment = {
        "job_id": job["id"],
        "type": AssessmentType.INTERVIEW,
        "description": "Test description",
        "completed": False,
        "deadline": "2030-01-01"
    }

    response = client.put(f"/jobs/update/{job['id']}/{assessment['id']}",
                          json=updated_assessment,
                          headers=auth_headers(authenticated_user)
                          )
    
    assert response.status_code == 200
    data = response.json()
    assert data["assessments"][0]["type"] == AssessmentType.INTERVIEW
    assert data["assessments"][0]["completed"] == False

def test_update_assessment_nonexistent_job(client, authenticated_user):
    updated_assessment = {
        "job_id": 1,
        "type": AssessmentType.INTERVIEW,
        "description": "Test description",
        "completed": False,
        "deadline": "2030-01-01"
    }

    response = client.put(f"/jobs/update/1/1",
                          json=updated_assessment,
                          headers=auth_headers(authenticated_user)
                          )
    
    assert response.status_code == 404

def test_update_nonexistent_assessment(client, authenticated_user):
    job = create_sample_job(client, authenticated_user)

    updated_assessment = {
        "job_id": job["id"],
        "type": AssessmentType.INTERVIEW,
        "description": "Test description",
        "completed": False,
        "deadline": "2030-01-01"
    }

    response = client.put(f"/jobs/update/{job['id']}/9999",
                          json=updated_assessment,
                          headers=auth_headers(authenticated_user)
                          )
    
    assert response.status_code == 404

def test_delete_assessment(client, authenticated_user):
    job = create_sample_job(client, authenticated_user)
    assessment = create_sample_assessment(client, authenticated_user, job["id"])

    response = client.delete(f"/jobs/delete/{job['id']}/{assessment['id']}",
                             headers=auth_headers(authenticated_user)
                             )
    assert response.status_code == 200

    response = client.get(f"/jobs/get/{job['id']}",
                          headers=auth_headers(authenticated_user)
                          )
    data = response.json()
    
    assert len(data["assessments"]) == 0

def test_delete_nonexistent_assessment(client, authenticated_user):
    job = create_sample_job(client, authenticated_user)

    response = client.delete(f"/jobs/delete/{job['id']}/1",
                             headers=auth_headers(authenticated_user)
                             )
    assert response.status_code == 404

    response = client.delete(f"/jobs/9999/1",
                             headers=auth_headers(authenticated_user)
                             )
    
    assert response.status_code == 404



