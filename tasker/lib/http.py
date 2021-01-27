# coding: utf-8
import sys
import json
import urllib3
import requests

from urllib3.util.retry import Retry
from urllib.parse import urljoin, quote
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter

from .log import Log

# from http.client import HTTPConnection
# HTTPConnection.debuglevel = 1

TIMEOUT_SEC = (10, 30)

urllib3.disable_warnings()


class HTTPClient:
    def __init__(self, name, base_url, headers={}, retries=3, verify=True):
        self.name = name
        self.base_url = base_url
        self.auth = None
        self.verify = verify
        self.session = self._build_session(base_url, headers, retries)

    def _build_session(self, base_url, headers, retries):
        session = requests.Session()
        session.headers.update(headers)
        retry = self._build_retry_strategy(retries)
        session.mount(base_url, HTTPAdapter(max_retries=retry))
        return session

    def _build_retry_strategy(self, retries):
        return Retry(
            allowed_methods=['GET', 'PUT', 'POST', 'DELETE'],
            backoff_factor=1,
            total=retries,
        )

    def _request(self, method, path, **kwargs):
        request = self._build_request(method, path, **kwargs)
        try:
            response = self.session.send(
                request,
                verify=self.verify,
                timeout=TIMEOUT_SEC
            )
            response.raise_for_status()
            message = response.reason
        except requests.HTTPError as err:
            err_message = f'{err} - {err.response.text}'
            message, response = err_message, err.response
        except requests.exceptions.SSLError as err:
            message, response = 'SSL error', err.response
        except requests.Timeout as err:
            message, response = 'Timeout error', err.response
        except requests.ConnectionError as err:
            message, response = 'Connection error', err.response
        except requests.RequestException as err:
            message, response = 'Request error', err.response

        evaluator = kwargs.get('evaluator', lambda r: r.json)
        return HTTPResponse(self.name, request, response, message, evaluator)

    def _build_request(self, method, path, **kwargs):
        request = requests.Request(
            method=method,
            url=urljoin(self.base_url, quote(str(path), safe="/.?&=")),
            auth=self.auth,
            headers=kwargs.get('headers', {}),
            data=json.dumps(kwargs.get('data', {}))
        )
        return self.session.prepare_request(request)

    def get(self, path, **kwargs):
        return self._request('GET', path, **kwargs)

    def list(self, path, **kwargs):
        return self._request('LIST', path, **kwargs)

    def post(self, path, **kwargs):
        return self._request('POST', path, **kwargs)

    def put(self, path, **kwargs):
        return self._request('PUT', path, **kwargs)

    def delete(self, path, **kwargs):
        return self._request('DELETE', path, **kwargs)

    def authenticate(self, login, password):
        self.auth = HTTPBasicAuth(login, password)


class HTTPResponse:
    def __init__(self, id, request, response, message, evaluator):
        self.id = id
        self.request = request
        self.response = response
        self.url = request.url
        self.headers = request.headers
        self.method = request.method
        self.message = message
        self.evaluator = evaluator

    @property
    def valid(self):
        return self.response is not None and self.response.ok

    @property
    def status(self):
        return 500 if self.response is None else self.response.status_code

    @property
    def bytes(self):
        return self.response.content if self.valid else b''

    @property
    def text(self):
        return self.response.text if self.valid else ''

    @property
    def json(self):
        try:
            return self.response.json()
        except json.decoder.JSONDecodeError:
            return {'text': self.response.text, 'status': self.status}

    @property
    def value(self):
        if not self.valid:
            return ''
        return self.evaluator(self)

    def __str__(self):
        return f'api={self.id}, method={self.method}, ' \
               f'url="{self.url}", status={self.status}, '\
               f'message="{self.message}", value={self.value}'


def request_handler(description):
    def decorator(method):
        logger = Log('DTC - MANAGER')

        def wrapped_method(self, *args, **kwargs):
            response = method(self, *args, **kwargs)
            resp_str = str(response)
            if response.valid:
                logger.info(resp_str)
                return response
            logger.error(f'{resp_str}, action="{description}", type=failure')
            return response
        return wrapped_method
    return decorator
