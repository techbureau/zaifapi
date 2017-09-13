from zaifapi.api_common import get_response, ZaifApi
from zaifapi.api_common import ApiUrl


class ZaifTokenApi(ZaifApi):
    def __init__(self, client_id, client_secret):
        super().__init__(ApiUrl(api_name=None,
                                version='v1',
                                dirs=['token'],
                                host='oauth.zaif.jp'))

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
        return get_response(self._url.get_absolute_url(), params)

    def refresh_token(self, refresh_token):
        params = {
            'refresh_token': refresh_token,
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'grant_type': 'refresh_token'
        }
        return get_response(self._url.get_absolute_url(), params)
