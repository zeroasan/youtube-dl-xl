import LogConfig
import os
import DownloadTaskProducer
import Downloader
import Configuration
import logging
import VideoLinkExtractor
from Utils import mkdirs

# setting log
#logging.basicConfig(filename=log_file_path, level=logging.INFO)


def main():
    # Initialize Configuration
    inputSearchText = raw_input(
        '1. Please input the key words you want to search.[default: ' + Configuration.runtime_search_text + ']\n')
    if inputSearchText.strip() != "":
        Configuration.runtime_search_text = inputSearchText

    inputMaxPageNumber = raw_input('2. Please input the maximum page number you want to search.[default: ' + str(
        Configuration.runtime_search_max_page_number) + ']\n')
    if inputMaxPageNumber.strip() != "":
        Configuration.runtime_search_max_page_number = int(inputMaxPageNumber)

    downloadPath = raw_input(
        '3. Please input the output folder of these videos.[default: ' + Configuration.runtime_download_root_path + ']\n')
    if downloadPath.strip() != "":
        Configuration.runtime_download_root_path = downloadPath

    inputDownloadThread = raw_input('4. Please input download threads number.[default: ' + str(
        Configuration.runtime_num_of_download_worker) + ']\n')
    if inputDownloadThread.strip() != "":
        Configuration.runtime_num_of_download_worker = int(inputDownloadThread)

    disableExtractor = raw_input('5. Disable video link extractor(y/n).[default: ' + (
    'y' if Configuration.runtime_disable_extractor else 'n') + ']\n')
    if disableExtractor.strip() == "y" or disableExtractor.strip() == "Y":
        Configuration.runtime_disable_extractor = True

    if not os.path.exists(Configuration.getDownloadPath()):
        mkdirs(Configuration.getDownloadPath())

    DownloadTaskProducer.start()
    Downloader.start()

    if not Configuration.runtime_disable_extractor:
        VideoLinkExtractor.start()
    else:
        logging.info('Video link extractor is disabled.')

    logging.info('App started ...')

    while True:
        pass

if __name__ == '__main__':
    main()