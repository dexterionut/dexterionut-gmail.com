import logging
import os
import sys
from time import sleep

import schedule
from digital_ocean_api import DigitalOceanApi, NoRecord
from utils import getMyIpAddress
from dotenv import load_dotenv

load_dotenv()


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

    try:
        ipAddress = getMyIpAddress()

        if not ipAddress:
            logging.error('There was an error while retrieving the current IP Address.')
            return

    except Exception as err:
        logging.error('There was an error while retrieving the current IP Address. Unexpected error: {}'.format(err))
        return

    digitalOceanApi = DigitalOceanApi(os.getenv('DIGITAL_OCEAN_API_URL'), os.getenv('DIGITAL_OCEAN_TOKEN'))

    try:
        record = digitalOceanApi.getRecord(DOMAIN_NAME, SUBDOMAIN_NAME, RTYPE)

        if record['data'] == ipAddress:
            logging.info('Already up to date!')
            return

        digitalOceanApi.updateRecord(DOMAIN_NAME, record, ipAddress, RTYPE, TTL)

    except NoRecord:
        digitalOceanApi.createRecord(DOMAIN_NAME, SUBDOMAIN_NAME, ipAddress, RTYPE, TTL)

    except Exception as err:
        logging.error('Unexpected error: {}'.format(err))
        pass


if __name__ == '__main__':
    RUN_EVERY = int(os.getenv('RUN_EVERY', -1))

    if RUN_EVERY < 0:
        main()
    else:
        schedule.every(RUN_EVERY).seconds.do(main)

        while True:
            schedule.run_pending()
            sleep(1)
