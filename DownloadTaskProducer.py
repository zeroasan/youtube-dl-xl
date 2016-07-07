from threading import Thread
import time, logging, Queue
import DownloadInfoService
from Configuration import download_task_fetch_count, \
    no_download_task_sleep_seconds, queue_size_valve_to_fetch_download_task

downloadQ = Queue.Queue()

def downloadTaskProducer():
    while True:
        if downloadQ.qsize() > queue_size_valve_to_fetch_download_task:
            logging.debug('[Download Producer] Queue is enough for download, sleep 1 second to check queue size')
            time.sleep(1)
            continue

        # fetch video info from db when size of queue is less than certain size
        videoArray = DownloadInfoService.getVideoInfoReadyToDownload(download_task_fetch_count)
        if len(videoArray) == 0:
            time.sleep(no_download_task_sleep_seconds)
            logging.info('[Download Producer] Todo download task loaded is empty, wait for %d seconds to fetch again.',
                         no_download_task_sleep_seconds)
            continue

        for item in videoArray:
            downloadQ.put(item)
        logging.info('[Download Producer] Put %d tasks into download queue, current size is %d',
                     len(videoArray), downloadQ.qsize())

        DownloadInfoService.batchMarkProcessingFlag(videoArray)
        logging.debug('[Download Producer] Mark new added video info to be processing status.')


def start():
    downloadThread = Thread(target=downloadTaskProducer)
    downloadThread.setDaemon(True)
    downloadThread.start()
    logging.info('[Download Producer] Producer has been started.')

    downloadQ.join();

