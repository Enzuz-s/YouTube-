from __future__ import unicode_literals

from datetime import datetime
import os
import shutil
import sys
import time
import traceback
from os import system, name
import yt_dlp



mystring = """
MMMWNK00OOOkkkkkkkkkkkkkkkkkOOO0KKNWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMWNNNWMMMMMMMMMMMMMMMMMMM
MW0dc:;,,,,,,,,,,,,,,,,,,,,,,,,,;;cd0WMMMXxdd0WMMXxdd0WMMMMMMMMMMMMMMMMMMMXxddddddddd0WMMMMMMMMMO:,c0MMMMMMMMMMMMMMMMMMM
WO:,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,c0WMMXc..cXMWx..,OMMMMMMMMMMMMMMMMMMMMO;''.....',dNMMMMMMMMWx..'kMMMMMMMMMMMMMMMMMMM
Nd,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,dNMMWk'.,OMXc..oNMMMMMMMMMMMMMMMMMMMMWXX0c..,kXXNMMMMMMMMMWx..'kMMMMMMMMMMMMMMMMMMM
Xl,,,,,,,,,,,,,:ol;,,,,,,,,,,,,,,,,,,oXWMMXl..oNk'.;0WKxoloddkXMMXxdxKWNkddOWNo..;0WKxdxXMXxdxKWx..'dOdooOWMMW0dolod0NMM
Kc,,,,,,,,,,,,,oXN0ko:,,,,,,,,,,,,,,,lKMMMMO,.;kl..dXk,..:;...:0Mk'..dW0;..lXNo..;0Wd..'kMO'..dNx...;c,..'xWNo..,:,..dNM
0c,,,,,,,,,,,,,oXMMMWXOdc,,,,,,,,,,,,cKMMMMNo..;,.:K0;..lX0;...oNk'..dW0;..lNNo..;0Wd..'kMO'..dNx...dN0;..cXO'.'kWx..,0M
0c,,,,,,,,,,,,,oXMMMMWXko;,,,,,,,,,,,c0WMMMM0;....xWk'..dWX:...:Xk'..dW0;..lNNo..;0Wd..'kMO'..dWx..'OMXc..:0d..,kWk'.'kM
0c,,,,,,,,,,,,,oXWNKko:,,,,,,,,,,,,,,lKWMMMMNd...cXMk'..dWXc...:Kk'..dW0;..lNNo..;0Wd..'kMO'..dNx..'kMXc..:0d...;:,..'OM
Kl,,,,,,,,,,,,,ckxl:,,,,,,,,,,,,,,,,,lXMMMMMMO'..dWMk'..dWXc...:Kk'..dW0;..lNNo..;0Wd..'kMO'..dNx..'kMXc..:0d..'okkkkOXM
Xo,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,dNMMMMMMO,..dWMO,..oNK:...cXk'..dW0;..lNNo..;0Wd..'kMO'..dNx..'kMK:..cXx..,OMKocdXM
Wk;,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,:kWMMMMMMO,..dWMNl..,ol...'kW0,..;ol'..cNNo..;0Mk'..:dc'..dWx...:dc...dWK:..:dc..:KM
MXx:,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,ckNMMMMMMMKl:cOWMMXxc;;;:clOWMWkc;;cxxc:xNWkc:oXMNx:,;cxdccOW0c:ldl;;:xNMWKd:;;;cdKWM
MMWXOkxxdddooooooooooooooooodddxxkOXWMMMMMMMMMWWWWMMMMMWNNNWWWMMMMMWNNWMMWWWMMWWWWMMMMWNNWMMWWWMWWWWMWNNWMMMMMMWNNNWMMMM
MMMMMMWMWWWWWWWWWWWWWWWWWWWWWWWMWWWWMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
"""# noqa

with open("location.txt", 'w+t') as s:
    print(mystring)
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
