def __getApptPath__():
    return 'C:/Users/zhengv/PycharmProjects/youtube-dl-xl/'

app_root_folder = __getApptPath__()

data_root_folder = app_root_folder + 'data/'

db_path = data_root_folder + 'data.db'
db_schema_path = data_root_folder + 'data_shcema.sql'
