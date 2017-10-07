import unittest
from unittest.mock import patch, MagicMock
from zaifapi import ZaifLeverageTradeApi
from urllib.parse import parse_qs


class TestPublicApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = ZaifLeverageTradeApi(key='test_key', secret='test_secret')
        cls.api._url._host = 'test_leverage_trade.com'
        cls.api._get_header = MagicMock(return_value={'key': 'key', 'sign': 'sign'})
        cls.api._get_nonce = MagicMock(return_value=1111111111)

    def setUp(self):
        self.response = MagicMock()
        self.response.status_code = 200
        self.response.text = '{"success": 1, "return": "return"}'
        self.assertEqual(self.api._url.get_absolute_url(),
                         'https://test_leverage_trade.com/tlapi')

    def tearDown(self):
        self.assertEqual(self.api._url.get_absolute_url(),
                         'https://test_leverage_trade.com/tlapi')

    def test_get_positions(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value = self.response
            self.api.get_positions(type='futures', from_num=0, count=1, from_id=2, end_id=3, order='DESC',
                                   since=1111, end=2222, currency_pair='test_jpy')

            params = {'method': ['get_positions'],
                      'nonce': ['1111111111'],
                      'from': ['0'],
                      'count': ['1'],
                      'from_id': ['2'],
                      'end_id': ['3'],
                      'order': ['DESC'],
                      'since': ['1111'],
                      'end': ['2222'],
                      'currency_pair': ['test_jpy'],
                      'type': ['futures']}

            self.assertEqual(mock_post.call_args[0], ('https://test_leverage_trade.com/tlapi',))
            self.assertDictEqual(parse_qs(mock_post.call_args[1]['data']), params)
            self.assertDictEqual(mock_post.call_args[1]['headers'], {'key': 'key', 'sign': 'sign'})

    def test_position_history(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value = self.response
            self.api.position_history(type='futures', group_id=1, leverage_id=12)

            params = {'method': ['position_history'],
                      'nonce': ['1111111111'],
                      'type': ['futures'],
                      'group_id': ['1'],
                      'leverage_id': ['12']}

            self.assertEqual(mock_post.call_args[0], ('https://test_leverage_trade.com/tlapi',))
            self.assertDictEqual(parse_qs(mock_post.call_args[1]['data']), params)
            self.assertDictEqual(mock_post.call_args[1]['headers'], {'key': 'key', 'sign': 'sign'})

    def test_active_positions(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value = self.response
            self.api.active_positions(type='futures', group_id=1, currency_pair='test_jpy')

            params = {'method': ['active_positions'],
                      'nonce': ['1111111111'],
                      'type': ['futures'],
                      'group_id': ['1'],
                      'currency_pair': ['test_jpy']}

            self.assertEqual(mock_post.call_args[0], ('https://test_leverage_trade.com/tlapi',))
            self.assertDictEqual(parse_qs(mock_post.call_args[1]['data']), params)
            self.assertDictEqual(mock_post.call_args[1]['headers'], {'key': 'key', 'sign': 'sign'})

    def test_create_position(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value = self.response
            self.api.create_position(type='futures', group_id=1, action='ask', price=12345, amount=12,
                                     leverage=5, limit=123, stop=12345566, currency_pair='test_jpy')

            params = {'method': ['create_position'],
                      'nonce': ['1111111111'],
                      'currency_pair': ['test_jpy'],
                      'type': ['futures'],
                      'group_id': ['1'],
                      'action': ['ask'],
                      'price': ['12345'],
                      'amount': ['12'],
                      'leverage': ['5'],
                      'limit': ['123'],
                      'stop': ['12345566']}

            self.assertEqual(mock_post.call_args[0], ('https://test_leverage_trade.com/tlapi',))
            self.assertDictEqual(parse_qs(mock_post.call_args[1]['data']), params)
            self.assertDictEqual(mock_post.call_args[1]['headers'], {'key': 'key', 'sign': 'sign'})

    def test_change_position(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value = self.response
            self.api.change_position(type='futures', group_id=1,  price=12345, leverage_id=5,
                                     limit=123, stop=12345566)

            params = {'method': ['change_position'],
                      'nonce': ['1111111111'],
                      'type': ['futures'],
                      'group_id': ['1'],
                      'price': ['12345'],
                      'leverage_id': ['5'],
                      'limit': ['123'],
                      'stop': ['12345566']}

            self.assertEqual(mock_post.call_args[0], ('https://test_leverage_trade.com/tlapi',))
            self.assertDictEqual(parse_qs(mock_post.call_args[1]['data']), params)
            self.assertDictEqual(mock_post.call_args[1]['headers'], {'key': 'key', 'sign': 'sign'})

    def test_cancel_position(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value = self.response
            self.api.cancel_position(type='futures', group_id=1,leverage_id=5)

            params = {'method': ['cancel_position'],
                      'nonce': ['1111111111'],
                      'type': ['futures'],
                      'group_id': ['1'],
                      'leverage_id': ['5']}

            self.assertEqual(mock_post.call_args[0], ('https://test_leverage_trade.com/tlapi',))
            self.assertDictEqual(parse_qs(mock_post.call_args[1]['data']), params)
            self.assertDictEqual(mock_post.call_args[1]['headers'], {'key': 'key', 'sign': 'sign'})


if __name__ == '__main__':
    unittest.main()
