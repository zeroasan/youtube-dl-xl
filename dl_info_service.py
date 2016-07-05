from db import conn
from video_info import VideoInfo
from exception.DuplicateError import DuplicateError
import sys

__column_names__ = ' url, uploader, author, isDownloaded, isUploaded, description '

__get_video_info_sql__ = 'select ' + __column_names__ + ' from video_info where url = ?'
__add_video_sql__ = 'insert into video_info(' + __column_names__ + ') values(?, ?, ?, ?, ?, ?)'
__mark_as_download_sql__ = 'update video_info set isDownloaded=1 where url = ?'
__mark_as_uploaded_sql__ = 'update video_info set isUploaded=1 where url = ?'
__check_url_exists__ = 'select 1 from video_info where url = ?'

__get_ready_to_downloaded_videos_sql__ = 'select ' + __column_names__ + ' from video_info where isDownloaded = 0 limit ? '
__get_ready_to_uploaded_videos_sql__ = 'select ' + __column_names__ + ' from video_info where isUploaded = 0 and isDownloaded = 1 order by id limit ? '

def getVideoInfo(url):
    cur = conn.execute(__get_video_info_sql__, (url,))

    video_info = VideoInfo()
    for row in cur:
        video_info.url = row[0]
        video_info.uploader = row[1]
        video_info.author = row[2]
        video_info.isDownloaded = row[3]
        video_info.isUploaded = row[4]
        video_info.description = row[5]
        break
    if video_info.url is None:

        return None
    return video_info


def checkExists(url):
    cur = conn.execute(__check_url_exists__, (url,))
    isExists = False
    for row in cur:
        if row[0] == 1 :
            isExists = True
    return isExists


def addVideoInfo(video_info):
    if checkExists(video_info.url):
        raise DuplicateError
    conn.execute(__add_video_sql__, (video_info.url, video_info.uploader, video_info.author, video_info.isDownloaded, video_info.isUploaded, video_info.description,))
    conn.commit()


def markAsDownloaded(url):
    conn.execute(__mark_as_download_sql__, (url,))
    conn.commit()


def markAsUploaded(url):
    conn.execute(__mark_as_uploaded_sql__, (url,))
    conn.commit()


def getVideoInfoReadyToDownload(count = sys.maxint):
    cur = conn.execute(__get_ready_to_downloaded_videos_sql__, (count,))
    array = []
    for row in cur:
        video_info = VideoInfo()
        video_info.url = row[0]
        video_info.uploader = row[1]
        video_info.author = row[2]
        video_info.isDownloaded = row[3]
        video_info.isUploaded = row[4]
        video_info.description = row[5]

        array.append(video_info)
    return array


def getVideoInfoReadyToUploaded(count = sys.maxint):
    cur = conn.execute(__get_ready_to_uploaded_videos_sql__, (count,))
    array = []
    for row in cur:
        video_info = VideoInfo()
        video_info.url = row[0]
        video_info.uploader = row[1]
        video_info.author = row[2]
        video_info.isDownloaded = row[3]
        video_info.isUploaded = row[4]
        video_info.description = row[5]

        array.append(video_info)
    return array
