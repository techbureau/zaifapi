from .impl import *
from .token import ZaifTokenApi

_MAX_COUNT = 1000
_MIN_WAIT_TIME_SEC = 1

__all__ = [
    'ZaifTradeApi',
    'ZaifPublicApi',
    'ZaifTokenTradeApi',
    'ZaifTokenApi',
    'ZaifPublicStreamApi',
    'ZaifLeverageTradeApi',
    'ZaifFuturesPublicApi'
]
