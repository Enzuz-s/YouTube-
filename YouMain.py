import logging
import os
import shutil
import sys
import time
from os import system, name

import yt_dlp
from yt_dlp.utils import DownloadError
from term_col import Tcolors

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
FILE_EXTENSIONS = ['.webp', '.png', 'jpg']

start_info = [
    f"{Tcolors.cyan}Youtube Downloader{Tcolors.clear}",
    f"{Tcolors.gray}Written in Python 3.11*",
    f"{Tcolors.red}By RhaZenZ0" + Tcolors.clear,
]


def download_video(video_url, file_location):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
        'download_archive': 'downloaded_songs.txt',
        'windowsfilenames': True,
        'outtmpl': os.path.join(file_location, '%(title)s.%(ext)s'),
        'writesubtitles': True,
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
        try:
            ydl.download([video_url])
        except DownloadError as error:
            logger.error(f"Error downloading video: {error}")


def move_thumbnails(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    files_to_move = [file for file in os.listdir(source_folder) if file.endswith('.webp')]
    for file in files_to_move:
        source_path = os.path.join(source_folder, file)
        destination_path = os.path.join(destination_folder, file)
        shutil.move(source_path, destination_path)
        print(f"Moved {file} to {destination_folder}")
        time.sleep(1)


def first_clear():
    system('cls' if name == 'nt' else 'clear')
    print("\n".join(start_info))
    print(f"{Tcolors.bold}-----------" + Tcolors.clear)


def clear_console():
    system('cls' if name == 'nt' else 'clear')


def start_again(prev_file_location):
    while True:
        ans = input(f"{Tcolors.cyan}\nDo you want to start again? (y/n) " + Tcolors.clear)
        if ans.lower() == "y":
            clear_console()
            time.sleep(0)
            run(prev_file_location)
        elif ans.lower() == 'n':
            clear_console()
            close()
        else:
            print(f"{Tcolors.red}Please respond with 'Y' or 'N'\n" + Tcolors.clear)


def close():
    time.sleep(0)
    print('\nBye')
    time.sleep(1)
    sys.exit()


def run(prev_file_location=None):
    file_location_previous = prev_file_location
    while True:
        video_url = input(f"{Tcolors.cyan}\nPlease enter a YouTube video URL: " + Tcolors.clear)

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

        download_video(video_url, sanitized_location)
        move_thumbnails(sanitized_location, os.path.join(sanitized_location, 'thumbnails'))
        clear_console()
        start_again(sanitized_location)


if __name__ == '__main__':
    try:
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
