import pytest
from main import app
from fastapi.testclient import TestClient
from classes.schemas_dto import Task
from database.firebase import authSession
from tests.conftest import auth_headers, driver_id

client =  TestClient(app)


def test_get_drivers( client):
    response = client.get("/api/driver")
    print(response)
    assert response.status_code == 200

def test_get_driver_by_id(client, cleanup, driver_id):
    
    
    response = client.get(f"/api/driver/{driver_id}")
    assert response.status_code == 200

def test_create_driver(client, cleanup):
    driver_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "test.create@example.com",
        "password": "password123"
    }
    response = client.post("/api/driver", json=driver_data)
    print(auth_headers)
    print(response.json()['id'])
    assert response.status_code == 201

def test_update_driver(client, cleanup):
    

    driver_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "test.update@example.com",
        "password": "password123"
    }
    driver = client.post("/api/driver", json=driver_data)
    
    auth_token = authSession.sign_in_with_email_and_password(email=driver_data['email'], password=driver_data['password'])['idToken']
    auth_headers= {"Authorization": f"Bearer {auth_token}"}
    
    driver_id = driver.json()['id']
    
    modified_driver_data = {
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "1234567890",
        "email": "test.update@example.com",
        "profile_picture": "path/to/profile_picture.jpg",
        "average_rating": 4.5,
        "current_location": "Paris",
        "password": "securepassword123"
    }
    response = client.put(f"/api/driver/{driver_id}", json=modified_driver_data, headers=auth_headers)
    print(response)
    assert response.status_code == 204

def test_update_driver_whithoutauthentication(client, cleanup, driver_id):
    
    modified_driver_data = {
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "1234567890",
        "email": "test.update@example.com",
        "profile_picture": "path/to/profile_picture.jpg",
        "average_rating": 4.5,
        "current_location": "Paris",
        "password": "securepassword123"
    }
    response = client.put(f"/api/driver/{driver_id}", json=modified_driver_data)
    assert response.status_code == 401

def test_delete_driver(client, auth_headers, driver_id):
    
    response = client.delete(f"/api/driver/{driver_id}", headers=auth_headers)
    assert response.status_code == 204

def test_delete_driver_none_auth(driver_id):
    
    response = client.delete(f"/api/driver/{driver_id}")
    assert response.status_code == 401