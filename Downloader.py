import DownloadInfoService
import time, logging, subprocess, threading
from DownloadTaskProducer import downloadQ
from Configuration import num_of_download_worker
import Configuration
import youtube_dl
import json

ydl_option = {
    'writethumbnail' : True,
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': '',
    'writesubtitles': True,
    'simulate': True
}


def __determine__(videoFormat, formatId):
    return videoFormat['format_id'] == formatId

def download(url):
    logging.info('Start downloading [%s]. ', url)
    try:

        ydl_option['outtmpl'] = Configuration.runtime_download_path + '/%(title)s-%(id)s.%(ext)s'
        ydl = youtube_dl.YoutubeDL(ydl_option)

        #process = subprocess.check_output(['youtube-dl', "-o downloads/video/%(uploader)s/%(title)s-%(id)s.%(ext)s", url], stderr=subprocess.STDOUT,shell=True)
        logging.info('Execute youtube-dl with url: [%s]', url)
        #info = ydl.extract_info(url=url, download=False)
        info = ydl.extract_info(url=url)
        # Redule the json info by removing unused format information
        info['formats'] = [x for x in info['formats'] if __determine__(x, info['format_id'])]

        jsonFileName = Configuration.runtime_download_path + '\{0}-({1}).json'.format(info['title'], info['id'])

        with open(jsonFileName, 'w') as f:
            json.dump(info, f, indent=1)

        logging.info("***downloaded: [%s] - [%s]", info['title'], info['format'])
        time.sleep(3)

    # Handle Exception
    except Exception as e:
        logging.warn("Exception: %s.", e.output)
    else:
        DownloadInfoService.markAsDownloaded(url)
        logging.info('Downloaded successfully: [%s] ', url)


def download_worker():
    logging.info('[%s] start to work... ', threading.currentThread().name)
    while True:
        # threadLock.acquire()
        item = downloadQ.get()
        # threadLock.release()
        download(item.url)
        downloadQ.task_done()




def start():
    for i in range(num_of_download_worker):
        t = threading.Thread(target=download_worker, name='DownloadWorker-' + `i`)
        t.daemon = True
        t.start()


#download("https://www.youtube.com/watch?v=HNOT_feL27Y", '')
#download("http://v.youku.com/v_show/id_XMTYyOTg3OTU2NA==?from=y1.3-dv-2016new-239-23143.225965.1-3", '')
#print 'after download'
