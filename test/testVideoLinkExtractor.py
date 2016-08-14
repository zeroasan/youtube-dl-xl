import unittest
from pyquery import PyQuery


class VideoLinkExtractorTest(unittest.TestCase):

    def test_get_current_page_number(self):
        url = 'https://www.youtube.com/results?search_query=360+3d+4k'
        pyContent = PyQuery(url)
        pageNumber = pyContent('.search-pager button[disabled="True"] span').text()
        print pageNumber
        self.assertEqual(int(pageNumber), 1, 'Page number of search page should be 1.')


    def test_extract_page_link(self):
        url = 'https://www.youtube.com/results?search_query=360+3d+4k'
        pyContent = PyQuery(url)
        currentPageNumber = int(pyContent('.search-pager button[disabled="True"] span').text())

        searchLinkArray = pyContent('.search-pager a').map(lambda i, e: getPageLinkIfValid(e, currentPageNumber))
        #searchLinkArray = pyContent('.search-pager a').map(lambda i, e: int(PyQuery(e).find('span').text()) if PyQuery(e).find('span').text().isdigit() else None)
        for searchLink in searchLinkArray:
            print "link: " + str(searchLink) + "\n"

def getPageLinkIfValid(element, currentPageNumber):
    pyElement = PyQuery(element)
    pageNumberText = pyElement.find('span').text()

    if pageNumberText.isdigit() and int(pageNumberText) > currentPageNumber:
        return 'https://www.youtube.com' + pyElement.attr('href')
    return None

def main():
    unittest.main()

if __name__ == '__main__':
    unittest.main()
