import logging

file_logging = logging.getLogger("file_logging")
file_logging.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs.log")
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(levelname)s - %(asctime)s - %(filename)s - %(funcName)s - %(message)s"
)
file_handler.setFormatter(formatter)

file_logging.addHandler(file_handler)
