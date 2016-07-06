import dl_info_service
import time, logging, subprocess, threading
from DownloadTaskProducer import downloadQ
from Configuration import num_of_download_worker


def download(url):
    logging.info('Start downloading [%s]. ', url)
    try:
        #process = subprocess.check_output(['youtube-dl', "-o downloads/video/%(uploader)s/%(title)s-%(id)s.%(ext)s", url], stderr=subprocess.STDOUT,shell=True)
        logging.info('Execute youtube-dl with url: [%s]', url)
        time.sleep(3)
    except subprocess.CalledProcessError as e:
        logging.warn("Exception: %s.", e.output)
    else:
        dl_info_service.markAsDownloaded(url)
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
