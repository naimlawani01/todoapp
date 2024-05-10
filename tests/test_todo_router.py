import pytest
from main import app
from fastapi.testclient import TestClient
from classes.schemas_dto import Task
from database.firebase import authSession
from tests.conftest import auth_headers

client = TestClient(app)


def test_get_todos(client):
    response = client.get("/api/todos")
    print(response)
    assert response.status_code == 200


def test_get_todos_by_id(client, cleanup, task_id):
   
    response = client.get(f"/api/todos/{task_id}")
    print(response.json())
    assert response.status_code == 200


def test_create_todos(client, cleanup, auth_headers):
    task_data = {
        "title": "Task 1",
        "description": "Description of task 1",
        "done": False
    }
    response = client.post("/api/todos", json=task_data, headers=auth_headers)
    assert response.status_code == 201


def test_update_todos(client, cleanup, auth_headers, task_id):
    
    
    modified_task_data = {
        "title": "Updated Task 1",
        "description": "Updated description of task 1",
        "done": True
    }
    response = client.put(f"/api/todos/{task_id}", json=modified_task_data, headers=auth_headers)
    assert response.status_code == 204


def test_update_todo_without_authentication(client, cleanup, task_id):
    modified_task_data = {
        "title": "Task 1",
        "description": "Description of task 1",
        "done": False
    }
    response = client.put(f"/api/todos/{task_id}", json=modified_task_data)
    assert response.status_code == 401


def test_delete_todo(client, auth_headers, task_id):
    response = client.delete(f"/api/todos/{task_id}", headers=auth_headers)
    assert response.status_code == 204


def test_delete_todo_none_auth(task_id):
    response = client.delete(f"/api/todos/{task_id}")
    assert response.status_code == 401
