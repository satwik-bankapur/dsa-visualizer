import logging
import logging.handlers
import os
from typing import Optional


def setup_logging(log_level:str, log_file: str = "app.log"):

    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):  # ← Check if log_dir is not empty
        os.makedirs(log_dir)

    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Clear existing handlers
    root_logger.handlers.clear()

    #console handlers
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    #file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)

if __name__ == "__main__":
    setup_logging("DEBUG", "test.log")
    logger = get_logger(__name__)
    logger.info("Logging setup completed!")
    logger.debug("This is a debug message")
    logger.warning("This is a warning message")
