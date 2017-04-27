zaifapi
======================
zaifが公開しているAPIを簡単に呼べる用にしました。
本モジュールはテックビューロ非公式です。ご利用は自己責任でご自由にどうぞ。

使い方
------
１．pipコマンドを実行し、モジュールをダウンロードしてください

    pip install zaifapi

２．クラスをインポートし、下記例の用に使用してください

    from zaifapi import *
    
    zaif = ZaifPublicApi()
    print(zaif.last_price('btc_jpy'))
    
    zaif = ZaifTradeApi(key, secret)
    print(zaif.get_info())
    print(zaif.get_info2())
    
    zaif = ZaifTokenTradeApi(token)
    print(zaif.get_info())
    
    token = ZaifTokenTradeApi(client_id, client_secret)
    reponse = token.get_token(code):
    print(reponse)
    >>>{'token_type': 'bearer',
        'state': '2a99cc45cef04c358dbc26db880f9d03',
        'access_token': 'bb12f3de5df2472290ff15331824a9cf', 
        'refresh_token': 'ef972ad13e484e17abffbfd5dba51750', 
        'expires_in': 3600}
    

機能紹介
------
### ZaifPublicApi
#### Zaifが公開している認証情報が要らないAPIを実行するクラスです
***
last_price(currency_pair):終値を取得

ticker(currency_pair):ティッカー

trades(currency_pair):全ての取引履歴

depth(currency_pair):板情報

streaming(currency_pair):websocketを利用したリアルタイム板情報と終値

| 名前 | 必須 | 説明 | デフォルト値 | 
|:-----------|:------------:|:-----------|:-----------| 
| currency_pair | ◯ | 取得する通貨ペア | - | 
戻り値：json

currency_pairはbtc_jpy、xem_jpy、mona_jpy、mona_btcが指定可能です

詳細は下記参考を御覧ください。

[参考](https://techbureau-api-document.readthedocs.io/ja/latest/public/index.html)
***

### ZaifPrivateApi
#### Zaifが公開している認証情報が必要なAPIを実行するクラスです
***
インスタンス生成時に、zaifで発行出来るkeyとsecretの文字列を指定してください。
その際、権限設定にご注意ください。

実行出来るメソッドやパラメータは下記参考ページそのままなので、そこをご覧ください。

ただし、fromパラメータはfrom_numと指定してください。

戻り値はすべてjsonとなっています。

[参考](https://techbureau-api-document.readthedocs.io/ja/latest/trade/index.html)
***

### ZaifPrivateTokenApi
#### ZaifPrivateApiをOAuth下で運用したい時に利用するクラスです
***
ZaifPrivateTokenApiと違い、OAuthで発行されたtokenを引数に指定します。

実行出来るメソッドやパラメータはZaifPrivateApiと同様になります。

***

### ZaifTokenApi
#### OAuth連携使用時に利用するクラスです。
***
client_id, client_secretを指定して、OAuth認可処理を実行します。

get_token(code, redirect_uri=None):

トークンを取得します

| 名前 | 必須 | 説明 | デフォルト値 | 
|:-----------|:------------:|:-----------|:-----------| 
| code | ◯ | 認可画面からリダイレクトされた時のcodeパラメータを指定します | - |
| redirect_uri | ☓ | 認可画面にリダイレクトした際、redirect_uriを指定している場合は同値を指定します | None |

refresh_token(refresh_token):

トークンを再発行します

| 名前 | 必須 | 説明 | デフォルト値 | 
|:-----------|:------------:|:-----------|:-----------| 
| refresh_token | ◯ | token発行時(get_token実行時)、返却されたrefresh_token値を指定します | - |

各関数の戻り値は下記を参照してください。
[OAuth認証機能利用手順](https://techbureau-api-document.readthedocs.io/ja/latest/oauth/index.html)

***


関連情報
--------
1. [[Zaif]Pythonで簡単に仮想通貨の取引が出来るようにしてみた(Qiita)](http://qiita.com/Akira-Taniguchi/items/e52930c881adc6ecfe07)
2. [LinkedIn](https://jp.linkedin.com/in/akirataniguchi1)
 
ライセンス
----------
Distributed under the [MIT License][mit].
[MIT]: http://www.opensource.org/licenses/mit-license.php
