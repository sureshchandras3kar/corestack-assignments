import pymongo

from flask import Flask, request, json
from pymongo import MongoClient
from bson.json_util import dumps
import logging
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)

logging.basicConfig(filename="flasklog.log",
                    format="%(asctime)s %(levelname)s %(message)s ",
                    filemode='a',
                    level=logging.DEBUG)

logging.info("/....................application started................../")


def mongodb_conn():
    try:
        client_conn = MongoClient()
        logging.info("*****created db connection*****")
        return client_conn
    except pymongo.errors.ConnectionFailure, e:
        logging.debug("*****Could not connect to server: %s ******" % e)


# call database connection function
client = mongodb_conn()

_testDb = client['Testapidb']

logging.info("*****database created successfully*****")
_collections = _testDb['APIcollection']
logging.info("*****collection created successfully*****")


@app.route("/", methods=["GET", "POST"])
def root():

    try:
        logging.info("running root page")
        return " api testing in database to POST,PUT,GET,DELETE ."
    except Exception, e:
        logging.error("Could not connect to server: %s" % e)


@app.route('/postdata', methods=["POST"])
def postquery():
    """
    POST endpoint returning a string
        This for documentation for specification
        ---

        consumes:
            - application/json
        parameters:
          - name: POST
            in: body
            type: application/json
            required: false
            default: all
        definitions:
          POST:
            type: object
        responses:
          200:
            description: data created in APIcollection
          400:
            description: invalid output

    """
    try:
        if request.method == 'POST':
            recvdata = request.get_json()
            typ = type(recvdata)

            # /......log ............/
            logging.debug("Incoming %s" % typ)
            logging.debug(recvdata)

            # /......db insertion..../
            _collections.insert_one(recvdata)
            logging.info(msg="data inserted in  db")
            return "data created in APIcollection "
    except Exception, e:
        logging.error("unable to create data in database due to %s" % e)


@app.route('/getdata', methods=["GET"])
def getquery():
    """GET endpoint returning a string
        This for documentation for specification
        ---

        parameters:
          - name: name
            in: query
            required: false
            default: all
        definitions:
          GET:
            type: object
        responses:
          200:
            description: return get data
          400:
            description: invalid output
        """

    try:
        if request.method == "GET":
            query_args = request.args.get("name")
            name = {"name": query_args}
            print type(name), name
            response = _collections.find_one(name)
            return dumps(response)

    except Exception, e:
        logging.error(msg="unable to get data from database %s" % e)


@app.route('/putdata', methods=["PUT"])
def putquery():
    """put endpoint returning a string
            This for documentation for specification
            ---

            parameters:
              - name: name
                in: body
                required: false
                default: all
            definitions:
              put:
                type: object
            responses:
              200:
                description: return get data
              400:
                description: invalid output
            """
    try:
        if request.method == "PUT":
            # get data from url
            upd_rec = json.loads(request.data)
            old_rec = upd_rec.get("old")
            new_recd = upd_rec.get("new")
            new_rec = {"$set": new_recd}
            _collections.update_one(old_rec, new_rec)
            return "record updated successfully.."
    except Exception, e:
        logging.error(msg="unable to update data in database %s" % e)


@app.route("/deletedata", methods=["DELETE"])
def deletequery():
    """delete endpoint returning a string
        This for documentation for specification
        ---

        parameters:
          - name: name
            in: body
            required: false
            default: all
        definitions:
          DELETE:
            type: object
        responses:
          200:
            description: return get data
          400:
            description: invalid output
        """
    try:

        if request.method == "DELETE":
            recvdata = request.get_json()
            logging.info(recvdata)

            x = _collections.find_one(recvdata)
            logging.info(type(x))

            _collections.delete_one(x)
            logging.info("data deleted from db")
            return "data deleted .... /"
    except Exception, e:
        logging.error(msg="unable to delete data in database %s" % e)


if __name__ == '__main__':
    app.run(debug=True)
