from pymongo import MongoClient
import threading
import datetime
import time as t

client = MongoClient()
_db = client["thread_db"]
_collection = _db["thread_coll"]


def database_conn(inp, res):
    inp_js = inp
    res_val = res
    time = datetime.datetime.now()
    formated_time = time.strftime("%Y-%m-%d %H:%M:%S")

    db_store_val = {"time": formated_time, "input_request": inp_js, "result": res_val}

    _collection.insert_one(db_store_val)


def posThreads(inp, res):
    i, j = inp, res
    for k in range(10):
        post_thread = threading.Thread(target=database_conn, args=(i, j))
        post_thread.start()
        t.sleep(5)
