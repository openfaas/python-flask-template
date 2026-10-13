#!/usr/bin/env python
import site

# The function's own dependencies are installed to a fixed path rather than
# a $HOME-derived one, so that they are still found when the platform runs
# the container as an arbitrary uid. Register it as a site directory rather
# than relying on PYTHONPATH alone, so that any .pth files shipped by those
# dependencies are processed as they would be in site-packages.
site.addsitedir("/home/app/python")

from flask import Flask, request, jsonify
from waitress import serve
import os

from function import handler

app = Flask(__name__)

class Event:
    def __init__(self):
        self.body = request.get_data()
        self.headers = request.headers
        self.method = request.method
        self.query = request.args
        self.path = request.path

class Context:
    def __init__(self):
        self.hostname = os.getenv('HOSTNAME', 'localhost')

def format_status_code(resp):
    if 'statusCode' in resp:
        return resp['statusCode']
    
    return 200

def format_body(resp):
    if 'body' not in resp:
        return ""
    elif type(resp['body']) == dict:
        return jsonify(resp['body'])
    else:
        return str(resp['body'])

def format_headers(resp):
    if 'headers' not in resp:
        return []
    elif type(resp['headers']) == dict:
        headers = []
        for key in resp['headers'].keys():
            header_tuple = (key, resp['headers'][key])
            headers.append(header_tuple)
        return headers
    
    return resp['headers']

def format_response(resp):
    if resp == None:
        return ('', 200)
    
    if type(resp) is dict:
        statusCode = format_status_code(resp)
        body = format_body(resp)
        headers = format_headers(resp)

        return (body, statusCode, headers)

    return resp

@app.route('/', defaults={'path': ''}, methods=['GET', 'PUT', 'POST', 'PATCH', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'PUT', 'POST', 'PATCH', 'DELETE'])
def call_handler(path):
    event = Event()
    context = Context()
    response_data = handler.handle(event, context)
    
    resp = format_response(response_data)
    return resp

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
