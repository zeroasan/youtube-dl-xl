import Queue
import array
from threading import Thread, Lock
import thread
import time
import random
import dl_info_service
from Configuration import download_task_fetch_count, upload_task_fetch_count

downloadQ = Queue.Queue()
uploadQ = Queue.Queue()


def downloadTaskProducer():
    while True:
        if downloadQ.qsize() > 5:
            time.sleep(1)
            continue

        # fetch video info from db when size of queue is less than certain size
        videoArray = dl_info_service.getVideoInfoReadyToDownload(download_task_fetch_count)
        for item in videoArray:
            downloadQ.put(item)
        print 'Add tasks to download queue, count=' + `downloadQ.qsize()`

t2 = Thread(target=downloadTaskProducer)
t2.start();


def uploadTaskProducer():
    while True:
        if uploadQ.qsize() > 5:
            time.sleep(1)
            continue

        # fetch video info from db when size of queue is less than certain size
        videoArray = dl_info_service.getVideoInfoReadyToUploaded(upload_task_fetch_count)

        # TODO add a processing column, when adding to task queue, set column value to 1. In initialization step, clear all processing flag
        # Just one column is enough, because one video info can only be processed in one task.(Can only be ready to download or update)

        for item in videoArray:
            uploadQ.put(item)
            print 'Add tasks to download queue, count=' + `uploadQ.qsize()`


uploadQ.join();
