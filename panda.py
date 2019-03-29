# import pymongo to data driven from collection hotel
import pymongo
import pandas
from pymongo import MongoClient, errors

# database connection 
def database_conn():
    try:
        conn = MongoClient()
        db = conn.aggregate_db
        _coll = db.hotel
        return _coll, conn
    except pymongo.errors.ConnectionFailure, e:
        print "Could not connect to server: %s" % e

# db_first_search function search single document
def db_first_search(_coll, search_data=None):
    if search_data is None:
        search_data = {}
    try:
        recvdata = _coll.find_one(search_data)
        print recvdata
        return recvdata
    except pymongo.errors.PyMongoError as e:
        print "given data is invalid:%s" % e

# db_search_all collect many document in db
def db_search_all(_coll, data=None):
    if data is None:
        data = {}
    try:
        dictlist = list()
        recvdata_coll = _coll.find(data)

        for docum in recvdata_coll:
            dictlist.append(docum)

        print len(dictlist)
        return dictlist

    except pymongo.errors.PyMongoError as e:
        print "given data is invalid:%s" % e


if __name__ == "__main__":
    conn = database_conn()

    coll_list = db_search_all(conn[0])
# written csv file
    brics = pandas.DataFrame(coll_list)
    brics.to_csv('mon.csv')
    
