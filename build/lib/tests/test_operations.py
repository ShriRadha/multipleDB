import pytest
from unittest.mock import MagicMock, patch
from src.db_operations import DatabaseOperations
from src.db_client import DatabaseClient

# Setup a fixture for DatabaseOperations with mocked DatabaseClient
@pytest.fixture
def db_ops():
    with patch('src.db_client.DatabaseClient') as mock_db_client:
        # Create instance of DatabaseClient
        client = mock_db_client.return_value
        client.mongo_client = MagicMock()
        client.mysql_connection = MagicMock()
        client.postgres_connection = MagicMock()

        # Mock cursor for SQL databases
        mock_cursor = MagicMock()
        client.mysql_connection.cursor.return_value = mock_cursor
        client.postgres_connection.cursor.return_value = mock_cursor

        # Instantiate DatabaseOperations with mocked DatabaseClient
        db_ops = DatabaseOperations(client)
        return db_ops, mock_cursor

# Test insert operations for all databases
@pytest.mark.parametrize("db_type", [("mongo"), ("mysql"), ("postgres")])
def test_insert(db_ops, db_type):
    db_operations, mock_cursor = db_ops
    collection_table = "test_collection" if db_type == "mongo" else "test_table"
    data = {"key": "value"}
    db_operations.insert(db_type, data, collection_table)
    if db_type == "mongo":
        db_operations.db_client.mongo_client['your_database'][collection_table].insert_one.assert_called_with(data)
    else:
        mock_cursor.execute.assert_called()
        assert mock_cursor.connection.commit.called

# Test find operations for all databases
@pytest.mark.parametrize("db_type", [("mongo"), ("mysql"), ("postgres")])
def test_find(db_ops, db_type):
    db_operations, mock_cursor = db_ops
    collection_table = "test_collection" if db_type == "mongo" else "test_table"
    query = {"key": "value"}
    db_operations.find(db_type, query, collection_table)
    if db_type == "mongo":
        db_operations.db_client.mongo_client['your_database'][collection_table].find_one.assert_called_with(query)
    else:
        mock_cursor.execute.assert_called()
        mock_cursor.fetchone.assert_called()

# Test update operations for all databases
@pytest.mark.parametrize("db_type", [("mongo"), ("mysql"), ("postgres")])
def test_update(db_ops, db_type):
    db_operations, mock_cursor = db_ops
    collection_table = "test_collection" if db_type == "mongo" else "test_table"
    query = {"key": "value"}
    new_values = {"key": "new_value"}
    db_operations.update(db_type, query, new_values, collection_table)
    if db_type == "mongo":
        db_operations.db_client.mongo_client['your_database'][collection_table].update_one.assert_called_with(query, {'$set': new_values})
    else:
        mock_cursor.execute.assert_called()
        assert mock_cursor.connection.commit.called

# Test delete operations for all databases
@pytest.mark.parametrize("db_type", [("mongo"), ("mysql"), ("postgres")])
def test_delete(db_ops, db_type):
    db_operations, mock_cursor = db_ops
    collection_table = "test_collection" if db_type == "mongo" else "test_table"
    query = {"key": "value"}
    db_operations.delete(db_type, query, collection_table)
    if db_type == "mongo":
        db_operations.db_client.mongo_client['your_database'][collection_table].delete_one.assert_called_with(query)
    else:
        mock_cursor.execute.assert_called()
        assert mock_cursor.connection.commit.called
