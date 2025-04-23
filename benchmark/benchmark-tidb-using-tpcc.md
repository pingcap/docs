---
title: How to Run TPC-C Test on TiDB
summary: このドキュメントでは、オンライントランザクション処理ベンチマークであるTPC-Cを用いてTiDBをテストする方法について説明します。データベースの初期状態を指定し、データのロード、テストの実行、そしてテストデータのクリーンアップを行うためのコマンドを提供します。このテストでは、tpmC（1分あたりのトランザクション数）を用いて、最大スループットを測定します。
---

# TiDBでTPC-Cテストを実行する方法 {#how-to-run-tpc-c-test-on-tidb}

このドキュメントでは、 [TPC-C](http://www.tpc.org/tpcc/)を使用して TiDB をテストする方法について説明します。

TPC-Cは、オンライントランザクション処理（OLTP）ベンチマークです。以下の5種類の異なるトランザクションを含む商品販売モデルを用いて、OLTPシステムをテストします。

-   ニューオーダー
-   支払い
-   注文状況
-   配達
-   在庫レベル

## 準備する {#prepare}

TPC-Cベンチマークでは、テスト前にデータベースの初期状態、つまりデータベースにおけるデータ生成のルールを指定します。テーブル`ITEM`には10万件の固定アイテムが含まれますが、倉庫の数は調整可能です。テーブル`WAREHOUSE`にW件のレコードがある場合、以下のようになります。

-   `STOCK`テーブルにはW * 100,000件のレコードがあります（各倉庫は100,000点の在庫データに対応します）
-   `DISTRICT`テーブルにはW * 10のレコードがあります（各倉庫は10の地区にサービスを提供しています）
-   `CUSTOMER`テーブルには W * 10 * 3,000 のレコードがあります (各地区には 3,000 人の顧客がいます)
-   `HISTORY`テーブルには W * 10 * 3,000 件のレコードがあります (各顧客には 1 つの取引履歴があります)
-   `ORDER`テーブルには W * 10 * 3,000 件のレコードがあります (各地区には 3,000 件の注文があり、生成された最後の 900 件の注文が`NEW-ORDER`テーブルに追加されます。各注文は 5 ~ 15 件の ORDER-LINE レコードをランダムに生成します。)

このドキュメントでは、TiDB をテストするために、例として 1,000 個のウェアハウスを使用します。

TPC-Cは、tpmC（1分あたりのトランザクション数）を使用して、最大適格スループット（MQTh、最大適格スループット）を測定します。トランザクションとはNewOrderトランザクションであり、最終的な測定単位は1分あたりに処理される新規注文数です。

このドキュメントのテストは[ゴーTPC](https://github.com/pingcap/go-tpc)に基づいて実装されています。テストプログラムは[TiUP](/tiup/tiup-overview.md)コマンドを使用してダウンロードできます。

```shell
tiup install bench
```

TiUP Benchコンポーネントの詳細な使用方法については、 [TiUPベンチ](/tiup/tiup-bench.md)参照してください。

172.16.5.140 と 172.16.5.141 にある 2 つの TiDB サーバーを含む TiDB クラスターを展開し、両方のサーバーがポート 4000 でリッスンしているとします。次の手順で TPC-C テストを実行できます。

## データを読み込む {#load-data}

**データのロードは、TPC-Cテスト全体の中で最も時間がかかり、問題が発生する段階です。**このセクションでは、データをロードするための以下のコマンドについて説明します。

シェルで次のTiUPコマンドを実行します。

```shell
tiup bench tpcc -H 172.16.5.140,172.16.5.141 -P 4000 -D tpcc --warehouses 1000 --threads 20 prepare
```

マシン構成によっては、この読み込み処理に数時間かかる場合があります。クラスターサイズが小さい場合は、テストに`WAREHOUSE`というより小さい値を使用できます。

データがロードされた後、 `tiup bench tpcc -H 172.16.5.140 -P 4000 -D tpcc --warehouses 4 check`コマンドを実行してデータの正確性を検証できます。

## テストを実行する {#run-the-test}

テストを実行するには、次のコマンドを実行します。

```shell
tiup bench tpcc -H 172.16.5.140,172.16.5.141 -P 4000 -D tpcc --warehouses 1000 --threads 100 --time 10m run
```

テスト中、テスト結果がコンソールに継続的に表示されます。

```text
[Current] NEW_ORDER - Takes(s): 4.6, Count: 5, TPM: 65.5, Sum(ms): 4604, Avg(ms): 920, 90th(ms): 1500, 99th(ms): 1500, 99.9th(ms): 1500
[Current] ORDER_STATUS - Takes(s): 1.4, Count: 1, TPM: 42.2, Sum(ms): 256, Avg(ms): 256, 90th(ms): 256, 99th(ms): 256, 99.9th(ms): 256
[Current] PAYMENT - Takes(s): 6.9, Count: 5, TPM: 43.7, Sum(ms): 2208, Avg(ms): 441, 90th(ms): 512, 99th(ms): 512, 99.9th(ms): 512
[Current] STOCK_LEVEL - Takes(s): 4.4, Count: 1, TPM: 13.8, Sum(ms): 224, Avg(ms): 224, 90th(ms): 256, 99th(ms): 256, 99.9th(ms): 256
...
```

テストが終了すると、テストの概要結果が印刷されます。

```text
[Summary] DELIVERY - Takes(s): 455.2, Count: 32, TPM: 4.2, Sum(ms): 44376, Avg(ms): 1386, 90th(ms): 2000, 99th(ms): 4000, 99.9th(ms): 4000
[Summary] DELIVERY_ERR - Takes(s): 455.2, Count: 1, TPM: 0.1, Sum(ms): 953, Avg(ms): 953, 90th(ms): 1000, 99th(ms): 1000, 99.9th(ms): 1000
[Summary] NEW_ORDER - Takes(s): 487.8, Count: 314, TPM: 38.6, Sum(ms): 282377, Avg(ms): 899, 90th(ms): 1500, 99th(ms): 1500, 99.9th(ms): 1500
[Summary] ORDER_STATUS - Takes(s): 484.6, Count: 29, TPM: 3.6, Sum(ms): 8423, Avg(ms): 290, 90th(ms): 512, 99th(ms): 1500, 99.9th(ms): 1500
[Summary] PAYMENT - Takes(s): 490.1, Count: 321, TPM: 39.3, Sum(ms): 144708, Avg(ms): 450, 90th(ms): 512, 99th(ms): 1000, 99.9th(ms): 1500
[Summary] STOCK_LEVEL - Takes(s): 487.6, Count: 41, TPM: 5.0, Sum(ms): 9318, Avg(ms): 227, 90th(ms): 512, 99th(ms): 1000, 99.9th(ms): 1000
```

テストが完了したら、 `tiup bench tpcc -H 172.16.5.140 -P 4000 -D tpcc --warehouses 4 check`コマンドを実行してデータの正確性を検証できます。

## テストデータをクリーンアップする {#clean-up-test-data}

テスト データをクリーンアップするには、次のコマンドを実行します。

```shell
tiup bench tpcc -H 172.16.5.140 -P 4000 -D tpcc --warehouses 4 cleanup
```
