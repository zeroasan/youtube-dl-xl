import sqlite3
import os, logging
from Configuration import db_path, db_schema_path

db_is_new = not os.path.exists(db_path)

if not db_is_new:
    inputRecreateDB = raw_input('DB already exists, do you want to clear data and recreate DB(y/n)?[default: n]\n')
    if inputRecreateDB == 'Y' or inputRecreateDB == 'y':
        os.remove(db_path)
        logging.info("DB file is deleted.")
        db_is_new = True

conn = sqlite3.connect(db_path, check_same_thread=False)
logging.info('DB connected.')

if db_is_new:
    with open(db_schema_path, 'rt') as f:
        schema = f.read()
        conn.executescript(schema)
        conn.commit()
    logging.info("DB schema created.")

#conn.execute(""" delete from video_info """)
#conn.execute(""" insert into video_info (url, uploader, author,description) values('http://www.baidu.com', 'zw', 'zw', 'asdfsadfsadfsadf') """)

