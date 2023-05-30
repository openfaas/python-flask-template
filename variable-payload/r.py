import random

def h():
    payload_size_mb = 1

    ret_val = ""
    # Generate a random number for ASCII between A and Z
    for i in range(0, 1024*1024):
        random_ch = random.randint(65, 90)
        ret_val += chr(random_ch)

    # Generate a random string of size: payload_size_mb
    ret = {
        "payload_size_mb": payload_size_mb,
        "payload": ret_val,
    }

    return ret

print(h())