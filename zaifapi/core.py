# -*- coding: utf-8 -*-
import time
import json
import requests
from decimal import Decimal
from datetime import datetime
from abc import ABCMeta, abstractmethod
from future.moves.urllib.parse import urlencode
from zaifapi.api_common import get_response
from zaifapi.api_error import ZaifApiError, ZaifApiNonceError, ZaifApiValidationError
from .validator import ZaifApiValidator, SCHEMA


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
        raise ZaifApiValidationError(json.dumps(v.errors))


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
