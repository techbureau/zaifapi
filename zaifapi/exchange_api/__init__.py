from abc import ABCMeta, abstractmethod
from zaifapi.api_common.validator import ZaifApiValidator
from zaifapi.api_common import ZaifApi


class ZaifExchangeApi(ZaifApi, metaclass=ABCMeta):
    def __init__(self, url, validator=None):
        super().__init__(url)
        self._validator = validator or ZaifApiValidator()

    @abstractmethod
    def _params_pre_processing(self, *args, **kwargs):
        raise NotImplementedError


from .public import ZaifPublicApi, ZaifFuturesPublicApi, ZaifPublicStreamApi  # NOQA
from .trade import ZaifTokenTradeApi, ZaifTradeApi, ZaifLeverageTradeApi  # NOQA


__all__ = [
    "ZaifLeverageTradeApi",
    "ZaifTradeApi",
    "ZaifTokenTradeApi",
    "ZaifFuturesPublicApi",
    "ZaifPublicApi",
    "ZaifPublicStreamApi",
]
