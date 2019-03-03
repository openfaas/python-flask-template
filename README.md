OpenFaaS Python Flask Templates
=============================================

The Python Flask templates that make use of the incubator project [of-watchdog](https://github.com/openfaas-incubator/of-watchdog).

Templates available in this repository:
- python27-flask
- python3-flask
- python3-flask-armhf
- python3-http
- python3-http-armhf

Notes:
- To build and deploy a function for Raspberry Pi or ARMv7 in general, use the language templates ending in *-armhf*

## Downloading the templates
```
$ faas template pull https://github.com/openfaas-incubator/python-flask-template
```

# Using the python27-flask/python3-flask templates
Create a new function
```
$ faas new --lang python27-flask <fn-name>
```
Build, push, and deploy
```
$ faas up -f <fn-name>.yml
```
Test the new function
```
$ echo -n content | faas invoke <fn-name>
```

# Using the python3-http templates
Create a new function
```
$ faas new --lang python3-http <fn-name>
```
Build, push, and deploy
```
$ faas up -f <fn-name>.yml
```
Set your OpenFaaS gateway URL. For example:
```
$ OPENFAAS_URL=http://127.0.0.1:8080
```
Test the new function
```
$ curl -i $OPENFAAS_URL/function/<fn-name>
```

## Event and Context Data
The function handler is passed two arguments, *event* and *context*.

*event* contains data about the request, including:
- body
- headers
- method
- query
- path

*context* contains basic information about the function, including:
- hostname

## Response Bodies
By default, the template will automatically attempt to set the correct Content-Type header for you based on the type of response. 

For example, returning a dict object type will automatically attach the header `Content-Type: application/json` and returning a string type will automatically attach the `Content-Type: text/html, charset=utf-8` for you.

## Example usage
### Custom status codes and response bodies
Successful response status code and JSON response body
```python
def handle(event, context):
    return {
        "statusCode": 200,
        "body": {
            "key": "value"
        }
    }
```
Successful response status code and string response body
```python
def handle(event, context):
    return {
        "statusCode": 201,
        "body": "Object successfully created"
    }
```
Failure response status code and JSON error message
```python
def handle(event, context):
    return {
        "statusCode": 400,
        "body": {
            "error": "Bad request"
        }
    }
```
### Custom Response Headers
Setting custom response headers
```python
def handle(event, context):
    return {
        "statusCode": 200,
        "body": {
            "key": "value"
        },
        "headers": {
            "Location": "https://www.example.com/"
        }   
    }
```
### Accessing Event Data
Accessing request body
```python
def handle(event, context):
    return {
        "statusCode": 200,
        "body": "You said: " + str(event.body)
    }
```
Accessing request method
```python
def handle(event, context):
    if event.method == 'GET':
        return {
            "statusCode": 200,
            "body": "GET request"
        }
    else:
        return {
            "statusCode": 405,
            "body": "Method not allowed"
        }
```
Accessing request query string arguments
```python
def handle(event, context):
    return {
        "statusCode": 200,
        "body": {
            "name": event.query['name']
        }
    }
```
Accessing request headers
```python
def handle(event, context):
    return {
        "statusCode": 200,
        "body": {
            "content-type-received": event.headers['Content-Type']
        }
    }
```