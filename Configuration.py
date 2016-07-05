def __getApptPath__():
    return 'C:/Users/zhengv/PycharmProjects/youtube-dl-xl/'

app_root_folder = __getApptPath__()

data_root_folder = app_root_folder + 'data/'

db_path = data_root_folder + 'data.db'
db_schema_path = data_root_folder + 'data_shcema.sql'

# number of download workers
num_of_download_worker = 2

# fetch certain count of ready-to-download task from db
download_task_fetch_count = 10

# fetch certain count of ready-to-upload task from db
upload_task_fetch_count = 10
