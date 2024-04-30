import pytest
from unittest.mock import patch, MagicMock
from src.db_client import DatabaseClient
from src.exceptions import DatabaseConnectionError

# Test the connection method

def test_connect():
    with patch('src.db_client.MongoClient') as mock_mongo, \
         patch('src.db_client.mysql.connector.connect') as mock_mysql, \
         patch('src.db_client.psycopg2.connect') as mock_postgres:
        
        # Mocking database connections
        mock_mongo.return_value = MagicMock()
        mock_mysql.return_value = MagicMock()
        mock_postgres.return_value = MagicMock()

        # Initialize DatabaseClient
        db_client = DatabaseClient("mongodb://localhost:27017", 
                                   {"host": "localhost", "user": "root", "password": "password", "database": "test"}, 
                                   {"host": "localhost", "user": "root", "password": "password", "dbname": "test"})

        # Connect to databases
        db_client.connect()

        # Assert that all connections are called
        mock_mongo.assert_called_once()
        mock_mysql.assert_called_once()
        mock_postgres.assert_called_once()

# Test the close method
def test_close():
    with patch('src.db_client.MongoClient') as mock_mongo, \
         patch('src.db_client.mysql.connector.connect') as mock_mysql, \
         patch('src.db_client.psycopg2.connect') as mock_postgres:
    
        mongo_instance = MagicMock()
        mysql_instance = MagicMock()
        postgres_instance = MagicMock()

        mock_mongo.return_value = mongo_instance
        mock_mysql.return_value = mysql_instance
        mock_postgres.return_value = postgres_instance

        mysql_instance.is_closed.return_value = False  # Mock the is_closed method if it exists
        
        db_client = DatabaseClient("mongodb://localhost:27017",
                                   {"host": "localhost", "user": "root", "password": "password", "database": "test"},
                                   {"host": "localhost", "user": "root", "password": "password", "dbname": "test"})
        
        db_client.connect()
        db_client.close()
        mysql_instance.close.assert_called_once()
        postgres_instance.close.assert_called_once()