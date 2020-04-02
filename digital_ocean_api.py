import logging
import os

import requests

from utils import createHeaders, logError

DIGITAL_OCEAN_API_URL = os.getenv('DIGITAL_OCEAN_API_URL')
RTYPE = os.getenv('RTYPE')


class NoRecord(Exception):
    pass


def getRecord(domainName, subdomainName):
    logging.info('Fetching Record ID for: {}.{}'.format(subdomainName, domainName))
    url = '{}/domains/{}/records'.format(DIGITAL_OCEAN_API_URL, domainName)

    while True:
        result = requests.get(url, headers=createHeaders()).json()

        for record in result['domain_records']:
            if record['type'] == RTYPE and record['name'] == subdomainName:
                return record

        if 'pages' in result['links'] and 'next' in result['links']['pages']:
            url = result['links']['pages']['next']
            # Replace http to https.
            # DigitalOcean forces https request, but links are returned as http
            url = url.replace('http://', 'https://')
        else:
            break

    raise NoRecord('Could not find record: {}.{}'.format(subdomainName, domainName))


def createRecord(domainName, subdomainName, ipAddress, rtype, ttl):
    logging.info('Creating record {}.{} with value {}'.format(subdomainName, domainName, ipAddress))

    url = '{}/domains/{}/records'.format(DIGITAL_OCEAN_API_URL, domainName)
    payload = {
        'type': rtype,
        'name': subdomainName,
        'data': ipAddress,
        'priority': None,
        'port': None,
        'ttl': ttl,
        'weight': None,
        'flags': None,
        'tag': None
    }

    result = requests.post(url, json=payload, headers=createHeaders()).json()

    if 'domain_record' not in result:
        logError('Creating record failed with the following error: {}'.format(result['message']))

    return result['domain_record']


def updateRecord(domainName, record, ipAddress, rtype, ttl):
    logging.info('Updating record {}.{} to {}'.format(record['name'], domainName, ipAddress))

    url = '{}/domains/{}/records/{}'.format(DIGITAL_OCEAN_API_URL, domainName, record['id'])
    payload = {
        'type': rtype,
        'data': ipAddress,
        'ttl': ttl
    }

    result = requests.put(url, json=payload, headers=createHeaders()).json()

    if 'domain_record' not in result:
        logError('Creating record failed with the following error: {}'.format(result['message']))

    if result['domain_record']['data'] == ipAddress:
        logging.info('Success!')
