import logging

# Create and configure a logger
logger = logging.getLogger('DatabaseLogger')
# Set the minimum logging level. DEBUG level means that all messages at this level and more severe will be logged.
logger.setLevel(logging.DEBUG)

# Create a file handler that logs even debug messages
# This handler directs the log messages to a file named 'database.log'.
fh = logging.FileHandler('database.log')
fh.setLevel(logging.DEBUG)  # Set the minimum log level for the file handler

# Define how the log messages should be formatted.
# This formatter specifies that each message should include the timestamp, logger name, log level, and the log message.
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add the formatter to the file handler so it knows how to format the messages
fh.setFormatter(formatter)

# Add the file handler to the logger so that it can process log messages.
logger.addHandler(fh)
