from urllib.parse import urlencode


class ApiUrl:
    _base = '{}://{}{}/{}'

    def __init__(self, api_name, scheme='https', host='api.zaif.jp', version=None, port=None, path=None, params=None):
        self._scheme = scheme
        self._host = host
        self._api_name = api_name
        self._port = port
        self._q_params = QueryParam(params)
        self._path = path or []
        self._version = str(version)

    def base_url(self):
        base = self._base.format(self._scheme, self._host, self._get_port(), self._api_name)
        if self._version:
            base += '/' + self._version
        return base

    def full_url(self):
        url = self.base_url()
        for path in self._path:
            url += '/' + path
        if len(self._q_params) == 0:
            return url
        url += '?' + self._q_params.encode()
        return url

    def _get_port(self):
        if self._port:
            return ':{}'.format(self._port)
        return ''

    def add_path(self, path, *paths):
        if path is not None:
            self._path.append(str(path))

        if len(paths) > 0:
            for path in paths:
                if path is not None:
                    self._path.append(str(path))


class QueryParam:
    def __init__(self, params=None):
        self._params = params or {}

    def encode(self):
        return urlencode(self._params)

    def __str__(self):
        return self.encode()

    def add_param(self, k, v):
        self._params[k] = v

    def add_params(self, dictionary):
        for k, v in dictionary.items():
            self._params[k] = v

    def __len__(self):
        return len(self._params)
