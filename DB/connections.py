from pydantic import BaseSettings
import logging
from pyorient import OrientDB
from pyorient.exceptions import PyOrientException
from constant.Errors import ErrorMessage


# Settings for OrientDB
class Settings(BaseSettings):
    ORIENTDB_HOST: str = "localhost"
    ORIENTDB_PORT: int = 2424
    ORIENTDB_USER: str = "root"
    ORIENTDB_PASSWORD: str = "root"
    ORIENTDB_DATABASE: str = "test_db"

    class Config:
        env_file = ".env"


settings = Settings()




# OrientDB Connection Manager
class OrientDBConnect:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = None

    def connect(self):
        """Establish a connection to OrientDB."""
        try:
            self.client = OrientDB(settings.ORIENTDB_HOST, settings.ORIENTDB_PORT)
            self.client.connect(settings.ORIENTDB_USER, settings.ORIENTDB_PASSWORD)

            if not self.client.db_exists(settings.ORIENTDB_DATABASE):
                self.client.db_create(settings.ORIENTDB_DATABASE, pyorient.DB_TYPE_GRAPH,
                                      pyorient.STORAGE_TYPE_PLOCAL)

            self.client.db_open(settings.ORIENTDB_DATABASE, settings.ORIENTDB_USER,
                                settings.ORIENTDB_PASSWORD)
            self.logger.info("Connected to OrientDB successfully.")
        except PyOrientException as error:
            self.logger.error(ErrorMessage.DB_CONNECTION)
            self.logger.error(error)
            raise Exception(ErrorMessage.DB_CONNECTION)

    def disconnect(self):
        """Close the connection to OrientDB."""
        try:
            if self.client:
                self.client.close()
                self.logger.info("Disconnected from OrientDB successfully.")
        except PyOrientException as error:
            self.logger.error(ErrorMessage.DB_DISCONNECTION)
            self.logger.error(error)
            raise Exception(ErrorMessage.DB_DISCONNECTION)

    def execute_query(self, query: str):
        """Execute a query on the connected database."""
        try:
            if not self.client:
                raise Exception("No active connection to OrientDB.")
            result = self.client.command(query)
            return result
        except PyOrientException as error:
            self.logger.error(ErrorMessage.DB_QUERY)
            self.logger.error(error)
            raise Exception(ErrorMessage.DB_QUERY)


# Example Usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    db = OrientDBConnect()

    try:
        # Connect to OrientDB


        # Execute a query
        query = "SELECT FROM V LIMIT 10"  # Example query
        result = db.execute_query(query)
        print("Query Result:", result)

    finally:
        # Disconnect from OrientDB
        db.disconnect()
