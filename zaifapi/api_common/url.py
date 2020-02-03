import itertools
from typing import List, Optional
from urllib.parse import urlencode


class ApiUrl:
    _skeleton_url = "{}://{}{}"

    def __init__(
        self,
        api_name,
        protocol="https",
        host="api.zaif.jp",
        version=None,
        port=None,
        dirs=None,
        params=None,
    ):

        self._protocol = protocol
        self._host = host
        self._api_name = api_name
        self._port = port
        self._q_params = QueryParam(params)
        self._dirs = dirs or []
        self._version = version

    def get_base_url(self) -> str:
        base = self._skeleton_url.format(self._protocol, self._host, self._get_port())
        if self._api_name:
            base += "/" + str(self._api_name)

        if self._version:
            base += "/" + str(self._version)
        return base

    def get_absolute_url(self, *, with_params: bool = False) -> str:
        absolute_url = self.get_base_url() + self.get_pathname()
        if with_params is True:
            absolute_url += self._q_params.get_str_params()
        return absolute_url

    def get_pathname(self) -> str:
        path_name = ""
        for dir_ in self._dirs:
            path_name += "/" + str(dir_)
        return path_name

    def _get_port(self) -> str:
        if self._port:
            return ":{}".format(self._port)
        return ""

    def add_dirs(self, dir_, *dirs) -> None:
        for dir_ in itertools.chain((dir_,), dirs):
            if dir_ is None:
                return
            self._dirs.append(str(dir_))

    def refresh_dirs(self) -> None:
        self._dirs = []

    def add_q_params(self, dict_) -> None:
        for key, value in dict_.items():
            self._q_params.add_param(key, value)

    def refresh_q_params(self) -> None:
        self._q_params.delete_all()


class QueryParam:
    def __init__(self, params=None):
        self._params = params or {}

    def _encode(self) -> str:
        return urlencode(self._params)

    def get_str_params(self) -> str:
        if len(self._params) == 0:
            return ""
        return "?" + self._encode()

    def __str__(self):
        return self._encode()

    def add_param(self, k, v) -> None:
        self._params[k] = v

    def add_params(self, dictionary) -> None:
        for k, v in dictionary.items():
            self._params[k] = v

    def delete_all(self) -> None:
        self._params = {}

    def __len__(self):
        return len(self._params)

    def __dict__(self):
        return self._params


def get_api_url(
    arg_api_url: Optional[ApiUrl],
    api_name: Optional[str],
    protocol: str = "https",
    host: str = "api.zaif.jp",
    version: Optional[str] = None,
    dirs: Optional[List[str]] = None,
    port: Optional[int] = None,
) -> ApiUrl:
    if arg_api_url is not None:
        return arg_api_url
    return ApiUrl(api_name, protocol=protocol, host=host, version=version, dirs=dirs, port=port)
