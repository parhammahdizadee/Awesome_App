from fastapi import FastAPI, HTTPException
import logging
from DB.connections import OrientDBConnect

app = FastAPI(
    title="Awesome_App",
    description="This is an example FastAPI application for CRUD on OrientDB",
)
logging.basicConfig(level=logging.INFO)
db = OrientDBConnect()


@app.post(path="/create")
def create_item(data: dict):
    """
    Create Object with inputed values

    :param data: dictionary containing value that should be stored in database
    :return: Bool:
    """
    try:
        # Check for existing item with the same ID (if applicable)
        if db.client.get_item_by_id(data.get('id')):
            raise HTTPException(status_code=400, detail="Item with this ID already exists")

        # Insert the item into the database
        db.client.insert_item(data)
        return {"message": "Item created successfully"}
    except Exception as e:
        logging.error(f"Error creating item: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get(path="/object")
def read_items():
    """
    Read all objects from the database

    :return: list of objects
    """
    try:
        objects = db.client.get_all_items()
        return objects
    except Exception as e:
        logging.error(f"Error reading items: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
@app.put(path="/object/{object_id}")
def update_item(object_id: int, data: dict):
    """
    Update an object in the database

    :param object_id: ID of the object to update
    :param data: dictionary containing the updated values
    :return: updated object
    """
    try:
        item = db.client.get_item_by_id(object_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        # Update the item in the database
        db.client.update_item(object_id, data) 
        return db.client.get_item_by_id(object_id) 
    except Exception as e:
        logging.error(f"Error updating item: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.delete(path="/object/{object_id}")
def delete_item(object_id: int):
    """
    Delete an object from the database

    :param object_id: ID of the object to delete
    :return: message indicating success
    """
    try:
        item = db.client.get_item_by_id(object_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        # Delete the item from the database
        db.client.delete_item(object_id) 
        return {"message": "Item deleted successfully"}
    except Exception as e:
        logging.error(f"Error deleting item: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")