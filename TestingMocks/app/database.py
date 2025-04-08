from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Database configuration and connection setup.
DATABASE_URL = "sqlite:///./test.db"

# Creates a database engine that manages the connection to the SQLite database.
# The `check_same_thread=False` argument allows multiple threads to access the same database connection.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Configures a session factory that provides database sessions.
# - `autocommit=False`: Transactions are managed manually to ensure data integrity.
# - `autoflush=False`: Prevents automatic flushing of changes to the database before committing.
# - `bind=engine`: Binds the session to the created database engine.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for defining ORM models.
# All database models should inherit from this class to be recognized by SQLAlchemy.
Base = declarative_base()
