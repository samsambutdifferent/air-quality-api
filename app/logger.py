import logging
import os

LOG_DIRECTORY = "logs"


def setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:
    """
    Setup a logger with a given name and log file.

    :param name: The name of the logger (can be module name).
    :param log_file: The log file where logs will be written.
    :param level: Logging level (default: logging.INFO).
    :return: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not os.path.exists(LOG_DIRECTORY):
        os.makedirs(LOG_DIRECTORY)

    log_file_path = os.path.join(LOG_DIRECTORY, log_file)

    logger = logging.getLogger(name)

    logger.setLevel(level)

    file_handler = logging.FileHandler(log_file_path)
    stream_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
