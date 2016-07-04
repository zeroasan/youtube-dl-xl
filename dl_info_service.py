from db import conn
from video_info import VideoInfo

get_video_info_sql = 'select url, uploader, author, isDownloaded, isUploaded, description from video_info where url = ?'
add_video_sql = 'insert into video_info(url, uploader, author, isDownloaded, isUploaded, description) values(?, ?, ?, ?, ?, ?)'
mark_as_download_sql = 'update video_info set isDownloaded = 1 where url = ?'
mark_as_uploaded_sql= 'update video_info set isUploaded where url = ?'
get_undownload_videos_sql = ''


def get_video_info(url):
    cur = conn.execute(get_video_info_sql, (url,))
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


def add_video_info(video_info):
    conn.execute(add_video_sql, (video_info.url, video_info.uploader, video_info.author, video_info.isDownloaded, video_info.isUploaded, video_info.description, ))
    conn.commit()


def mark_as_downloaded(url):
    conn.execute(mark_as_download_sql)
    conn.commit()


def mark_as_uploaded(url):
    conn.execute(mark_as_uploaded_sql)
    conn.commit()


def get_undownload_videos(count):
    conn.execute(get_undownload_videos_sql)
    conn.commit()

videoArray = get_video_info('http://www.baidu.com')
for videoItem in videoArray:
    print 'Get Url: ' + videoItem.url


