# -*- coding: utf-8 -*-
import json
from abc import ABCMeta, abstractmethod
from zaifapi.api_error import ZaifApiValidationError
from .validator import ZaifApiValidator, SCHEMA


class ZaifApi:
    __metaclass__ = ABCMeta

    def __init__(self, url):
        self._url = url


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
