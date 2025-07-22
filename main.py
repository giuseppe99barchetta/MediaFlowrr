import os
from dotenv import load_dotenv
from config.config import Config
from client.tmdb_client import TMDBClient
from file_handler.file_organizer import FileOrganizer
from file_handler.file_processor import FileProcessor
from config.logger import Logger

# Load environment variables and initialize configuration before main
load_dotenv()
config = Config()
config.validate_config()
logger = Logger("main", config)

def main():
    # Initialize TMDb client
    tmdb_client = TMDBClient(config.TMDB_API_KEY, config.FILE_NAME_LANGUAGE)
    logger.debug("TMDb client initialized successfully.")

    # Initialize file organizer
    file_organizer = FileOrganizer(config, tmdb_client)
    logger.debug("File organizer initialized successfully.")

    # Process files
    file_processor = FileProcessor(config, file_organizer)
    file_processor.process_files()


if __name__ == "__main__":
    # Ensure destination library exists
    os.makedirs(config.LIBRARY_FOLDER, exist_ok=True)  # Create the directory if it doesn't exist
    main()
