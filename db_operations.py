from .db_client import DatabaseClient
from .exceptions import *
from .logger import logger

class DatabaseOperations:
    """
    Handles database operations across multiple database types including MongoDB, MySQL, and PostgreSQL.
    This class abstracts CRUD operations to work with any of the specified database types by providing
    a uniform interface for operations like insert, find, update, and delete.

    Attributes:
        db_client (DatabaseClient): An instance of DatabaseClient which manages the connections to different databases.
    """

    def __init__(self, db_client):
        """
        Initializes the DatabaseOperations with a DatabaseClient.

        Args:
            db_client (DatabaseClient): The database client used to execute operations across MongoDB, MySQL, and PostgreSQL.
        """
        self.db_client = db_client

    def insert(self, db_type, data, collection_table):
        """
        Inserts data into the specified database type and collection or table.

        Args:
            db_type (str): Type of database ('mongo', 'mysql', 'postgres').
            data (dict): Data to insert into the database.
            collection_table (str): The name of the collection or table where data will be inserted.

        Returns:
            The inserted document's ID for MongoDB or the last row ID for SQL databases.

        Raises:
            InsertionError: If the insertion operation fails.
        """
        try:
            if db_type == 'mongo':
                collection = self.db_client.mongo_client['your_database'][collection_table]
                result = collection.insert_one(data)
                return result.inserted_id
            elif db_type in ['mysql', 'postgres']:
                cursor = self.db_client.mysql_connection.cursor() if db_type == 'mysql' else self.db_client.postgres_connection.cursor()
                placeholders = ', '.join(['%s'] * len(data))
                columns = ', '.join(data.keys())
                sql = f"INSERT INTO {collection_table} ({columns}) VALUES ({placeholders})"
                cursor.execute(sql, list(data.values()))
                cursor.connection.commit()
        except InsertionError as e:
            logger.error(f"Insert failed: {e}")
            raise

    def find(self, db_type, query, collection_table):
        """
        Finds a document or a row from the specified collection or table based on the query.

        Args:
            db_type (str): Type of database ('mongo', 'mysql', 'postgres').
            query (dict): Query to find the document or row.
            collection_table (str): The name of the collection or table to query.

        Returns:
            The document or row from the database that matches the query.

        Raises:
            DocumentNotFoundError: If no document matches the query.
        """
        try:
            if db_type == 'mongo':
                collection = self.db_client.mongo_client['your_database'][collection_table]
                return collection.find_one(query)
            elif db_type in ['mysql', 'postgres']:
                cursor = self.db_client.mysql_connection.cursor() if db_type == 'mysql' else self.db_client.postgres_connection.cursor()
                where_clause = ' AND '.join([f"{k}=%s" for k in query.keys()])
                sql = f"SELECT * FROM {collection_table} WHERE {where_clause}"
                cursor.execute(sql, tuple(query.values()))
                return cursor.fetchone()
        except DocumentNotFoundError as e:
            logger.error(f"Find failed: {e}")
            raise

    def update(self, db_type, query, new_values, collection_table):
        """
        Updates a document or a row in the specified collection or table based on the query.

        Args:
            db_type (str): Type of database ('mongo', 'mysql', 'postgres').
            query (dict): Query that identifies the document or row to update.
            new_values (dict): Values to update in the document or row.
            collection_table (str): The collection or table where the update will occur.

        Returns:
            The result of the update operation.

        Raises:
            UpdateError: If the update operation fails.
        """
        try:
            if db_type == 'mongo':
                collection = self.db_client.mongo_client['your_database'][collection_table]
                return collection.update_one(query, {'$set': new_values})
            elif db_type in ['mysql', 'postgres']:
                cursor = self.db_client.mysql_connection.cursor() if db_type == 'mysql' else self.db_client.postgres_connection.cursor()
                set_clause = ', '.join([f"{k}=%s" for k in new_values.keys()])
                where_clause = ', '.join([f"{k}=%s" for k in query.keys()])
                sql = f"UPDATE {collection_table} SET {set_clause} WHERE {where_clause}"
                cursor.execute(sql, list(new_values.values()) + list(query.values()))
                cursor.connection.commit()
        except UpdateError as e:
            logger.error(f"Update failed: {e}")
            raise

    def delete(self, db_type, query, collection_table):
        """
        Deletes a document or a row from the specified collection or table based on the query.

        Args:
            db_type (str): Type of database ('mongo', 'mysql', 'postgres').
            query (dict): Query that identifies the document or row to delete.
            collection_table (str): The collection or table from which the document or row will be deleted.

        Returns:
            The result of the delete operation.

        Raises:
            DeletionError: If the delete operation fails.
        """
        try:
            if db_type == 'mongo':
                collection = self.db_client.mongo_client['your_database'][collection_table]
                return collection.delete_one(query)
            elif db_type in ['mysql', 'postgres']:
                cursor = self.db_client.mysql_connection.cursor() if db_type == 'mysql' else self.db_client.postgres_connection.cursor()
                where_clause = ' AND '.join([f"{k}=%s" for k in query.keys()])
                sql = f"DELETE FROM {collection_table} WHERE {where_clause}"
                cursor.execute(sql, tuple(query.values()))
                cursor.connection.commit()
        except DeletionError as e:
            logger.error(f"Delete failed: {e}")
            raise
