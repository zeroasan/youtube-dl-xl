import dl_info_service
import subprocess
from threading import Thread
import time
from DownloadTaskProducer import downloadQ
from Configuration import num_of_download_worker
import dl_info_service


def download(name, url):
    print 'Thread:' + name + ', start downloading: ' + url
    try:
        #process = subprocess.check_output(['youtube-dl', "-o downloads/video/%(uploader)s/%(title)s-%(id)s.%(ext)s", url], stderr=subprocess.STDOUT,shell=True)
        print 'Thread:{}, youtube-dl executed url:{}'.format(name, url)
        time.sleep(3)
    except subprocess.CalledProcessError as e:
        print "exception: " + e.output
    else:
        dl_info_service.markAsDownloaded(url)
        print 'Thread:' + name + ', downloaded successfully: ' + url


def download_worker(name):
    print 'Worker started: ' + name
    while True:
        # threadLock.acquire()
        item = downloadQ.get()
        # threadLock.release()
        download(name, item.url);
        downloadQ.task_done()

    print 'Worker done: ' +  name

def start():
    for i in range(num_of_download_worker):
        t = Thread(target=download_worker, args=('DownloadWorker' + `i`,))
        t.daemon = True
        t.start()


#download("https://www.youtube.com/watch?v=HNOT_feL27Y", '')
#download("http://v.youku.com/v_show/id_XMTYyOTg3OTU2NA==?from=y1.3-dv-2016new-239-23143.225965.1-3", '')
#print 'after download'
