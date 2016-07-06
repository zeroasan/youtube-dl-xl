def __getApptPath__():
    return 'C:/Users/zhengv/PycharmProjects/youtube-dl-xl/'

app_root_folder = __getApptPath__()

data_root_folder = app_root_folder + 'data/'

db_path = data_root_folder + 'data.db'
db_schema_path = data_root_folder + 'data_schema.sql'

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
