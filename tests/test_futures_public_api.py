import unittest
from unittest.mock import patch, MagicMock
from zaifapi import ZaifFuturesPublicApi


class TestPublicApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = ZaifFuturesPublicApi()
        cls.api._url._api_name = 'test_futures'

    def setUp(self):
        self.response = MagicMock()
        self.response.status_code = 200
        self.response.text = '{}'
        self.assertEqual(self.api._url.get_absolute_url(),
                         'https://api.zaif.jp/test_futures/1')

    def tearDown(self):
        self.assertEqual(self.api._url.get_absolute_url(),
                         'https://api.zaif.jp/test_futures/1')

    def test_last_price(self):
        with patch('requests.get') as mock_get:
            currency_pair = 'test_jpy'
            mock_get.return_value = self.response
            self.api.last_price(currency_pair=currency_pair, group_id=17)
            mock_get.assert_called_once_with('https://api.zaif.jp/test_futures/1/last_price/17/test_jpy',
                                             params={})

    def test_ticker(self):
        with patch('requests.get') as mock_get:
            currency_pair = 'test_jpy'
            mock_get.return_value = self.response
            self.api.ticker(currency_pair=currency_pair, group_id='all')
            mock_get.assert_called_once_with('https://api.zaif.jp/test_futures/1/ticker/all/test_jpy',
                                             params={})

    def test_trades(self):
        with patch('requests.get') as mock_get:
            currency_pair = 'test_jpy'
            mock_get.return_value = self.response
            self.api.trades(currency_pair=currency_pair, group_id=1212)
            mock_get.assert_called_once_with('https://api.zaif.jp/test_futures/1/trades/1212/test_jpy',
                                             params={})

    def test_depth(self):
        with patch('requests.get') as mock_get:
            currency_pair = 'test_jpy'
            mock_get.return_value = self.response
            self.api.depth(currency_pair=currency_pair, group_id='group_id')
            mock_get.assert_called_once_with('https://api.zaif.jp/test_futures/1/depth/group_id/test_jpy',
                                             params={})

    def test_groups(self):
        with patch('requests.get') as mock_get:
            mock_get.return_value = self.response
            self.api.groups(group_id=3)
            mock_get.assert_called_once_with('https://api.zaif.jp/test_futures/1/groups/3',
                                             params={})


if __name__ == '__main__':
    unittest.main()
