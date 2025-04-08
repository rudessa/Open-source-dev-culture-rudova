import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from app.routes import users, files
from app.database import Base, engine
import uvicorn


# Initialize database tables.
# This command ensures that all database models inheriting from `Base` are created.
Base.metadata.create_all(bind=engine)

# Create a FastAPI application instance with a custom title.
app = FastAPI(title="FastAPI CSV API")

# Include routers for different API endpoints.
# - `users.router` handles user-related operations under the `/users` prefix.
# - `files.router` handles file-related operations under the `/files` prefix.
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(files.router, prefix="/files", tags=["Files"])

@app.get("/")
async def root():
    """
    Root endpoint to check if the FastAPI application is running.

    Returns:
        dict: A simple message confirming the API is active.
    """
    return {"message": "FastAPI is running"}

# Entry point for running the FastAPI application with Uvicorn.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    """
    Starts the FastAPI server using Uvicorn.

    - `host="0.0.0.0"`: Makes the API accessible from any network interface.
    - `port=8000`: Runs the application on port 8000.
    """
