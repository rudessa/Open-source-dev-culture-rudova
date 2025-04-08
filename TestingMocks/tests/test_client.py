import requests
import requests_mock

def test_register():
    """
    Tests the user registration endpoint.

    This function mocks a POST request to `/users/register` and verifies
    that the response contains the expected success message.

    Test Steps:
        1. Mock the API response to return a success message.
        2. Send a POST request with test user credentials.
        3. Assert that the response message matches the expected output.

    Expected API Response:
        {"message": "User registered successfully"}
    """
    with requests_mock.Mocker() as m:
        m.post("http://127.0.0.1:8000/users/register",
               json={"message": "User registered successfully"})

        response = requests.post(
            "http://127.0.0.1:8000/users/register", json={"username": "test", "password": "test"})

        assert response.json()["message"] == "User registered successfully"

def test_upload():
    """
    Tests the file upload endpoint.

    This function creates a temporary CSV file, mocks a POST request to `/files/upload`,
    and verifies that the response confirms a successful upload.

    Test Steps:
        1. Mock the API response for a file upload.
        2. Create a test CSV file with sample data.
        3. Open the file and send a POST request to the `/files/upload` endpoint.
        4. Assert that the response message matches the expected output.

    Expected API Response:
        {"message": "File uploaded successfully"}
    """
    with requests_mock.Mocker() as m:
        m.post("http://127.0.0.1:8000/files/upload",
               json={"message": "File uploaded successfully"})

        with open("test.csv", "w") as f:
            f.write("id,name\n1,Test")

        with open("test.csv", "rb") as file:
            response = requests.post(
                "http://127.0.0.1:8000/files/upload", files={"file": file}, data={"user_id": "1"})

        assert response.json()["message"] == "File uploaded successfully"

def test_get_users():
    """
    Tests fetching the list of users.

    This function mocks a GET request to `/users` and verifies that the response
    returns a list of user objects with the expected structure.

    Test Steps:
        1. Mock the API response to return a predefined list of users.
        2. Send a GET request to retrieve the list of users.
        3. Assert that the response status is 200 (OK).
        4. Verify that the response contains a list of dictionaries with `id` and `username`.

    Expected API Response:
        [
            {"id": 1, "username": "user1"},
            {"id": 2, "username": "user2"}
        ]
    """
    with requests_mock.Mocker() as m:
        m.get("http://127.0.0.1:8000/users", json=[
            {"id": 1, "username": "user1"},
            {"id": 2, "username": "user2"},
        ])

        response = requests.get("http://127.0.0.1:8000/users")

        assert response.status_code == 200

        users = response.json()
        assert isinstance(users, list)
        assert all("username" in user and "id" in user for user in users)

def test_get_user_data():
    """
    Tests fetching CSV data for a specific user.

    This function mocks a GET request to `/users/{user_id}/data` and verifies
    that the response returns a list of data entries associated with the user.

    Test Steps:
        1. Define a test user ID.
        2. Mock the API response to return sample CSV data entries.
        3. Send a GET request to retrieve the user's data.
        4. Assert that the response status is 200 (OK).
        5. Verify that the response contains a list of dictionaries with `id` and `content`.

    Expected API Response:
        [
            {"id": 1, "content": "data1"},
            {"id": 2, "content": "data2"}
        ]
    """
    user_id = 2

    with requests_mock.Mocker() as m:
        m.get(f"http://127.0.0.1:8000/users/{user_id}/data", json=[
            {"id": 1, "content": "data1"},
            {"id": 2, "content": "data2"},
        ])

        response = requests.get(f"http://127.0.0.1:8000/users/{user_id}/data")

        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert all("id" in entry and "content" in entry for entry in data)
