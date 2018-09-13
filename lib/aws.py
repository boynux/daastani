import boto3
import datetime
import requests


class CredentialsProvider(object):
    def __init__(self, url, certs):
        self.url = url
        self.certs = certs
        self._creds = None
        self._session = None
        self._expiration = datetime.datetime.now()

    def renewCredentials(self):
        res = requests.get(self.url, cert=self.certs)

        creds = res.json()
        self._creds = creds['credentials']
        self._expiration = datetime.datetime.strptime(self._creds['expiration'], '%Y-%m-%dT%H:%M:%SZ')

        return self._creds

    def getSession(self):
        if self._isAboutToExpire():

            self.renewCredentials()

            # Or via the Session
            self._session = boto3.Session(
                aws_access_key_id=self._creds['accessKeyId'],
                aws_secret_access_key=self._creds['secretAccessKey'],
                aws_session_token=self._creds['sessionToken']
            )

        return self._session

    def _isAboutToExpire(self, seconds=900):
        delta = datetime.datetime.now() - self._expiration

        return delta.total_seconds() < seconds
