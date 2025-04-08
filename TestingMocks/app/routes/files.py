from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import CSVData
from app.parse_csv import parse_csv

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


@router.post("/upload")
async def upload_file(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Endpoint to upload a CSV file and store its content in the database.
    
    Args:
        user_id (int): ID of the user uploading the file.
        file (UploadFile): The uploaded CSV file.
        db (Session): Database session dependency.
    
    Returns:
        dict: Confirmation message of successful upload.
    """
    content = await file.read()
    db_entry = CSVData(user_id=user_id, content=content.decode())
    db.add(db_entry)
    db.commit()
    return {"message": "File uploaded successfully"}


@router.get("/json/{string}")
def get_json(string: str):
    """
    Endpoint to process a CSV string and return parsed JSON data.
    
    Args:
        string (str): The CSV string to be parsed.
    
    Returns:
        dict: Parsed JSON representation of the CSV string.
    """
    return parse_csv(string)
