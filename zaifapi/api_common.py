import inspect
import cerberus
import json
import requests
from urllib.parse import urlencode
from decimal import Decimal
from zaifapi.api_error import ZaifApiValidationError


def get_response(url, params=None, headers=None):
    response = requests.post(url, data=params, headers=headers)
    if response.status_code != 200:
        raise Exception('return status code is {}'.format(response.status_code))
    return json.loads(response.text)


def method_name():
    return inspect.stack()[1][3]


class ApiUrl:
    _base = '{}://{}{}'

    def __init__(self, api_name, scheme='https', host='api.zaif.jp', version=None, port=None, path=None, params=None):
        self._scheme = scheme
        self._host = host
        self._api_name = api_name
        self._port = port
        self._q_params = _QueryParam(params)
        self._path = path or []
        self._version = version

    def base_url(self):
        base = self._base.format(self._scheme, self._host, self._get_port())
        if self._api_name:
            base += '/' + str(self._api_name)

        if self._version:
            base += '/' + str(self._version)
        return base

    def full_url(self):
        url = self.base_url()
        for path in self._path:
            url += '/' + path
        if len(self._q_params) == 0:
            return url
        url += '?' + self._q_params.encode()
        return url

    def _get_port(self):
        if self._port:
            return ':{}'.format(self._port)
        return ''

    def add_path(self, path, *paths):
        if path is not None:
            self._path.append(str(path))

        if len(paths) > 0:
            for path in paths:
                if path is not None:
                    self._path.append(str(path))

    def add_param(self, key, value):
        self._q_params.add_param(key, value)


class _QueryParam:
    def __init__(self, params=None):
        self._params = params or {}

    def encode(self):
        return urlencode(self._params)

    def __str__(self):
        return self.encode()

    def add_param(self, k, v):
        self._params[k] = v

    def add_params(self, dictionary):
        for k, v in dictionary.items():
            self._params[k] = v

    def __len__(self):
        return len(self._params)


class ZaifApiValidator:
    def __init__(self):
        self._schema = _ZaifValidationSchema()

    def params_pre_processing(self, keys, params):
        self._validate(keys, params)
        return self._edit_params(params)

    @classmethod
    def _edit_params(cls, params):
        if 'from_num' in params:
            params['from'] = params['from_num']
            del (params['from_num'])
        return params

    def _validate(self, keys, params):
        required_schema = self._schema.select(keys)
        v = _UnitValidator(required_schema)
        if v.validate(params):
            return
        raise ZaifApiValidationError(json.dumps(v.errors))


class FuturesPublicApiValidator(ZaifApiValidator):
    def __init__(self):
        super().__init__()
        self._schema.updates({
            'currency_pair': {
                'type': 'string',
                'nullable': True
            },
        })


class _UnitValidator(cerberus.Validator):
    @staticmethod
    def _validate_type_decimal(value):
        if isinstance(value, Decimal):
            return True

    def validate(self, params):
        return super().validate(params)


class _ZaifValidationSchema:
    def __init__(self):
        self._schema = DEFAULT_SCHEMA

    def all(self):
        return self._schema

    def select(self, keys):
        return dict(filter(lambda item: item[0] in keys, self._schema.items()))

    def update(self, k, v):
        self._schema[k] = v

    def updates(self, dictionary):
        for k, v, in dictionary.items():
            self.update(k, v)


DEFAULT_SCHEMA = {
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
        'type': ['number', 'decimal']
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
        'type': ['number', 'decimal']
    },
    'limit': {
        'type': ['number', 'decimal']
    },
    'is_token': {
        'type': 'boolean'
    },
    'is_token_both': {
        'type': 'boolean'
    },
    'comment': {
        'type': 'string'
    },
    'group_id': {
        'type': ['string', 'integer']
    },
    'type': {
        'type': 'string',
        'allowed': ['margin', 'futures']
    },
    'leverage': {
        'type': ['number', 'decimal']
    },
    'leverage_id': {
        'type': 'integer',
    }
}
