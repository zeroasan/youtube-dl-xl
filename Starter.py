import DownloadTaskProducer
import Downloader
from Configuration import log_file_path
import logging

# setting log
#logging.basicConfig(filename=log_file_path, level=logging.INFO)
logging.basicConfig(level=logging.INFO)

logging.info('Starting App...')

DownloadTaskProducer.start()
Downloader.start()

logging.info('App started ...')

while True:
    pass