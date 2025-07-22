import logging
import traceback
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Logger:
    def __init__(self, name, level=logging.INFO):
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(os.getenv('LOG_LEVEL', level))

        # Create a handler (e.g., file handler or stream handler)
        handler = logging.StreamHandler()  # Or use FileHandler for writing to a file
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def error(self, message):
        self.logger.error(message)

    def exception(self, message):  # For logging exceptions with tracebacks
        self.logger.error(f"{message}: {traceback.format_exc()}")

    def debug(self, message):
        self.logger.debug(message)
        
    def info(self, message):
        self.logger.info(message)
        
    def warning(self, message):
        self.logger.warning(message)
