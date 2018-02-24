# Copyright (c) Alex Ellis 2017. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

from flask import Flask, request
from function import handler
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def main_route():
    ret = handler.handle(request.get_data())
    return ret

app.debug = False

if __name__ == '__main__':
    WSGIServer(('0.0.0.0', 5000), app)
