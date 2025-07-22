
# MediaFlowrr

<p align="center">
   <img width="250" height="210" src="https://github.com/giuseppe99barchetta/MediaFlowrr/blob/main/unraid/logo.png">
</p>
This project aim to automatically organizes downloaded files from a source folder (for example JDownloader download folder), renaming them and moving them into appropriate folders based on movie/TV show information retrieved from the TMDB API. It’s designed (but not mandatory) to integrate with media server software like Jellyfin or Plex.

## ✨ Main Features
✅ **Automatic organization of movies and TV shows** using TMDB metadata <br>
📁 **Multi-folder support**: recursively scans the source directory <br>
🧠 **Language detection** from file names <br>
🛠️ **Smart renaming** with uniform formatting <br>
🕘 **Full cron job** support for scheduled scans <br>
🔧 **Simple configuration** via environment variables <br>
🐳 **Available as a Docker container** via GHCR/Docker Hub or Python Script <br>

## Prerequisites

- **Python 3.7+**: The script requires Python 3.7 or higher.
- **Docker (Optional)**: For containerized deployment.
- **TMDB API Key (Optional)**: You can obtain an API key from [TMDB](https://www.themoviedb.org/).

## How to run MediaFlowrr?

You can choose three different method to run MediaFlowrr:

1. [Using Docker](#using-docker)
2. [Using Python](#using-python)
3. [As system service](#running-as-a-linux-service)

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

4. **Run MediaFlowrr**:
```bash
   python entrypoint.sh
```

### Running as a Linux service

You can run MediaFlowrr automatically at boot using `systemd`.

### 1. Create a service unit file

Save the following as `/etc/systemd/system/mediaflowrr.service`:

```ini
[Unit]
Description=MediaFlowrr - Media Organizer
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/your_username/MediaFlowrr
EnvironmentFile=/home/your_username/MediaFlowrr/.env
ExecStart=/usr/bin/python3 /home/your_username/MediaFlowrr/entrypoint.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

> 🔁 Replace `your_username` and paths as needed.

---

### 2. Configure the environment variables
   Create a `.env` file with your specific settings:

   - `SOURCE_FOLDER`: The directory where your downloader places the media.
   - `LIBRARY_FOLDER`: The root directory where your media files are stored.
   - `MOVIE_FOLDER`: The subfolder within `LIBRARY_FOLDER` for movies.
   - `TV_FOLDER`: The subfolder within `LIBRARY_FOLDER` for TV shows.
   - `TMDB_API_KEY`: API key retrieved from [TMDB](https://www.themoviedb.org/).
   - `CHUNK_SIZE`: The chunk size used when copying files from source folder to media folder (adjust if needed).
   - `CRON_SCHEDULE`: Cron expression to schedule periodic runs inside the container.
   - `TZ` (optional): Timezone string for scheduling.

---

### 3. Enable and start the service

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable mediaflowrr
sudo systemctl start mediaflowrr
```

To check logs:
```bash
journalctl -u mediaflowrr -f
```

---

### Using Docker

1. **Pull the Docker image from Docker Hub**:
```bash
   docker pull ciuse99/mediaflowrr:latest
```

2. **Run the container, passing your variables**:
```bash
   docker run -d \
     -e MOVIE_FOLDER=movies \
     -e TV_FOLDER=tv \
     -e TMDB_API_KEY=your_api_key_here \
     -e CRON_SCHEDULE=*/30 * * * * \
     -e TZ=Europe/Rome \
     -e CHUNK_SIZE=4096 \
     -e LOG_LEVEL=INFO \
     -e FILE_NAME_LANGUAGE=en-EN \
     -v /host/downloads:/path/to/downloads:ro \
     -v /host/library:/path/to/library \
     ciuse99/mediaflowrr:latest
```

2. **Or use the docker-compose**:
```yaml
   version: "3.8"
   services:
     mediaflowrr:
       image: ciuse99/mediaflowrr:latest
       volumes:
         - /mnt/jdownloader:/media/source # Path to your downloaded media folder
         - /mnt/jellyfin:/media/library # Path to your media library
       environment:
         - MOVIE_FOLDER=movies # Path to your movie folder inside the media library
         - TV_FOLDER=tv # Path to your TV shows folder inside the media library
         - CHUNK_SIZE=4096 # Size of the chunks to process (leave as default unless you have specific needs)
         - TMDB_API_KEY=YOUR_TMDB_API_KEY # Replace with your actual TMDB API key
         - LOG_LEVEL=INFO # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
         - FILE_NAME_LANGUAGE=en-EN # Language for file names (e.g., en-EN, it-IT)
         - CRON_SCHEDULE=*/30 * * * * # Cron schedule for running the service (every 30 minutes)
         - TZ=Europe/Rome # Set your timezone
       restart: unless-stopped
```

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please submit an issue or pull request on GitHub.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
