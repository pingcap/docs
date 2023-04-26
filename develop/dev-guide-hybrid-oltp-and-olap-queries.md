---
title: HTAP Queries
summary: Introduce the HTAP queries in TiDB.
---

# HTAP クエリ {#htap-queries}

HTAP は Hybrid Transactional and Analytical Processing の略です。従来、データベースは多くの場合、トランザクションまたは分析のシナリオ向けに設計されているため、データ プラットフォームは多くの場合、トランザクション処理と分析処理に分割する必要があり、データをトランザクション データベースから分析データベースに複製して、分析クエリに迅速に応答する必要があります。 TiDB データベースはトランザクション タスクと分析タスクの両方を実行できるため、データ プラットフォームの構築が大幅に簡素化され、ユーザーはより新しいデータを分析に使用できるようになります。

TiDB は、オンライン トランザクション処理 (OLTP) 用に行ベースのstorageエンジンである TiKV を使用し、オンライン分析処理 (OLAP) 用に列型storageエンジンであるTiFlashを使用します。 HTAP では、行ベースのstorageエンジンと列指向のstorageエンジンが共存します。どちらのstorageエンジンもデータを自動的にレプリケートし、強力な整合性を維持できます。行ベースのstorageエンジンは OLTP のパフォーマンスを最適化し、列ベースのstorageエンジンは OLAP のパフォーマンスを最適化します。

