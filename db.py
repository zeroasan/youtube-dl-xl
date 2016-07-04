import sqlite3
import os

db_filename = 'data.db'
schema_filename = 'data_schema.sql'

db_is_new = not os.path.exists(db_filename)

conn = sqlite3.connect(db_filename)
print 'DB connected.'

if db_is_new:
    print 'Creating schema'
    with open(schema_filename, 'rt') as f:
        schema = f.read()
        conn.executescript(schema)
else:
    print 'DB file already exists.'

conn.execute(""" delete from video_info """)
conn.execute(""" insert into video_info (url, uploader, author,description) values('http://www.baidu.com', 'zw', 'zw', 'asdfsadfsadfsadf') """)
conn.commit()


