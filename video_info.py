class VideoInfo:
    def __init__(self, url=None, uploader=None, author=None, isDownloaded=0, isUploaded=0, description=None):
        self.url = url
        self.uploader = uploader
        self.author = author
        self.isDownloaded = isDownloaded
        self.isUploaded = isUploaded
        self.description = description
