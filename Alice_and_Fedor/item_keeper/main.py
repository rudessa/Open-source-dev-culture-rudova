from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items")
def get_items(skip: int = Query(0), limit: int = Query(10)):
    """
    Retrieves a list of items with pagination support.

    This function returns a subset of available items based on the specified 
    skip and limit values. It allows fetching a paginated list of items to 
    optimize data retrieval.

    Parameters:
        skip (int, optional): The number of initial items to skip. Defaults to 0.
        limit (int, optional): The maximum number of items to return. Defaults to 10.

    Returns:
        dict: A dictionary containing the paginated list of items.

    Example:
        Requesting `get_items(skip=1, limit=2)` would return the second and third items.

    Raises:
        No exceptions are explicitly raised in this function.
    """
    all_items = [
        {"id": 1, "name": "item1", "description": "A fancy item", "price": 10.99},
        {"id": 2, "name": "item2", "description": "A useful item", "price": 5.49},
        {"id": 3, "name": "item3", "description": "A rare item", "price": 99.99},
        {"id": 4, "name": "item4", "description": "A common item", "price": 1.99},
        {"id": 5, "name": "item5", "description": "A premium item", "price": 49.99},
    ]
    return {"items": all_items[skip : skip + limit]}
