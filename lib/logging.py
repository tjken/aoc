import logging

_file_handler = logging.FileHandler("debug_log")
_formatter = logging.Formatter(
    "{levelname}\n{message}",
    style="{",
)
_file_handler.setFormatter(_formatter)

def get_debug_logger():
    logger = logging.getLogger("AoC Debug")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(_file_handler)

    return logger