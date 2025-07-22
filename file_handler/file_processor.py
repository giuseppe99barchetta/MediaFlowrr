import os
from config.logger import Logger

logger = Logger(__name__)


class FileProcessor:
    """Class responsible for processing files in the download folder."""

    def __init__(self, config, file_organizer):
        """Initializes the file processor."""
        self.config = config
        self.file_organizer = file_organizer

    def process_files(self):
        """Processes all files in the download folder."""
        try:
            files = [f for f in os.listdir(self.config.SOURCE_FOLDER) if os.path.isfile(os.path.join(self.config.SOURCE_FOLDER, f))]
            for filename in files:
                filepath = os.path.join(self.config.SOURCE_FOLDER, filename)
                self.file_organizer.organize_file(filepath)
        except Exception as e:
            logger.error(f"Error processing files: {e}")
