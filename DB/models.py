from pyorient import OrientDB

def create_item_class(client: OrientDB):
    query = """
    CREATE CLASS Item IF NOT EXISTS EXTENDS V
    """
    client.command(query)
    client.command("""
    CREATE PROPERTY Item.name STRING
    CREATE PROPERTY Item.description STRING
    """)
