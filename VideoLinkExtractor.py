from threading import Thread
import time, logging, Queue

from threading import Thread, Lock
from pyquery import PyQuery
#from lxml import etree
from Configuration import app_root_folder, start_search_page_url
import DownloadInfoService
from VideoInfo import VideoInfo

# TODO remove log config
import LogConfig

logger = logging.getLogger(__name__)

__html_file_path__ = app_root_folder + 'test/data/test.html'


def loadHtmlMock(url) :
    if url != 'http://www.baidu.com':
        return None
    # TODO Change this to read from online page
    with open(__html_file_path__, 'rt') as f:
        htmlContent = f.read()
        return PyQuery(htmlContent)
    return None


def loadHtml(url) :
    pass


# TODO move this to a sperated file for customization purpose
def extractLink(pqContent):
    ret = {'videoLinks':None, 'searchLinks':None}
    if pqContent is not None:
        videoLinkArray = pqContent('.yt-lockup-video').map(lambda i, e: 'https://www.youtube.com/watch?v=' + PyQuery(e).attr('data-context-item-id'))
        ret['videoLinks'] = videoLinkArray
        searchLinkArray = pqContent('.search-pager a').map(lambda i, e: PyQuery(e).attr('href'))
        # remove duplicate links
        searchLinkArray = list(set(searchLinkArray))

        ret['searchLinks'] = searchLinkArray
    return ret


def extractLinkWorker(pendingSearchLinks):
    while len(pendingSearchLinks) > 0:
        search_page_url = pendingSearchLinks.pop()

        pqContent = loadHtmlMock(search_page_url)
        extractInfo = extractLink(pqContent)
        videoLinks = extractInfo['videoLinks']
        searchLinks = extractInfo['searchLinks']

        if videoLinks is not None:
            # add video links to db
            for videoLink in videoLinks:
                videoInfo = VideoInfo()
                videoInfo.url = videoLink
                DownloadInfoService.addVideoInfo(videoInfo)
            print '[LinkExtractor] Add video links to db: [{}]'.format(' , \n'.join(videoLinks))
            # TODO add video links to db

        if searchLinks is not None:
            pendingSearchLinks = list(set(pendingSearchLinks).union(set(searchLinks)))
            logger.debug( '[LinkExtractor] Extracted search links: [{}]'.format(' ,\n'.join(searchLinks)))
        else:
            logger.debug('[LinkExtractor] search links is none for url:[{}]'.format(search_page_url))

        logger.info('[LinkExtractor] Sleep 3 seconds to continue.')
        time.sleep(3)
        pass

    logger.warn('[LinkExtractor] Link Extractor stopped')

def start():
    pendingSearchLinks = []
    pendingSearchLinks.append(start_search_page_url)

    downloadThread = Thread(target=extractLinkWorker, args=(pendingSearchLinks, ))
    downloadThread.setDaemon(True)
    downloadThread.start()
    logger.info('[LinkExtractor] Producer has been started.')

    return downloadThread


downloadThread = start()
downloadThread.join()