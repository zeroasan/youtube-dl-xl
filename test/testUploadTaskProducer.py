import DownloadTaskProducer

import logging

logging.basicConfig(level=logging.DEBUG)

thread = DownloadTaskProducer.start()
thread.join()

