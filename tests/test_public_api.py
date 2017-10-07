import unittest
from unittest.mock import patch, MagicMock
from zaifapi import ZaifPublicApi


class TestPublicApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = ZaifPublicApi()
        cls.api._url._api_name = 'test_public'

    def setUp(self):
        self.response = MagicMock()
        self.response.status_code = 200
        self.response.text = '{}'
        self.assertEqual(self.api._url.get_absolute_url(),
                         'https://api.zaif.jp/test_public/1')

    def tearDown(self):
        self.assertEqual(self.api._url.get_absolute_url(),
                         'https://api.zaif.jp/test_public/1')

    def test_last_price(self):
        with patch('requests.get') as mock_get:
            currency_pair = 'test_jpy'
            mock_get.return_value = self.response
            self.api.last_price(currency_pair=currency_pair)
            mock_get.assert_called_once_with('https://api.zaif.jp/test_public/1/last_price/test_jpy',
                                             params={})

    def test_ticker(self):
        with patch('requests.get') as mock_get:
            currency_pair = 'test_jpy'
            mock_get.return_value = self.response
            self.api.ticker(currency_pair=currency_pair)
            mock_get.assert_called_once_with('https://api.zaif.jp/test_public/1/ticker/test_jpy',
                                             params={})

    def test_trades(self):
        with patch('requests.get') as mock_get:
            currency_pair = 'test_jpy'
            mock_get.return_value = self.response
            self.api.trades(currency_pair=currency_pair)
            mock_get.assert_called_once_with('https://api.zaif.jp/test_public/1/trades/test_jpy',
                                             params={})

    def test_depth(self):
        with patch('requests.get') as mock_get:
            currency_pair = 'test_jpy'
            mock_get.return_value = self.response
            self.api.depth(currency_pair=currency_pair)
            mock_get.assert_called_once_with('https://api.zaif.jp/test_public/1/depth/test_jpy',
                                             params={})

    def test_currency_pairs(self):
        with patch('requests.get') as mock_get:
            currency_pair = 'test_jpy'
            mock_get.return_value = self.response
            self.api.currency_pairs(currency_pair=currency_pair)
            mock_get.assert_called_once_with('https://api.zaif.jp/test_public/1/currency_pairs/test_jpy',
                                             params={})

    def test_currency(self):
        with patch('requests.get') as mock_get:
            currency_pair = 'test_coin'
            mock_get.return_value = self.response
            self.api.currencies(currency=currency_pair)
            mock_get.assert_called_once_with('https://api.zaif.jp/test_public/1/currencies/test_coin',
                                             params={})


if __name__ == '__main__':
    unittest.main()
