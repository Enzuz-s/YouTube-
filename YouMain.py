import logging
import os
import re
import sys
import time
from os import system, name

import yt_dlp

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
FILE_EXTENSIONS = ['.webp', '.png', 'jpg']


def run():
    while True:
        video_url = input("\nplease enter youtube video url: ")
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
            'download_archive': 'downloaded_songs.txt',
            'windowsfilenames': True,
            'outtmpl': sanitize + '/%(title)s.%(ext)s',
            'writesubtitles': True,
            'subtitleslangs': ['en', '-live_chat'],
            'writethumbnail': True,
            'embedthumbnail': True,
            'ignoreerrors': True,
            "error_logger": logger,
            'postprocessors': [
                {'key': 'FFmpegMetadata',
                 'add_metadata': True, },
                {'key': 'FFmpegEmbedSubtitle'},
                {'key': 'EmbedThumbnail',
                 'already_have_thumbnail': True,
                 },
            ],
        }

        url_error = 'Error. Moving on to the next URL.'
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                error_code = ydl.download([video_url])

                if error_code:
                    print('Some videos could not be downloaded')
                else:
                    print("\nDownload completed... ")
                    move_with_thumbnail(sanitize, os.path.join(sanitize, "thumbnail"), FILE_EXTENSIONS)
                    clear()
        except yt_dlp.utils.DownloadError:
            logger.error(url_error)
            return False


def move_with_thumbnail(source, dest, file_extensions):
    thumbnail_dir = os.path.join(os.getcwd(), "thumbnails")
    if not os.path.exists(thumbnail_dir):
        os.makedirs(thumbnail_dir)

    for root, dirs, files in os.walk(source):
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions):
                source_path = os.path.join(root, file)
                thumbnail_name = re.sub(r'\.\w+$', '.' + file_extensions, file, count=1)
                thumbnail_path = os.path.join(thumbnail_dir, thumbnail_name)

                if os.path.realpath(source_path).startswith(os.path.realpath(source)):
                    with open(source_path, 'rb') as src, open(thumbnail_path, 'wb') as dst:
                        dst.write(src.read())
                    os.remove(source_path)

    os.rename(source, dest)


def close():
    time.sleep(0)
    print('\nBye')
    time.sleep(1)
    sys.exit()


def clear():
    while True:
        ans = input("\nDo you want to start again? (y/n) ")
        if ans.lower() == "y":
            system('cls' if name == 'nt' else 'clear')
            time.sleep(0)
            run()
        elif ans.lower() == 'n':
            system('cls' if name == 'nt' else 'clear')
            close()
        else:
            print("Please respond with 'Yes' or 'No'\n")


if __name__ == '__main__':
    try:
        # check_package_updates()

        data = input("Enter file location to save files: ")
        data = data.strip()
        if os.name == 'nt':
            data = data.replace("\\", "/")
        else:
            data = data.replace("\\", os.sep)
        sanitize = os.path.normpath(data)
        if not os.path.isdir(sanitize):
            print("Error: Invalid file location")
        else:
            print("Thumbnails will be moved to " + os.path.join(sanitize, "thumbnail"))

        run()
    except KeyboardInterrupt:
        print('\nInterrupted')
        while True:
            clear()

    except (FileNotFoundError, PermissionError) as e:
        logger.error(f"Error occurred: {e}")
        time.sleep(10)
        close()
