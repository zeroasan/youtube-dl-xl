import unittest
import DownloadInfoService
from VideoInfo import VideoInfo
from exception.DuplicateError import DuplicateError
from DB import conn
from Configuration import app_root_folder
import sys


__test_video_ready_to_download_sql_file__ = app_root_folder + 'test/data/test_data_video_ready_to_download.sql'
__test_video_ready_to_upload_sql_file__ = app_root_folder + 'test/data/test_data_video_ready_to_upload.sql'
__test_video_downloading_sql_file__ = app_root_folder + 'test/data/test_data_video_downloading.sql'
__test_video_uploading_sql_file__ = app_root_folder + 'test/data/test_data_video_uploading.sql'
__test_clean_data_sql_file__ = app_root_folder + 'test/data/clean_data.sql'

class DLInfoServiceTest(unittest.TestCase):
    def tearDown(self):
        self.__init_run_data__(__test_clean_data_sql_file__)

    def test_add_video_simple(self):
        video = self.__createVideoInfo__()
        video.url = 'http://testDuplicate.com'
        video.description = '__test__'

        DownloadInfoService.addVideoInfo(video)

        video2 = DownloadInfoService.getVideoInfo(video.url)

        self.assertIsNotNone(video2.id)
        self.assertIsNotNone(video2.url)
        self.assertIsNotNone(video2.author)
        self.assertIsNotNone(video2.uploader)
        self.assertIsNotNone(video2.isDownloaded)
        self.assertIsNotNone(video2.isUploaded)
        self.assertIsNotNone(video2.isProcessing)
        self.assertIsNotNone(video2.description)

    def test_add_video_with_duplicate_url(self):
        video = self.__createVideoInfo__()
        video.url = 'http://testDuplicate.com'
        video.description = '__test__'

        DownloadInfoService.addVideoInfo(video)

        video2 = DownloadInfoService.getVideoInfo(video.url)
        self.assertEqual(video.url, video2.url, 'Video info gotten from db should equals to info inserted.')

        #self.assertRaises(DpError, DownloadInfoService.addVideoInfo, [video,])
        with self.assertRaises(DuplicateError):
            DownloadInfoService.addVideoInfo(video2)


    def test_add_video_default_isDownloaded_isUploaded_value(self):
        video = VideoInfo()
        video.url = 'http://testAddDefaultValue'
        video.description = '__test__'

        DownloadInfoService.addVideoInfo(video)

        video2 = DownloadInfoService.getVideoInfo(video.url)
        self.assertEqual(video2.isDownloaded, 0)
        self.assertEqual(video2.isUploaded, 0)


    def test_mark_as_downloaded(self):
        video = self.__createVideoInfo__()
        video.url = 'http://testMarkAsDownloaded.com'
        video.description = '__test__'

        DownloadInfoService.addVideoInfo(video)
        self.assertIsNotNone(DownloadInfoService.getVideoInfo(video.url))

        DownloadInfoService.markAsDownloaded(video.url)

        video2 = DownloadInfoService.getVideoInfo(video.url)
        self.assertEqual(video2.isDownloaded, 1)


    def test_mark_as_uploaded(self):
        video = self.__createVideoInfo__()
        video.url = 'http://testMarkAsUploaded.com'
        video.description = '__test__'

        DownloadInfoService.addVideoInfo(video)
        self.assertIsNotNone(DownloadInfoService.getVideoInfo(video.url))

        DownloadInfoService.markAsUploaded(video.url)

        video2 = DownloadInfoService.getVideoInfo(video.url)
        self.assertEqual(video2.isUploaded, 1)


    def test_get_video_ready_to_download_for_given_count(self):
        self.__init_run_data__(__test_video_ready_to_download_sql_file__)

        count = 2
        array = DownloadInfoService.getVideoInfoReadyToDownload(count)
        self.assertEqual(len(array), count)

        count = 3
        array = DownloadInfoService.getVideoInfoReadyToDownload(count)
        self.assertEqual(len(array), count)

    def test_get_video_ready_to_download_after_mark_download(self):
        self.__init_run_data__(__test_video_ready_to_download_sql_file__)
        array = DownloadInfoService.getVideoInfoReadyToDownload()
        count1 = len(array)
        video = array.pop(0)

        DownloadInfoService.markAsDownloaded(video.url)
        array = DownloadInfoService.getVideoInfoReadyToDownload()
        count2 = len(array)

        self.assertEqual(count1 - 1, count2)

    def test_get_video_ready_to_download_for_given_count(self):
        self.__init_run_data__(__test_video_ready_to_upload_sql_file__)
        array = DownloadInfoService.getVideoInfoReadyToUpload()

        count = 2
        array = DownloadInfoService.getVideoInfoReadyToUpload(count)
        self.assertEqual(len(array), count)

        count = 3
        array = DownloadInfoService.getVideoInfoReadyToUpload(count)
        self.assertEqual(len(array), count)


    def test_get_video_ready_to_download_after_mark_upload(self):
        self.__init_run_data__(__test_video_ready_to_upload_sql_file__)
        array = DownloadInfoService.getVideoInfoReadyToUpload()
        count1 = len(array)
        video = array.pop(0)

        DownloadInfoService.markAsUploaded(video.url)
        array = DownloadInfoService.getVideoInfoReadyToUpload()
        count2 = len(array)

        self.assertEqual(count1 - 1, count2)


    def test_clear_processing_flag(self):
        self.__init_run_data__(__test_video_downloading_sql_file__)
        array = DownloadInfoService.getVideoInfoReadyToDownload()
        self.assertEqual(0, len(array))
        DownloadInfoService.clearProcessingFlag()

        array = DownloadInfoService.getVideoInfoReadyToDownload()
        self.assertGreater(len(array), 0)


    def test_should_not_get_downloads_when_processing(self):
        self.__init_run_data__(__test_video_downloading_sql_file__)
        array = DownloadInfoService.getVideoInfoReadyToDownload()
        self.assertEqual(0, len(array))


    def test_should_not_get_uploads_when_processing(self):
        self.__init_run_data__(__test_video_uploading_sql_file__)
        array = DownloadInfoService.getVideoInfoReadyToUpload()
        self.assertEqual(0, len(array))

    def test_ready_to_download_change_after_batch_mark_processing(self):
        self.__init_run_data__(__test_video_ready_to_download_sql_file__)
        array = DownloadInfoService.getVideoInfoReadyToDownload()

        count1 = len(array)

        markCount = 3
        DownloadInfoService.batchMarkProcessingFlag(array[0:markCount])

        array = DownloadInfoService.getVideoInfoReadyToDownload()
        count2 = len(array)

        self.assertEqual(count1 - markCount, count2)


    def __createVideoInfo__(self):
        video = VideoInfo('')

        video.url = 'http://www.baidu1.com'
        video.author = 'zw'
        video.uploader = 'zw'
        video.isDownloaded = 0
        video.isUploaded = 0
        video.description = 'This is test video description'
        return video

    def __init_run_data__(self, filePath):
        with open(filePath, 'rt') as f:
            data_file = f.read()
            conn.executescript(data_file)
            print 'script executed'
            conn.commit()



def main():
    unittest.main()

if __name__ == '__main__':
    unittest.main()
