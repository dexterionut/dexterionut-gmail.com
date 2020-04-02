import logging
import os
import sys

import env
from digital_ocean_api import getRecord, createRecord, updateRecord, NoRecord
from utils import getMyIpAddress


def configLogging():
    import time
    logging.getLogger().setLevel(logging.INFO)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.basicConfig(format='{}: GMT: %(asctime)s %(levelname)s %(message)s'.format(os.path.split(sys.argv[0])[1]))
    logging.Formatter.converter = time.gmtime


def main():
    DOMAIN_NAME = os.getenv('DOMAIN_NAME')
    SUBDOMAIN_NAME = os.getenv('SUBDOMAIN_NAME')
    RTYPE = os.getenv('RTYPE')
    TTL = os.getenv('TTL')

    configLogging()
    ipAddress = getMyIpAddress()

    try:
        record = getRecord(DOMAIN_NAME, SUBDOMAIN_NAME)

        if record['data'] == ipAddress:
            logging.info('Already up to date!')
            exit(0)

        updateRecord(DOMAIN_NAME, record, ipAddress, RTYPE, TTL)
    except NoRecord:
        createRecord(DOMAIN_NAME, SUBDOMAIN_NAME, ipAddress, RTYPE, TTL)


if __name__ == '__main__':
    main()
