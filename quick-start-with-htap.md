---
title: Quick Start with TiDB HTAP
summary: TiDB HTAPをすぐに使い始める方法を学びます。
---

# TiDB HTAPのクイックスタート {#quick-start-with-tidb-htap}

このガイドでは、TiDB のハイブリッド トランザクションおよび分析処理 (HTAP) のワンストップ ソリューションを最も簡単に使い始める方法について説明します。

> **注記：**
>
> このガイドで紹介する手順は、テスト環境での迅速な開始のみを目的としています。本番環境では、 [HTAPを探索する](/explore-htap.md)推奨します。

## 基本概念 {#basic-concepts}

TiDB HTAP を使用する前に、 [TiKV](/tikv-overview.md) 、TiDB オンライン トランザクション処理 (OLTP) 用の行ベースのストレージ エンジン、および[TiFlash](/tiflash/tiflash-overview.md) 、TiDB オンライン分析処理 (OLAP) 用の列ベースのstoragestorageに関する基本的な知識が必要です。

-   HTAPのストレージエンジン：HTAPでは、行ベースstorageエンジンと列指向storageエンジンが共存します。どちらのstorageエンジンもデータを自動的に複製し、強力な一貫性を維持できます。行ベースstorageエンジンはOLTPパフォーマンスを最適化し、列指向storageエンジンはOLAPパフォーマンスを最適化します。
-   HTAP のデータ一貫性: 分散型トランザクション キー値データベースである TiKV は、 ACID準拠のトランザクション インターフェイスを提供し、 [Raftコンセンサスアルゴリズム](https://raft.github.io/raft.pdf)の実装により複数のレプリカ間のデータ一貫性と高可用性を保証します。TiKV の列指向storage拡張機能であるTiFlash は、 Raft Learnerコンセンサス アルゴリズムに従って TiKV からデータをリアルタイムで複製し、TiKV とTiFlash間でデータの強力な一貫性を保証します。
-   HTAP のデータ分離: HTAP リソース分離の問題を解決するために、必要に応じて TiKV とTiFlash を異なるマシンに展開できます。
-   MPPコンピューティングエンジン： [MPP](/tiflash/use-tiflash-mpp-mode.md#control-whether-to-select-the-mpp-mode)は、TiDB 5.0以降TiFlashエンジンによって提供される分散コンピューティングフレームワークであり、ノード間のデータ交換を可能にし、高性能かつ高スループットのSQLアルゴリズムを提供します。MPPモードでは、分析クエリの実行時間を大幅に短縮できます。

## 手順 {#steps}

このドキュメントでは、 [TPC-H](http://www.tpc.org/tpch/)データセットのサンプルテーブルをクエリすることで、 TiDB HTAPの利便性と高いパフォーマンスを体験できます。TPC-Hは、大量のデータと高度な複雑さを扱うビジネス指向のアドホッククエリスイートで構成される、広く使用されている意思決定支援ベンチマークです。TPC-Hを使用した22の完全なSQLクエリを体験するには、クエリステートメントとデータの生成方法については、 [tidb-benchリポジトリ](https://github.com/pingcap/tidb-bench/tree/master/tpch/queries)または[TPC-H](http://www.tpc.org/tpch/)ご覧ください。

### ステップ1. ローカルテスト環境をデプロイ {#step-1-deploy-a-local-test-environment}

TiDB HTAPを使用する前に、 [TiDBセルフマネージドのクイックスタート](/quick-start-with-tidb.md)の手順に従ってローカル テスト環境を準備し、次のコマンドを実行して TiDB クラスターをデプロイします。

```shell
tiup playground
```

> **注記：**
>
> `tiup playground`コマンドはクイック スタート専用であり、本番用ではありません。

### ステップ2. テストデータの準備 {#step-2-prepare-test-data}

以下の手順で、 TiDB HTAPを使用するためのテストデータとして[TPC-H](http://www.tpc.org/tpch/)データセットを作成します。TPC-H にご興味がある場合は、 [一般的な実装ガイドライン](http://tpc.org/tpc_documents_current_versions/pdf/tpc-h_v3.0.0.pdf)ご覧ください。

> **注記：**
>
> 既存のデータを分析クエリに使用する場合は、 [データをTiDBに移行する](/migration-overview.md)実行できます。独自のテスト データを設計および作成する場合は、SQL ステートメントを実行するか、関連ツールを使用して作成できます。

1.  次のコマンドを実行して、テスト データ生成ツールをインストールします。

    ```shell
    tiup install bench
    ```

2.  次のコマンドを実行してテスト データを生成します。

    ```shell
    tiup bench tpch --sf=1 prepare
    ```

    このコマンドの出力に`Finished`表示される場合は、データが作成されたことを示します。

3.  生成されたデータを表示するには、次の SQL ステートメントを実行します。

    ```sql
    SELECT
      CONCAT(table_schema,'.',table_name) AS 'Table Name',
      table_rows AS 'Number of Rows',
      FORMAT_BYTES(data_length) AS 'Data Size',
      FORMAT_BYTES(index_length) AS 'Index Size',
      FORMAT_BYTES(data_length+index_length) AS'Total'
    FROM
      information_schema.TABLES
    WHERE
      table_schema='test';
    ```

    出力からわかるように、合計 8 つのテーブルが作成され、最大のテーブルには 650 万行があります (データはランダムに生成されるため、ツールによって作成される行数は実際の SQL クエリ結果によって異なります)。

    ```sql
    +---------------+----------------+-----------+------------+-----------+
    |  Table Name   | Number of Rows | Data Size | Index Size |   Total   |
    +---------------+----------------+-----------+------------+-----------+
    | test.nation   |             25 | 2.44 KiB  | 0 bytes    | 2.44 KiB  |
    | test.region   |              5 | 416 bytes | 0 bytes    | 416 bytes |
    | test.part     |         200000 | 25.07 MiB | 0 bytes    | 25.07 MiB |
    | test.supplier |          10000 | 1.45 MiB  | 0 bytes    | 1.45 MiB  |
    | test.partsupp |         800000 | 120.17 MiB| 12.21 MiB  | 132.38 MiB|
    | test.customer |         150000 | 24.77 MiB | 0 bytes    | 24.77 MiB |
    | test.orders   |        1527648 | 174.40 MiB| 0 bytes    | 174.40 MiB|
    | test.lineitem |        6491711 | 849.07 MiB| 99.06 MiB  | 948.13 MiB|
    +---------------+----------------+-----------+------------+-----------+
    8 rows in set (0.06 sec)
    ```

    これは商用発注システムのデータベースです。テーブル`test.nation`は国に関する情報、テーブル`test.region`は地域に関する情報、テーブル`test.part`は部品に関する情報、テーブル`test.supplier`はサプライヤーに関する情報、テーブル`test.partsupp`はサプライヤーの部品に関する情報、テーブル`test.customer`は顧客に関する情報、テーブル`test.customer`は注文に関する情報、テーブル`test.lineitem`はオンライン商品に関する情報を示しています。

### ステップ3. 行ベースのstorageエンジンでデータをクエリする {#step-3-query-data-with-the-row-based-storage-engine}

行ベースのstorageエンジンのみを使用した TiDB のパフォーマンスを確認するには、次の SQL ステートメントを実行します。

```sql
USE test;
SELECT
    l_orderkey,
    SUM(
        l_extendedprice * (1 - l_discount)
    ) AS revenue,
    o_orderdate,
    o_shippriority
FROM
    customer,
    orders,
    lineitem
WHERE
    c_mktsegment = 'BUILDING'
AND c_custkey = o_custkey
AND l_orderkey = o_orderkey
AND o_orderdate < DATE '1996-01-01'
AND l_shipdate > DATE '1996-02-01'
GROUP BY
    l_orderkey,
    o_orderdate,
    o_shippriority
ORDER BY
    revenue DESC,
    o_orderdate
limit 10;
```

これは配送優先度クエリで、指定日までに発送されていない、最も収益の高い注文の優先度と潜在収益を取得します。潜在収益は`l_extendedprice * (1-l_discount)`の合計として定義されます。注文は収益の降順でリストされます。この例では、このクエリは潜在収益が上位10件の未発送注文をリストします。

### ステップ4. テストデータを列指向storageエンジンに複製する {#step-4-replicate-the-test-data-to-the-columnar-storage-engine}

TiFlashを導入した後、TiKV はデータをすぐにTiFlashに複製しません。複製するテーブルを指定するには、TiDB の MySQL クライアントで以下の DDL 文を実行する必要があります。その後、TiDB は指定されたレプリカをTiFlashに作成します。

```sql
ALTER TABLE test.customer SET TIFLASH REPLICA 1;
ALTER TABLE test.orders SET TIFLASH REPLICA 1;
ALTER TABLE test.lineitem SET TIFLASH REPLICA 1;
```

特定のテーブルのレプリケーション ステータスを確認するには、次のステートメントを実行します。

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'test' and TABLE_NAME = 'customer';
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'test' and TABLE_NAME = 'orders';
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'test' and TABLE_NAME = 'lineitem';
```

上記のステートメントの結果:

-   `AVAILABLE` 、特定のテーブルのTiFlashレプリカが利用可能かどうかを示します。2 `1`利用可能、 `0`利用不可を意味します。6 フィールドが`AVAILABLE` `1`なると、このステータスは変更されなくなります。
-   `PROGRESS`レプリケーションの進行状況を表します。値は0.0～1.0の範囲です。1はTiFlashレプリカのレプリケーションの進行状況が完了したことを意味します。

### ステップ5. HTAPを使用してデータをより速く分析する {#step-5-analyze-data-faster-using-htap}

もう一度[ステップ3](#step-3-query-data-with-the-row-based-storage-engine)の SQL 文を実行すると、 TiDB HTAPのパフォーマンスを確認できます。

TiFlashレプリカを持つテーブルの場合、TiDBオプティマイザーはコスト見積もりに基づいてTiFlashレプリカを使用するかどうかを自動的に決定します。TiFlashTiFlashが選択されているかどうかを確認するには、 `desc`または`explain analyze`ステートメントを使用します。例：

```sql
USE test;
EXPLAIN ANALYZE SELECT
    l_orderkey,
    SUM(
        l_extendedprice * (1 - l_discount)
    ) AS revenue,
    o_orderdate,
    o_shippriority
FROM
    customer,
    orders,
    lineitem
WHERE
    c_mktsegment = 'BUILDING'
AND c_custkey = o_custkey
AND l_orderkey = o_orderkey
AND o_orderdate < DATE '1996-01-01'
AND l_shipdate > DATE '1996-02-01'
GROUP BY
    l_orderkey,
    o_orderdate,
    o_shippriority
ORDER BY
    revenue DESC,
    o_orderdate
limit 10;
```

`EXPLAIN`ステートメントの結果に`ExchangeSender`と`ExchangeReceiver`演算子が表示されている場合は、MPP モードが有効になっていることを示します。

さらに、クエリ全体の各部分をTiFlashエンジンのみを使用して計算するように指定することもできます。詳細については、 [TiDBを使用してTiFlashレプリカを読み取る](/tiflash/use-tidb-to-read-tiflash.md)参照してください。

これら 2 つの方法のクエリ結果とクエリ パフォーマンスを比較できます。

## 次は何？ {#what-s-next}

-   [TiDB HTAPのアーキテクチャ](/tiflash/tiflash-overview.md#architecture)
-   [HTAPを探索する](/explore-htap.md)
-   [TiFlashを使用する](/tiflash/tiflash-overview.md#use-tiflash)
