import Queue
from threading import Thread
import time
import dl_info_service
from Configuration import upload_task_fetch_count, no_upload_task_sleep_seconds, queue_size_valve_to_fetch_upload_task

uploadQ = Queue.Queue()

def uploadTaskProducer():
    while True:
        if uploadQ.qsize() > queue_size_valve_to_fetch_upload_task:
            time.sleep(1)
            continue

        # fetch video info from db when size of queue is less than certain size
        videoArray = dl_info_service.getVideoInfoReadyToUpload(upload_task_fetch_count)
        if len(videoArray) == 0:
            time.sleep(no_upload_task_sleep_seconds)
            print 'Fetched upload task is empty, sleep to wait for {} seconds'.format(no_upload_task_sleep_seconds)
            continue
        dl_info_service.batchMarkProcessingFlag(videoArray)

        for item in videoArray:
            uploadQ.put(item)
        dl_info_service.batchMarkProcessingFlag(videoArray)
        print 'Add {} tasks to upload queue.'.format(`uploadQ.qsize()`)


#uploadQ.join()
def start():
    uploadThread = Thread(target=uploadTaskProducer)
    uploadThread.setDaemon(True)
    uploadThread.start()

    uploadQ.join();
