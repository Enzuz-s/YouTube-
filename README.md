# YouTube Downloader Script

This Python script allows users to download YouTube videos and organize them by moving associated thumbnails.

## Requirements

- Python 3.11 or later
- yt_dlp library (install using: `pip install yt-dlp` and `pip install -r requirements.txt`)

## Usage

1. Run the script.
2. Enter a valid YouTube video URL.
3. Specify the file location to save downloaded files.
4. Customize video quality, audio format, and subtitles (optional).
5. The script will download the video, associated subtitles, and thumbnail.
6. Thumbnails will be moved to a 'thumbnails' folder within the specified location.

## Author

- **Author**: RhaZenZ0

## Getting Started

1. Clone the repository: `git clone https://github.com/RhaZenZ0/YouTube-.git`
2. Install the required dependencies: `pip install -r requirements.txt`

## Usage Example

```bash
python YouMain.py
```

# Configuration

- **DEFAULT_VIDEO_QUALITY**: Default video quality if not specified by the user.
- **DEFAULT_AUDIO_FORMAT**: Default audio format if not specified by the user.
- **DEFAULT_SUBTITLES**: Default subtitles inclusion if not specified by the user.

# Contributing

Contributions are welcome! Please check the [Contribution Guidelines](CONTRIBUTING.md).

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# Acknowledgments

Special thanks to [yt_dlp](https://github.com/yt-dlp/yt-dlp) for providing the library used in this script.