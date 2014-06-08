import requests
import uuid

from dreamhostapi.module import Module


class DreamHostAPI(object):
    API_URL = 'https://api.dreamhost.com'

    def __init__(self, key):
        self.key = key

    def __getattr__(self, module_name):
        if module_name.startswith('__'):
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, module_name))

        module = Module(module_name, self._call)

        setattr(self, module_name, module)

        return module

    def _call(self, command, params=None):
        if params is None:
            params = {}

        params.update({
            'key': self.key,
            'cmd': command,
            'unique_id': str(uuid.uuid1()),
            'format': 'json',
        })

        http_response = requests.get(self.API_URL, params=params)

        # Something's very wrong if we don't get a 200 OK
        if http_response.status_code != requests.codes.ok:
            http_response.raise_for_status()

        return http_response.json()
