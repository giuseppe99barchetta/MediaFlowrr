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

    def extract_tv_info(self, filename):
        """
        Tries multiple regex patterns to extract TV show title, season, and episode info.
        Returns (title, season, episode) or (None, None, None) if no match is found.
        """

        patterns = [
            # Example: Stranger.Things.S01E01, stranger things s01e01
            r'(?P<title>.+?)[\.\s\-_]+[Ss](?P<season>\d{1,2})[Ee](?P<episode>\d{1,2})',

            # Example: Stranger.Things.1x01
            r'(?P<title>.+?)[\.\s\-_]+(?P<season>\d{1,2})x(?P<episode>\d{1,2})',

            # Example: Stranger Things Season 1 Episode 2
            r'(?P<title>.+?)[\.\s\-_]+Season[\.\s]*(?P<season>\d{1,2})[\.\s]*Episode[\.\s]*(?P<episode>\d{1,2})',

            # Example: Stranger Things - 1x02 - Episode Title
            r'(?P<title>.+?)[\.\s\-_]+(?P<season>\d{1,2})x(?P<episode>\d{1,2})[\.\s\-_]+.*',

            # Example: Stranger.Things.102 (Where 102 means Season 1, Episode 2)
            r'(?P<title>.+?)[\.\s\-_]+(?P<season>\d)(?P<episode>\d{2})\b',
        ]

        for pattern in patterns:
            match = re.search(pattern, filename, re.IGNORECASE)
            if match:
                title = match.group('title')
                season = int(match.group('season'))
                episode = int(match.group('episode'))
                # Pulisce il titolo da simboli strani
                cleaned_title = re.sub(r'[\.\-_]+', ' ', title).strip()
                logger.debug(f"Extracted TV info: Title='{cleaned_title}', Season={season}, Episode={episode}")
                return cleaned_title, season, episode

        logger.debug("No TV info found in filename.")
        return None, None, None

    def get_file_extension(self, filepath):
        """Gets the file extension from a given filepath."""
        _, ext = os.path.splitext(filepath)
        return ext.lower() if ext else ""

    def is_video_file(self, filename):
        """Checks if a file is a video file based on its extension."""
        return filename.lower().endswith((".mp4", ".avi", ".mkv", ".mov", ".webm"))

    def sanitize_name_before_saving(self, name):
        """Remove or replace characters not allowed in Windows file names."""
        return re.sub(r'[<>:"/\\|?*]', '', name)

    def create_destination_path(self, info, file_type, season=None):
        """Creates the destination folder path based on movie or TV show information."""
        if file_type == "movie":
            movie_name = self.sanitize_name_before_saving(info.original_title or info.title)
            logger.debug(f"Movine name obtained: {movie_name}")
            year = info.year
            movie_folder_name = f"{movie_name} ({year})" if year else movie_name
            destination_path = os.path.join(self.config.LIBRARY_FOLDER, self.config.MOVIE_FOLDER, movie_folder_name)
        
        elif file_type == "tv":
            show_name = self.sanitize_name_before_saving(info.original_name or info.name)
            logger.debug(f"TV show name obtained: {show_name}")
            destination_path = os.path.join(
                self.config.LIBRARY_FOLDER, self.config.TV_FOLDER, show_name
            )

            if season is not None:
                season_folder = f"Season {season:02d}"
                destination_path = os.path.join(destination_path, season_folder)
        
        return destination_path

    def create_new_filename(self, info, file_type, season=None, episode=None):
        """Creates the new filename based on movie or TV show information."""
        if file_type == "movie":
            movie_name = self.sanitize_name_before_saving(info.original_title or info.title)
            year = info.year
            new_filename = f"{movie_name} ({year})" if year else movie_name
        else:
            show_name = self.sanitize_name_before_saving(info.original_name or info.name)
            if season is not None and episode is not None:
                new_filename = f"{show_name} - S{season:02d}E{episode:02d}"
            else:
                new_filename = show_name

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

            # Check if it looks like a TV episode
            title_candidate, season, episode = self.extract_tv_info(filename)

            if title_candidate:
                logger.debug(f"Detected TV show: {title_candidate}, Season {season}, Episode {episode}")
                file_type = "tv"
                info = self.tmdb_client.get_movie_or_tv_info(title_candidate, file_type)
                
            else:
                cleaned_filename = self.clean_filename(filename)
                file_type = "movie"
                info = self.tmdb_client.get_movie_or_tv_info(cleaned_filename, file_type)

            if info:
                file_type = self.tmdb_client.check_movie_or_tv(info)
                destination_path = self.create_destination_path(info, file_type, season)
                new_filename = self.create_new_filename(info, file_type, season, episode)

                if not os.path.exists(destination_path):
                    os.makedirs(destination_path, exist_ok=True)

                self.move_and_rename_file(filepath, destination_path, new_filename)

            else:
                logger.warning(f"Could not identify '{filename}'. Leaving in original folder.")

        except Exception as e:
            logger.error(f"Error processing file '{filename}': {e}")

