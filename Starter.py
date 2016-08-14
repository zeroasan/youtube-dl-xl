import os
import DownloadTaskProducer
import Downloader
import Configuration
import LogConfig
import logging
import DownloadInfoService
import VideoLinkExtractor

# setting log
#logging.basicConfig(filename=log_file_path, level=logging.INFO)

# Initialize Configuration
inputSearchText = raw_input('1. Please input the key words you want to search.[default: ' + Configuration.runtime_search_text + ']\n')
if inputSearchText.strip() != "":
    Configuration.runtime_search_text = inputSearchText

inputMaxCount = raw_input('2. Please input the maximum page number you want to search.[default: ' + str(Configuration.runtime_search_max_page_number) + ']\n')
if inputMaxCount.strip() != "":
    Configuration.runtime_search_max_page_number = int(inputMaxCount)

downloadPath = raw_input('3. Please input the output folder of these videos.[default: ' + Configuration.runtime_download_path + ']\n')
if downloadPath.strip() != "":
    Configuration.runtime_download_path = downloadPath

if not os.path.exists(Configuration.runtime_download_path):
    os.mkdir(Configuration.runtime_download_path)
if not os.path.exists(Configuration.runtime_download_path + "/" + Configuration.runtime_search_text):
    os.mkdir(Configuration.runtime_download_path + "/" + Configuration.runtime_search_text)


DownloadTaskProducer.start()
Downloader.start()

VideoLinkExtractor.start()

logging.info('App started ...')

while True:
    pass