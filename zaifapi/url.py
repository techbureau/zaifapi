class BaseUrl:
    _base = '{}://{}{}/{}{}'

    def __init__(self, api_name, scheme='https', host='api.zaif.jp', port=None):
        self._scheme = scheme
        self._host = host
        self._api_name = api_name
        self._port = port

    def get_base_url(self):
        return self._base.format(self._scheme, self._host, self._get_port(), self._api_name)

    def create_url(self, *args):
        url = self.get_base_url()
        for arg in args:
            url += '/{}'.format(arg)
        return url

    def _get_port(self):
        if self._port:
            return ':{}'.format(self._port)
        return ''


class PublicBaseUrl(BaseUrl):
    def __init__(self, api_name, version, **kwargs):
        super().__init__(api_name, **kwargs)
        self._version = version

    def get_base_url(self):
        base = super().get_base_url()
        return base + '/{}'.format(self._version)


class TradeBaseUrl(BaseUrl):
    pass


class StreamBaseUrl(BaseUrl):
    pass
