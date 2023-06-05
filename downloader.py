######################
#                    #
#     Downloader     #
#                    #
######################

import os

import yt_dlp

from pathlib import Path

from PIL import Image

import json

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
        # print(url)
        # print(type(url))
        with yt_dlp.YoutubeDL(ytdl_format_options) as ydl:
            # if type(url) is not str:
            for video in url:
                print(video)
                domains = ["youtube.com/", "music.youtube.com/", "youtu.be/"]
                for domain in domains:
                    print('domain {}'.format(domain))
                    if video.startswith('https://' + domain[0]):
                        print('downloading from list with link')
                        ydl.download(video)
                        in_domain = True
                        break
                    else:
                        in_domain = False

                if not in_domain:
                    try:
                        info = ydl.extract_info(f'ytsearch: {url}', download = False)['entries'][0]
                        real_url = info['webpage_url']
                        # print(f'real_url {real_url}')
                        print('downloading from list with search')
                        ydl.download(real_url)
                        break
                    except ...:
                        print('Something went wrong during the download of the file!')
                        break

            # OLD IMPLEMENTATION: DOWNLOADS FROM STR INPUT USING SEARCH
            # else:
            #     # real_url = ydl.dl(name = url, info = ydl.extract_info(f'ytsearch:{url}', download = True))
            #     info = ydl.extract_info(f'ytsearch: {url}', download = False)['entries'][0]
            #     real_url = info['webpage_url']
            #     # print(f'real_url {real_url}')
            #     print('Downloading from str input')
            #     ydl.download(real_url)


        for filename in self.directory.iterdir():
            if filename.suffix in [".webp", ".jpg", ".jpeg", ".png"]:
                # print(filename.name)
                Cover = Image.open(filename)
                Cover = Cover.crop([280, 0, 1000, 720])
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
