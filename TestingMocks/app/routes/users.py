from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, CSVData
from app.schemas import UserCreate
import hashlib

router = APIRouter()


def get_db():
    """
    Dependency to get a database session.
    
    Yields:
        Session: SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint to register a new user with a hashed password.
    
    Args:
        user (UserCreate): User registration data.
        db (Session): Database session dependency.
    
    Returns:
        dict: Confirmation message of successful registration.
    """
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    db_user = User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully"}

@router.get("/", response_model=list[dict[str, str]])
async def get_users(db: Session = Depends(get_db)):
    """
    Endpoint to retrieve a list of all registered users.
    
    Args:
        db (Session): Database session dependency.
    
    Returns:
        list[dict[str, str]]: List of user dictionaries containing username and ID.
    """
    users = db.query(User).all()
    return [{"username": user.username, "id": str(user.id)} for user in users]
@router.get("/{user_id}/data", response_model=list[dict[str, str]])

async def get_user_data(user_id: int, db: Session = Depends(get_db)):
    """
    Endpoint to retrieve all CSV data entries associated with a specific user.
    
    Args:
        user_id (int): ID of the user whose data is being retrieved.
        db (Session): Database session dependency.
    
    Raises:
        HTTPException: If the user is not found.
    
    Returns:
        list[dict[str, str]]: List of CSV data entries containing ID and content.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    data = db.query(CSVData).filter(CSVData.user_id == user_id).all()
    return [{"id": str(entry.id), "content": entry.content} for entry in data]