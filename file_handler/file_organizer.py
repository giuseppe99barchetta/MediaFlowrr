import os
import re
import tqdm
from config.logger import Logger

logger = Logger(__name__)

class FileOrganizer:
    """Class responsible for organizing files based on TMDb data."""

    def __init__(self, config, tmdb_client):
        """Initializes the file organizer."""
        self.config = config
        self.tmdb_client = tmdb_client

    def clean_filename(self, filename):
        """Extracts the most likely title from a JDownloader filename."""
        # Convert to lowercase for case-insensitive matching
        filename = filename.lower()

        # Remove file extensions
        filename = re.sub(r"\.(mkv|mp4|avi|mov)$", "", filename)

        # Find the year (if present)
        year_match = re.search(r"(\d{4})", filename)

        if year_match:
            # Title is everything before the year
            title_candidate = filename[:year_match.start()]
        else:
            # If no year is found, take the first 10 words (adjust as needed)
            words = filename.split(".")
            title_candidate = ".".join(words[:min(10, len(words))])

        # Remove a year at the end of the string, but keep numbers in the title
        title_candidate = re.sub(r"\s*\(?\d{4}\)?\s*$", "", title_candidate)

        # Remove common separators and extra spaces
        title_candidate = re.sub(r"[-_]", " ", title_candidate)
        title_candidate = title_candidate.replace(".", " ")
        title_candidate = re.sub(r"\s+", " ", title_candidate).strip()

        logger.debug(f"Extracted title candidate: {title_candidate}")
        return title_candidate

    def get_file_extension(self, filepath):
        """Gets the file extension from a given filepath."""
        _, ext = os.path.splitext(filepath)
        return ext.lower() if ext else ""

    def is_video_file(self, filename):
        """Checks if a file is a video file based on its extension."""
        return filename.lower().endswith((".mp4", ".avi", ".mkv", ".mov", ".webm"))

    def create_destination_path(self, info, file_type):
        """Creates the destination folder path based on movie or TV show information."""
        if file_type == "movie":
            movie_name = info.original_title or info.title
            year = info.year
            movie_folder_name = f"{movie_name} ({year})" if year else movie_name
            destination_path = os.path.join(self.config.LIBRARY_FOLDER, self.config.MOVIE_FOLDER, movie_folder_name)
        
        elif file_type == "tv":
            show_name = info.original_name or info.name
            destination_path = os.path.join(self.config.LIBRARY_FOLDER, self.config.TV_FOLDER, show_name)
        
        return destination_path

    def create_new_filename(self, info, file_type):
        """Creates the new filename based on movie or TV show information."""
        if file_type == "movie":
            movie_name = info.original_title or info.title
            year = info.year
            new_filename = f"{movie_name} ({year})" if year else movie_name
        else:
            new_filename = info.original_name or info.name  # Use original name for TV shows

        return new_filename

    def move_and_rename_file(self, filepath, destination_path, new_filename):
        """Moves and renames the file with a progress bar."""
        original_ext = self.get_file_extension(filepath)
        new_filename += original_ext  # Add extension back

        new_filepath = os.path.join(destination_path, new_filename)

        total_size = os.path.getsize(filepath)
        with tqdm.tqdm(
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc=os.path.basename(filepath),  # Use the original filename for progress bar description
            total=total_size,
        ) as pbar:
            try:
                with open(filepath, 'rb') as source, open(new_filepath, 'wb') as dest:
                    while True:
                        chunk = source.read(self.config.CHUNK_SIZE)
                        if not chunk:
                            break
                        dest.write(chunk)
                        pbar.update(len(chunk))
                os.remove(filepath)  # Remove the original file after copying
                logger.debug(f"Moved '{os.path.basename(filepath)}' to '{new_filepath}'")
            except Exception as e:
                logger.error(f"Error copying/removing file: {e}")

    def organize_file(self, filepath):
        """Organize a single file by moving it to the correct folder."""
        try:
            filename = os.path.basename(filepath)

            # Check if it's a video file
            if not self.is_video_file(filename):
                logger.debug(f"Skipping non-video file: {filename}")
                return

            # Get movie or TV show info from TMDb
            cleaned_filename = self.clean_filename(filename)
            info = self.tmdb_client.get_movie_or_tv_info(cleaned_filename)

            if info:
                file_type = self.tmdb_client.check_movie_or_tv(info)
                destination_path = self.create_destination_path(info, file_type)
                new_filename = self.create_new_filename(info, file_type)

                if not os.path.exists(destination_path):
                    os.makedirs(destination_path, exist_ok=True)

                self.move_and_rename_file(filepath, destination_path, new_filename)

            else:
                logger.warning(f"Could not identify '{filename}'. Leaving in original folder.")

        except Exception as e:
            logger.error(f"Error processing file '{filename}': {e}")

