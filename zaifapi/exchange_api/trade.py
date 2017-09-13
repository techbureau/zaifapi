import time
import hmac
import hashlib
from decimal import Decimal
from datetime import datetime
from abc import ABCMeta, abstractmethod
from urllib.parse import urlencode
from zaifapi.api_common import get_response, ApiUrl, method_name
from zaifapi.api_error import ZaifApiError, ZaifApiNonceError
from . import ZaifExchangeApi


class _ZaifTradeApiBase(ZaifExchangeApi, metaclass=ABCMeta):
    @abstractmethod
    def _get_header(self, params):
        raise NotImplementedError()

    @staticmethod
    def _get_nonce():
        now = datetime.now()
        nonce = str(int(time.mktime(now.timetuple())))
        microseconds = '{0:06d}'.format(now.microsecond)
        return Decimal(nonce + '.' + microseconds)

    def _execute_api(self, func_name, schema_keys=None, params=None):
        schema_keys = schema_keys or []
        params = params or {}

        params = self._params_pre_processing(schema_keys, params, func_name)
        header = self._get_header(params)
        url = self._url.get_absolute_url()

        res = get_response(url, params, header)
        if res['success'] == 0:
            if res['error'].startswith('nonce'):
                raise ZaifApiNonceError(res['error'])
            raise ZaifApiError(res['error'])
        return res['return']

    def _params_pre_processing(self, keys, params, func_name):
        params = self._validator.params_pre_processing(keys, params)
        params['method'] = func_name
        params['nonce'] = self._get_nonce()
        return urlencode(params)


def _make_signature(key, secret, params):
    signature = hmac.new(bytearray(secret.encode('utf-8')),
                         digestmod=hashlib.sha512)
    signature.update(params.encode('utf-8'))
    return {
        'key': key,
        'sign': signature.hexdigest()
    }


class ZaifTradeApi(_ZaifTradeApiBase):
    def __init__(self, key, secret):
        super().__init__(ApiUrl(api_name='tapi'))
        self._key = key
        self._secret = secret

    def _get_header(self, params):
        return _make_signature(self._key, self._secret, params)

    def get_info(self):
        return self._execute_api(method_name())

    def get_info2(self):
        return self._execute_api(method_name())

    def get_personal_info(self):
        return self._execute_api(method_name())

    def get_id_info(self):
        return self._execute_api(method_name())

    def trade_history(self, **kwargs):
        schema_keys = ['from_num', 'count', 'from_id',
                       'end_id', 'order', 'since', 'end',
                       'currency_pair', 'is_token']
        return self._execute_api(method_name(), schema_keys, kwargs)

    def active_orders(self, **kwargs):
        schema_keys = ['currency_pair', 'is_token', 'is_token_both']
        return self._execute_api(method_name(), schema_keys, kwargs)

    def _inner_history_api(self, func_name, kwargs):
        schema_keys = ['currency', 'from_num', 'count', 'from_id',
                       'end_id', 'order', 'since', 'end', 'is_token']
        return self._execute_api(func_name, schema_keys, kwargs)

    def withdraw_history(self, **kwargs):
        return self._inner_history_api(method_name(), kwargs)

    def deposit_history(self, **kwargs):
        return self._inner_history_api(method_name(), kwargs)

    def withdraw(self, **kwargs):
        schema_keys = ['currency', 'address',
                       'message', 'amount', 'opt_fee']
        return self._execute_api(method_name(), schema_keys, kwargs)

    def cancel_order(self, **kwargs):
        schema_keys = ['order_id', 'is_token', 'currency_pair']
        return self._execute_api(method_name(), schema_keys, kwargs)

    def trade(self, **kwargs):
        schema_keys = ['currency_pair', 'action',
                       'price', 'amount', 'limit', 'comment']
        return self._execute_api(method_name(), schema_keys, kwargs)


class ZaifLeverageTradeApi(_ZaifTradeApiBase):
    def __init__(self, key, secret):
        super().__init__(ApiUrl(api_name='tlapi'))
        self._key = key
        self._secret = secret

    def _get_header(self, params):
        return _make_signature(self._key, self._secret, params)

    def get_positions(self, **kwargs):
        schema_keys = ['type', 'group_id', 'from_num', 'count',
                       'from_id', 'end_id', 'order',
                       'since', 'end', 'currency_pair']

        return self._execute_api(method_name(), schema_keys, kwargs)

    def position_history(self, **kwargs):
        schema_keys = ['type', 'group_id', 'leverage_id']
        return self._execute_api(method_name(), schema_keys, kwargs)

    def active_positions(self, **kwargs):
        schema_keys = ['type', 'group_id', 'currency_pair']
        return self._execute_api(method_name(), schema_keys, kwargs)

    def create_position(self, **kwargs):
        schema_keys = ['type', 'group_id', 'currency_pair', 'action',
                       'price', 'amount', 'leverage', 'limit', 'stop']
        return self._execute_api(method_name(), schema_keys, kwargs)

    def change_position(self, **kwargs):
        schema_keys = ['type', 'group_id', 'leverage_id',
                       'price', 'limit', 'stop']
        return self._execute_api(method_name(), schema_keys, kwargs)

    def cancel_position(self, **kwargs):
        schema_keys = ['type', 'group_id', 'leverage_id']
        return self._execute_api(method_name(), schema_keys, kwargs)


class ZaifTokenTradeApi(ZaifTradeApi):
    def __init__(self, token):
        self._token = token
        super().__init__(None, None)

    def get_header(self, params):
        return {
            'token': self._token
        }
