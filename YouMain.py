from __future__ import unicode_literals

import os
import shutil
import sys
import time
import traceback
from datetime import datetime
from os import system, name

import yt_dlp


with open("location.txt", 'w+t') as s:
    s.write(input("path to save files: "))
    s.seek(0)
    data = s.read()
    print("thumbnails will be moved to " + data + "\\thumbnail")


def run():
    while True:
        video_url = input("\nplease enter youtube video url: ")
        # noinspection SpellCheckingInspection
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
            'download_archive': 'downloaded_songs.txt',
            'windowsfilenames': True,
            'outtmpl': data + '/%(title)s.%(ext)s',
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
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                error_code = ydl.download([video_url])
                video_info = ydl.extract_info(url=video_url, download=False)
                filename = f"{video_info['title']}"
                print('Some videos failed to download {}'.format(filename) if error_code
                      else "\nDownload complete... {}".format(filename))
                thumbnail_path()
                clear()
        except yt_dlp.utils.DownloadError:
            print('Error. Moving to next URL.')
            continue
        except yt_dlp.utils.ExtractorError:
            print('Error. Moving to next URL.')
            continue


def thumbnail_path():
    start_time = datetime.now()
    source_path = data
    source_files = os.listdir(source_path)
    destination_path = data + '/thumbnail'
    thumbnail = os.path.exists(destination_path)
    if not thumbnail:
        os.makedirs(destination_path)
    for file in source_files:
        if file.endswith('.webp'):
            shutil.move(os.path.join(source_path, file), os.path.join(destination_path, file))
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))


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
        run()
    except KeyboardInterrupt:
        print('\nInterrupted')
        while True:
            clear()
    except Exception:
        with open("log.txt", "w") as log:
            traceback.print_exc(file=log)
            print('\nError is printed to log.txt')
            close()
