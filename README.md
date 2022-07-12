# A YouTube Downloader
* Downloads video and audio plus if available English subtitles are also downloaded, from the specified YouTube link

## Subtitles 
* The subtitles are embedded in tho the .mp4 file

## Thumbnails
* Thumbnails will be moved to a different folder

# To Skip Private video
* you need to edit line 905 or 
``` python
raise DownloadError(message, exc_info)
to # raise DownloadError(message, exc_info)
```