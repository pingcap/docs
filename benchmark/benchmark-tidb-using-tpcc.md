---
title: How to Run TPC-C Test on TiDB
---

# TiDBでTPC-Cテストを実行する方法 {#how-to-run-tpc-c-test-on-tidb}

このドキュメントでは、 [TPC-C](http://www.tpc.org/tpcc/)を使用してTiDBをテストする方法について説明します。

TPC-Cは、オンライントランザクション処理（OLTP）ベンチマークです。これは、異なるタイプの次の5つのトランザクションを含む商品販売モデルを使用してOLTPシステムをテストします。

-   新規注文
-   支払い
-   注文の状況
-   配達
-   在庫量

## 準備 {#prepare}

テストの前に、TPC-Cベンチマークはデータベースの初期状態を指定します。これは、データベースでのデータ生成のルールです。 `ITEM`のテーブルには固定数の100,000アイテムが含まれていますが、倉庫の数は調整できます。 `WAREHOUSE`のテーブルにWレコードがある場合、次のようになります。

-   `STOCK`のテーブルにはW*100,000レコードがあります（各倉庫は100,000アイテムの在庫データに対応します）
-   `DISTRICT`のテーブルにはW*10レコードがあります（各倉庫は10の地区にサービスを提供します）
-   `CUSTOMER`のテーブルにはW*10 * 3,000レコードがあります（各地区には3,000人の顧客がいます）
-   `HISTORY`のテーブルにはW*10 * 3,000レコードがあります（各顧客には1つのトランザクション履歴があります）
-   `ORDER`のテーブルにはW*10 * 3,000レコードがあります（各地区には3,000の注文があり、最後に生成された900の注文が`NEW-ORDER`のテーブルに追加されます。各注文はランダムに5〜15のORDER-LINEレコードを生成します。

このドキュメントでは、テストでは、TiDBをテストするための例として1,000のウェアハウスを使用します。

TPC-Cは、tpmC（1分あたりのトランザクション数）を使用して、最大認定スループット（MQTh、最大認定スループット）を測定します。トランザクションはNewOrderトランザクションであり、最終的な測定単位は1分あたりに処理された新しい注文の数です。

このドキュメントのテストは、 [go-tpc](https://github.com/pingcap/go-tpc)に基づいて実装されています。 [TiUP](/tiup/tiup-overview.md)のコマンドを使用してテストプログラムをダウンロードできます。

{{< copyable "" >}}

```shell
tiup install bench
```

TiUPベンチコンポーネントの詳細な使用法については、 [TiUPベンチ](/tiup/tiup-bench.md)を参照してください。

## データを読み込む {#load-data}

**データのロードは通常、TPC-Cテスト全体の中で最も時間と問題のある段階です。**このセクションでは、データをロードするための次のコマンドを提供します。

シェルで次のTiUPコマンドを実行します。

{{< copyable "" >}}

```shell
tiup bench tpcc -H 172.16.5.140 -P 4000 -D tpcc --warehouses 1000 prepare
```

さまざまなマシン構成に基づいて、このロードプロセスには数時間かかる場合があります。クラスタサイズが小さい場合は、小さい`WAREHOUSE`の値をテストに使用できます。

データがロードされた後、 `tiup bench tpcc -H 172.16.5.140 -P 4000 -D tpcc --warehouses 4 check`コマンドを実行してデータの正確さを検証できます。

## テストを実行します {#run-the-test}

次のコマンドを実行して、テストを実行します。

{{< copyable "" >}}

```shell
tiup bench tpcc -H 172.16.5.140 -P 4000 -D tpcc --warehouses 1000 run
```

テスト中、テスト結果はコンソールに継続的に印刷されます。

```text
[Current] NEW_ORDER - Takes(s): 4.6, Count: 5, TPM: 65.5, Sum(ms): 4604, Avg(ms): 920, 90th(ms): 1500, 99th(ms): 1500, 99.9th(ms): 1500
[Current] ORDER_STATUS - Takes(s): 1.4, Count: 1, TPM: 42.2, Sum(ms): 256, Avg(ms): 256, 90th(ms): 256, 99th(ms): 256, 99.9th(ms): 256
[Current] PAYMENT - Takes(s): 6.9, Count: 5, TPM: 43.7, Sum(ms): 2208, Avg(ms): 441, 90th(ms): 512, 99th(ms): 512, 99.9th(ms): 512
[Current] STOCK_LEVEL - Takes(s): 4.4, Count: 1, TPM: 13.8, Sum(ms): 224, Avg(ms): 224, 90th(ms): 256, 99th(ms): 256, 99.9th(ms): 256
...
```

テストが終了すると、テストの概要結果が出力されます。

```text
[Summary] DELIVERY - Takes(s): 455.2, Count: 32, TPM: 4.2, Sum(ms): 44376, Avg(ms): 1386, 90th(ms): 2000, 99th(ms): 4000, 99.9th(ms): 4000
[Summary] DELIVERY_ERR - Takes(s): 455.2, Count: 1, TPM: 0.1, Sum(ms): 953, Avg(ms): 953, 90th(ms): 1000, 99th(ms): 1000, 99.9th(ms): 1000
[Summary] NEW_ORDER - Takes(s): 487.8, Count: 314, TPM: 38.6, Sum(ms): 282377, Avg(ms): 899, 90th(ms): 1500, 99th(ms): 1500, 99.9th(ms): 1500
[Summary] ORDER_STATUS - Takes(s): 484.6, Count: 29, TPM: 3.6, Sum(ms): 8423, Avg(ms): 290, 90th(ms): 512, 99th(ms): 1500, 99.9th(ms): 1500
[Summary] PAYMENT - Takes(s): 490.1, Count: 321, TPM: 39.3, Sum(ms): 144708, Avg(ms): 450, 90th(ms): 512, 99th(ms): 1000, 99.9th(ms): 1500
[Summary] STOCK_LEVEL - Takes(s): 487.6, Count: 41, TPM: 5.0, Sum(ms): 9318, Avg(ms): 227, 90th(ms): 512, 99th(ms): 1000, 99.9th(ms): 1000
```

テストが終了したら、 `tiup bench tpcc -H 172.16.5.140 -P 4000 -D tpcc --warehouses 4 check`コマンドを実行してデータの正確性を検証できます。

## テストデータをクリーンアップする {#clean-up-test-data}

次のコマンドを実行して、テストデータをクリーンアップします。

{{< copyable "" >}}

```shell
tiup bench tpcc -H 172.16.5.140 -P 4000 -D tpcc --warehouses 4 cleanup
```
