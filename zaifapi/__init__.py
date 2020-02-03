from .exchange_api import (
    ZaifTradeApi,
    ZaifPublicApi,
    ZaifTokenTradeApi,
    ZaifPublicStreamApi,
    ZaifLeverageTradeApi,
    ZaifFuturesPublicApi,
)
from .oauth import ZaifTokenApi

_MAX_COUNT = 1000
_MIN_WAIT_TIME_SEC = 1

__version__ = "1.7.0"

__all__ = [
    "__version__",
    "ZaifTradeApi",
    "ZaifPublicApi",
    "ZaifTokenTradeApi",
    "ZaifTokenApi",
    "ZaifPublicStreamApi",
    "ZaifLeverageTradeApi",
    "ZaifFuturesPublicApi",
]
