#!/usr/bin/env python
from fastapi import FastAPI, Request

app = FastAPI()

import os

from function import handler

class Event:
    def __init__(self, request: Request,body ):
        self.body = body
        self.headers = request.headers
        self.method = request.method
        self.query = request.query_params
        self.path = request.url.path

class Context:
    def __init__(self):
        self.hostname = os.getenv('HOSTNAME', 'localhost')

def format_status_code(res):
    if 'statusCode' in res:
        return res['statusCode']
    
    return 200

def format_body(res, content_type):
    if content_type == 'application/octet-stream':
        return res['body']

    if 'body' not in res:
        return ""
    elif type(res['body']) == dict:
        return jsonify(res['body'])
    else:
        return str(res['body'])

def format_headers(res):
    if 'headers' not in res:
        return []
    elif type(res['headers']) == dict:
        headers = []
        for key in res['headers'].keys():
            header_tuple = (key, res['headers'][key])
            headers.append(header_tuple)
        return headers
    
    return res['headers']

def get_content_type(res):
    content_type = ""
    if 'headers' in res:
        content_type = res['headers'].get('Content-type', '')
    return content_type

def format_response(res):
    if res == None:
        return ('', 200)

    statusCode = format_status_code(res)
    content_type = get_content_type(res)
    body = format_body(res, content_type)

    headers = format_headers(res)

    return (body, statusCode, headers)

@app.api_route("/", methods=["GET", "POST", "DELETE", "PUT", "PATCH", "OPTIONS", "HEAD"])
async def root(request: Request):

    body = await request.body()
    event = Event(request, body)

    context = Context()

    response_data = handler.handle(event, context)
    
    res = format_response(response_data)
    return res
