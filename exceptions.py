class Error(Exception):
    """
    Base class for custom exceptions in a MongoDB application.
    
    This class is a base class for all other custom exceptions defined in this module.
    It extends Python's built-in Exception class.
    """
    pass  # No additional functionality; serves as a base class

class DatabaseConnectionError(Error):
    """
    Exception raised for errors that occur during database connection.

    Attributes:
        message (str): Explanation of the error
    """
    def __init__(self, message="Could not connect to the database"):
        """
        Initialize the exception with a message that describes the error.

        Args:
            message (str): Custom message describing the error. Default message is used
                           if none is provided.
        """
        self.message = message  # Store the error message
        super().__init__(self.message)  # Initialize the superclass with the message

class InsertionError(Error):
    """
    Exception raised for errors that occur during data insertion into the database.

    Attributes:
        message (str): Explanation of the error
    """
    def __init__(self, message="Failed to insert data into the database"):
        """
        Initialize the exception with a message that describes the error.

        Args:
            message (str): Custom message describing the error. Default message is used
                           if none is provided.
        """
        self.message = message
        super().__init__(self.message)

class DocumentNotFoundError(Error):
    """
    Exception raised when a query operation fails to find any documents.

    Attributes:
        message (str): Explanation of the error
    """
    def __init__(self, message="No document found matching the query"):
        """
        Initialize the exception with a message that describes the error.

        Args:
            message (str): Custom message describing the error. Default message is used
                           if none is provided.
        """
        self.message = message
        super().__init__(self.message)

class UpdateError(Error):
    """
    Exception raised for errors that occur during document update operations.

    Attributes:
        message (str): Explanation of the error
    """
    def __init__(self, message="Failed to update the document"):
        """
        Initialize the exception with a message that describes the error.

        Args:
            message (str): Custom message describing the error. Default message is used
                           if none is provided.
        """
        self.message = message
        super().__init__(self.message)

class DeletionError(Error):
    """
    Exception raised for errors that occur during document deletion operations.

    Attributes:
        message (str): Explanation of the error
    """
    def __init__(self, message="Failed to delete the document"):
        """
        Initialize the exception with a message that describes the error.

        Args:
            message (str): Custom message describing the error. Default message is used
                           if none is provided.
        """
        self.message = message
        super().__init__(self.message)
