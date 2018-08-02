import json
import requests
from abc import ABCMeta

from zaifapi.api_error import ZaifApiError
from websocket import create_connection
from zaifapi.api_common import method_name, get_api_url, FuturesPublicApiValidator
from . import ZaifExchangeApi


class _ZaifPublicApiBase(ZaifExchangeApi, metaclass=ABCMeta):
    def _execute_api(self, func_name, schema_keys=None, q_params=None, **kwargs):
        schema_keys = schema_keys or []
        q_params = q_params or {}
        params = self._params_pre_processing(schema_keys, kwargs)
        self._url.add_dirs(func_name, *params.values())
        response = requests.get(self._url.get_absolute_url(), params=q_params)
        self._url.refresh_dirs()
        if response.status_code != 200:
            raise ZaifApiError('return status code is {}'.format(response.status_code))
        return json.loads(response.text)

    def _params_pre_processing(self, keys, params):
        return self._validator.params_pre_processing(keys, params)


class ZaifPublicApi(_ZaifPublicApiBase):
    def __init__(self, api_url=None):
        super().__init__(get_api_url(api_url, 'api', version=1))

    def last_price(self, currency_pair):
        schema_keys = ['currency_pair']
        return self._execute_api(method_name(),
                                 schema_keys,
                                 currency_pair=currency_pair)

    def ticker(self, currency_pair):
        schema_keys = ['currency_pair']
        return self._execute_api(method_name(),
                                 schema_keys,
                                 currency_pair=currency_pair)

    def trades(self, currency_pair):
        schema_keys = ['currency_pair']
        return self._execute_api(method_name(),
                                 schema_keys,
                                 currency_pair=currency_pair)

    def depth(self, currency_pair):
        schema_keys = ['currency_pair']
        return self._execute_api(method_name(),
                                 schema_keys,
                                 currency_pair=currency_pair)

    def currency_pairs(self, currency_pair):
        schema_keys = ['currency_pair']
        return self._execute_api(method_name(),
                                 schema_keys,
                                 currency_pair=currency_pair)

    def currencies(self, currency):
        schema_keys = ['currency']
        return self._execute_api(method_name(),
                                 schema_keys,
                                 currency=currency)


class ZaifFuturesPublicApi(_ZaifPublicApiBase):
    def __init__(self, api_url=None):
        api_url = get_api_url(api_url, 'fapi', version=1)
        super().__init__(
            api_url,
            FuturesPublicApiValidator()
        )

    # Want to delete this method
    def _execute_api(self, func_name, schema_keys=None, q_params=None, **kwargs):
        schema_keys = schema_keys or []
        q_params = q_params or {}
        params = self._params_pre_processing(schema_keys, kwargs)
        if params.get('page', None):
            self._url.add_dirs(func_name, params.get('group_id'), params.get('currency_pair'),
                               params.get('page'))
        else:
            self._url.add_dirs(func_name, params.get('group_id'), params.get('currency_pair'))
        response = requests.get(self._url.get_absolute_url(), params=q_params)
        self._url.refresh_dirs()
        if response.status_code != 200:
            raise ZaifApiError('return status code is {}'.format(response.status_code))
        return json.loads(response.text)

    def last_price(self, group_id, currency_pair=None):
        schema_keys = ['currency_pair', 'group_id']
        return self._execute_api(method_name(),
                                 schema_keys,
                                 group_id=group_id,
                                 currency_pair=currency_pair)

    def ticker(self, group_id, currency_pair):
        schema_keys = ['currency_pair', 'group_id']
        return self._execute_api(method_name(),
                                 schema_keys,
                                 group_id=group_id,
                                 currency_pair=currency_pair)

    def trades(self, group_id, currency_pair):
        schema_keys = ['currency_pair', 'group_id']
        return self._execute_api(method_name(),
                                 schema_keys,
                                 group_id=group_id,
                                 currency_pair=currency_pair)

    def depth(self, group_id, currency_pair):
        schema_keys = ['currency_pair', 'group_id']
        return self._execute_api(method_name(),
                                 schema_keys,
                                 group_id=group_id,
                                 currency_pair=currency_pair)

    def groups(self, group_id):
        schema_keys = ['group_id']
        return self._execute_api(method_name(),
                                 schema_keys,
                                 group_id=group_id)

    def swap_history(self, group_id, currency_pair, page=None):
        if not page:
            schema_keys = ['currency_pair', 'group_id']
            return self._execute_api(method_name(),
                                     schema_keys,
                                     group_id=group_id,
                                     currency_pair=currency_pair)
        schema_keys = ['currency_pair', 'group_id', 'page']
        return self._execute_api(method_name(),
                                 schema_keys,
                                 group_id=group_id,
                                 currency_pair=currency_pair,
                                 page=page)


class ZaifPublicStreamApi(_ZaifPublicApiBase):
    def __init__(self, api_url=None):
        api_url = get_api_url(api_url, 'stream', protocol='wss', host='ws.zaif.jp', port=8888)
        super().__init__(api_url)
        self._continue = True

    def stop(self):
        self._continue = False

    def execute(self, currency_pair):
        params = {'currency_pair': currency_pair}
        params = self._params_pre_processing(['currency_pair'], params=params)
        self._url.add_q_params(params)
        ws = create_connection(self._url.get_absolute_url(with_params=True))
        while self._continue:
            result = ws.recv()
            yield json.loads(result)
        ws.close()
