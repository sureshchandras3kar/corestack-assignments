import pymongo

from flask import Flask, request, json
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)


def mongodb_conn():
    try:
        dbclient = MongoClient()
        return dbclient
    except pymongo.errors.ConnectionFailure, e:
        return "Could not connect to server: %s" % e


client = mongodb_conn()

_testdb = client['Testapidb']

_collections = _testdb['APIcollection']


@app.route("/", methods=["GET", "POST"])
def root():
    return "<h2> api testing in database to POST,PUT,GET,DELETE . </h2>"


@app.route('/postdata', methods=["POST"])
def postquery():
    try:
        if request.method == 'POST':
            recvdata = request.get_json()
            # print type(recvdata)

            _collections.insert_one(recvdata)
            return "data created in Testapidb "
    except Exception as e:
        return "unable to create data in database due to %s" % e


@app.route('/getdata', methods=["GET"])
def getquery():
    if request.method == "GET":
        # jdict = {}

        recvdata = request.get_json()

        data = _collections.find_one(recvdata)
        # print data
        jdata = dumps(data)
        return jdata


@app.route('/putdata', methods=["PUT"])
def putquery():
    if request.method == "PUT":
        query = request.args.to_dict("search_query")
        print query, query['search_query'], type(query['search_query'])
        recvdata = request.get_json()
        print recvdata, type(recvdata)

        updata = _collections.update_one(json.loads(query['search_query']), recvdata)
        return "data updated.........///"


@app.route("/deletedata", methods=["DELETE"])
def deletequery():
    if request.method == "DELETE":
        recvdata = request.get_json()
        # print recvdata
        x = _collections.find_one(recvdata)
        print x, type(x)
        _collections.delete_one(x)
        return "data deleted .... /"


if __name__ == 'main':
    app.run()
