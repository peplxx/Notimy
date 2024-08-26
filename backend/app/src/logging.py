from datetime import datetime
import os
import logging

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Set log file name with current date
log_filename = os.path.join(log_dir, f"notimy_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.log")


# Basic configuration for logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S',  # Date format
    handlers=[
        logging.FileHandler(log_filename),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)

logger = logging.getLogger("app")
