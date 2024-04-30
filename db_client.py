from pymongo import MongoClient
import mysql.connector
import psycopg2
from .exceptions import *

class DatabaseClient:

    """
    A multi-database client manager class that supports connections to MongoDB, MySQL, and PostgreSQL databases.
    It provides methods to connect to, retrieve, and close connections to these databases.

    Attributes:
        mongo_uri (str): URI used for connecting to MongoDB.
        mysql_config (dict): Configuration dictionary containing MySQL connection parameters.
        postgres_config (dict): Configuration dictionary containing PostgreSQL connection parameters.
        mongo_client (PymongoClient or None): Client object for MongoDB, initialized after successful connection.
        mysql_connection (Connection or None): Connection object for MySQL, initialized after successful connection.
        postgres_connection (Connection or None): Connection object for PostgreSQL, initialized after successful connection.
    """
    def __init__(self, mongo_uri, mysql_config, postgres_config):
        """
        Initializes the DatabaseClient with connection parameters for MongoDB, MySQL, and PostgreSQL.

        Args:
            mongo_uri (str): MongoDB URI string used to connect to the database.
            mysql_config (dict): Configuration settings (host, user, password, database) for MySQL.
            postgres_config (dict): Configuration settings (host, user, password, dbname) for PostgreSQL.
        """
        self.mongo_uri = mongo_uri
        self.mysql_config = mysql_config
        self.postgres_config = postgres_config
        self.mongo_client = None
        self.mysql_connection = None
        self.postgres_connection = None

    def connect(self):
        """
        Attempts to connect to all specified databases using the provided configuration settings.

        Raises:
            DatabaseConnectionError: Custom exception raised if any connection fails, with an error message indicating the failure.
        """
        try:
            self.mongo_client = MongoClient(self.mongo_uri)
            self.mysql_connection = mysql.connector.connect(**self.mysql_config)
            self.postgres_connection = psycopg2.connect(**self.postgres_config)
        except DatabaseConnectionError as e:
            raise DatabaseConnectionError(f"Failed to connect to database: {e}")

    def get_database(self, db_name=None):

        """
        Retrieves the currently open database connections in a dictionary format.

        Args:
            db_name (str, optional): Specific database name for MongoDB. If provided, returns the specific MongoDB database object.

        Returns:
            dict: A dictionary containing the open database connections, keyed by database type ('mongo', 'mysql', 'postgres').

        Raises:
            DatabaseConnectionError: If no database connections are currently open.
        """
        databases = {}
        if self.mongo_client:
            databases['mongo'] = self.mongo_client[db_name] if db_name else self.mongo_client
        if self.mysql_connection and not self.mysql_connection.is_closed():
            databases['mysql'] = self.mysql_connection
        if self.postgres_connection:
            databases['postgres'] = self.postgres_connection

        if not databases:
            raise DatabaseConnectionError("No database connections are currently open.")
        
        return databases


    def close(self):
        """
        Closes all open database connections safely.

        This method checks each connection individually and closes it if it is open. This is crucial to free up resources and avoid potential leaks.
        """
        if self.mongo_client:
            self.mongo_client.close()
        if self.mysql_connection:
            # Assuming is_closed() is a method you've implemented or exists in the MySQL connection API
            if not self.mysql_connection.is_closed():
                self.mysql_connection.close()
        if self.postgres_connection:
            self.postgres_connection.close()

