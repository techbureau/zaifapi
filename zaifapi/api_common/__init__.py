import inspect


def method_name():
    return inspect.stack()[1][3]


from .response import get_response
from .url import ApiUrl
from .validator import ZaifApiValidator, FuturesPublicApiValidator
