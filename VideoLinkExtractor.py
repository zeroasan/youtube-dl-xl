import time, logging, Queue
from threading import Thread, Lock
from pyquery import PyQuery
import DownloadInfoService
from exception.DuplicateError import DuplicateError
from VideoInfo import VideoInfo
from Configuration import getSearchPageURL
import Configuration

# TODO remove log config
import LogConfig

logger = logging.getLogger(__name__)

youtube_url_prefix = 'https://www.youtube.com/watch?v='

# TODO move this to a sperated file for customization purpose
def extractLink(pyContent):
    ret = {'videoLinks':None, 'searchLinks':None}
    if pyContent is not None:
        currentPageNumber = getCurrentPageNumber(pyContent)

        videoLinkArray = pyContent('.yt-lockup-video').map(lambda i, e: youtube_url_prefix + PyQuery(e).attr('data-context-item-id'))
        ret['videoLinks'] = videoLinkArray

        if(currentPageNumber != None):
            searchLinkArray = pyContent('.search-pager a').map(lambda i, e: getPageLinkIfValid(e, currentPageNumber))
            searchLinkArray = list(set(searchLinkArray))

        logger.info('[LinkExtractor] Detected %d videos and %d pages for Page-%d', len(videoLinkArray), len(searchLinkArray), currentPageNumber)

        ret['searchLinks'] = searchLinkArray
    return ret


def getPageLinkIfValid(element, currentPageNumber):
    pyElement = PyQuery(element)
    pageNumberText = pyElement.find('span').text()

    if not pageNumberText.isdigit():
        return None

    pageNumber = int(pageNumberText)
    if currentPageNumber < pageNumber <= Configuration.runtime_search_max_page_number:
        return 'https://www.youtube.com' + pyElement.attr('href')
    return None

allSearchLinks = [];
def extractLinkWorker(pendingSearchLinks):
    allSearchSet = set(pendingSearchLinks)
    while len(pendingSearchLinks) > 0:
        search_page_url = pendingSearchLinks.pop()

        pyContent = PyQuery(search_page_url)

        extractInfo = extractLink(pyContent)
        videoLinks = extractInfo['videoLinks']
        searchLinks = extractInfo['searchLinks']

        if videoLinks is not None:
            logger.info('[LinkExtractor] Add video links to db: [%s]', ' ,\n'.join(videoLinks))
            # Add video links to db
            for videoLink in videoLinks:
                videoInfo = VideoInfo()
                videoInfo.url = videoLink
                try:
                    DownloadInfoService.addVideoInfo(videoInfo)
                except DuplicateError:
                    logging.info("[LinkExtractor] URL [%s] has been already in DB.", videoInfo.url)

        newSearchLinks = [];
        if searchLinks is not None:
            for newLink in searchLinks:
                if newLink not in allSearchSet:
                    pendingSearchLinks.append(newLink)
                    newSearchLinks.append(newLink)
                    allSearchSet.add(newLink)
        if len(newSearchLinks) != 0:
            logger.debug( '[LinkExtractor] Extracted new search links: [{}]'.format(' ,\n'.join(newSearchLinks)))
        else:
            logger.debug('[LinkExtractor] search links is none for url:[{}]'.format(search_page_url))

        logger.info('[LinkExtractor] Sleep 3 seconds to continue.')
        time.sleep(3)
        pass

    logger.warn('[LinkExtractor] Link Extractor stopped')


def getCurrentPageNumber(pyContent):
    pageNumber = pyContent('.search-pager button[disabled="True"] span').text()
    if pageNumber != '' and pageNumber.isdigit():
        return int(pageNumber)
    else:
        return None

def start():
    pendingSearchLinks = []
    pendingSearchLinks.append(getSearchPageURL())

    extractorThread = Thread(target=extractLinkWorker, name='Extractor', args=(pendingSearchLinks, ))
    extractorThread.setDaemon(True)
    extractorThread.start()
    logger.info('[LinkExtractor] Producer has been started.')
