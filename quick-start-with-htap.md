---
title: Quick start with HTAP
summary: TiDB HTAPをすぐに使い始める方法を学びます。
---

# TiDB HTAPクイック スタート ガイド {#quick-start-guide-for-tidb-htap}

このガイドでは、TiDB のハイブリッド トランザクションおよび分析処理 (HTAP) のワンストップ ソリューションを最も迅速に開始する方法について説明します。

> **注記：**
>
> このガイドで提供される手順は、テスト環境での迅速な開始のみを目的としています。本番環境では、 [HTAPを探索する](/explore-htap.md)推奨されます。

## 基本概念 {#basic-concepts}

TiDB HTAPを使用する前に、 [ティクヴ](/tikv-overview.md) （TiDB オンライン トランザクション処理 (OLTP) 用の行ベースのstorageエンジン）と[TiFlash](/tiflash/tiflash-overview.md) （TiDB オンライン分析処理 (OLAP) 用の列ベースのstorageエンジン）に関する基本的な知識が必要です。

-   HTAP のストレージ エンジン: HTAP には、行ベースのstorageエンジンと列ベースのstorageエンジンが共存します。両方のstorageエンジンは、データを自動的に複製し、強力な一貫性を維持できます。行ベースのstorageエンジンは OLTP パフォーマンスを最適化し、列ベースのstorageエンジンは OLAP パフォーマンスを最適化します。
-   HTAP のデータ一貫性: 分散型トランザクション キー値データベースとして、TiKV はACID準拠のトランザクション インターフェイスを提供し、 [Raftコンセンサスアルゴリズム](https://raft.github.io/raft.pdf)の実装により複数のレプリカ間のデータ一貫性と高可用性を保証します。TiKV の列指向storage拡張機能として、 TiFlash はRaft Learnerコンセンサス アルゴリズムに従って TiKV からデータをリアルタイムで複製し、TiKV とTiFlash間でデータの強い一貫性を保証します。
-   HTAP のデータ分離: HTAP リソース分離の問題を解決するために、必要に応じて TiKV とTiFlash を異なるマシンに展開できます。
-   MPP コンピューティング エンジン: [マルチレベル](/tiflash/use-tiflash-mpp-mode.md#control-whether-to-select-the-mpp-mode) 、TiDB 5.0 以降TiFlashエンジンによって提供される分散コンピューティング フレームワークであり、ノード間のデータ交換を可能にし、高性能で高スループットの SQL アルゴリズムを提供します。MPP モードでは、分析クエリの実行時間を大幅に短縮できます。

## 手順 {#steps}

このドキュメントでは、 [TPC-H](http://www.tpc.org/tpch/)データセット内のサンプル テーブルをクエリすることで、 TiDB HTAPの利便性と高いパフォーマンスを体験できます。TPC-H は、大量のデータと高度な複雑さを伴うビジネス指向のアドホック クエリのスイートで構成される、一般的な意思決定サポート ベンチマークです。TPC-H を使用して 22 の完全な SQL クエリを体験するには、クエリ ステートメントとデータを生成する手順について[tidb-bench リポジトリ](https://github.com/pingcap/tidb-bench/tree/master/tpch/queries)または[TPC-H](http://www.tpc.org/tpch/)を参照してください。

### ステップ1. ローカルテスト環境をデプロイ {#step-1-deploy-a-local-test-environment}

TiDB HTAPを使用する前に、 [TiDB データベース プラットフォームのクイック スタート ガイド](/quick-start-with-tidb.md)の手順に従ってローカル テスト環境を準備し、次のコマンドを実行して TiDB クラスターをデプロイします。

```shell
tiup playground
```

> **注記：**
>
> `tiup playground`コマンドはクイック スタート専用であり、本番用ではありません。

### ステップ2. テストデータを準備する {#step-2-prepare-test-data}

以下の手順では、 TiDB HTAPを使用するためのテストデータとして[TPC-H](http://www.tpc.org/tpch/)データセットを作成します。TPC-H に興味のある方は[一般的な実装ガイドライン](http://tpc.org/tpc_documents_current_versions/pdf/tpc-h_v3.0.0.pdf)を参照してください。

> **注記：**
>
> 分析クエリに既存のデータを使用する場合は、 [データをTiDBに移行する](/migration-overview.md)実行できます。独自のテスト データを設計および作成する場合は、SQL ステートメントを実行するか、関連ツールを使用して作成できます。

1.  次のコマンドを実行して、テスト データ生成ツールをインストールします。

    ```shell
    tiup install bench
    ```

2.  次のコマンドを実行してテスト データを生成します。

    ```shell
    tiup bench tpch --sf=1 prepare
    ```

    このコマンドの出力に`Finished`表示された場合、データが作成されたことを示します。

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

    出力からわかるように、合計 8 つのテーブルが作成され、最大のテーブルには 650 万行があります (データはランダムに生成されるため、ツールによって作成される行数は実際の SQL クエリの結果によって異なります)。

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

    これは商用発注システムのデータベースです。テーブル`test.nation`は国に関する情報、テーブル`test.region`は地域に関する情報、テーブル`test.part`は部品に関する情報、テーブル`test.supplier`は仕入先に関する情報、テーブル`test.partsupp`は仕入先の部品に関する情報、テーブル`test.customer`は顧客に関する情報、テーブル`test.customer`は注文に関する情報、テーブル`test.lineitem`はオンライン商品に関する情報を示しています。

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

これは出荷優先度クエリであり、指定された日付までに出荷されていない、最も収益の高い注文の優先度と潜在的収益を提供します。潜在的収益は`l_extendedprice * (1-l_discount)`の合計として定義されます。注文は収益の降順でリストされます。この例では、このクエリは、潜在的なクエリ収益が上位 10 件の未出荷注文をリストします。

### ステップ4. テストデータを列指向storageエンジンに複製する {#step-4-replicate-the-test-data-to-the-columnar-storage-engine}

TiFlashがデプロイされた後、TiKV はデータをすぐにTiFlashに複製しません。複製する必要があるテーブルを指定するには、TiDB の MySQL クライアントで次の DDL ステートメントを実行する必要があります。その後、TiDB はそれに応じて指定されたレプリカをTiFlashに作成します。

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

-   `AVAILABLE` 、特定のテーブルのTiFlashレプリカが使用可能かどうかを示します。 `1`は使用可能、 `0`使用不可を意味します。 `AVAILABLE`フィールドが`1`になると、このステータスは変更されなくなります。
-   `PROGRESS`レプリケーションの進行状況を意味します。値は 0.0 ～ 1.0 の間です。1 はTiFlashレプリカのレプリケーションの進行状況が完了したことを意味します。

### ステップ5. HTAPを使用してデータをより速く分析する {#step-5-analyze-data-faster-using-htap}

[ステップ3](#step-3-query-data-with-the-row-based-storage-engine) SQL 文を再度実行すると、 TiDB HTAPのパフォーマンスを確認できます。

TiFlashレプリカを持つテーブルの場合、TiDB オプティマイザーはコスト見積もりに基づいてTiFlashレプリカを使用するかどうかを自動的に決定します。TiFlash レプリカが選択されているかどうかを確認するには、 `desc`または`explain analyze`ステートメントを使用できます。TiFlash:

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

`EXPLAIN`ステートメントの結果に`ExchangeSender`および`ExchangeReceiver`演算子が表示される場合、MPP モードが有効になっていることを示します。

さらに、クエリ全体の各部分をTiFlashエンジンのみを使用して計算するように指定することもできます。詳細については、 [TiDBを使用してTiFlashレプリカを読み取る](/tiflash/use-tidb-to-read-tiflash.md)参照してください。

これら 2 つの方法のクエリ結果とクエリ パフォーマンスを比較できます。

## 次は何ですか {#what-s-next}

-   [TiDB HTAPのアーキテクチャ](/tiflash/tiflash-overview.md#architecture)
-   [HTAPを探索する](/explore-htap.md)
-   [TiFlashを使用する](/tiflash/tiflash-overview.md#use-tiflash)
