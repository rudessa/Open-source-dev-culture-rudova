from pydantic import BaseModel

class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    This model is used for user registration, ensuring that the required fields 
    are provided and conform to expected data types.

    Attributes:
        username (str): The unique username of the user.
        password (str): The password for the user account.
    """
    username: str
    password: str


class CSVDataResponse(BaseModel):
    """
    Schema for returning CSV data associated with a user.

    This model is used as a response format when retrieving CSV data, ensuring 
    consistency in the API response.

    Attributes:
        user_id (int): The ID of the user to whom the CSV data belongs.
        content (str): The CSV file content stored as a string.
    """
    user_id: int
    content: str
