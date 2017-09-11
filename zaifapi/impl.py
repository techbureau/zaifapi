# -*- coding: utf-8 -*-
import time
import json
import hmac
import hashlib
import inspect
import requests
from decimal import Decimal
from datetime import datetime
from abc import ABCMeta, abstractmethod
from websocket import create_connection
from future.moves.urllib.parse import urlencode
from zaifapi.api_common import get_response
from zaifapi.api_error import ZaifApiError, ZaifApiNonceError

from .validator import ZaifApiValidator, SCHEMA
from .url import PublicBaseUrl, TradeBaseUrl


_MAX_COUNT = 1000
_MIN_WAIT_TIME_SEC = 1


class ZaifExchangeApiCore(metaclass=ABCMeta):
    def __init__(self, base_url):
        self._base_url = base_url
        self._schema = self._override_schema(SCHEMA)

    def params_pre_processing(self, schema_keys, params):
        schema = self._select_schema(schema_keys)
        self._validate(params, schema)
        return self._edit_params(params)

    def _select_schema(self, keys):
        # extract schema by keys input
        schema = {k: v for k, v in filter(lambda t: t[0] in keys, self._schema.items())}
        return schema

    @abstractmethod
    def _override_schema(self, default_scheme):
        raise NotImplementedError

    @classmethod
    def _edit_params(cls, params):
        if 'from_num' in params:
            params['from'] = params['from_num']
            del (params['from_num'])
        return params

    @classmethod
    def _validate(cls, params, schema):
        v = ZaifApiValidator(schema)
        if v.validate(params):
            return
        raise Exception(json.dumps(v.errors))


class ZaifPublicApiBase(ZaifExchangeApiCore, metaclass=ABCMeta):
    pass


class SpotPublicApiImpl(ZaifPublicApiBase):
    def __init__(self):
        super().__init__(PublicBaseUrl(api_name='api', version=1).get_base_url())

    def _override_schema(self, default_scheme):
        return default_scheme


class FuturesPublicApiImpl(ZaifPublicApiBase):
    def __init__(self):
        super().__init__(PublicBaseUrl(api_name='fapi', version=1).get_base_url())

    def _override_schema(self, default_scheme):
        return default_scheme


class ZaifPublicApi(SpotPublicApiImpl):
    def _execute_api(self, func_name, currency_pair, params=None):
        self.params_pre_processing(['currency_pair'], {'currency_pair': currency_pair})
        url = '{}/{}/{}'.format(self._base_url, func_name, currency_pair)
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception('return status code is {}'.format(response.status_code))
        return json.loads(response.text)

    def last_price(self, currency_pair):
        return self._execute_api(inspect.currentframe().f_code.co_name, currency_pair)

    def ticker(self, currency_pair):
        return self._execute_api(inspect.currentframe().f_code.co_name, currency_pair)

    def trades(self, currency_pair):
        return self._execute_api(inspect.currentframe().f_code.co_name, currency_pair)

    def depth(self, currency_pair):
        return self._execute_api(inspect.currentframe().f_code.co_name, currency_pair)

    def currency_pairs(self, currency_pair):
        return self._execute_api(inspect.currentframe().f_code.co_name, currency_pair)

    def currencies(self, currency):
        return self._execute_api(inspect.currentframe().f_code.co_name, currency)


class ZaifFuturesPublicApi(FuturesPublicApiImpl):
    def _execute_api(self, func_name, group_id, currency_pair='', params=None):
        self.params_pre_processing(['currency_pair', 'group_id'], {'currency_pair': currency_pair, 'group_id': group_id})
        if currency_pair is None:
            url = '{}/{}/{}'.format(self._base_url, func_name, group_id)
        else:
            url = '{}/{}/{}/{}'.format(self._base_url, func_name, group_id, currency_pair)
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception('return status code is {}'.format(response.status_code))
        return json.loads(response.text)

    def last_price(self, group_id, currency_pair):
        return self._execute_api(inspect.currentframe().f_code.co_name, group_id, currency_pair)

    def ticker(self, group_id, currency_pair):
        return self._execute_api(inspect.currentframe().f_code.co_name, group_id, currency_pair)

    def trades(self, group_id, currency_pair):
        return self._execute_api(inspect.currentframe().f_code.co_name, group_id, currency_pair)

    def depth(self, group_id, currency_pair):
        return self._execute_api(inspect.currentframe().f_code.co_name, group_id, currency_pair)

    def groups(self, group_id):
        return self._execute_api(inspect.currentframe().f_code.co_name, group_id)


