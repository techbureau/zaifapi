# -*- coding: utf-8 -*-
import json
import hmac
import hashlib
import inspect
from websocket import create_connection


_MAX_COUNT = 1000
_MIN_WAIT_TIME_SEC = 1


def _method_name():
    return inspect.stack()[1][3]


class ZaifPublicApi(ZaifPublicApiBase):
    def __init__(self):
        super().__init__(PublicBaseUrl(api_name='api', version=1))

    def last_price(self, currency_pair):
        schema_keys = ['currency_pair']
        return self._execute_api(_method_name(), schema_keys, currency_pair=currency_pair)

    def ticker(self, currency_pair):
        schema_keys = ['currency_pair']
        return self._execute_api(_method_name(), schema_keys, currency_pair=currency_pair)

    def trades(self, currency_pair):
        schema_keys = ['currency_pair']
        return self._execute_api(_method_name(), schema_keys, currency_pair=currency_pair)

    def depth(self, currency_pair):
        schema_keys = ['currency_pair']
        return self._execute_api(_method_name(), schema_keys, currency_pair=currency_pair)

    def currency_pairs(self, currency_pair):
        schema_keys = ['currency_pair']
        return self._execute_api(_method_name(), schema_keys, currency_pair=currency_pair)

    def currencies(self, currency):
        schema_keys = ['currency']
        return self._execute_api(_method_name(), schema_keys, currency=currency)


class ZaifFuturesPublicApi(ZaifPublicApiBase):
    def __init__(self):
        super().__init__(PublicBaseUrl(api_name='fapi', version=1))

    def last_price(self, group_id, currency_pair):
        schema_keys = ['currency_pair', 'group_id']
        return self._execute_api(_method_name(), schema_keys, group_id=group_id, currency_pair=currency_pair)

    def ticker(self, group_id, currency_pair):
        schema_keys = ['currency_pair', 'group_id']
        return self._execute_api(_method_name(), schema_keys, group_id=group_id, currency_pair=currency_pair)

    def trades(self, group_id, currency_pair):
        schema_keys = ['currency_pair', 'group_id']
        return self._execute_api(_method_name(), schema_keys, group_id=group_id, currency_pair=currency_pair)

    def depth(self, group_id, currency_pair):
        schema_keys = ['currency_pair', 'group_id']
        return self._execute_api(_method_name(), schema_keys, group_id=group_id, currency_pair=currency_pair)

    def groups(self, group_id):
        schema_keys = ['group_id']
        return self._execute_api(_method_name(), schema_keys, group_id=group_id)


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