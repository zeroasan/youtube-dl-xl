import youtube_dl

ydl = youtube_dl.YoutubeDL()
ydl.download()
ydl.download_with_info_file()
ydl.extract_info()
