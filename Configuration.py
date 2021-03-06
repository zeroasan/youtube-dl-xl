import os

def __getApptPath__():
    return os.path.dirname(os.path.realpath(__file__)) + "\\"

app_root_folder = __getApptPath__()

data_root_folder = app_root_folder + 'data/'

db_path = data_root_folder + 'data.db'
db_schema_path = data_root_folder + 'data_schema.sql'

# TODO Log file
log_file_path = app_root_folder + '/logs/my.log'



# fetch certain count of ready-to-download task from db
download_task_fetch_count = 10

# fetch certain count of ready-to-upload task from db
upload_task_fetch_count = 10

# sleep with certain seconds when no task loaded from db
no_download_task_sleep_seconds = 5
no_upload_task_sleep_seconds = 5

# when queue size is below this size, the producer will start to fetch more task
queue_size_valve_to_fetch_download_task = 5
queue_size_valve_to_fetch_upload_task = 5


# runtime configuration
runtime_search_text = '360 3d 4k'
runtime_search_max_page_number = 30
runtime_start_search_page_url = 'https://www.youtube.com/results?search_query='
runtime_download_root_path = __getApptPath__()
runtime_disable_extractor = False
# number of download workers
runtime_num_of_download_worker = 1

def getSearchPageURL():
    return runtime_start_search_page_url + runtime_search_text.replace(' ', '+')

def getDownloadPath():
    return runtime_download_root_path + '\\downloads\\' + runtime_search_text