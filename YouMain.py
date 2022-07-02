from __future__ import unicode_literals

import sys
import time
import traceback
from os import system, name

import youtube_dl as yb

with open("location.txt", 'w+t') as s:
    s.write(input("path to save files: "))
    s.seek(0)
    data = s.read()


def run():
    while True:
        video_url = input("\nplease enter youtube video url: ")
        video_info = yb.YoutubeDL().extract_info(
            url=video_url, download=False)

        filename = f"{video_info['title']}.mp4"
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
            'download_archive': 'downloaded_songs.txt',
            'outtmpl': data + '/%(title)s.%(ext)s',

        }

        with yb.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_info['webpage_url']])
            print("\nDownload complete... {}".format(filename))
            clear()


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
    # noinspection PyBroadException
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
