import random
import sys

def handle(event, context):
    payload_size_mb = 1

    if "payload_size_mb" in event.query:
        payload_size_mb = int(event.query["payload_size_mb"])

    sys.stderr.write("payload_size_mb: {}\n".format(payload_size_mb))

    ret_val = ""
    # Generate a random number for ASCII between A and Z
    for i in range(0, 1024*1024*payload_size_mb):
        random_ch = random.randint(65, 90)
        ret_val += chr(random_ch)

    # Generate a random string of size: payload_size_mb
    ret = {
        "payload_size_mb": payload_size_mb,
        "payload": ret_val,
    }
    
    return {
        "statusCode": 200,
        "body": ret,
    }
