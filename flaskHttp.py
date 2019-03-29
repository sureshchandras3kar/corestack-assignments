
#import packages flask ,json

from flask import Flask, request
from flask import redirect
import json

app = Flask(__name__)

dictlist = list()


# find  requests methods
@app.route('/', methods=['POST', "GET"])
def root():
    if request.method == 'POST':

        file1 = open("PostFileData.txt", 'a+')
        #  get data as dict get_json()

        writedata = request.get_json()
        print(writedata)
        dictlist.append(writedata)
        print(type(writedata))

        # dictionary to string conversion json.dumps
        _StrData = json.dumps(writedata)
        print(_StrData, type(_StrData))

        #  writing data to file
        file1.write(_StrData + '\n')
        file1.flush()
        print("file created post method called")
        return "file created json data {}".format(_StrData)
    else:
        return "hello i'm in root page. method used %s" % request.method


# passing string value -> text in url

@app.route('/user/<user_name>')
def username(user_name):
    return "hey %s" % user_name


# passing integer value ->  integer in url
@app.route('/post/<int:po_id>')
def post_show(po_id):
    return "post id %s" % po_id


# redirect to another url
@app.route('/google')
def search():
    return redirect("https://www.google.com/")


# write data to file using put method
@app.route('/PUT', methods=["PUT"])
def putdata():
    if request.method == 'PUT':
        dictdata = request.get_json()
        strdata = json.dumps(dictdata)
        _name = request.args.get("name")

        print(dictdata, type(dictdata))
        for count, dict in enumerate(dictlist):
            if dict['name'] == _name:
                dictlist[count] = dictdata
        print(dictlist)
        return "data updated" + strdata


@app.route('/DELETE', methods=["DELETE"])
def deletedata():
    if request.method == 'DELETE':
        _name = request.args.get("name")
        for count, dict in enumerate(dictlist):
            if dict['name'] == _name:
                print(dict)
                del dictlist[count]
                print(dict)
        return "value deleted "


if "__name__" == 'main':
    app.run(debug=True)
