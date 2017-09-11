class BaseUrl:
    def __init__(self, api_name, scheme='https', host='api.zaif.jp'):
        self._scheme = scheme
        self._host = host
        self._api_name = api_name

    def get_base_url(self):
        base = '{}://{}/{}'
        return base.format(self._scheme, self._host, self._api_name)


class PublicBaseUrl(BaseUrl):
    def __init__(self, api_name, version, **kwargs):
        super().__init__(api_name, **kwargs)
        self._version = version

    def get_base_url(self):
        base = super().get_base_url()
        return '{}/{}'.format(base, self._version)


class TradeBaseUrl(BaseUrl):
    pass
