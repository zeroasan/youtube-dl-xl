class VideoInfo:
    def __init__(self, dbid=None, url=None, uploader=None, author=None, isDownloaded=0, isUploaded=0, description=None):
        self.dbid = dbid
        self.url = url
        self.uploader = uploader
        self.author = author
        self.isDownloaded = isDownloaded
        self.isUploaded = isUploaded
        self.description = description
