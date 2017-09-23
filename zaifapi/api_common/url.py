import itertools
from urllib.parse import urlencode


class ApiUrl:
    _skeleton_url = '{}://{}{}'

    def __init__(self, api_name, protocol='https', host='api.zaif.jp',
                 version=None, port=None, dirs=None, params=None):

        self._protocol = protocol
        self._host = host
        self._api_name = api_name
        self._port = port
        self._q_params = QueryParam(params)
        self._dirs = dirs or []
        self._version = version

    def get_base_url(self):
        base = self._skeleton_url.format(self._protocol, self._host, self._get_port())
        if self._api_name:
            base += '/' + str(self._api_name)

        if self._version:
            base += '/' + str(self._version)
        return base

    def get_absolute_url(self, *, with_params=False):
        absolute_url = self.get_base_url() + self.get_pathname()
        if with_params is True:
            absolute_url += self._q_params.get_str_params()
        return absolute_url

    def get_pathname(self):
        path_name = ''
        for dir_ in self._dirs:
            path_name += '/' + str(dir_)
        return path_name

    def _get_port(self):
        if self._port:
            return ':{}'.format(self._port)
        return ''

    def add_dirs(self, dir_, *dirs):
        for dir_ in itertools.chain((dir_, ), dirs):
            if dir_ is None:
                return
            self._dirs.append(str(dir_))

    def refresh_dirs(self):
        self._dirs = []

    def add_q_params(self, dict_):
        for key, value in dict_.items():
            self._q_params.add_param(key, value)

    def refresh_q_params(self):
        self._q_params.delete_all()


class QueryParam:
    def __init__(self, params=None):
        self._params = params or {}

    def _encode(self):
        return urlencode(self._params)

    def get_str_params(self):
        if len(self._params) == 0:
            return ''
        return '?' + self._encode()

    def __str__(self):
        return self._encode()

    def add_param(self, k, v):
        self._params[k] = v

    def add_params(self, dictionary):
        for k, v in dictionary.items():
            self._params[k] = v

    def delete_all(self):
        self._params = {}

    def __len__(self):
        return len(self._params)

    def __dict__(self):
        return self._params
