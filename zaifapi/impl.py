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
from .url import PublicBaseUrl, TradeBaseUrl, StreamBaseUrl
from .util import method_name

_MAX_COUNT = 1000
_MIN_WAIT_TIME_SEC = 1


class ZaifExchangeApiCore(metaclass=ABCMeta):
    def __init__(self, url):
        self._url = url
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
    def _execute_api(self, func_name, schema_keys=None, params=None, **kwargs):
        schema_keys = schema_keys or []
        params = params or {}

        self.params_pre_processing(schema_keys, kwargs)
        url = self._url.create_url(func_name, *kwargs.values())
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception('return status code is {}'.format(response.status_code))
        return json.loads(response.text)

    def _override_schema(self, default_scheme):
        return default_scheme


class ZaifPublicApi(ZaifPublicApiBase):
    def __init__(self):
        super().__init__(PublicBaseUrl(api_name='api', version=1))

    def last_price(self, currency_pair):
        schema_keys = ['currency_pair']
        return self._execute_api(method_name(), schema_keys, currency_pair=currency_pair)

    def ticker(self, currency_pair):
        schema_keys = ['currency_pair']
        return self._execute_api(method_name(), schema_keys, currency_pair=currency_pair)

    def trades(self, currency_pair):
        schema_keys = ['currency_pair']
        return self._execute_api(method_name(), schema_keys, currency_pair=currency_pair)

    def depth(self, currency_pair):
        schema_keys = ['currency_pair']
        return self._execute_api(method_name(), schema_keys, currency_pair=currency_pair)

    def currency_pairs(self, currency_pair):
        schema_keys = ['currency_pair']
        return self._execute_api(method_name(), schema_keys, currency_pair=currency_pair)

    def currencies(self, currency):
        schema_keys = ['currency']
        return self._execute_api(method_name(), schema_keys, currency=currency)


class ZaifFuturesPublicApi(ZaifPublicApiBase):
    def __init__(self):
        super().__init__(PublicBaseUrl(api_name='fapi', version=1))

    def last_price(self, group_id, currency_pair):
        schema_keys = ['currency_pair', 'group_id']
        return self._execute_api(method_name(), schema_keys, group_id=group_id, currency_pair=currency_pair)

    def ticker(self, group_id, currency_pair):
        schema_keys = ['currency_pair', 'group_id']
        return self._execute_api(method_name(), schema_keys, group_id=group_id, currency_pair=currency_pair)

    def trades(self, group_id, currency_pair):
        schema_keys = ['currency_pair', 'group_id']
        return self._execute_api(method_name(), schema_keys, group_id=group_id, currency_pair=currency_pair)

    def depth(self, group_id, currency_pair):
        schema_keys = ['currency_pair', 'group_id']
        return self._execute_api(method_name(), schema_keys, group_id=group_id, currency_pair=currency_pair)

    def groups(self, group_id):
        schema_keys = ['group_id']
        return self._execute_api(method_name(), schema_keys, group_id=group_id)


class ZaifTradeApiBase(ZaifExchangeApiCore, metaclass=ABCMeta):
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
        params = self.params_pre_processing(schema_keys, params)
        params = self._get_parameter(func_name, params)
        header = self.get_header(params)
        url = self._url.create_url()
        res = get_response(url, params, header)
        if res['success'] == 0:
            if res['error'].startswith('nonce'):
                raise ZaifApiNonceError(res['error'])
            raise ZaifApiError(res['error'])
        return res['return']

    def _override_schema(self, default_scheme):
        return default_scheme


class ZaifTradeApi(ZaifTradeApiBase):
    def __init__(self, key, secret):
        self._key = key
        self._secret = secret
        super().__init__(url=TradeBaseUrl(api_name='tapi'))

    def get_header(self, params):
        signature = hmac.new(bytearray(self._secret.encode('utf-8')), digestmod=hashlib.sha512)
        signature.update(params.encode('utf-8'))
        return {
            'key': self._key,
            'sign': signature.hexdigest()
        }

    def get_info(self):
        return self._execute_api(inspect.currentframe().f_code.co_name)

    def get_info2(self):
        return self._execute_api(inspect.currentframe().f_code.co_name)

    def get_personal_info(self):
        return self._execute_api(inspect.currentframe().f_code.co_name)

    def get_id_info(self):
        return self._execute_api(inspect.currentframe().f_code.co_name)

    def trade_history(self, **kwargs):
        schema_keys = ['from_num', 'count', 'from_id', 'end_id', 'order', 'since', 'end', 'currency_pair', 'is_token']
        return self._execute_api(inspect.currentframe().f_code.co_name, schema_keys, kwargs)

    def active_orders(self, **kwargs):
        schema_keys = ['currency_pair', 'is_token', 'is_token_both']
        return self._execute_api(inspect.currentframe().f_code.co_name, schema_keys, kwargs)

    def _inner_history_api(self, func_name, kwargs):
        schema_keys = ['currency', 'from_num', 'count', 'from_id', 'end_id', 'order', 'since', 'end', 'is_token']
        return self._execute_api(func_name, schema_keys, kwargs)

    def withdraw_history(self, **kwargs):
        return self._inner_history_api(inspect.currentframe().f_code.co_name, kwargs)

    def deposit_history(self, **kwargs):
        return self._inner_history_api(inspect.currentframe().f_code.co_name, kwargs)

    def withdraw(self, **kwargs):
        schema_keys = ['currency', 'address', 'message', 'amount', 'opt_fee']
        return self._execute_api(inspect.currentframe().f_code.co_name, schema_keys, kwargs)

    def cancel_order(self, **kwargs):
        schema_keys = ['order_id', 'is_token', 'currency_pair']
        return self._execute_api(inspect.currentframe().f_code.co_name, schema_keys, kwargs)

    def trade(self, **kwargs):
        schema_keys = ['currency_pair', 'action', 'price', 'amount', 'limit', 'comment']
        return self._execute_api(inspect.currentframe().f_code.co_name, schema_keys, kwargs)


class ZaifPublicStreamApi(ZaifExchangeApiCore):
    def __init__(self):
        self._continue = True
        super().__init__(url=StreamBaseUrl(api_name='stream', scheme='wss', host='ws.zaif.jp', port=8888))

    def stop(self):
        self._continue = False

    def execute(self, currency_pair):
        self.params_pre_processing(currency_pair)
        url = self._url.create_url() + '?currency_pair={}'.format(currency_pair)
        ws = create_connection(url)
        while self._continue:
            result = ws.recv()
            yield json.loads(result)
        ws.close()

    def _override_schema(self, default_scheme):
        return default_scheme


# class ZaifTokenTradeApi(SpotTradeApiImpl):
#     def __init__(self, token):
#         self._token = token
#         super(ZaifTokenTradeApi, self).__init__()
#
#     def get_header(self, params):
#         return {
#             'token': self._token
#         }