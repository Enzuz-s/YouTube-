"""
YouTube Downloader Script

This script allows users to download YouTube videos and organize them by moving associated thumbnails.

Requirements:
- Python 3.11 or later
- yt_dlp library (install using: pip install yt-dlp)

Usage:
1. Run the script.
2. Enter a valid YouTube video URL.
3. Specify the file location to save downloaded files.
4. Customize video quality, audio format, and subtitles (optional).
5. The script will download the video, associated subtitles, and thumbnail.
6. Thumbnails will be moved to a 'thumbnails' folder within the specified location.

Author: RhaZenZ0
"""

import logging
import os
import shutil
import subprocess
import sys
import time
from os import system, name
from typing import Dict

import yt_dlp

from Tcolors import Tcolors

logger = logging.getLogger(__name__)
FILE_EXTENSIONS = ('.webp', '.png', '.jpg', '.jpeg')
DEFAULT_VIDEO_QUALITY = 'best'
DEFAULT_AUDIO_FORMAT = 'best'
DEFAULT_SUBTITLES = True

start_info = [
    f"{Tcolors.cyan}Youtube Downloader{Tcolors.clear}",
    f"{Tcolors.gray}Written in Python 3.11*",
    f"{Tcolors.red}By RhaZenZ0" + Tcolors.clear,
]


# Function to configure logging
def configure_logging():
    # Disable logging
    logging.disable(logging.CRITICAL)
    check_yt_dlp_availability()


def check_yt_dlp_availability():
    try:
        subprocess.run(['yt-dlp', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("yt-dlp is installed and available.")
    except FileNotFoundError:
        print("yt-dlp is not installed")
        time.sleep(5)
        exit()


# Function to get user options
def get_user_options() -> Dict[str, str]:
    """
    Gets user-specified options for video quality, audio format, and subtitles.

    Returns:
    - dict: A dictionary containing user options.
    """
    options = {
        'video_quality': input(
            f"Enter video quality (default: {DEFAULT_VIDEO_QUALITY}): ").strip() or DEFAULT_VIDEO_QUALITY,
        'audio_format': input(
            f"Enter audio format (default: {DEFAULT_AUDIO_FORMAT}): ").strip() or DEFAULT_AUDIO_FORMAT,
        'subtitles': input(
            f"Include subtitles? (y/n, default: y ): ").strip().lower() == 'y' or DEFAULT_SUBTITLES
    }
    return options


# Function to move thumbnails
def move_thumbnails(source_folder: str, destination_folder: str) -> None:
    """
    Moves thumbnail files from the source folder to the destination folder.

    Parameters:
    - source_folder (str): The source folder containing thumbnail files.
    - destination_folder (str): The destination folder to move thumbnail files to.
    """
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    files_to_move = [file for file in os.listdir(source_folder) if file.endswith(FILE_EXTENSIONS)]
    for file in files_to_move:
        source_path = os.path.join(source_folder, file)
        destination_path = os.path.join(destination_folder, file)
        shutil.move(source_path, destination_path)
        print(f"Moved {file} to {destination_folder}")
        time.sleep(1)


def remove_ytdl_files(directory: str) -> None:
    """
    Removes files with the .ytdl extension from the specified directory.

    Parameters:
    - directory (str): The directory to remove .ytdl files from.
    """
    files_to_remove = [file for file in os.listdir(directory) if file.endswith('.ytdl')]
    for file in files_to_remove:
        file_path = os.path.join(directory, file)
        os.remove(file_path)


# Function to download video with options
def download_video_with_options(video_url: str, file_location: str, user_options: Dict[str, str]) -> None:
    """
    Downloads a YouTube video using yt_dlp with user-specified options and saves it to the specified file location.

    Parameters:
    - video_url (str): The YouTube video URL.
    - file_location (str): The file location to save the downloaded video.
    - user_options (dict): User-specified options for video quality, audio format, and subtitles.
    """
    try:
        ydl_opts = {
            'format': f'bestvideo[ext=mp4]+bestaudio[ext={user_options["audio_format"]}]/bestvideo+bestaudio/'
                      f'{user_options["video_quality"]}',
            'download_archive': 'downloaded_songs.txt',
            'windowsfilenames': True,
            'outtmpl': os.path.join(file_location, '%(title)s.%(ext)s'),
            'writesubtitles': user_options['subtitles'],
            'subtitleslangs': ['en', '-live_chat'],
            'writethumbnail': True,
            'embedthumbnail': True,
            'ignoreerrors': True,
            "error_logger": logger,
            'postprocessors': [
                {'key': 'FFmpegMetadata', 'add_metadata': True},
                {'key': 'FFmpegEmbedSubtitle'},
                {'key': 'EmbedThumbnail', 'already_have_thumbnail': True},
            ],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

    except yt_dlp.utils.DownloadError as error:
        logger.error(f"Error downloading video: {error}")


# Function to clear the console
def clear_console() -> None:
    system('cls' if name == 'nt' else 'clear')


def first_clear():
    system('cls' if name == 'nt' else 'clear')
    print("\n".join(start_info))
    print(f"{Tcolors.bold}-----------" + Tcolors.clear)


# Function to start again
def start_again(prev_file_location: str) -> None:
    while True:
        ans = input(f"{Tcolors.cyan}\nDo you want to start again? (y/n) " + Tcolors.clear).strip().lower()
        if ans == "y":
            clear_console()
            time.sleep(0)
            run(prev_file_location)
        elif ans == 'n':
            clear_console()
            close()
        else:
            print(f"{Tcolors.red}Please respond with 'Y' or 'N'\n" + Tcolors.clear)


# Function to close the program
def close() -> None:
    time.sleep(0)
    print('\nBye')
    time.sleep(1)
    sys.exit()


# Function to run the program
def run(prev_file_location: str = None) -> None:
    file_location_previous = prev_file_location
    while True:
        video_url = None
        try:
            video_url = input(f"{Tcolors.cyan}\nPlease enter a YouTube video URL: " + Tcolors.clear).strip()
        except Exception as video_id:
            logger.error(f"An error occurred: {video_id}")

        if not file_location_previous:
            file_location = input(f"{Tcolors.cyan}\nEnter file location to save files: " + Tcolors.clear).strip()
        else:
            file_location = input(
                f"{Tcolors.cyan}\nEnter file location to save files (default: {file_location_previous}): "
                + Tcolors.clear).strip()
            if not file_location:
                file_location = file_location_previous

        if os.name == 'nt':
            file_location = file_location.replace("\\", "/")
        else:
            file_location = file_location.replace("\\", os.sep)
        sanitized_location = os.path.normpath(file_location)
        if not os.path.isdir(sanitized_location):
            print(f"{Tcolors.red}Error: Invalid file location" + Tcolors.clear)
            continue

        download_video_with_options(video_url, sanitized_location, get_user_options())
        move_thumbnails(sanitized_location, os.path.join(sanitized_location, 'thumbnails'))
        remove_ytdl_files(sanitized_location)
        clear_console()
        start_again(sanitized_location)


if __name__ == '__main__':
    try:
        configure_logging()
        first_clear()
        run()
    except KeyboardInterrupt:
        print('\nInterrupted')
        while True:
            clear_console()

    except (FileNotFoundError, PermissionError) as e:
        logger.error(f"Error occurred: {e}")
        time.sleep(10)
        close()
    except OSError:
        print("Error: Unrecognized operating system")
        sys.exit()
