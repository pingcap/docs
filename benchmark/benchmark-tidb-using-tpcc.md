---
title: How to Run TPC-C Test on TiDB
---

# TiDB で TPC-C テストを実行する方法 {#how-to-run-tpc-c-test-on-tidb}

このドキュメントでは、 [TPC-C](http://www.tpc.org/tpcc/)使用して TiDB をテストする方法について説明します。

TPC-C は、オンライン トランザクション処理 (OLTP) のベンチマークです。次の 5 つの異なる種類のトランザクションを含む商品販売モデルを使用して、OLTP システムをテストします。

-   新規注文
-   支払い
-   注文の状況
-   配達
-   在庫量

## 準備 {#prepare}

テストの前に、TPC-C Benchmark はデータベースの初期状態を指定します。これは、データベース内のデータ生成のルールです。 `ITEM`テーブルには 100,000 アイテムの固定数が含まれていますが、倉庫の数は調整できます。 `WAREHOUSE`テーブルに W 個のレコードがある場合:

-   `STOCK`テーブルにW×10万レコード（各倉庫が10万アイテムの在庫データに相当）
-   `DISTRICT`テーブルには W * 10 レコードがあります (各倉庫は 10 地区にサービスを提供します)
-   `CUSTOMER`テーブルには W * 10 * 3,000 レコードがあります (各地区には 3,000 人の顧客がいます)
-   `HISTORY`テーブルには W * 10 * 3,000 レコードがあります (各顧客には 1 つの取引履歴があります)
-   `ORDER`テーブルには W * 10 * 3,000 レコードがあります (各地区には 3,000 の注文があり、最後に生成された 900 の注文が`NEW-ORDER`テーブルに追加されます。各注文はランダムに 5 ~ 15 の ORDER-LINE レコードを生成します。

このドキュメントでは、テストでは TiDB をテストするための例として 1,000 のウェアハウスを使用します。

TPC-C は tpmC (1 分あたりのトランザクション数) を使用して、認定された最大スループット (MQTh、認定された最大スループット) を測定します。トランザクションは NewOrder トランザクションであり、最終的な測定単位は 1 分あたりに処理される新しい注文の数です。

このドキュメントのテストは[ゴーtpc](https://github.com/pingcap/go-tpc)に基づいて実装されています。 [TiUP](/tiup/tiup-overview.md)コマンドを使用して、テスト プログラムをダウンロードできます。

{{< copyable "" >}}

```shell
tiup install bench
```

TiUP Benchコンポーネントの詳細な使用方法については、 [TiUPベンチ](/tiup/tiup-bench.md)を参照してください。

172.16.5.140 と 172.16.5.141 に配置された 2 つの TiDB サーバーを使用して TiDB クラスターをデプロイし、両方のサーバーがポート 4000 でリッスンしているとします。次の手順で TPC-C テストを実行できます。

## データを読み込む {#load-data}

**通常、データのロードは、TPC-C テスト全体で最も時間がかかり、問題のある段階です。**このセクションでは、データをロードする次のコマンドを提供します。

シェルで次のTiUPコマンドを実行します。

{{< copyable "" >}}

```shell
tiup bench tpcc -H 172.16.5.140,172.16.5.141 -P 4000 -D tpcc --warehouses 1000 --threads 20 prepare
```

さまざまなマシン構成に基づいて、このロード プロセスには数時間かかる場合があります。クラスタ サイズが小さい場合は、テストに小さい`WAREHOUSE`の値を使用できます。

データがロードされたら、 `tiup bench tpcc -H 172.16.5.140 -P 4000 -D tpcc --warehouses 4 check`コマンドを実行してデータの正確性を検証できます。

## テストを実行する {#run-the-test}

次のコマンドを実行して、テストを実行します。

{{< copyable "" >}}

```shell
tiup bench tpcc -H 172.16.5.140,172.16.5.141 -P 4000 -D tpcc --warehouses 1000 --threads 100 --time 10m run
```

テスト中、テスト結果がコンソールに継続的に出力されます。

```text
[Current] NEW_ORDER - Takes(s): 4.6, Count: 5, TPM: 65.5, Sum(ms): 4604, Avg(ms): 920, 90th(ms): 1500, 99th(ms): 1500, 99.9th(ms): 1500
[Current] ORDER_STATUS - Takes(s): 1.4, Count: 1, TPM: 42.2, Sum(ms): 256, Avg(ms): 256, 90th(ms): 256, 99th(ms): 256, 99.9th(ms): 256
[Current] PAYMENT - Takes(s): 6.9, Count: 5, TPM: 43.7, Sum(ms): 2208, Avg(ms): 441, 90th(ms): 512, 99th(ms): 512, 99.9th(ms): 512
[Current] STOCK_LEVEL - Takes(s): 4.4, Count: 1, TPM: 13.8, Sum(ms): 224, Avg(ms): 224, 90th(ms): 256, 99th(ms): 256, 99.9th(ms): 256
...
```

テストが終了すると、テストの要約結果が出力されます。

```text
[Summary] DELIVERY - Takes(s): 455.2, Count: 32, TPM: 4.2, Sum(ms): 44376, Avg(ms): 1386, 90th(ms): 2000, 99th(ms): 4000, 99.9th(ms): 4000
[Summary] DELIVERY_ERR - Takes(s): 455.2, Count: 1, TPM: 0.1, Sum(ms): 953, Avg(ms): 953, 90th(ms): 1000, 99th(ms): 1000, 99.9th(ms): 1000
[Summary] NEW_ORDER - Takes(s): 487.8, Count: 314, TPM: 38.6, Sum(ms): 282377, Avg(ms): 899, 90th(ms): 1500, 99th(ms): 1500, 99.9th(ms): 1500
[Summary] ORDER_STATUS - Takes(s): 484.6, Count: 29, TPM: 3.6, Sum(ms): 8423, Avg(ms): 290, 90th(ms): 512, 99th(ms): 1500, 99.9th(ms): 1500
[Summary] PAYMENT - Takes(s): 490.1, Count: 321, TPM: 39.3, Sum(ms): 144708, Avg(ms): 450, 90th(ms): 512, 99th(ms): 1000, 99.9th(ms): 1500
[Summary] STOCK_LEVEL - Takes(s): 487.6, Count: 41, TPM: 5.0, Sum(ms): 9318, Avg(ms): 227, 90th(ms): 512, 99th(ms): 1000, 99.9th(ms): 1000
```

テストが終了したら、 `tiup bench tpcc -H 172.16.5.140 -P 4000 -D tpcc --warehouses 4 check`コマンドを実行してデータの正確性を検証できます。

## テストデータのクリーンアップ {#clean-up-test-data}

次のコマンドを実行して、テスト データをクリーンアップします。

{{< copyable "" >}}

```shell
tiup bench tpcc -H 172.16.5.140 -P 4000 -D tpcc --warehouses 4 cleanup
```
