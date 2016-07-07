from DB import conn
from Configuration import app_root_folder

__test_clean_data_sql_file__ = app_root_folder + 'test/data/clean_data.sql'
__test_video_ready_to_download_sql_file__ = app_root_folder + 'test/data/test_data_video_ready_to_download.sql'


def __init_run_data__(filePath):
    with open(filePath, 'rt') as f:
        data_file = f.read()
        conn.executescript(data_file)
        print 'script executed'
        conn.commit()

__init_run_data__(__test_clean_data_sql_file__)
__init_run_data__(__test_video_ready_to_download_sql_file__)