import unittest
from unittest.mock import patch, MagicMock
from zaifapi import ZaifTradeApi
from urllib.parse import urlencode
from urllib.parse import parse_qs


class TestPublicApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = ZaifTradeApi(key='test_key', secret='test_secret')
        cls.api._url._host = 'test_trade.com'
        cls.api._get_header = MagicMock(return_value={'key': 'key', 'sign': 'sign'})
        cls.api._get_nonce = MagicMock(return_value=1111111111)

    def setUp(self):
        self.response = MagicMock()
        self.response.status_code = 200
        self.response.text = '{"success": 1, "return": "return"}'
        self.assertEqual(self.api._url.get_absolute_url(),
                         'https://test_trade.com/tapi')

    def tearDown(self):
        self.assertEqual(self.api._url.get_absolute_url(),
                         'https://test_trade.com/tapi')

    def test_get_info(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value = self.response
            self.api.get_info()
            params = urlencode({'method': 'get_info', 'nonce': 1111111111})

            mock_post.assert_called_once_with('https://test_trade.com/tapi',
                                              data=params,
                                              headers={'key': 'key', 'sign': 'sign'})

    def test_get_info2(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value = self.response
            self.api.get_info2()
            params = urlencode({'method': 'get_info2', 'nonce': 1111111111})

            mock_post.assert_called_once_with('https://test_trade.com/tapi',
                                              data=params,
                                              headers={'key': 'key', 'sign': 'sign'})

    def test_get_personal_info(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value = self.response
            self.api.get_personal_info()
            params = urlencode({'method': 'get_personal_info', 'nonce': 1111111111})

            mock_post.assert_called_once_with('https://test_trade.com/tapi',
                                              data=params,
                                              headers={'key': 'key', 'sign': 'sign'})

    def test_get_id_info(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value = self.response
            self.api.get_id_info()
            params = urlencode({'method': 'get_id_info', 'nonce': 1111111111})

            mock_post.assert_called_once_with('https://test_trade.com/tapi',
                                              data=params,
                                              headers={'key': 'key', 'sign': 'sign'})

    def test_trade_history(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value = self.response
            self.api.trade_history(from_num=0, count=1, from_id=2, end_id=3, order='DESC',
                                   since=1111, end=2222, currency_pair='test_jpy', is_token=False)

            params = {'method': ['trade_history'],
                      'nonce': ['1111111111'],
                      'from': ['0'],
                      'count': ['1'],
                      'from_id': ['2'],
                      'end_id': ['3'],
                      'order': ['DESC'],
                      'since': ['1111'],
                      'end': ['2222'],
                      'currency_pair': ['test_jpy'],
                      'is_token': ['False']}

            self.assertEqual(mock_post.call_args[0], ('https://test_trade.com/tapi',))
            self.assertDictEqual(parse_qs(mock_post.call_args[1]['data']), params)
            self.assertDictEqual(mock_post.call_args[1]['headers'], {'key': 'key', 'sign': 'sign'})

    def test_active_orders(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value = self.response
            self.api.active_orders(currency_pair='test_jpy', is_token=False, is_token_both=True)

            params = {'method': ['active_orders'],
                      'nonce': ['1111111111'],
                      'currency_pair': ['test_jpy'],
                      'is_token': ['False'],
                      'is_token_both': ['True']}

            self.assertEqual(mock_post.call_args[0], ('https://test_trade.com/tapi',))
            self.assertDictEqual(parse_qs(mock_post.call_args[1]['data']), params)
            self.assertDictEqual(mock_post.call_args[1]['headers'], {'key': 'key', 'sign': 'sign'})

    def test_withdraw_history(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value = self.response
            self.api.withdraw_history(from_num=0, count=1, from_id=2, end_id=3, order='DESC',
                                      since=1111, end=2222, currency='test_coin', is_token=False)

            params = {'method': ['withdraw_history'],
                      'nonce': ['1111111111'],
                      'from': ['0'],
                      'count': ['1'],
                      'from_id': ['2'],
                      'end_id': ['3'],
                      'order': ['DESC'],
                      'since': ['1111'],
                      'end': ['2222'],
                      'currency': ['test_coin'],
                      'is_token': ['False']}

            self.assertEqual(mock_post.call_args[0], ('https://test_trade.com/tapi',))
            self.assertDictEqual(parse_qs(mock_post.call_args[1]['data']), params)
            self.assertDictEqual(mock_post.call_args[1]['headers'], {'key': 'key', 'sign': 'sign'})

    def test_deposit_history(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value = self.response
            self.api.deposit_history(from_num=0, count=1, from_id=2, end_id=3, order='DESC',
                                      since=1111, end=2222, currency='test_coin', is_token=False)

            params = {'method': ['deposit_history'],
                      'nonce': ['1111111111'],
                      'from': ['0'],
                      'count': ['1'],
                      'from_id': ['2'],
                      'end_id': ['3'],
                      'order': ['DESC'],
                      'since': ['1111'],
                      'end': ['2222'],
                      'currency': ['test_coin'],
                      'is_token': ['False']}

            self.assertEqual(mock_post.call_args[0], ('https://test_trade.com/tapi',))
            self.assertDictEqual(parse_qs(mock_post.call_args[1]['data']), params)
            self.assertDictEqual(mock_post.call_args[1]['headers'], {'key': 'key', 'sign': 'sign'})

    def test_withdraw(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value = self.response
            self.api.withdraw(currency='test_coin', address='test_address', message='test_message',
                              amount=1000, opt_fee=1)

            params = {'method': ['withdraw'],
                      'nonce': ['1111111111'],
                      'currency': ['test_coin'],
                      'address': ['test_address'],
                      'message': ['test_message'],
                      'amount': ['1000'],
                      'opt_fee': ['1']}

            self.assertEqual(mock_post.call_args[0], ('https://test_trade.com/tapi',))
            self.assertDictEqual(parse_qs(mock_post.call_args[1]['data']), params)
            self.assertDictEqual(mock_post.call_args[1]['headers'], {'key': 'key', 'sign': 'sign'})

    def test_cancel_order(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value = self.response
            self.api.cancel_order(order_id=123, is_token=True, currency_pair='test_jpy')

            params = {'method': ['cancel_order'],
                      'nonce': ['1111111111'],
                      'currency_pair': ['test_jpy'],
                      'order_id': ['123'],
                      'is_token': ['True']}

            self.assertEqual(mock_post.call_args[0], ('https://test_trade.com/tapi',))
            self.assertDictEqual(parse_qs(mock_post.call_args[1]['data']), params)
            self.assertDictEqual(mock_post.call_args[1]['headers'], {'key': 'key', 'sign': 'sign'})

    def test_trade(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value = self.response
            self.api.trade(currency_pair='test_jpy', action='bid', price=12345,
                           amount=12, limit=123456, comment='test')

            params = {'method': ['trade'],
                      'nonce': ['1111111111'],
                      'currency_pair': ['test_jpy'],
                      'action': ['bid'],
                      'price': ['12345'],
                      'amount': ['12'],
                      'limit': ['123456'],
                      'comment': ['test']}

            self.assertEqual(mock_post.call_args[0], ('https://test_trade.com/tapi',))
            self.assertDictEqual(parse_qs(mock_post.call_args[1]['data']), params)
            self.assertDictEqual(mock_post.call_args[1]['headers'], {'key': 'key', 'sign': 'sign'})


if __name__ == '__main__':
    unittest.main()
