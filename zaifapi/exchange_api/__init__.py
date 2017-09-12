# -*- coding: utf-8 -*-
from abc import ABCMeta
from zaifapi.api_common import ZaifApiValidator, ZaifApi


class ZaifExchangeApi(ZaifApi):
    __metaclass__ = ABCMeta

    def __init__(self, url, validator=None):
        super().__init__(url)
        self._validator = validator or ZaifApiValidator()

    def params_pre_processing(self, keys, params):
        return self._validator.params_pre_processing(keys, params)


from .public import ZaifPublicApi, ZaifFuturesPublicApi
from .trade import ZaifTokenTradeApi, ZaifTradeApi, ZaifLeverageTradeApi


__all__ = [
    'ZaifLeverageTradeApi',
    'ZaifTradeApi',
    'ZaifTokenTradeApi',
    'ZaifFuturesPublicApi',
    'ZaifPublicApi'
]
