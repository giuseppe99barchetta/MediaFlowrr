
# MediaFlowrr

<p align="center">
   <img width="250" height="210" src="https://github.com/giuseppe99barchetta/MediaFlowrr/blob/main/unraid/logo.png">
</p>
This project aim to automatically organizes downloaded files from a source folder (for example JDownloader download folder), renaming them and moving them into appropriate folders based on movie/TV show information retrieved from the TMDB API. It’s designed (but not mandatory) to integrate with media server software like Jellyfin or Plex.

## Prerequisites

- **Python 3.7+**: The script requires Python 3.7 or higher.
- **Docker (Optional)**: For containerized deployment.
- **TMDB API Key (Optional)**: You can obtain an API key from [TMDB](https://www.themoviedb.org/).

### Using Python

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/giuseppe99barchetta/MediaFlowrr
   cd MediaFlowrr
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the Script**:
   Create a `.env` file with your specific settings:

   - `SOURCE_FOLDER`: The directory where your downloader places the media.
   - `LIBRARY_FOLDER`: The root directory where your media files are stored.
   - `MOVIE_FOLDER`: The subfolder within `LIBRARY_FOLDER` for movies.
   - `TV_FOLDER`: The subfolder within `LIBRARY_FOLDER` for TV shows.
   - `TMDB_API_KEY`: API key retrieved from [TMDB](https://www.themoviedb.org/).
   - `CHUNK_SIZE`: The chunk size used when copying files from source folder to media folder (adjust if needed).
   - `CRON_SCHEDULE`: Cron expression to schedule periodic runs inside the container.
   - `TZ` (optional): Timezone string for scheduling.

## Usage

1. **Populate Download Folder**:
   Ensure that the downloader has completed downloading the files you want to organize and they are present in its download folder.

2. **Run the Script**:
   ```bash
   python entrypoint.py
   ```

3. **Monitor Logs**:
   The script will log its progress, including any errors or skipped files. Check the console output for information.

---

1. **Pull the Docker image from GHCR**:
   ```bash
   docker pull ghcr.io/giuseppe99barchetta/mediaflowrr:latest

2. **Run the container, passing your variables**:
```bash
   docker run -d \
     -e SOURCE_FOLDER=/path/to/downloads \
     -e LIBRARY_FOLDER=/path/to/library \
     -e MOVIE_FOLDER=movies \
     -e TV_FOLDER=tv \
     -e TMDB_API_KEY=your_api_key_here \
     -e CRON_SCHEDULE="*/30 * * * *" \
     -e TZ="Europe/Rome" \
     -v /host/downloads:/path/to/downloads:ro \
     -v /host/library:/path/to/library \
     ghcr.io/giuseppe99barchetta/mediaflowrr:latest

2. **Or use the docker-compose.yml**:

```

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please submit an issue or pull request on GitHub.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
