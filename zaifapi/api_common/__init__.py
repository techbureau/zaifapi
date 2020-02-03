import inspect
from abc import ABCMeta
from .response import get_response  # NOQA
from .url import ApiUrl, get_api_url  # NOQA
from .validator import ZaifApiValidator, FuturesPublicApiValidator  # NOQA


def method_name() -> str:
    return inspect.stack()[1][3]


class ZaifApi(metaclass=ABCMeta):
    def __init__(self, url: ApiUrl):
        self._url = url
