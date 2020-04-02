import logging
import os
import re
import time
import requests
from functools import wraps


def logError(message):
    logging.error(message)
    exit(-1)


def retry(times=-1, delay=0.5, errors=(Exception,)):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            count = 0
            while True:
                try:
                    count = count + 1
                    return f(*args, **kwargs)
                except errors as e:
                    if count == times:
                        logError('Unexpected error: {0}'.format(e))
                    time.sleep(delay)

        return wrapper

    return decorator


@retry(times=5, delay=1.0)
def getMyIpAddress():
    logging.info('Fetching current ip address')
    response = requests.get(os.getenv('WHAT_IS_MY_IP_URL'))

    ipFound = re.findall(r'[0-9]+(?:\.[0-9]+){3}', response.text)

    if len(ipFound) > 0:
        logging.info('Found IP Address: {}'.format(ipFound[0]))
        return ipFound[0]

    raise Exception('There was an error while retrieving the current IP Address.')
