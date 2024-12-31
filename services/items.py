from app.database import get_orientdb_client

def create_item(data):
    client = get_orientdb_client()
    query = "INSERT INTO Item (name, description) VALUES (?, ?)"
    client.command(query, (data.name, data.description))
    return {"name": data.name, "description": data.description}

def get_items():
    client = get_orientdb_client()
    result = client.command("SELECT FROM Item")
    return [{"id": record._rid, "name": record.name, "description": record.description} for record in result]
