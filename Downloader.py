from __future__ import unicode_literals
import time, logging, threading, json, copy, youtube_dl
import DownloadInfoService
import Configuration
from DownloadTaskProducer import videoLinkQ

# Download options for youtube-dl
ydl_option = {
    'writethumbnail' : True,
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': '',
    'writesubtitles': False,
    'simulate': False
}

def download(item):
    try:
        url = item.url
        #copy an instance
        runtime_ydl_option = copy.copy(ydl_option)

        runtime_ydl_option['outtmpl'] = Configuration.getDownloadPath() + '/' + str(item.id) + '-%(id)s.%(ext)s'
        ydl = youtube_dl.YoutubeDL(runtime_ydl_option)

        #process = subprocess.check_output(['youtube-dl', "-o downloads/video/%(uploader)s/%(title)s-%(id)s.%(ext)s", url], stderr=subprocess.STDOUT,shell=True)
        logging.info('[%s] Start downloading [%s]. ', threading.currentThread().name, url)
        #info = ydl.extract_info(url=url, download=False)
        info = ydl.extract_info(url=url)
        # Reduce the json info by removing unused format information
        info['formats'] = None

        logging.info('[%s] after extract info', threading.currentThread().name)

        jsonFileName = Configuration.getDownloadPath() + '/{0}-{1}.json'.format(str(item.id), info['id'])

        with open(jsonFileName, 'w') as f:
            json.dump(info, f, indent=1)

        logging.info("[%s] ******Downloading finished: [%s] - [%s]", threading.currentThread().name, info['title'], info['format'])
        time.sleep(3)

    # Handle Exception
    except Exception as e:
        logging.warn("[%s] Exception: %s.", threading.currentThread().name, e.message)
    else:
        DownloadInfoService.markAsDownloaded(url)
        logging.info('[%s] Downloaded successfully, mark [%s] to downloaded in DB.', threading.currentThread().name, url)


def download_worker():
    logging.info('[%s] start to work... ', threading.currentThread().name)
    while True:
        # threadLock.acquire()
        item = videoLinkQ.get()
        # threadLock.release()
        download(item)
        videoLinkQ.task_done()

def start():
    for i in range(Configuration.runtime_num_of_download_worker):
        downloadWorker = threading.Thread(target=download_worker, name='DownloadWorker-' + `i`)
        downloadWorker.setDaemon(True)
        downloadWorker.start()

