import logging
import os
import subprocess
import sys
import time
import traceback
from os import system, name

import yt_dlp

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
# File extensions to move to the "thumbnail" directory
FILE_EXTENSIONS = ['.webp', '.png', 'jpg']


class PackageUpdateError(Exception):
    pass


def check_package_updates():
    try:
        with open(os.devnull, "w") as fnull:
            packages = subprocess.check_output(["pip", "list", "--outdated"], stderr=fnull)
    except subprocess.CalledProcessError as e:
        raise PackageUpdateError(f"Error checking outdated packages: {e}") from e

    packages = packages.decode().split("\n")[2:-1]

    if packages:
        print("The following packages have updates available:")
        for package in packages:
            package_name = package.split()[0]
            print(package_name)
        answer = input("Do you want to update all packages? (y/n) ").lower()
        if answer == 'y':
            for package in packages:
                package_name = package.split()[0]
                try:
                    subprocess.check_call(["pip", "install", "--upgrade", package_name], stdout=fnull, stderr=fnull)
                    print(f"Successfully updated {package_name}")
                except subprocess.CalledProcessError as e:
                    raise PackageUpdateError(f"Error updating package {package_name}: {e}") from e
    else:
        print("All packages are up to date")


def run():
    # Loop indefinitely to download multiple videos
    while True:
        # Get the URL of the YouTube video from the user
        video_url = input("\nplease enter youtube video url: ")
        # noinspection SpellCheckingInspection
        # Set the options for the yt_dlp library
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
            'download_archive': 'downloaded_songs.txt',
            'windowsfilenames': True,
            'outtmpl': sanitize + '/%(title)s.%(ext)s',
            'writesubtitles': True,
            'subtitleslangs': ['en', '-live_chat'],
            'writethumbnail': True,
            'embedthumbnail': True,
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

        # Error message to log if an error occurs while downloading the video
        url_error = 'Error. Moving to next URL.'
        try:
            # Use the yt_dlp library to download the video and its thumbnail
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                error_code = ydl.download([video_url])

                # Check if any videos failed to download, and log an error if so
                if error_code:
                    print('Some videos failed to download ')
                else:
                    print("\nDownload complete... ")
                    # Move the thumbnail to the appropriate directory
                    thumbnail_path(FILE_EXTENSIONS)
                    # Clear the screen and ask the user if they want to download another video
                    clear()
        except yt_dlp.utils.DownloadError:
            logger.error(url_error)
            return False


def move_file(src_path, dest_path):
    try:
        os.rename(src_path, dest_path)
        print(f"Moved file {src_path} to {dest_path}")
    except OSError as e:
        print(f"Error moving file {src_path} to {dest_path}: {e}")


def thumbnail_path(file_extensions):
    thumbnail_dir = os.path.join(sanitize, 'thumbnail')
    os.makedirs(thumbnail_dir, exist_ok=True)
    for file in os.listdir(sanitize):
        if os.path.splitext(file)[1] in file_extensions:
            src_path = os.path.join(sanitize, file)
            dest_path = os.path.join(thumbnail_dir, file)
            move_file(src_path, dest_path)


def close():
    # Wait for one second before closing the program
    time.sleep(0)
    print('\nBye')
    time.sleep(1)
    sys.exit()


def clear():
    # Loop indefinitely until the user provides a valid response
    while True:
        # Ask the user if they want to download another video
        ans = input("\nDo you want to start again? (y/n) ")
        # If the user responds with "y", clear the screen and start the download process again
        if ans.lower() == "y":
            system('cls' if name == 'nt' else 'clear')
            time.sleep(0)
            run()
        # If the user responds with "n", clear the screen and close the program
        elif ans.lower() == 'n':
            system('cls' if name == 'nt' else 'clear')
            close()
        # If the user provides any other response, ask them to try again
        else:
            print("Please respond with 'Yes' or 'No'\n")


# If the script is run directly (i.e. not imported as a module), run the main download process
if __name__ == '__main__':
    # noinspection PyBroadException
    try:
        check_package_updates()

        data = input("Enter file location to save files: ")
        # Remove any trailing or leading white spaces
        data = data.strip()
        # Check the operating system and use the appropriate path separator
        if os.name == 'nt':
            data = data.replace("\\", "/")
        else:
            data = data.replace("\\", os.sep)
        # Remove any non-alphanumeric characters except for a few allowed characters
        data = ''.join(e for e in data if e.isalnum() or e in ['/', '_', '-', '.', ':'])
        # Normalize the path to remove any redundant separators
        sanitize = os.path.normpath(data)
        # Check if the path exists and is a directory
        if not os.path.isdir(sanitize):
            print("Error: Invalid file location")
        else:
            # Print the sanitized input
            print("Thumbnails will be moved to " + os.path.join(sanitize, "thumbnail"))

        run()
    except KeyboardInterrupt:
        # If the user interrupts the process (e.g. with Ctrl+C), log an error and ask if they want to try again
        print('\nInterrupted')
        while True:
            clear()
    except Exception:
        # If any other error occurs, log it to a file and print a message to the user
        with open("log.txt", "w") as log:
            traceback.print_exc(file=log)
            print('\nError is printed to log.txt')
            close()
