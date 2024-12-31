from pyorient import OrientDB
from app.config import settings

def get_orientdb_client():
    client = OrientDB(settings.ORIENTDB_HOST, settings.ORIENTDB_PORT)
    session_id = client.connect(settings.ORIENTDB_USER, settings.ORIENTDB_PASSWORD)
    if not client.db_exists(settings.ORIENTDB_DATABASE):
        client.db_create(settings.ORIENTDB_DATABASE, pyorient.DB_TYPE_GRAPH)
    client.db_open(settings.ORIENTDB_DATABASE, settings.ORIENTDB_USER, settings.ORIENTDB_PASSWORD)
    return client
