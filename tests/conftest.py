import pytest
from firebase_admin import auth
from fastapi.testclient import TestClient
from main import app
from database.firebase import authSession
import uuid

@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    #Nettoyer le directory une fois fini
    def remove_test_users():
        users = auth.list_users().iterate_all()
        for user in users:
            if user.email.startswith("test"):
                auth.delete_user(user.uid)
    request.addfinalizer(remove_test_users)
@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def auth_headers():
    # Génération des en-têtes d'authentification si nécessaire
    email = "test.auth"+ str(uuid.uuid4()) + "@gmail.com"
    password = "password123"
    user = auth.create_user(
        email=email,
        password=password
    )
    token = authSession.sign_in_with_email_and_password(email=email, password=password)['idToken']
    headers = {"Authorization": f"Bearer {token}"}
    return headers


@pytest.fixture
def task_id(client, auth_headers):
    task_data = {
        "title": "Task 1",
        "description": "Description of task 1",
        "done": False
    }
    task = client.post("/api/todos", json=task_data, headers=auth_headers)
    task_id =str( task.json()['id'])
    print(task_id)
    return task_id

@pytest.fixture
def valid_user_data():
    return {
        "email": "test.auth1@example.com",
        "password": "securepassword"
    }