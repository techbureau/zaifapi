import inspect
from abc import ABCMeta
from .response import get_response
from .url import ApiUrl
from .validator import ZaifApiValidator, FuturesPublicApiValidator


def method_name():
    return inspect.stack()[1][3]


class ZaifApi(metaclass=ABCMeta):

    def __init__(self, url):
        self._url = url