[テーブルを作成する](/develop/dev-guide-create-table.md#use-htap-capabilities)番目のセクションでは、TiDB の HTAP 機能を有効にする方法を紹介します。以下では、HTAP を使用してデータをより高速に分析する方法について説明します。

## データ準備 {#data-preparation}

開始する前に、さらにサンプル データをインポートできます[`tiup demo`コマンド経由](/develop/dev-guide-bookshop-schema-design.md#method-1-via-tiup-demo) 。例えば：

```shell
tiup demo bookshop prepare --users=200000 --books=500000 --authors=100000 --ratings=1000000 --orders=1000000 --host 127.0.0.1 --port 4000 --drop-tables
```

または[TiDB Cloudのインポート機能を利用する](/develop/dev-guide-bookshop-schema-design.md#method-2-via-tidb-cloud-import)事前に準備されたサンプル データをインポートすることもできます。

## ウィンドウ関数 {#window-functions}

データベースを使用する場合、データを保存し、アプリケーション機能 (書籍の注文や評価など) を提供するだけでなく、データベース内のデータを分析して、さらなる操作や決定を下す必要がある場合もあります。

[1 つのテーブルからデータをクエリする](/develop/dev-guide-get-data-from-single-table.md)ドキュメントでは、集計クエリを使用してデータ全体を分析する方法を紹介しています。より複雑なシナリオでは、複数の集計クエリの結果を 1 つのクエリに集計したい場合があります。特定の書籍の注文金額の過去の傾向を知りたい場合は、各月のすべての注文データを`sum`集計し、 `sum`結果を集計して過去の傾向を取得できます。

このような分析を容易にするために、TiDB v3.0 以降、TiDB はウィンドウ関数をサポートしています。データの行ごとに、この関数は複数の行にまたがるデータにアクセスする機能を提供します。ウィンドウ関数は、通常の集計クエリとは異なり、結果セットを 1 つの行にマージせずに行を集計します。

集計関数と同様に、ウィンドウ関数を使用する場合は、固定された一連の構文に従う必要があります。

```sql
SELECT
    window_function() OVER ([partition_clause] [order_clause] [frame_clause]) AS alias
FROM
    table_name
```

### <code>ORDER BY</code>句 {#code-order-by-code-clause}

集計ウィンドウ関数`sum()`を使用すると、特定の書籍の注文金額の過去の傾向を分析できます。例えば：

```sql
WITH orders_group_by_month AS (
  SELECT DATE_FORMAT(ordered_at, '%Y-%c') AS month, COUNT(*) AS orders
  FROM orders
  WHERE book_id = 3461722937
  GROUP BY 1
)
SELECT
month,
SUM(orders) OVER(ORDER BY month ASC) as acc
FROM orders_group_by_month
ORDER BY month ASC;
```

`sum()`関数は、 `OVER`節の`ORDER BY`ステートメントで指定された順序でデータを累積します。結果は次のとおりです。

```
+---------+-------+
| month   | acc   |
+---------+-------+
| 2011-5  |     1 |
| 2011-8  |     2 |
| 2012-1  |     3 |
| 2012-2  |     4 |
| 2013-1  |     5 |
| 2013-3  |     6 |
| 2015-11 |     7 |
| 2015-4  |     8 |
| 2015-8  |     9 |
| 2017-11 |    10 |
| 2017-5  |    11 |
| 2019-5  |    13 |
| 2020-2  |    14 |
+---------+-------+
13 rows in set (0.01 sec)
```

上記のデータを横軸を時間、縦軸を累計注文額とした折れ線グラフで可視化します。傾きの変化から本の歴史的な順序傾向を簡単に知ることができます。

### <code>PARTITION BY</code>句 {#code-partition-by-code-clause}

さまざまな種類の書籍の過去の注文傾向を分析し、それを複数の系列を持つ同じ折れ線グラフで視覚化するとします。

`PARTITION BY`句を使用して、書籍をタイプ別にグループ化し、各タイプの履歴順序を個別にカウントできます。

```sql
WITH orders_group_by_month AS (
    SELECT
        b.type AS book_type,
        DATE_FORMAT(ordered_at, '%Y-%c') AS month,
        COUNT(*) AS orders
    FROM orders o
    LEFT JOIN books b ON o.book_id = b.id
    WHERE b.type IS NOT NULL
    GROUP BY book_type, month
), acc AS (
    SELECT
        book_type,
        month,
        SUM(orders) OVER(PARTITION BY book_type ORDER BY book_type, month ASC) as acc
    FROM orders_group_by_month
    ORDER BY book_type, month ASC
)
SELECT * FROM acc;
```

結果は次のとおりです。

```
+------------------------------+---------+------+
| book_type                    | month   | acc  |
+------------------------------+---------+------+
| Magazine                     | 2011-10 |    1 |
| Magazine                     | 2011-8  |    2 |
| Magazine                     | 2012-5  |    3 |
| Magazine                     | 2013-1  |    4 |
| Magazine                     | 2013-6  |    5 |
...
| Novel                        | 2011-3  |   13 |
| Novel                        | 2011-4  |   14 |
| Novel                        | 2011-6  |   15 |
| Novel                        | 2011-8  |   17 |
| Novel                        | 2012-1  |   18 |
| Novel                        | 2012-2  |   20 |
...
| Sports                       | 2021-4  |   49 |
| Sports                       | 2021-7  |   50 |
| Sports                       | 2022-4  |   51 |
+------------------------------+---------+------+
1500 rows in set (1.70 sec)
```

### 非集合ウィンドウ関数 {#non-aggregate-window-functions}

TiDB は、より多くの分析ステートメントのために、いくつかの非集計[ウィンドウ関数](/functions-and-operators/window-functions.md)も提供します。

たとえば、 [ページネーション クエリ](/develop/dev-guide-paginate-results.md)ドキュメントでは、 `row_number()`関数を使用して効率的なページネーション バッチ処理を実現する方法を紹介しています。

## ハイブリッド ワークロード {#hybrid-workload}

ハイブリッド ロード シナリオでリアルタイムのオンライン分析処理に TiDB を使用する場合、TiDB のエントリ ポイントをデータに提供するだけで済みます。 TiDB は、特定のビジネスに基づいてさまざまな処理エンジンを自動的に選択します。

### TiFlashレプリカの作成 {#create-tiflash-replicas}

TiDB は、デフォルトで行ベースのstorageエンジン TiKV を使用します。カラムナstorageエンジンTiFlashを使用するには、 [HTAP 機能を有効にする](/develop/dev-guide-create-table.md#use-htap-capabilities)を参照してください。 TiFlashを介してデータをクエリする前に、次のステートメントを使用して、 `books`および`orders`テーブルのTiFlashレプリカを作成する必要があります。

```sql
ALTER TABLE books SET TIFLASH REPLICA 1;
ALTER TABLE orders SET TIFLASH REPLICA 1;
```

次のステートメントを使用して、 TiFlashレプリカの進行状況を確認できます。

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'bookshop' and TABLE_NAME = 'books';
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'bookshop' and TABLE_NAME = 'orders';
```

1 の`PROGRESS`列は進行状況が 100% 完了していることを示し、1 の`AVAILABLE`列はレプリカが現在使用可能であることを示します。

```
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| bookshop     | books      |      143 |             1 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
1 row in set (0.07 sec)
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| bookshop     | orders     |      147 |             1 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
1 row in set (0.07 sec)
```

レプリカが追加されたら、 `EXPLAIN`ステートメントを使用して、上記のウィンドウ関数[`PARTITION BY`句](#partition-by-clause)の実行計画を確認できます。実行計画に`cop[tiflash]`表示された場合は、 TiFlashエンジンが動作を開始したことを意味します。

その後、 [`PARTITION BY`句](#partition-by-clause)のサンプルSQL文を再度実行してください。結果は次のとおりです。

```
+------------------------------+---------+------+
| book_type                    | month   | acc  |
+------------------------------+---------+------+
| Magazine                     | 2011-10 |    1 |
| Magazine                     | 2011-8  |    2 |
| Magazine                     | 2012-5  |    3 |
| Magazine                     | 2013-1  |    4 |
| Magazine                     | 2013-6  |    5 |
...
| Novel                        | 2011-3  |   13 |
| Novel                        | 2011-4  |   14 |
| Novel                        | 2011-6  |   15 |
| Novel                        | 2011-8  |   17 |
| Novel                        | 2012-1  |   18 |
| Novel                        | 2012-2  |   20 |
...
| Sports                       | 2021-4  |   49 |
| Sports                       | 2021-7  |   50 |
| Sports                       | 2022-4  |   51 |
+------------------------------+---------+------+
1500 rows in set (0.79 sec)
```

2 つの実行結果を比較すると、 TiFlashの方がクエリ速度が大幅に向上していることがわかります (データ量が多いほど向上します)。これは、ウィンドウ関数は通常、一部の列の完全なテーブル スキャンに依存しており、列ベースのTiFlashは行ベースの TiKV よりもこの種の分析タスクの処理に適しているためです。 TiKV の場合、主キーまたはインデックスを使用してクエリ対象の行数を減らすと、クエリも高速になり、 TiFlashと比較して消費するリソースが少なくなります。

### クエリ エンジンを指定する {#specify-a-query-engine}

TiDB は Cost Based Optimizer (CBO) を使用して、コストの見積もりに基づいてTiFlashレプリカを使用するかどうかを自動的に選択します。ただし、クエリがトランザクションまたは分析のどちらであるかが明らかな場合は、使用するクエリ エンジンを[オプティマイザーのヒント](/optimizer-hints.md)で指定できます。

クエリで使用するエンジンを指定するには、次のステートメントのように`/*+ read_from_storage(engine_name[table_name]) */`ヒントを使用できます。

> **ノート：**
>
> -   テーブルにエイリアスがある場合は、ヒントでテーブル名の代わりにエイリアスを使用します。そうでない場合、ヒントは機能しません。
> -   `read_from_storage`ヒントは[共通テーブル式](/develop/dev-guide-use-common-table-expression.md)では機能しません。

```sql
WITH orders_group_by_month AS (
    SELECT
        /*+ read_from_storage(tikv[o]) */
        b.type AS book_type,
        DATE_FORMAT(ordered_at, '%Y-%c') AS month,
        COUNT(*) AS orders
    FROM orders o
    LEFT JOIN books b ON o.book_id = b.id
    WHERE b.type IS NOT NULL
    GROUP BY book_type, month
), acc AS (
    SELECT
        book_type,
        month,
        SUM(orders) OVER(PARTITION BY book_type ORDER BY book_type, month ASC) as acc
    FROM orders_group_by_month mo
    ORDER BY book_type, month ASC
)
SELECT * FROM acc;
```

`EXPLAIN`ステートメントを使用して、上記の SQL ステートメントの実行計画を確認できます。タスク列に`cop[tiflash]`と`cop[tikv]`同時に表示される場合は、 TiFlashと TiKV の両方がこのクエリを完了するようにスケジュールされていることを意味します。通常、 TiFlashと TiKVstorageエンジンは異なる TiDB ノードを使用するため、2 つのクエリ タイプは互いに影響を受けないことに注意してください。

TiDB がどのようにTiFlashを使用するかについての詳細は、 [TiDB を使用してTiFlashレプリカを読み取る](/tiflash/use-tidb-to-read-tiflash.md)を参照してください。

## 続きを読む {#read-more}

<CustomContent platform="tidb">

-   [HTAP のクイック スタート](/quick-start-with-htap.md)
-   [HTAP を調べる](/explore-htap.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [TiDB CloudHTAP クイック スタート](/tidb-cloud/tidb-cloud-htap-quickstart.md)

</CustomContent>

-   [ウィンドウ関数](/functions-and-operators/window-functions.md)
-   [TiFlashを使用する](/tiflash/tiflash-overview.md#use-tiflash)
