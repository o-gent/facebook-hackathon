import requests
import json

from fastmental.logger import setup_logger

WIT_API_HOST = 'https://api.wit.ai'
WIT_API_VERSION = '20200513'


class WitError(Exception):
    pass


class Wit:

    def __init__(self, access_token, logger=None):
        self.access_token = access_token
        self.logger = logger


    def message(self, msg, context=None, n=None, verbose=None):
        params = {}
        params['q'] = msg

        if n:
            params['n'] = n
        if context:
            params['context'] = json.dumps(context)
        if verbose:
            params['verbose'] = verbose
        
        resp = self.req(self.access_token, 'GET', '/message', params)

        return resp
    

    def train(self):
        """
        https://wit.ai/docs/http/20200513#post__utterances_link
        """
        raise NotImplementedError()
    

    def speech(self, audio_file, headers=None, verbose=None):
        """ 
        Sends an audio file to the /speech API.
        Uses the streaming feature of requests (see `req`), so opening the file
        in binary mode is strongly reccomended (see
        http://docs.python-requests.org/en/master/user/advanced/#streaming-uploads).
        Add Content-Type header as specified here: https://wit.ai/docs/http/20200513#post--speech-link
        :param audio_file: an open handler to an audio file
        :param headers: an optional dictionary with request headers
        :param verbose: for legacy versions, get extra information
        :return:
        """
        params = {}
        headers = headers or {}
        
        if verbose:
            params['verbose'] = True

        resp = self.req(self.logger, 
                self.access_token, 
                'POST', 
                '/speech', 
                params,
                data=audio_file, 
                headers=headers
                )
        return resp
    

    def req(method, path, params, **kwargs):
        """
        Request helper function
        """
        full_url = WIT_API_HOST + path
        logger.debug('%s %s %s', method, full_url, params)

        headers = {
            'authorization': 'Bearer ' + self.access_token,
            'accept': 'application/vnd.wit.' + WIT_API_VERSION + '+json'
        }    
        headers.update(kwargs.pop('headers', {}))

        response = requests.request(
            method,
            full_url,
            headers=headers,
            params=params,
            **kwargs
        )

        if response.status_code != 200:
            raise WitError('Wit responded with status: ' + str(rsp.status_code) + ' (' + rsp.reason + ')')
        
        response_json = response.json()
        if 'error' in response_json:
            raise WitError('Wit responded with an error: ' + response_json['error'])

        logger.debug('%s %s %s', method, full_url, response_json)

        return response_json
