import os
import traceback

dir_locate = input("the directory to the subtitles file location:")
print(dir_locate)
mp4_locate = input("the directory to the mp4 file location")
print(mp4_locate)


def extractsub():
    """
    This function extract the sub of mkv file and put it in mp4Folder folder.
    """
    for filename in os.listdir(dir_locate):
        if filename.endswith(".mkv"):
            os.system("ffmpeg -i {0}  -map 0:s:0 {0}.ass".format(dir_locate + filename))


def burnsub():
    """
    This function burn/hardsub the sub extract with extractSub() function and put in the final mp4 file.
    """
    for filename in os.listdir(dir_locate):
        if filename.endswith(".mkv"):
            os.system("ffmpeg -i {0} subtitles={0} {1}.mp4".format(dir_locate + filename, mp4_locate + filename[0:-4]))


if __name__ == '__main__':
    try:
        extractsub()
        burnsub()
    except KeyboardInterrupt:
        print('\nInterrupted')
    except Exception:
        with open("log.txt", "w") as log:
            traceback.print_exc(file=log)
            print('\nError is printed to log.txt')
