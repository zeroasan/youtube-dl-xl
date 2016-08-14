from threading import Thread
import time, logging, Queue
import urllib2

from threading import Thread, Lock
from pyquery import PyQuery
#from lxml import etree
from Configuration import app_root_folder, start_search_page_url
import DownloadInfoService
from exception.DuplicateError import DuplicateError
from VideoInfo import VideoInfo
from Configuration import runtime_search_max_page_number, getSearchPageURL

# TODO remove log config
import LogConfig

logger = logging.getLogger(__name__)

# TODO move this to a sperated file for customization purpose
def extractLink(pyContent):
    ret = {'videoLinks':None, 'searchLinks':None}
    if pyContent is not None:
        videoLinkArray = pyContent('.yt-lockup-video').map(lambda i, e: 'https://www.youtube.com/watch?v=' + PyQuery(e).attr('data-context-item-id'))
        ret['videoLinks'] = videoLinkArray

        currentPageNumber = getCurrentPageNumber(pyContent)
        if(currentPageNumber != None):
            searchLinkArray = pyContent('.search-pager a').map(lambda i, e: getPageLinkIfValid(e, currentPageNumber))
            searchLinkArray = list(set(searchLinkArray))

        ret['searchLinks'] = searchLinkArray
    return ret


def getPageLinkIfValid(element, currentPageNumber):
    pyElement = PyQuery(element)
    pageNumberText = pyElement.find('span').text()

    if not pageNumberText.isdigit():
        return None

    pageNumber = int(pageNumberText)
    if currentPageNumber < pageNumber <= runtime_search_max_page_number:
        return 'https://www.youtube.com' + pyElement.attr('href')
    return None

allSearchLinks = [];
def extractLinkWorker(pendingSearchLinks):
    allSearchSet = set(pendingSearchLinks)
    while len(pendingSearchLinks) > 0:
        search_page_url = pendingSearchLinks.pop()

        pqContent = PyQuery(search_page_url)

        extractInfo = extractLink(pqContent)
        videoLinks = extractInfo['videoLinks']
        searchLinks = extractInfo['searchLinks']

        if videoLinks is not None:
            # add video links to db
            for videoLink in videoLinks:
                videoInfo = VideoInfo()
                videoInfo.url = videoLink
                try:
                    DownloadInfoService.addVideoInfo(videoInfo)
                except DuplicateError:
                    logging.info("URL [{}] has been already added.".format(videoInfo.url))
            print '[LinkExtractor] Add video links to db: [{}]'.format(' , \n'.join(videoLinks))
            # TODO add video links to db

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


def getCurrentPageNumber(pqContent):
    pageNumber = pqContent('.search-pager button[disabled="True"] span').text()
    if pageNumber != '' and pageNumber.isdigit():
        return int(pageNumber)
    else:
        return None

def start():
    pendingSearchLinks = []
    pendingSearchLinks.append(getSearchPageURL())

    downloadThread = Thread(target=extractLinkWorker, args=(pendingSearchLinks, ))
    downloadThread.setDaemon(True)
    downloadThread.start()
    logger.info('[LinkExtractor] Producer has been started.')

    return downloadThread
