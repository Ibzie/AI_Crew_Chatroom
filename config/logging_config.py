# config/logging_config.py
import logging
import sys
from colorama import Fore, Style, init
from rich.logging import RichHandler

# Initialize colorama
init(autoreset=True)

# Custom log formatter for non-rich handlers
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{Style.RESET_ALL}"
            record.msg = f"{self.COLORS[levelname]}{record.msg}{Style.RESET_ALL}"
        return super().format(record)

# Configure logging
def configure_logging():
    logger = logging.getLogger("ai_hangout")
    logger.setLevel(logging.INFO)  # Use logging.INFO (the constant), not logging.info (the function)
    
    # Rich console handler for pretty formatting
    rich_handler = RichHandler(rich_tracebacks=True)
    rich_format = "%(message)s"
    rich_handler.setFormatter(logging.Formatter(rich_format))
    
    # Add handlers to logger
    logger.addHandler(rich_handler)
    
    return logger

# Create logger instance
logger = configure_logging()