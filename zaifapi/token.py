# -*- coding: utf-8 -*-
from zaifapi.api_common import get_response
from .core import ZaifApi


# todo: 消す
class AbsZaifBaseApi(object):
    __metaclass__ = ABCMeta
    _use_https = True

    def get_protocol(self):
        if self._use_https:
            return 'https'
        return 'http'


class ZaifTokenApi():
    pass


class ZaifTokenApi(AbsZaifBaseApi):
    _API_URL = '{}://{}/v1/token'
    _api_domain = 'oauth.zaif.jp'

    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret

    def get_token(self, code, redirect_uri=None):
        params = {
            'code': code,
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'grant_type': 'authorization_code'
        }
        if redirect_uri:
            params['redirect_uri'] = redirect_uri
        return get_response(self._API_URL.format(self.get_protocol(), self._api_domain), params)

    def refresh_token(self, refresh_token):
        params = {
            'refresh_token': refresh_token,
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'grant_type': 'refresh_token'
        }
        return get_response(self._API_URL, params)
