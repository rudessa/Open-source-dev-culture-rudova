from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    """
    Database model representing a user.

    Attributes:
        id (int): Primary key, unique identifier for each user.
        username (str): Unique username for the user, indexed for faster lookups.
        password (str): Hashed password for authentication purposes.
    """
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


class CSVData(Base):
    """
    Database model representing CSV file data associated with a user.

    Attributes:
        id (int): Primary key, unique identifier for each CSV entry.
        user_id (int): Foreign key referencing the `id` column in the `users` table.
        content (str): The content of the CSV file stored as a string.
        user (User): Relationship linking each CSV entry to its associated user.
    """
    __tablename__ = "csv_data"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)

    # Establish a relationship between CSVData and User
    user = relationship("User")
