# backend/app/config.py
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Data File Paths ---
trade_files_str = os.getenv("TRADE_FILES_PATHS", "")
TRADE_FILES = trade_files_str.split(',') if trade_files_str else []

# --- Logging Configuration ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

def setup_logging():
    """Configures the root logger for the application."""
    log_format = "[%(asctime)s] [%(levelname)s] - %(message)s"
    log_date_format = "%Y-%m-%d %H:%M:%S"
    
    # Basic configuration sets up the root logger
    logging.basicConfig(
        level=LOG_LEVEL,
        format=log_format,
        datefmt=log_date_format,
        handlers=[
            logging.StreamHandler()  # Outputs logs to the console
        ]
    )
    # Get the logger for this application
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level {LOG_LEVEL}")
    return logger

logger = setup_logging()