

from flask import Flask, request
import json
import Flask_Threads
import threading

app = Flask(__name__)


@app.route('/POST', methods=['POST'])
def post():
    # res_st = "Request received successfully.."
    req = json.loads(request.data)
    op = req.get("operation")
    val1 = req.get("value1")
    val2 = req.get("value2")

    thread = threading.Thread(target=operate, args=(req, op, val1, val2))
    thread.start()
    return "request processed.."


def operate(req, op, val1, val2):
    if op == "add":
        res_d = val1 + val2
        Flask_Threads.posThreads(req, res_d)
        # return res_st
    elif op == "sub":
        res_d = val1 - val2
        Flask_Threads.posThreads(req, res_d)
        # return res_st
    elif op == "mul":
        res_d = val1*val2
        Flask_Threads.posThreads(req, res_d)
        # return res_st
    elif op == "div":
        res_d = val1/val2
        Flask_Threads.posThreads(req, res_d)
        # return res_st
    else:
        return "Operation not available.."


if __name__ == '__main__':
    app.run()