# class ZaifPublicStreamApi(ZaifPublicApiBase):
#     def __init__(self):
#         self._continue = True
#
#     def stop(self):
#         self._continue = False
#
#     def execute(self, currency_pair):
#         self._params_pre_processing(currency_pair)
#         ws = create_connection('wss://ws.zaif.jp:8888/stream?currency_pair={}'.format(currency_pair))
#         while self._continue:
#             result = ws.recv()
#             yield json.loads(result)
#         ws.close()
#
#
# class _AbsZaifTradeApi(AbsZaifApi):
#     _API_URL = '{}://{}/tapi'
#
#     @abstractmethod
#     def get_header(self, params):
#         raise NotImplementedError()
#
#     @staticmethod
#     def _get_nonce():
#         now = datetime.now()
#         nonce = str(int(time.mktime(now.timetuple())))
#         microseconds = '{0:06d}'.format(now.microsecond)
#         return Decimal(nonce + '.' + microseconds)
#
#     def _get_parameter(self, func_name, params):
#         params['method'] = func_name
#         params['nonce'] = self._get_nonce()
#         return urlencode(params)
#
#     def _execute_api(self, func_name, schema_keys=None, params=None):
#         if schema_keys is None:
#             schema_keys = []
#         if params is None:
#             params = {}
#         params = self.params_pre_processing(schema_keys, params)
#         params = self._get_parameter(func_name, params)
#         header = self.get_header(params)
#         res = get_response(self._API_URL.format(self.get_protocol(), self._api_domain), params, header)
#         if res['success'] == 0:
#             if res['error'].startswith('nonce'):
#                 raise ZaifApiNonceError(res['error'])
#             raise ZaifApiError(res['error'])
#         return res['return']
#
#     def get_info(self):
#         return self._execute_api(inspect.currentframe().f_code.co_name)
#
#     def get_info2(self):
#         return self._execute_api(inspect.currentframe().f_code.co_name)
#
#     def get_personal_info(self):
#         return self._execute_api(inspect.currentframe().f_code.co_name)
#
#     def get_id_info(self):
#         return self._execute_api(inspect.currentframe().f_code.co_name)
#
#     def trade_history(self, **kwargs):
#         schema_keys = ['from_num', 'count', 'from_id', 'end_id', 'order', 'since', 'end', 'currency_pair', 'is_token']
#         return self._execute_api(inspect.currentframe().f_code.co_name, schema_keys, kwargs)
#
#     def active_orders(self, **kwargs):
#         schema_keys = ['currency_pair', 'is_token', 'is_token_both']
#         return self._execute_api(inspect.currentframe().f_code.co_name, schema_keys, kwargs)
#
#     def _inner_history_api(self, func_name, kwargs):
#         schema_keys = ['currency', 'from_num', 'count', 'from_id', 'end_id', 'order', 'since', 'end', 'is_token']
#         return self._execute_api(func_name, schema_keys, kwargs)
#
#     def withdraw_history(self, **kwargs):
#         return self._inner_history_api(inspect.currentframe().f_code.co_name, kwargs)
#
#     def deposit_history(self, **kwargs):
#         return self._inner_history_api(inspect.currentframe().f_code.co_name, kwargs)
#
#     def withdraw(self, **kwargs):
#         schema_keys = ['currency', 'address', 'message', 'amount', 'opt_fee']
#         return self._execute_api(inspect.currentframe().f_code.co_name, schema_keys, kwargs)
#
#     def cancel_order(self, **kwargs):
#         schema_keys = ['order_id', 'is_token', 'currency_pair']
#         return self._execute_api(inspect.currentframe().f_code.co_name, schema_keys, kwargs)
#
#     def trade(self, **kwargs):
#         schema_keys = ['currency_pair', 'action', 'price', 'amount', 'limit', 'comment']
#         return self._execute_api(inspect.currentframe().f_code.co_name, schema_keys, kwargs)
#
#
# class ZaifTradeApi(_AbsZaifTradeApi):
#     def __init__(self, key, secret):
#         self._key = key
#         self._secret = secret
#         super(ZaifTradeApi, self).__init__()
#
#     def get_header(self, params):
#         signature = hmac.new(bytearray(self._secret.encode('utf-8')), digestmod=hashlib.sha512)
#         signature.update(params.encode('utf-8'))
#         return {
#             'key': self._key,
#             'sign': signature.hexdigest()
#         }
#
#
# class ZaifTokenTradeApi(_AbsZaifTradeApi):
#     def __init__(self, token):
#         self._token = token
#         super(ZaifTokenTradeApi, self).__init__()
#
#     def get_header(self, params):
#         return {
#             'token': self._token
#         }
#
#
# class ZaifFuturesPublicApi:
#     pass
#
#
# class ZaifLeverageTradeApi:
#     pass