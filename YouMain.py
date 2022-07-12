from __future__ import unicode_literals

from datetime import datetime
import os
import shutil
import sys
import time
import traceback
from os import system, name
import yt_dlp as yb

with open("location.txt", 'w+t') as s:
    s.write(input("path to save files: "))
    s.seek(0)
    data = s.read()
    print("thumbnails will be moved to " + data + "\\thumbnail")


def run():
    while True:
        video_url = input("\nplease enter youtube video url: ")
        video_info = yb.YoutubeDL().extract_info(
            url=video_url, download=False)
        filename = f"{video_info['title']}"

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

        with yb.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_info['webpage_url']])
            print("\nDownload complete... {}".format(filename))
            thumbnail_path()
            clear()


def thumbnail_path():
    start_time = datetime.now()
    sourcepath = data
    sourcefiles = os.listdir(sourcepath)
    destinationpath = data + '/thumbnail'
    thumbnail = os.path.exists(destinationpath)
    if not thumbnail:
        os.makedirs(destinationpath)
    for file in sourcefiles:
        if file.endswith('.webp'):
            shutil.move(os.path.join(sourcepath, file), os.path.join(destinationpath, file))
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
            if name == "nt":
                system('cls')
                time.sleep(0)
                run()

            else:
                system('clear')
                time.sleep(0)
                run()

        elif ans.lower() == 'n':
            if name == 'nt':
                system('cls')
                close()

            else:
                system('clear')
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
        pass
