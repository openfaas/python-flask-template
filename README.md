OpenFaaS Python Flask Templates
=============================================

The Python Flask templates that make use of the incubator project [of-watchdog](https://github.com/openfaas-incubator/of-watchdog).

Templates available in this repository:

- python3-http
- python3-http-debian (ideal for compiled dependencies like numpy, pandas, pillow)

- python3-flask
- python3-flask-debian (ideal for compiled dependencies like numpy, pandas, pillow)

- python27-flask (Python 2.7 is deprecated)

Notes:
- To build and deploy a function for an ARM computer, you'll need to use `faas-cli publish --platforms`

## SSH authentication for private Git repositories and Pip modules

If you need to install Pip modules from private Git repositories, we provide an alternative set of templates for OpenFaaS Pro customers:

* [OpenFaaS Pro templates for Python](https://github.com/openfaas/pro-templates)

## Picking your template

The templates named `python*-flask*` are designed as a drop-in replacement for the classic `python3` template, but using the more efficient of-watchdog. The move to use flask as an underlying framework allows for greater control over the HTTP request and response.

Those templates named `python*-http*` are designed to offer full control over the HTTP request and response. Flask is used as an underlying framework.

The `witness` HTTP server is used along with Flask for all templates.

Are you referencing pip modules which require a native build toolchain? It's advisable to use the template with a `-debian` suffix in this case. The Debian images are larger, however they are usually more efficient for use with modules like `numpy` and `pandas`.

## Python Versioning

We try to keep the default Python 3 version up-to-date, however, you can specify a specific python version using the `PYTHON_VERSION` build argument.

The current stable version of Python is 3.12, you might want to test the next pre-release using:

```yaml
functions:
  pgfn:
    lang: python3-http-debian
    handler: ./pgfn
    image: pgfn:latest
    build_args:
      - PYTHON_VERSION=3.12
```
Or pin to a older version while you wait for your dependencies to be updated.

```yaml
functions:
  pgfn:
    lang: python3-http-debian
    handler: ./pgfn
    image: pgfn:latest
    build_args:
      - PYTHON_VERSION=3.10
```

This can also be set using the `--build-arg` flag.

```bash
faas-cli build --build-arg PYTHON_VERSION=3.12
```

For the `-debian` templates, the `DEBIAN_OS` build_args is also available to specify the Debian version. The default is currently `bookworm`.

## Downloading the templates

Using template pull with the repository's URL:

```bash
faas-cli template pull https://github.com/openfaas-incubator/python-flask-template
```

Using the template store:

```bash
# Either command downloads both templates
faas-cli template store pull python3-http

# Or
faas-cli template store pull python3-flask
```

Using your `stack.yml` file:

```yaml
configuration:
    templates:
        - name: python3-http
```

# Using the python3-http templates

Create a new function

```
export OPENFAAS_PREFIX=alexellis2
export FN="tester"
faas-cli new --lang python3-http $FN
```

Build, push, and deploy

```
faas-cli up -f $FN.yml
```

Test the new function

```
echo -n content | faas-cli invoke $FN
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

### Return a JSON body with a Content-Type

```python
def handle(event, context):
    return {
        "statusCode": 200,
        "body": {"message": "Hello from OpenFaaS!"},
        "headers": {
            "Content-Type": "application/json"
        }
    }
```

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
            "content-type-received": event.headers.get('Content-Type')
        }
    }
```

### Example with Postgresql:

stack.yml

```yaml
version: 1.0
provider:
  name: openfaas
  gateway: http://127.0.0.1:8080
functions:
  pgfn:
    lang: python3-http-debian
    handler: ./pgfn
    image: pgfn:latest
    build_options:
      - libpq
```

Alternatively you can specify `ADDITIONAL_PACKAGE` in the `build_args` section for the function.

```yaml
    build_args:
      ADDITIONAL_PACKAGE: "libpq-dev gcc python3-dev"
```

requirements.txt

```
psycopg2==2.9.3
```

Create a database and table:

```sql
CREATE DATABASE main;

\c main;

CREATE TABLE users (
    name TEXT,
);

-- Insert the original Postgresql author's name into the test table:

INSERT INTO users (name) VALUES ('Michael Stonebraker');
```

handler.py:

```python
import psycopg2

def handle(event, context):

    try:
        conn = psycopg2.connect("dbname='main' user='postgres' port=5432 host='192.168.1.35' password='passwd'")
    except Exception as e:
        print("DB error {}".format(e))
        return {
            "statusCode": 500,
            "body": e
        }

    cur = conn.cursor()
    cur.execute("""SELECT * from users;""")
    rows = cur.fetchall()

    return {
        "statusCode": 200,
        "body": rows
    }
```

Always read the secret from an OpenFaaS secret at `/var/openfaas/secrets/secret-name`. The use of environment variables is an anti-pattern and will be visible via the OpenFaaS API.

# Using the python3-flask template

Create a new function

```
export OPENFAAS_PREFIX=alexellis2
export FN="tester"
faas-cli new --lang python3-flask $FN
```

Build, push, and deploy

```
faas-cli up -f $FN.yml
```

Test the new function

```
echo -n content | faas-cli invoke $FN
```

## Example of returning a string

```python
def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    return "Hi" + str(req)
```

## Example of returning a custom HTTP code

```python
def handle(req):
    return "request accepted", 201
```

## Example of returning a custom HTTP code and content-type

```python
def handle(req):
    return "request accepted", 201, {"Content-Type":"binary/octet-stream"}
```

## Example of accepting raw bytes in the request

Update stack.yml:

```yaml
    environment:
      RAW_BODY: True
```

> Note: the value for `RAW_BODY` is case-sensitive.

```python
def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    # req is bytes, so an input of "hello" returns i.e. b'hello'
    return str(req)
```


## Testing
The `python3` templates will run `pytest` using `tox` during the `faas-cli build`. There are several options for controlling this.

### Disabling testing
The template exposes the build arg `TEST_ENABLED`. You can completely disable testing during build by passing the following flag to the CLI

```sh
--build-arg 'TEST_ENABLED=false'
```

You can also set it permanently in your stack.yaml, see the [YAML reference in the docs](https://docs.openfaas.com/reference/yaml/#function-build-args-build-args).

### Changing the test configuration
The template creates a default `tox.ini` file, modifying this file can completely control what happens during the test. You can change the test command, for example switching to `nose`. See the [tox docs](https://tox.readthedocs.io/en/latest/index.html) for more details and examples.

### Changing the test command
If you don't want to use `tox` at all, you can also change the test command that is used. The template exposes the build arg `TEST_COMMAND`. You can override the test command during build by passing the following flag to the CLI

```sh
--build-arg 'TEST_COMMAND=bash test.sh'
```
Setting the command to any other executable in the image or any scripts you have in your function.

You can also set it permanently in your stack.yaml, see the [YAML reference in the docs](https://docs.openfaas.com/reference/yaml/#function-build-args-build-args).
