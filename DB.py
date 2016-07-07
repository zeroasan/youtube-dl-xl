import sqlite3
import os
from Configuration import db_path, db_schema_path

db_is_new = not os.path.exists(db_path)

conn = sqlite3.connect(db_path, check_same_thread=False)
print 'DB connected.'

if db_is_new:
    print 'Creating schema'
    with open(db_schema_path, 'rt') as f:
        schema = f.read()
        conn.executescript(schema)
        conn.commit()
else:
    print 'DB file already exists.'

#conn.execute(""" delete from video_info """)
#conn.execute(""" insert into video_info (url, uploader, author,description) values('http://www.baidu.com', 'zw', 'zw', 'asdfsadfsadfsadf') """)

