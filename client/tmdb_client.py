import re

from fuzzywuzzy import fuzz
from themoviedb import TMDb, PartialMovie, PartialTV
from config.logger import Logger

logger = Logger(__name__)


class TMDBClient:
    """Client for interacting with the The Movie Database (TMDb) API."""

    def __init__(self, api_key, region):
        """Initializes the TMDb client."""
        self.tmdb = TMDb(key=api_key, language=region)

    def get_movie_or_tv_info(self, filename, type):
        """Search TMDB for movie or TV show info, using multiple fuzzy searches."""
        try:
            # Generate different search variations
            variations = [
                filename,
                filename.lower(),
                re.sub(r" la ", "", filename),  # Remove "La"
                re.sub(r" scheme$", "", filename), #Remove Scheme
            ]

            results = []
            
            for variation in variations:
                logger.debug(f"Searching for: {variation}")
                if type == "tv":
                    result = self.tmdb.search().tv(variation)
                else:
                    result = self.tmdb.search().movies(variation)
                if result:
                    results.append((result[0], fuzz.ratio(filename.lower(), variation)))

            # Sort results by fuzzy score (highest first)
            results.sort(key=lambda x: x[1], reverse=True)

            if results:
                logger.debug(f"Best match found with score {results[0][1]}: {results[0][0]}")
                return results[0][0]  # Return the best matching movie/tv show
            else:
                logger.warning("No matches found.")
                return None

        except Exception as e:
            logger.error(f"Error searching TMDB: {e}")
            return None
        
    def check_movie_or_tv(self, api_type):
        """Check if the API type is a movie or TV show."""
        if isinstance(api_type, PartialMovie):
            return "movie"
        elif isinstance(api_type, PartialTV):
            return "tv"
        else:
            return None
