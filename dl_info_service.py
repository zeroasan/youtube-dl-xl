from db import conn
from video_info import VideoInfo
from exception.DuplicateError import DuplicateError
from threading import RLock
import sys

__column_name_array__ = ['url', 'uploader', 'author', 'isDownloaded', 'isUploaded', 'description']
__select_column_name_array__ = ['id'] + __column_name_array__

__get_video_info_sql__ = 'select ' + ','.join(__select_column_name_array__) + ' from video_info where url = ?'
__add_video_sql__ = 'insert into video_info(' + ','.join(__column_name_array__) + ') values(?, ?, ?, ?, ?, ?)'
__mark_as_download_sql__ = 'update video_info set isDownloaded=1,isProcessing=0 where url = ?'
__mark_as_uploaded_sql__ = 'update video_info set isUploaded=1,isProcessing=0 where url = ?'
__check_url_exists__ = 'select 1 from video_info where url = ?'

__get_ready_to_downloaded_videos_sql__ = 'select ' + ','.join(__select_column_name_array__) + ' from video_info where isDownloaded = 0 and isProcessing = 0 order by id limit ? '
__get_ready_to_uploaded_videos_sql__ = 'select ' + ','.join(__select_column_name_array__) + ' from video_info where isUploaded = 0 and isDownloaded = 1 and isProcessing = 0 order by id limit ? '

__clear_process_flag__ = 'update video_info set isProcessing = 0'

dbAccessLock = RLock()

def getVideoInfo(url):
    dbAccessLock.acquire()
    try:
        cur = conn.execute(__get_video_info_sql__, (url,))
        video_info = VideoInfo()
        for row in cur:
            for i in range(0, len(__select_column_name_array__)):
                setattr(video_info, __select_column_name_array__[i], row[i])
            break
        if video_info.url is None:
            return None
        return video_info
    finally:
        dbAccessLock.release()


def checkExists(url):
    dbAccessLock.acquire()
    try:
        cur = conn.execute(__check_url_exists__, (url,))
        isExists = False
        for row in cur:
            if row[0] == 1 :
                isExists = True
        return isExists
    finally:
        dbAccessLock.release()


def addVideoInfo(video_info):
    dbAccessLock.acquire()
    try:
        if checkExists(video_info.url):
            raise DuplicateError
        conn.execute(__add_video_sql__, (video_info.url, video_info.uploader, video_info.author, video_info.isDownloaded, video_info.isUploaded, video_info.description,))
        conn.commit()
    finally:
        dbAccessLock.release()


def markAsDownloaded(url):
    dbAccessLock.acquire()
    try:
        conn.execute(__mark_as_download_sql__, (url,))
        conn.commit()
    finally:
        dbAccessLock.release()


def markAsUploaded(url):
    dbAccessLock.acquire()
    try:
        conn.execute(__mark_as_uploaded_sql__, (url,))
        conn.commit()
    finally:
        dbAccessLock.release()

def getVideoInfoReadyToDownload(count = sys.maxint):
    dbAccessLock.acquire()
    try:
        cur = conn.execute(__get_ready_to_downloaded_videos_sql__, (count,))
        array = []
        for row in cur:
            video_info = VideoInfo()
            for i in range(0, len(__select_column_name_array__)):
                setattr(video_info, __select_column_name_array__[i], row[i])

            array.append(video_info)
        return array
    finally:
        dbAccessLock.release()


def getVideoInfoReadyToUpload(count = sys.maxint):
    dbAccessLock.acquire()
    try:
        cur = conn.execute(__get_ready_to_uploaded_videos_sql__, (count,))
        array = []
        for row in cur:
            video_info = VideoInfo()
            for i in range(0, len(__select_column_name_array__)):
                setattr(video_info, __select_column_name_array__[i], row[i])

            array.append(video_info)
        return array
    finally:
        dbAccessLock.release()


def clearProcessingFlag():
    dbAccessLock.acquire()
    try:
        conn.execute(__clear_process_flag__)
        conn.commit()
    finally:
        dbAccessLock.release()

def batchMarkProcessingFlag(videoArray):
    dbAccessLock.acquire()
    try:
        update_processing_sql = 'update video_info set isProcessing = 1 where id in ('+','.join(['?']*len(videoArray))+')'
        ids = []
        for i in range(0, len(videoArray)):
            ids.append(videoArray[i].id)
        conn.execute(update_processing_sql, tuple(ids))
        conn.commit()
    finally:
        dbAccessLock.release()
