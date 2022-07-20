---
title: Quick start with HTAP
summary: Learn how to quickly get started with the TiDB HTAP.
---

# TiDB HTAPのクイックスタートガイド {#quick-start-guide-for-tidb-htap}

このガイドでは、TiDBのハイブリッドトランザクションおよび分析処理（HTAP）のワンストップソリューションを開始するための最も簡単な方法について説明します。

> **ノート：**
>
> このガイドに記載されている手順は、テスト環境でのクイックスタートのみを目的としています。実稼働環境では、 [HTAPを探索する](/explore-htap.md)をお勧めします。

## 基本概念 {#basic-concepts}

TiDB HTAPを使用する前に、TiDBオンライントランザクション処理（OLTP）用の行ベースのストレージエンジンである[TiKV](/tikv-overview.md) 、およびTiDBオンライン分析処理（OLAP）用の列型ストレージエンジンである[TiFlash](/tiflash/tiflash-overview.md)に関する基本的な知識が必要です。

-   HTAPのストレージエンジン：HTAPでは、行ベースのストレージエンジンと列型ストレージエンジンが共存します。どちらのストレージエンジンもデータを自動的に複製し、強力な一貫性を保つことができます。行ベースのストレージエンジンはOLTPパフォーマンスを最適化し、列型ストレージエンジンはOLAPパフォーマンスを最適化します。
-   HTAPのデータ整合性：分散型およびトランザクション型のKey-Valueデータベースとして、TiKVはACID準拠のトランザクション型インターフェースを提供し、 [Raftコンセンサスアルゴリズム](https://raft.github.io/raft.pdf)の実装により、複数のレプリカ間のデータ整合性と高可用性を保証します。 TiKVの列型ストレージ拡張として、TiFlashはRaft Learnerコンセンサスアルゴリズムに従ってリアルタイムでTiKVからデータを複製します。これにより、TiKVとTiFlashの間でデータの一貫性が確保されます。
-   HTAPのデータ分離：TiKVとTiFlashは、HTAPリソース分離の問題を解決するために、必要に応じて異なるマシンに展開できます。
-   MPPコンピューティングエンジン： [MPP](/tiflash/use-tiflash-mpp-mode.md#control-whether-to-select-the-mpp-mode)は、TiDB 5.0以降のTiFlashエンジンによって提供される分散コンピューティングフレームワークであり、ノード間のデータ交換を可能にし、高性能、高スループットのSQLアルゴリズムを提供します。 MPPモードでは、分析クエリの実行時間を大幅に短縮できます。

## 手順 {#steps}

このドキュメントでは、 [TPC-H](http://www.tpc.org/tpch/)のデータセットのサンプルテーブルをクエリすることで、 TiDB HTAPの便利さと高性能を体験できます。 TPC-Hは、大量のデータと高度な複雑さを備えた一連のビジネス指向のアドホッククエリで構成される一般的な意思決定支援ベンチマークです。 TPC-Hを使用して22の完全なSQLクエリを体験するには、クエリステートメントとデータを生成する方法について[tidb-ベンチリポジトリ](https://github.com/pingcap/tidb-bench/tree/master/tpch/queries)または[TPC-H](http://www.tpc.org/tpch/)にアクセスしてください。

### 手順1.ローカルテスト環境をデプロイする {#step-1-deploy-a-local-test-environment}

TiDB HTAPを使用する前に、 [TiDBデータベースプラットフォームのクイックスタートガイド](/quick-start-with-tidb.md)の手順に従ってローカルテスト環境を準備し、次のコマンドを実行してTiDBクラスタを展開します。

{{< copyable "" >}}

```shell
tiup playground
```

> **ノート：**
>
> `tiup playground`コマンドはクイックスタート専用であり、実動用ではありません。

### ステップ2.テストデータを準備する {#step-2-prepare-test-data}

次の手順では、 TiDB HTAPを使用するためのテストデータとして[TPC-H](http://www.tpc.org/tpch/)のデータセットを作成できます。 TPC-Hに興味がある場合は、 [一般的な実装ガイドライン](http://tpc.org/tpc_documents_current_versions/pdf/tpc-h_v3.0.0.pdf)を参照してください。

> **ノート：**
>
> 分析クエリに既存のデータを使用する場合は、 [データをTiDBに移行する](/migration-overview.md)を実行できます。独自のテストデータを設計および作成する場合は、SQLステートメントを実行するか、関連するツールを使用して作成できます。

1.  次のコマンドを実行して、テストデータ生成ツールをインストールします。

    {{< copyable "" >}}

    ```shell
    tiup install bench
    ```

2.  次のコマンドを実行して、テストデータを生成します。

    {{< copyable "" >}}

    ```shell
    tiup bench tpch --sf=1 prepare
    ```

    このコマンドの出力に`Finished`が表示されている場合は、データが作成されていることを示しています。

3.  次のSQLステートメントを実行して、生成されたデータを表示します。

    {{< copyable "" >}}

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

    出力からわかるように、合計8つのテーブルが作成され、最大のテーブルには650万行があります（データはランダムに生成されるため、ツールによって作成される行数は実際のSQLクエリ結果によって異なります）。

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

    これは、商用注文システムのデータベースです。ここで、 `test.nation`の表は国に関する情報を示し、 `test.region`の表は地域に関する情報を示し、 `test.part`の表は部品に関する情報を示し、 `test.supplier`の表はサプライヤーに関する情報を示し、 `test.partsupp`の表はサプライヤーの部品に関する情報を示します。 `test.customer`の表は顧客に関する情報を示し、 `test.customer`の表は注文に関する情報を示し、 `test.lineitem`の表はオンラインアイテムに関する情報を示します。

### 手順3.行ベースのストレージエンジンを使用してデータをクエリする {#step-3-query-data-with-the-row-based-storage-engine}

行ベースのストレージエンジンのみを使用したTiDBのパフォーマンスを知るには、次のSQLステートメントを実行します。

{{< copyable "" >}}

```sql
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

これは出荷優先度クエリであり、指定された日付より前に出荷されていない最高収益の注文の優先度と潜在的な収益を提供します。潜在的な収益は、 `l_extendedprice * (1-l_discount)`の合計として定義されます。注文は収益の降順で一覧表示されます。この例では、このクエリは、上位10に潜在的なクエリ収益がある未出荷の注文を一覧表示します。

### ステップ4.テストデータを列型ストレージエンジンに複製します {#step-4-replicate-the-test-data-to-the-columnar-storage-engine}

TiFlashが展開された後、TiKVはデータをTiFlashにすぐに複製しません。 TiDBのMySQLクライアントで次のDDLステートメントを実行して、レプリケートする必要のあるテーブルを指定する必要があります。その後、TiDBはそれに応じてTiFlashに指定されたレプリカを作成します。

{{< copyable "" >}}

```sql
ALTER TABLE test.customer SET TIFLASH REPLICA 1;
ALTER TABLE test.orders SET TIFLASH REPLICA 1;
ALTER TABLE test.lineitem SET TIFLASH REPLICA 1;
```

特定のテーブルのレプリケーションステータスを確認するには、次のステートメントを実行します。

{{< copyable "" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'test' and TABLE_NAME = 'customer';
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'test' and TABLE_NAME = 'orders';
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'test' and TABLE_NAME = 'lineitem';
```

上記のステートメントの結果：

-   `AVAILABLE`は、特定のテーブルのTiFlashレプリカが使用可能かどうかを示します。 `1`は利用可能、 `0`は利用不可を意味します。レプリカが使用可能になると、このステータスは変更されなくなります。 DDLステートメントを使用してレプリカの数を変更すると、レプリケーションステータスが再計算されます。
-   `PROGRESS`は、レプリケーションの進行状況を意味します。値は0.0から1.0の間です。 1は、少なくとも1つのレプリカが複製されることを意味します。

### ステップ5.HTAPを使用してデータをより高速に分析する {#step-5-analyze-data-faster-using-htap}

[ステップ3](#step-3-query-data-with-the-row-based-storage-engine)でSQLステートメントを再度実行すると、 TiDB HTAPのパフォーマンスを確認できます。

TiFlashレプリカを含むテーブルの場合、TiDBオプティマイザは、コスト見積もりに基づいてTiFlashレプリカを使用するかどうかを自動的に決定します。 TiFlashレプリカが選択されているかどうかを確認するには、 `desc`または`explain analyze`ステートメントを使用できます。例えば：

{{< copyable "" >}}

```sql
explain analyze SELECT
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

`EXPLAIN`ステートメントの結果に`ExchangeSender`および`ExchangeReceiver`のオペレーターが示されている場合は、MPPモードが有効になっていることを示しています。

さらに、クエリ全体の各部分がTiFlashエンジンのみを使用して計算されるように指定できます。詳細については、 [TiDBを使用してTiFlashレプリカを読み取る](/tiflash/use-tidb-to-read-tiflash.md)を参照してください。

これら2つの方法のクエリ結果とクエリパフォーマンスを比較できます。

## 次は何ですか {#what-s-next}

-   [TiDB HTAPのアーキテクチャ](/tiflash/tiflash-overview.md#architecture)
-   [HTAPを探索する](/explore-htap.md)
-   [TiFlashを使用する](/tiflash/tiflash-overview.md#use-tiflash)
