import logging
import sys

# ANSI цвета
WHITE = "\033[0m"
BLUE = "\033[34m"


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        asc_time = f"{BLUE}{self.formatTime(record, self.datefmt)}{WHITE}"
        level_name = f"{WHITE}{record.levelname}"
        name = f"{WHITE}{record.name}"
        message = f"{WHITE}{record.getMessage()}"
        return f"{asc_time} | {level_name} | {name} | {message}"


class UvicornAccessFormatter(logging.Formatter):
    def format(self, record):
        asctime = f"{BLUE}{self.formatTime(record, self.datefmt)}{WHITE}"
        message = f"{WHITE}{record.getMessage()}"
        return f"{asctime} | {message}"


def setup_logging():
    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        ColoredFormatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

    for logger_name in ["uvicorn", "uvicorn.error"]:
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False

    access_handler = logging.StreamHandler(sys.stdout)
    access_handler.setFormatter(
        UvicornAccessFormatter("%(asctime)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    )

    access_logger = logging.getLogger("uvicorn.access")
    access_logger.handlers.clear()
    access_logger.addHandler(access_handler)
    access_logger.setLevel(logging.INFO)
    access_logger.propagate = False
