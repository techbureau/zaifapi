import cerberus
from decimal import Decimal


class ZaifApiValidator(cerberus.Validator):
    @staticmethod
    def _validate_type_decimal(value):
        if isinstance(value, Decimal):
            return True

    def validate(self, params):
        return super().validate(params)


class DynamicValidationSchema:
    def __init__(self):
        self._schema = DEFAULT_SCHEMA

    def all(self):
        return self._schema

    def select(self, keys):
        return dict(filter(lambda item: item[0] in keys, self._schema.items()))

    def update(self, key, value):
        pass


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
    }
}
