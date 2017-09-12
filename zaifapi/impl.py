_MAX_COUNT = 1000
_MIN_WAIT_TIME_SEC = 1


from zaifapi.trade import (
    ZaifTradeApi,
    ZaifLeverageTradeApi,
    ZaifTokenTradeApi,
)


from zaifapi.public import (
    ZaifPublicStreamApi,
    ZaifPublicApi,
    ZaifFuturesPublicApi,
)

__all__ = [
    'ZaifTradeApi',
    'ZaifLeverageTradeApi',
    'ZaifTokenTradeApi',
    'ZaifPublicStreamApi',
    'ZaifPublicApi',
    'ZaifFuturesPublicApi',
]
