# -*- coding: utf-8 -*-
import json
import requests
from abc import ABCMeta
from zaifapi.core import ZaifExchangeApi
from zaifapi.api_error import ZaifApiError
from zaifapi.validator import ZaifApiValidator


class ZaifPublicApiBase(ZaifExchangeApi):
    __metaclass__ = ABCMeta

    def _execute_api(self, func_name, schema_keys=None, q_params=None, **kwargs):
        schema_keys = schema_keys or []
        q_params = q_params or {}

        self.params_pre_processing(schema_keys, kwargs)
        self._url.add_path(func_name, *kwargs.values())
        response = requests.get(self._url.full_url(), params=q_params)
        if response.status_code != 200:
            raise ZaifApiError('return status code is {}'.format(response.status_code))
        return json.loads(response.text)


class SpotPublicApiValidator(ZaifApiValidator):
    pass


class FuturesPublicApiValidator(ZaifApiValidator):
    def __init__(self):
        super().__init__()
        self._schema.updates({
            'currency_pair': {
                'type': 'string',
                'nullable': True
            },
        })
