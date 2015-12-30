#Twilight Trader

Twilight Traderは、各種金融商品(FX,CFD,現物,信用)の自動売買に必要なプログラム群をまとめたものです。
提供される機能は以下の4つです。

	1. データ収集(collect)
	2. データ解析(analyze)
	3. 売買発注(signal)
	4. インターフェース(ui)

##構成

├── README.md
├── analyze //データ解析 : TODO
├── collect //データ収集
│   ├── investing //リアルタイムデータ取得
│   ├── yahoo_finance //経済指標取得
│   └── scripts
│       ├── realtime_demo_alive.sh
│       ├── realtime_master.sh //リアルタイムデータ取得のmaster(デーモン)
│       ├── realtime_slave.sh //リアルタイムデータ取得のslave(デーモン)
│       ├── ecomonic_indicator.sh //経済指標の取得
│       └── realtime_stop.sh
├── config
│   ├── common.ini
│   ├── investing.json
│   └── private.ini.sample
├── db
│   └── 20151231
│       ├── eurjpy.csv
│       ├── eurusd.csv
│       ├── oil.csv
│       └── usdjpy.csv
├── material
│   ├── TwilightTrader.png
│   └── UML.asta
├── signal
└── ui

#データ収集(collect)

データ収集の機能はcollectにまとまっています。
経済指標は、Yahoo Financeのhtmlをパーズして取得します。
リアルタイムレートは、investing.comからWebSocketを用いて取得します。
TODO : リアルタイムレート取得はmaster/slaveで冗長性を実現します。

##インストール
下記のツールに依存しています。適時インストールを行ってください。

	python3 : PyV8
	node : socket-client

##経済指標を取得する

1.config/common.iniに取得したい経済指標を追加する。

例 : 

```xml
[yahoo_finance]
# 非農業部門雇用者数変化 [前月比](失業率は無視)
cec = http://info.finance.yahoo.co.jp/fx/marketcalendar/detail/9031
# 小売売上高 [前月比]
retail_sales = http://info.finance.yahoo.co.jp/fx/marketcalendar/detail/9041
# 米CPI
cpi = http://info.finance.yahoo.co.jp/fx/marketcalendar/detail/9051
```

2.TODO

##リアルタイムレートを取得する

1.config/investing.jsonに取得したい経済指標を追加する。

例 : 

```json
{
  "url" : "http://stream20.forexpros.com:80/echo",
  "TimeZoneID" : 29,
  "contents" : {
    "1": {
    "name" : "eurusd",
    "param": [
      "pid-1:",
      "isOpenExch-1002:",
      "isOpenExch-1:"
    ]
    },
    "3": {
      "name" : "usdjpy",
      "param": [
          "pid-3:",
          "isOpenExch-1002:", 
          "isOpenExch-3:"
      ]
    },
    "9": {
      "name" : "eurjpy",
      "param": [
          "pid-9:", 
          "isOpenExch-1002:", 
          "isOpenExch-9:"
      ]
    },
    "8849": {
      "name" : "oil",
      "param": [
          "pid-8849:",
          "isOpenPair-8849:" 
      ]
    }
  }
}
```

2.collect/node/investing/investing_websocket.jsを実行する。

すると、db/[date]/[商品名].csvで保存される。

#TODO

1. デーモン監視ツールの作成

2. データの圧縮機能の追加


Copyright and License
---------------------

Copyright (C) 2015 [RV](http://asserter.net) 


Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.