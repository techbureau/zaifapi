# -*- coding: utf-8 -*-
import json
import requests
from abc import ABCMeta
from zaifapi.core import ZaifExchangeApiCore


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
