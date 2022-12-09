import os
import platform
import shutil
import sys
import threading
import time
import traceback
from os import system

import yt_dlp


class YoutubeDL:
    def __init__(self, video_url, data_path):
        self.video_url = video_url
        self.data_path = data_path
        self.ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
            'download_archive': 'downloaded_songs.txt',
            'windowsfilenames': True,
            'outtmpl': data_path + '/%(title)s.%(ext)s',
            'writesubtitles': True,
            'subtitleslangs': ['en', '-live_chat'],
            'writethumbnail': True,
            'embedthumbnail': True,
            'postprocessors': [
                {'key': 'FFmpegMetadata',
                 'add_metadata': True, },
                {'key': 'FFmpegEmbedSubtitle'},
                {'key': 'EmbedThumbnail',
                 'already_have_thumbnail': True,
                 },
            ],
        }

    def download(self):
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                error_code = ydl.download([self.video_url])
                video_info = ydl.extract_info(url=self.video_url, download=False)
                filename = f"{video_info['title']}"
                print('Some videos failed to download {}'.format(filename) if error_code
                      else "\nDownload complete... {}".format(filename))
        except yt_dlp.utils.DownloadError:
            print('Error. Moving to next URL.')
            return False
        except yt_dlp.utils.ExtractorError:
            print('Error. Moving to next URL.')
            return False


class FileManager:
    def __init__(self, data_path):
        self.data_path = data_path

    def move_thumbnail(self):

        source_path = self.data_path
        source_files = os.listdir(source_path)
        destination_path = self.data_path + '/thumbnail'
        temp_path = self.data_path + '/temp'

        # Hide the temp folder from the user
        if platform.system() == 'Windows':
            system('attrib +h ' + temp_path)
        else:
            system('chflags hidden ' + temp_path)

        # Create the thumbnail and temp directories if they don't exist
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)

        # Move the thumbnail files to the temp directory
        for file in source_files:
            if file.endswith('.webp'):
                shutil.move(os.path.join(source_path, file), os.path.join(temp_path, file))

        # Wait for all downloads to finish
        while threading.active_count() > 0:
            time.sleep(1)

        # Move the files from the temp directory to the thumbnail directory
        temp_files = os.listdir(temp_path)
        for file in temp_files:
            shutil.move(os.path.join(temp_path, file), os.path.join(destination_path, file))


class InputHandler:
    @staticmethod
    def clear_screen():
        if platform.system() == 'Windows':
            system('cls')
        else:
            system('clear')

    @staticmethod
    def get_save_location():
        with open("location.txt", 'w+t') as save_location_file:
            save_location_file.write(input("path to save files: "))
            save_location_file.seek(0)
            data = save_location_file.read()
            print("thumbnails will be moved to " + data + "\\thumbnail")
        return data

    @staticmethod
    def get_video_url():
        return input("\nplease enter youtube video url: ")

    @staticmethod
    def prompt_continue():
        while True:
            ans = input("\nDo you want to start again? (y/n) ")
            if ans.lower() == "y":
                InputHandler.clear_screen()
                time.sleep(0)
                return True
            elif ans.lower() == 'n':
                InputHandler.clear_screen()
                return False
            else:
                print("Please respond with 'Yes' or 'No'\n")


class Application:
    def __init__(self):
        self.data_path = InputHandler.get_save_location()
        self.file_manager = FileManager(self.data_path)

    def run(self):
        while True:
            video_url = InputHandler.get_video_url()
            youtube_dl = YoutubeDL(video_url, self.data_path)
            if youtube_dl.download():
                self.file_manager.move_thumbnail()
            if not InputHandler.prompt_continue():
                break

    def close(self):
        print('\nBye')
        time.sleep(1)
        sys.exit()


if __name__ == '__main__':
    try:
        app = Application()
        app.run()
    except KeyboardInterrupt:
        print('\nInterrupted')
        app.close()
    except Exception:
        with open("log.txt", "w") as log:
            traceback.print_exc(file=log)
            print('\nError is printed to log.txt')
            app.close()
