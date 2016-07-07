import os

def __getApptPath__():
    return os.path.dirname(os.path.realpath(__file__)) + "\\"

app_root_folder = __getApptPath__()

data_root_folder = app_root_folder + 'data/'

db_path = data_root_folder + 'data.db'
db_schema_path = data_root_folder + 'data_schema.sql'

# Log file
log_file_path = app_root_folder + '/logs/my.log'

# number of download workers
num_of_download_worker = 2

# fetch certain count of ready-to-download task from db
download_task_fetch_count = 10

# fetch certain count of ready-to-upload task from db
upload_task_fetch_count = 10

# sleep with certain seconds when no task loaded from db
no_download_task_sleep_seconds = 5
no_upload_task_sleep_seconds = 5

# when queue size is below this size, the producer will start to fetch more task
queue_size_valve_to_fetch_download_task=5
queue_size_valve_to_fetch_upload_task=5

# page to start search video urls
start_search_page_url = 'https://www.youtube.com/results?search_query=360+3d+4k'
