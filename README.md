![](https://img.shields.io/apm/l/vim-mode.svg) ![](https://img.shields.io/badge/Python-after%20v3-red.svg)

:snake: zaifapi [![](https://travis-ci.org/techbureau/zaifapi.svg?branch=master)](https://travis-ci.org/techbureau/zaifapi)
======================
zaifが公開しているAPIを簡単に呼べるようにしました。  
本モジュールはテックビューロ非公式です。ご利用は自己責任でご自由にどうぞ。

使い方
------
１．pipコマンドを実行し、モジュールをダウンロードしてください

    pip install zaifapi

２．クラスをインポートし、下記例の用に使用してください

```python
from zaifapi import *

zaif = ZaifPublicApi()
zaif.last_price('btc_jpy')

zaif = ZaifTradeApi(key, secret)
zaif.trade(currency_pair='btc_jpy',
           action='ask',
           amount=2,
           price=400000,
           limit=200000)

zaif = ZaifFuturesPublicApi()
zaif.last_price(group_id=1, currency_pair='btc_jpy')

zaif = ZaifLeverageTradeApi(key, secret)
zaif.create_position(type='margin',
                     currency_pair='btc_jpy',
                     action='bid',
                     amount=1,
                     price=300000,
                     leverage=2)
```
    
より詳しい機能については、[**Wiki**](https://github.com/techbureau/zaifapi/wiki)にてご確認ください。


関連情報
--------
* [[Zaif]Pythonで簡単に仮想通貨の取引が出来るようにしてみた(Qiita)](http://qiita.com/Akira-Taniguchi/items/e52930c881adc6ecfe07)
 
ライセンス
----------
Distributed under the [MIT License][mit].
[MIT]: http://www.opensource.org/licenses/mit-license.php
