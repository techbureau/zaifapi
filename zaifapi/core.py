# -*- coding: utf-8 -*-
from abc import ABCMeta
from .validator import ZaifApiValidator


class ZaifApi:
    __metaclass__ = ABCMeta

    def __init__(self, url):
        self._url = url


class ZaifExchangeApi(ZaifApi):
    __metaclass__ = ABCMeta

    def __init__(self, url, validator=None):
        super().__init__(url)
        self._validator = validator or ZaifApiValidator()

    def params_pre_processing(self, keys, params):
        return self._validator.params_pre_processing(keys, params)
