# -*- coding: utf-8 -*-
import time
import json
import hmac
import hashlib
import inspect
import cerberus
import requests
from datetime import datetime
from abc import ABCMeta, abstractmethod
from websocket import create_connection
from future.moves.urllib.parse import urlencode
from zaifapi.api_common import get_response, AbsZaifBaseApi
from zaifapi.api_error import ZaifApiError, ZaifApiNonceError


SCHEMA = {
    'from_num': {
        'type': 'integer'
    },
    'count': {
        'type': 'integer'
    },
    'from_id': {
        'type': 'integer'
    },
    'end_id': {
        'type': ['string', 'integer']
    },
    'order': {
        'type': 'string',
        'allowed': ['ASC', 'DESC']
    },
    'since': {
        'type': 'integer'
    },
    'end': {
        'type': ['string', 'integer']
    },
    'currency_pair': {
        'type': 'string'
    },
    'currency': {
        'required': True,
        'type': 'string'
    },
    'address': {
        'required': True,
        'type': 'string'
    },
    'message': {
        'type': 'string'
    },
    'amount': {
        'required': True,
        'type': 'number'
    },
    'opt_fee': {
        'type': 'number'
    },
    'order_id': {
        'required': True,
        'type': 'integer'
    },
    'action': {
        'required': True,
        'type': 'string',
        'allowed': ['bid', 'ask']
    },
    'price': {
        'required': True,
        'type': 'number'
    },
    'limit': {
        'type': 'number'
    },
    'is_token': {
        'type': 'boolean'
    },
    'is_token_both': {
        'type': 'boolean'
    }
}
_MAX_COUNT = 1000
_MIN_WAIT_TIME_SEC = 1


class AbsZaifApi(AbsZaifBaseApi):
    __metaclass__ = ABCMeta
    _api_domain = 'api.zaif.jp'

    def params_pre_processing(self, schema_keys, params):
        schema = self._get_schema(schema_keys)
        self._validate(schema, params)
        return self._edit_params(params)

    @classmethod
    def _get_schema(cls, keys):
        schema = {}
        for key in keys:
            schema[key] = SCHEMA[key]
        return schema

    @classmethod
    def _edit_params(cls, params):
        if 'from_num' in params:
            params['from'] = params['from_num']
            del (params['from_num'])
        return params

    @classmethod
    def _validate(cls, schema, param):
        v = cerberus.Validator(schema)
        if v.validate(param):
            return
        raise Exception(json.dumps(v.errors))


class ZaifPublicApiBase(AbsZaifApi):
    __metaclass__ = ABCMeta

    def _params_pre_processing(self, currency_pair):
        params = {
            'currency_pair': currency_pair
        }
        super(ZaifPublicApiBase, self).params_pre_processing(['currency_pair'], params)


class ZaifPublicApi(ZaifPublicApiBase):
    _API_URL = '{}://{}/api/1/{}/{}'

    def _execute_api(self, func_name, currency_pair, params=None):
        self._params_pre_processing(currency_pair)
        url = self._API_URL.format(self.get_protocol(), self._api_domain, func_name, currency_pair)
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

    def everything(self, func_name, currency_pair, params):
        return self._execute_api(func_name, currency_pair, params)


class ZaifPublicStreamApi(ZaifPublicApiBase):
    def __init__(self):
        self._continue = True

    def stop(self):
        self._continue = False

    def execute(self, currency_pair):
        self._params_pre_processing(currency_pair)
        ws = create_connection('wss://ws.zaif.jp:8888/stream?currency_pair={}'.format(currency_pair))
        while self._continue:
            result = ws.recv()
            yield json.loads(result)
        ws.close()


class _AbsZaifPrivateApi(AbsZaifApi):
    _API_URL = '{}://{}/tapi'

    def __init__(self, nonce=None):
        if nonce is None:
            now = datetime.now()
            nonce = int(time.mktime(now.timetuple()))
        self._nonce = nonce

    @abstractmethod
    def get_header(self, params):
        raise NotImplementedError()

    @property
    def nonce(self):
        return self._nonce

    def _get_parameter(self, func_name, params):
        params['method'] = func_name
        self._nonce += 1
        params['nonce'] = self._nonce
        return urlencode(params)

    def _execute_api(self, func_name, schema_keys=None, params=None):
        if schema_keys is None:
            schema_keys = []
        if params is None:
            params = {}
        params = self.params_pre_processing(schema_keys, params)
        params = self._get_parameter(func_name, params)
        header = self.get_header(params)
        res = get_response(self._API_URL.format(self.get_protocol(), self._api_domain), params, header)
        if res['success'] == 0:
            if res['error'].startswith('nonce'):
                raise ZaifApiNonceError(res['error'])
            raise ZaifApiError(res['error'])
        return res['return']

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
        schema_keys = ['order_id', 'is_token']
        return self._execute_api(inspect.currentframe().f_code.co_name, schema_keys, kwargs)

    def trade(self, **kwargs):
        schema_keys = ['currency_pair', 'action', 'price', 'amount', 'limit']
        return self._execute_api(inspect.currentframe().f_code.co_name, schema_keys, kwargs)


class ZaifPrivateApi(_AbsZaifPrivateApi):
    def __init__(self, key, secret, nonce=None):
        self._key = key
        self._secret = secret
        super(ZaifPrivateApi, self).__init__(nonce)

    def get_header(self, params):
        signature = hmac.new(bytearray(self._secret.encode('utf-8')), digestmod=hashlib.sha512)
        signature.update(params.encode('utf-8'))
        return {
            'key': self._key,
            'sign': signature.hexdigest()
        }


class ZaifPrivateTokenApi(_AbsZaifPrivateApi):
    def __init__(self, token, nonce=None):
        self._token = token
        super(ZaifPrivateTokenApi, self).__init__(nonce)

    def get_header(self, params):
        return {
            'token': self._token
        }
