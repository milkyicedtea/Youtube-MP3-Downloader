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


def Downloader(url: list):
    for video in range(len(url)):
        print(url)
        print(video)
        with yt_dlp.YoutubeDL(ytdl_format_options) as ydl:
            ydl.download(url[video])
    
    directory = Path(str(os.getcwd()))
    print(directory)
    for filename in directory.iterdir():
        if filename.suffix == ".webp" or filename.suffix == ".jpg":
            print(filename.name)
            image = Image.open(filename)
            new_dir = Path(str(directory) + "\Covers")
            if not new_dir.exists():
                new_dir.mkdir()
            image.resize([image.height, image.height])
            image.save(fp = Path(str(new_dir) + "\\" + filename.name[:-len(filename.suffix)] + ".png"), format = "png")
            filename.unlink()

if __name__ == "__main__":
    txtFile = open('urls.txt', 'r')
    urls = txtFile.readlines()

    Downloader(url = urls)