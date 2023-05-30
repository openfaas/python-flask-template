def handle(event, context):

    
    return {
        "statusCode": 200,
        "body": "Hello from OpenFaaS! {}".format(event.body.decode("utf-8")),
    }
