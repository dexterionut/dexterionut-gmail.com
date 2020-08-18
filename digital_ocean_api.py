import logging
import os

import requests

from utils import logError

RTYPE = os.getenv('RTYPE')


class NoRecord(Exception):
    pass


class DigitalOceanApi:
    _headers: dict
    _digitalOceanApiUrl: str
    _digitalOceanToken: str

    def __init__(self, digitalOceanApiUrl, digitalOceanToken):
        self._digitalOceanToken = digitalOceanToken
        self._digitalOceanApiUrl = digitalOceanApiUrl

        self.setHeaders()

    def setHeaders(self, extraHeaders=None):
        headers = {
            'Authorization': "Bearer {}".format(self._digitalOceanToken),
            'Content-Type': 'application/json'
        }

        if extraHeaders:
            headers.update(extraHeaders)

        self._headers = headers

    def getRecord(self, domainName, subdomainName, rtype):
        logging.info('Fetching Record ID for: {}.{}'.format(subdomainName, domainName))
        url = '{}/domains/{}/records'.format(self._digitalOceanApiUrl, domainName)

        while True:
            result = requests.get(url, headers=self._headers).json()

            for record in result['domain_records']:
                if record['type'] == rtype and record['name'] == subdomainName:
                    return record

            if 'pages' in result['links'] and 'next' in result['links']['pages']:
                url = result['links']['pages']['next']
                # Replace http to https.
                # DigitalOcean forces https request, but links are returned as http
                url = url.replace('http://', 'https://')
            else:
                break

        raise NoRecord('Could not find record: {}.{}'.format(subdomainName, domainName))

    def createRecord(self, domainName, subdomainName, ipAddress, rtype, ttl):
        logging.info('Creating record {}.{} with value {}'.format(subdomainName, domainName, ipAddress))

        url = '{}/domains/{}/records'.format(self._digitalOceanApiUrl, domainName)
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

        result = requests.post(url, json=payload, headers=self._headers).json()

        if 'domain_record' not in result:
            logError('Creating record failed with the following error: {}'.format(result['message']))
            return False

        return result['domain_record']

    def updateRecord(self, domainName, record, ipAddress, rtype, ttl):
        logging.info('Updating record {}.{} to {}'.format(record['name'], domainName, ipAddress))

        url = '{}/domains/{}/records/{}'.format(self._digitalOceanApiUrl, domainName, record['id'])
        payload = {
            'type': rtype,
            'data': ipAddress,
            'ttl': ttl
        }

        result = requests.put(url, json=payload, headers=self._headers).json()

        if 'domain_record' not in result:
            logError('Updating record failed with the following error: {}'.format(result['message']))
            return False

        if result['domain_record']['data'] == ipAddress:
            logging.info('Success!')
