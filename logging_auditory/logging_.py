import logging
import sys
import structlog
import json
from logging.handlers import HTTPHandler
import requests

FORMATTER_STRING = "%(asctime)s — %(name)s — %(levelname)s — %(message)s"
FORMATTER = logging.Formatter(FORMATTER_STRING)


class JSONHTTPHandler(HTTPHandler):
    """
    Custom HTTPHandler that sends logs in JSON format.
    """
    def emit(self, record):
        """
        Processes and sends log records in JSON format.

        Args:
            record (logging.LogRecord): The log record to be sent.
        """
        log_entry = {
            "time": self.formatter.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "name": record.name
        }
        if record.exc_info:
            log_entry["exception"] = self.formatter.formatException(record.exc_info)

        # Send the log data as JSON
        headers = {"Content-Type": "application/json"}
        try:
            requests.post(
                f"http://{self.host}{self.url}",
                data=json.dumps(log_entry),
                headers=headers
            )
        except Exception as e:
            self.handleError(record)



def get_logger(logger_name):
    """
    Creates and configures a logger.

    Args:
        logger_name (str): The name of the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    logger.addHandler(console_handler)

    # HTTP Handler for critical errors
    http_handler = JSONHTTPHandler(
        host="127.0.0.1:5000",  # Local logging server
        url="/log",  # API endpoint
        method="POST"  # Request method
    )
    http_handler.setLevel(logging.CRITICAL)
    http_handler.setFormatter(logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'))
    
    logger.addHandler(http_handler)

    return logger

def replace_user(_, __, event_dict):
    """
    Replaces the username with a token.

    Args:
        event_dict (dict): Dictionary containing log event data.

    Returns:
        dict: Updated log event dictionary.
    """
    user = event_dict.get("user")
    if user:
        user_token = "some_string_that_we_can_learn_username_from"
        event_dict["user"] = user_token
    return event_dict

def censor_password(_, __, event_dict):
    """
    Masks passwords in logs to protect sensitive information.

    Args:
        event_dict (dict): Dictionary containing log event data.

    Returns:
        dict: Updated log event dictionary with censored password.
    """
    if "password" in event_dict:
        event_dict["password"] = "*CENSORED*"
    return event_dict

log = structlog.wrap_logger(
    get_logger("my_app_logger"),
    processors=[
        censor_password,
        replace_user,
        structlog.processors.JSONRenderer(indent=1, sort_keys=True),
    ],
)


if __name__ == "__main__":
    log.warning("Test warning", password="test_password")
    log.warning("Test warning", user="TestUser")
    log.critical("Test critical log", user="Admin")
    log.info("Test info log")
    
