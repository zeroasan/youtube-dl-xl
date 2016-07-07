class VideoInfo:
    def __init__(self, id=None, url=None, uploader=None, author=None, isDownloaded=0, isUploaded=0, isProcessing=0, description=None):
        self.id = id
        self.url = url
        self.uploader = uploader
        self.author = author
        self.isDownloaded = isDownloaded
        self.isUploaded = isUploaded
        self.isProcessing = isProcessing
        self.description = description
