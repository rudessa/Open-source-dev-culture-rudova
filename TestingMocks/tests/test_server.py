from fastapi.testclient import TestClient
from app.main import app
import io
from app.database import SessionLocal
from app.models import User


# Create a test client for the FastAPI application
client = TestClient(app)


def test_register_user():
    """
    Tests the user registration endpoint.

    This function ensures that a user can be registered successfully 
    by sending a POST request to `/users/register`.

    Test Steps:
        1. Connect to the test database.
        2. Check if a user with the test username exists and delete them if necessary.
        3. Send a registration request with test credentials.
        4. Assert that the response status code is 200.
        5. Verify that the response contains the expected success message.

    Expected API Response:
        {"message": "User registered successfully"}
    """
    db = SessionLocal()

    user = db.query(User).filter(User.username == "test").first()
    db.delete(user)
    db.commit()

    response = client.post(
        "/users/register", json={"username": "test", "password": "test"})
    
    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"


def test_upload_file():
    """
    Tests the file upload endpoint.

    This function verifies that a CSV file can be uploaded successfully
    to the `/files/upload` endpoint.

    Test Steps:
        1. Create an in-memory CSV file.
        2. Send a POST request to upload the file with a `user_id` parameter.
        3. Assert that the response status code is 200.
        4. Verify that the response contains the expected success message.

    Expected API Response:
        {"message": "File uploaded successfully"}
    """
    csv_content = io.BytesIO(b"id,name\n1,Test")

    files = {"file": ("test.csv", csv_content, "text/csv")}
    response = client.post("/files/upload?user_id=1", files=files)
    
    assert response.status_code == 200
    assert response.json()["message"] == "File uploaded successfully"


def test_get_users():
    """
    Tests retrieving the list of users.

    This function sends a GET request to `/users` and verifies that
    the response contains a valid list of users.

    Test Steps:
        1. Send a GET request to fetch all users.
        2. Assert that the response status code is 200.
        3. Verify that the response is a list of user objects.
        4. Ensure each user object contains `id` and `username`.

    Expected API Response:
        [
            {"id": 1, "username": "user1"},
            {"id": 2, "username": "user2"}
        ]
    """
    response = client.get("/users")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert all("username" in user and "id" in user for user in users)


def test_get_user_data():
    """
    Tests retrieving CSV data associated with a user.

    This function sends a GET request to `/users/{user_id}/data`
    and verifies that the response contains valid data entries.

    Test Steps:
        1. Define a test user ID.
        2. Send a GET request to retrieve data for the specified user.
        3. Assert that the response status code is 200.
        4. Verify that the response is a list of data entries.
        5. Ensure each data entry contains `id` and `content`.

    Expected API Response:
        [
            {"id": 1, "content": "data1"},
            {"id": 2, "content": "data2"}
        ]
    """
    user_id = 2
    response = client.get(f"/users/{user_id}/data")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all("id" in entry and "content" in entry for entry in data)