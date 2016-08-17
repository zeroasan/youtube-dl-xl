from threading import Thread
import time, logging, Queue
import DownloadInfoService
from Configuration import download_task_fetch_count, \
    no_download_task_sleep_seconds, queue_size_valve_to_fetch_download_task

videoLinkQ = Queue.Queue()
queue_size_check_interval = 5

def downloadTaskProducer():
    while True:
        if videoLinkQ.qsize() > queue_size_valve_to_fetch_download_task:
            logging.debug('[Download Producer] Queue size %d, is enough for download, sleep %d second to check queue size',
                          len(videoLinkQ), queue_size_check_interval)
            time.sleep(queue_size_check_interval)
            continue

        # fetch video info from db when size of queue is less than certain size
        videoArray = DownloadInfoService.getVideoInfoReadyToDownload(download_task_fetch_count)
        if len(videoArray) == 0:
            time.sleep(no_download_task_sleep_seconds)
            logging.info('[Download Producer] Todo download task loaded is empty, wait for %d seconds to fetch again.',
                         no_download_task_sleep_seconds)
            continue

        for item in videoArray:
            videoLinkQ.put(item)
        logging.info('[Download Producer] Put %d tasks into download queue, current size is %d',
                     len(videoArray), len(videoLinkQ))

        DownloadInfoService.batchMarkProcessingFlag(videoArray)
        logging.debug('[Download Producer] Mark new added video info to be processing status.')


def start():
    downloadThread = Thread(target=downloadTaskProducer)
    downloadThread.setDaemon(True)
    downloadThread.start()
    logging.info('[Download Producer] Producer has been started.')
    return downloadThread

