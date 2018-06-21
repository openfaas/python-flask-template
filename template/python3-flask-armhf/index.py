# Copyright (c) Alex Ellis 2017. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.

from flask import Flask, request
from function import handler
#from gevent.wsgi import WSGIServer
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def main_route():
    ret = handler.handle(request.get_data())
    return ret

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, debug=False)

    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
