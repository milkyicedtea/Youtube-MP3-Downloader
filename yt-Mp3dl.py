####################
#                  #
#     yt-Mp3dl     #
#                  #
####################


import json
import os
from PIL import Image
from pathlib import Path

import yt_dlp

ytdl_format_options = {
    'format': 'mp3/bestaudio/best',
    'outtmpl': '/%(title)s.%(ext)s',
    'writethumbnail': 'true',
    'nooverwrites': 'true',
    'postprocessors': 
    [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }]
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class Downloader:
    def __init__(self):
        self.directory = Path(str(os.getcwd()))
        self.downloaded = {
            "songs": [

            ]
        }

    def Download(self, url: list[str]):
        for video in url:
            print(video)
            with yt_dlp.YoutubeDL(ytdl_format_options) as ydl:
                ydl.download(video)

        for filename in self.directory.iterdir():
            if filename.suffix in [".webp", ".jpg", ".jpeg", ".png"]:
                # print(filename.name)
                Cover = Image.open(filename)
                Cover.resize([Cover.height, Cover.height])
                cover_dir = Path(str(self.directory) + "\\" + "Covers")
                if not cover_dir.exists():
                    cover_dir.mkdir()
                if Path(str(cover_dir) + "\\" + str(filename.name)).exists():
                    # filename.rename(str(image_dir) + "\\" + filename.name)
                    filename.unlink()
                else:
                    Cover.save(fp = Path(str(cover_dir) + "\\" + filename.name[:-len(filename.suffix)] + ".png"), format = "png")
                    filename.unlink()

            elif filename.suffix in [".mp3", ".wav", ".aac", ".ogg"]:
                # print(filename.name)
                song_dir = Path(str(self.directory) + "\\" + "Songs")
                if not song_dir.exists():
                    song_dir.mkdir()
                # print(Path(str(song_dir) + str(filename.name)).exists())
                # print(str(song_dir) + str(filename.name))
                if Path(str(song_dir) + "\\" + str(filename.name)).exists():
                    # filename.rename(str(song_dir) + "\\" + filename.name)
                    filename.unlink()
                else:
                    filename.rename(str(song_dir) + "\\" + filename.name)
                    to_append: dict = {
                        "name": f"{filename.name[:-len(filename.suffix)]}",
                        "path": f"{str(song_dir)}\\{str(filename.name)}"
                    }
                    self.downloaded["songs"].append(to_append)

    def WriteJson(self):
        with open("Songs.json", "w") as outfile:
            json.dump(self.downloaded, outfile, indent = 1)
            outfile.close()
        print('All the songs were downloaded and a record can be found in "Songs.Json" ')


if __name__ == "__main__":
    txtFile = open('urls.txt', 'r')
    urls = txtFile.readlines()

    downloader = Downloader()
    downloader.Download(urls)
    downloader.WriteJson()