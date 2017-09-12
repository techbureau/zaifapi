# -*- coding: utf-8 -*-
import time
from decimal import Decimal
from datetime import datetime
from abc import ABCMeta, abstractmethod
from urllib.parse import urlencode
from zaifapi.api_common import get_response
from zaifapi.api_error import ZaifApiError, ZaifApiNonceError
from zaifapi.core import ZaifExchangeApi


class ZaifTradeApiBase(ZaifExchangeApi):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_header(self, params):
        raise NotImplementedError()

    @staticmethod
    def _get_nonce():
        now = datetime.now()
        nonce = str(int(time.mktime(now.timetuple())))
        microseconds = '{0:06d}'.format(now.microsecond)
        return Decimal(nonce + '.' + microseconds)

    def _get_parameter(self, func_name, params):
        params['method'] = func_name
        params['nonce'] = self._get_nonce()
        return urlencode(params)

    def _execute_api(self, func_name, schema_keys=None, params=None):
        schema_keys = schema_keys or []
        params = params or {}
        self.params_pre_processing(schema_keys, params)
        params = self._get_parameter(func_name, params)
        header = self.get_header(params)
        url = self._url.full_url()
        res = get_response(url, params, header)
        if res['success'] == 0:
            if res['error'].startswith('nonce'):
                raise ZaifApiNonceError(res['error'])
            raise ZaifApiError(res['error'])
        return res['return']
