import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    """Configuration class for application settings."""

    SOURCE_FOLDER = os.environ.get("SOURCE_FOLDER")
    LIBRARY_FOLDER = os.environ.get("LIBRARY_FOLDER")
    TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
    MOVIE_FOLDER = os.environ.get("MOVIE_FOLDER")
    TV_FOLDER = os.environ.get("TV_FOLDER")
    FILE_NAME_LANGUAGE = os.environ.get("FILE_NAME_LANGUAGE", "en-EN")  # Default to English if not set
    CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 8192))  # Default chunk size for file operations
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()  # Default log level

    def validate_config(self):
        """Validates that required configuration variables are set."""
        if not all([self.SOURCE_FOLDER, self.LIBRARY_FOLDER, self.TMDB_API_KEY]):
            raise ValueError("Missing required environment variables.")