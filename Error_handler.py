import csv
import os
import traceback
from datetime import datetime


class ErrorHandler:
    """A class to handle logging and managing errors in a CSV file."""

    def __init__(self, log_file='error_log.csv'):
        """Initialize the error handler with a log file."""
        self.log_file = log_file

        # Ensure the log file exists and has the correct header
        if not os.path.exists(self.log_file):
            with open(self.log_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Timestamp', 'Error Message', 'Exception Details'])

    def log_error(self, message, exception=None):
        """
        Log an error message to the CSV file.

        Args:
            message (str): Custom error message.
            exception (Exception, optional): Exception details, if any.
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Get full exception details (stack trace)
        if exception:
            exception_details = traceback.format_exc()
        else:
            exception_details = ''

        # Write the error to the CSV file
        with open(self.log_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, message, exception_details])

    def print_error(self, message):
        """
        Args:
            message (str): The error message to display.
        """
        print(f"Error: {message}")

    def handle_error(self, message, exception=None):
        """
        Handle an error by logging it to the CSV file and printing it to the console.

        Args:
            message (str): Custom error message.
            exception (Exception, optional): Exception details, if any.
        """
        self.log_error(message, exception)
        self.print_error(message)
