import pymysql

from contextlib import contextmanager

@contextmanager
def get_connection():
    conn = pymysql.connect(
        host='127.0.0.1',        
        user='root',
        password='12345', 
        port=3306  ,
        database="test_main",
        # database="warranty",
        local_infile=True,
        cursorclass=pymysql.cursors.DictCursor
    )
    
    try:
        yield conn
    finally:
        conn.close()
