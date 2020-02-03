from typing import Optional
from zaifapi.api_common import get_response, ZaifApi
from zaifapi.api_common import ApiUrl, get_api_url


class ZaifTokenApi(ZaifApi):
    def __init__(self, client_id: str, client_secret: str, api_url: Optional[ApiUrl] = None):
        setup_api_url = get_api_url(
            api_url, None, host="oauth.zaif.jp", version="v1", dirs=["token"]
        )
        super().__init__(setup_api_url)
        self._client_id = client_id
        self._client_secret = client_secret

    def get_token(self, code: str, redirect_uri: Optional[str] = None):
        params = {
            "code": code,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "grant_type": "authorization_code",
        }
        if redirect_uri:
            params["redirect_uri"] = redirect_uri
        return get_response(self._url.get_absolute_url(), params)

    def refresh_token(self, refresh_token: str):
        params = {
            "refresh_token": refresh_token,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "grant_type": "refresh_token",
        }
        return get_response(self._url.get_absolute_url(), params)
