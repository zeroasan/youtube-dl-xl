import Queue
from threading import Thread
import time
import dl_info_service
from Configuration import download_task_fetch_count, no_download_task_sleep_seconds, queue_size_valve_to_fetch_download_task

downloadQ = Queue.Queue()

def downloadTaskProducer():
    while True:
        if downloadQ.qsize() > queue_size_valve_to_fetch_download_task:
            time.sleep(1)
            continue

        # fetch video info from db when size of queue is less than certain size
        videoArray = dl_info_service.getVideoInfoReadyToDownload(download_task_fetch_count)
        if len(videoArray) == 0:
            time.sleep(no_download_task_sleep_seconds)
            print 'Fetched download task is empty, sleep to wait for {} seconds'.format(no_download_task_sleep_seconds)
            continue

        for item in videoArray:
            downloadQ.put(item)
        dl_info_service.batchMarkProcessingFlag(videoArray)
        print 'Add tasks to download queue, count=' + `downloadQ.qsize()`

def start():
    downloadThread = Thread(target=downloadTaskProducer)
    downloadThread.setDaemon(True)
    downloadThread.start()

    downloadQ.join();

