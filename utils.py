import logging
import os
import re
import requests


def logError(message):
    logging.error(message)


def getMyIpAddress():
    logging.info('Fetching current ip address')
    response = requests.get(os.getenv('WHAT_IS_MY_IP_URL'))

    ipFound = re.findall(r'[0-9]+(?:\.[0-9]+){3}', response.text)

    if len(ipFound) > 0:
        logging.info('Found IP Address: {}'.format(ipFound[0]))
        return ipFound[0]

    logError('There was an error while retrieving the current IP Address.')
    return False
