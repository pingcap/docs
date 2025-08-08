---
title: HTAP Queries
summary: TiDB に HTAP クエリを導入します。
---

# HTAPクエリ {#htap-queries}

HTAPは、Hybrid Transactional and Analytical Processing（ハイブリッド・トランザクション・アンド・アナリティカル・プロセッシング）の略です。従来、データベースはトランザクション処理または分析シナリオ向けに設計されることが多く、データプラットフォームはトランザクション処理と分析処理に分割する必要があり、分析クエリへの迅速な応答のために、トランザクションデータベースから分析データベースへのデータの複製が必要でした。TiDBデータベースはトランザクションと分析の両方のタスクを実行できるため、データプラットフォームの構築が大幅に簡素化され、ユーザーはより新鮮なデータを分析に使用できるようになります。

TiDBは、オンライントランザクション処理（OLTP）には行ベースのstorageエンジンであるTiKVを使用し、オンライン分析処理（OLAP）には列指向storageエンジンであるTiFlashを使用します。HTAPでは、行ベースのstorageエンジンと列指向storageエンジンが共存します。どちらのstorageエンジンも、データを自動的に複製し、強力な一貫性を維持できます。行ベースのstorageエンジンはOLTPのパフォーマンスを最適化し、列指向storageエンジンはOLAPのパフォーマンスを最適化します。

セクション[テーブルを作成する](/develop/dev-guide-create-table.md#use-htap-capabilities) 、TiDBのHTAP機能を有効にする方法を紹介します。以下では、HTAPを使用してデータをより高速に分析する方法について説明します。

## データ準備 {#data-preparation}

始める前に、さらにサンプルデータ[`tiup demo`コマンド経由](/develop/dev-guide-bookshop-schema-design.md#method-1-via-tiup-demo)インポートすることができます。例えば：

```shell
tiup demo bookshop prepare --users=200000 --books=500000 --authors=100000 --ratings=1000000 --orders=1000000 --host 127.0.0.1 --port 4000 --drop-tables
```

または、 [TiDB Cloudのインポート機能を使用する](/develop/dev-guide-bookshop-schema-design.md#method-2-via-tidb-cloud-import)実行して、事前に準備されたサンプル データをインポートすることもできます。

## ウィンドウ関数 {#window-functions}

データベースを使用する場合、データを保存し、アプリケーション機能 (書籍の注文や評価など) を提供するだけでなく、データベース内のデータを分析して、さらなる操作や決定を行う必要がある場合もあります。

[単一のテーブルからデータをクエリする](/develop/dev-guide-get-data-from-single-table.md)ドキュメントでは、集計クエリを使用してデータ全体を分析する方法を紹介しています。より複雑なシナリオでは、複数の集計クエリの結果を1つのクエリに集約したい場合があります。特定の書籍の注文金額の推移を知りたい場合は、各月の注文データすべてについて`sum`集計クエリを実行し、さらに`sum`集計クエリの結果をまとめて集計することで、推移を把握できます。

このような分析を容易にするために、TiDB v3.0以降、TiDBはウィンドウ関数をサポートしています。この関数は、データの各行に対して、複数行にわたるデータへのアクセスを可能にします。通常の集計クエリとは異なり、ウィンドウ関数は結果セットを1行にまとめることなく行を集計します。

集計関数と同様に、ウィンドウ関数を使用する場合も、固定された一連の構文に従う必要があります。

```sql
SELECT
    window_function() OVER ([partition_clause] [order_clause] [frame_clause]) AS alias
FROM
    table_name
```

### <code>ORDER BY</code>句 {#code-order-by-code-clause}

集計ウィンドウ関数`sum()`使用すると、特定の書籍の注文量の推移を分析できます。例えば、次のようになります。

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

`sum()`の関数は、 `OVER`番目の節の`ORDER BY`の文で指定された順序でデータを累積します。結果は次のようになります。

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

上記のデータを、横軸に時間、縦軸に累計受注額を取った折れ線グラフで視覚化します。傾きの変化から、書籍の過去の受注傾向を簡単に把握できます。

### <code>PARTITION BY</code>句 {#code-partition-by-code-clause}

さまざまな種類の書籍の過去の注文傾向を分析し、それを複数のシリーズを含む同じ折れ線グラフで視覚化したいとします。

`PARTITION BY`句を使用すると、書籍を種類別にグループ化し、種類ごとに履歴注文を個別にカウントできます。

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

### 非集計ウィンドウ関数 {#non-aggregate-window-functions}

TiDB は、より多くの分析ステートメント用に、集約されていない[ウィンドウ関数](/functions-and-operators/window-functions.md)もいくつか提供します。

たとえば、 [ページネーションクエリ](/develop/dev-guide-paginate-results.md)ドキュメントでは、 `row_number()`関数を使用して効率的なページ区切りのバッチ処理を実現する方法を紹介しています。

## ハイブリッドワークロード {#hybrid-workload}

ハイブリッド負荷シナリオにおけるリアルタイムオンライン分析処理にTiDBを使用する場合、データへのTiDBのエントリポイントを提供するだけで済みます。TiDBは、特定のビジネスに基づいて異なる処理エンジンを自動的に選択します。

### TiFlashレプリカを作成する {#create-tiflash-replicas}

TiDBはデフォルトで行ベースのstorageエンジンであるTiKVを使用します。列指向storageエンジンであるTiFlashを使用するには、 [HTAP機能を有効にする](/develop/dev-guide-create-table.md#use-htap-capabilities)参照してください。TiFlashを介してデータをクエリする前に、次のステートメントを使用して`books`と`orders`テーブルのTiFlashレプリカを作成する必要があります。

```sql
ALTER TABLE books SET TIFLASH REPLICA 1;
ALTER TABLE orders SET TIFLASH REPLICA 1;
```

次のステートメントを使用して、 TiFlashレプリカの進行状況を確認できます。

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'bookshop' and TABLE_NAME = 'books';
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'bookshop' and TABLE_NAME = 'orders';
```

`PROGRESS`列目が 1 の場合は進行状況が 100% 完了していることを示し、 `AVAILABLE`列目が 1 の場合はレプリカが現在利用可能であることを示します。

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

レプリカを追加した後、 `EXPLAIN`ステートメントを使用して、上記のウィンドウ関数[`PARTITION BY`句](#partition-by-clause)実行プランを確認できます。実行プランに`cop[tiflash]`表示されている場合は、 TiFlashエンジンが動作を開始したことを意味します。

次に、 [`PARTITION BY`句](#partition-by-clause)のサンプルSQL文を再度実行します。結果は以下のようになります。

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

2つの実行結果を比較すると、 TiFlashによってクエリ速度が大幅に向上していることがわかります（データ量が多いほど、その向上は顕著です）。これは、ウィンドウ関数は通常、一部の列に対してテーブル全体のスキャンに依存しており、行ベースの TiKV よりも列ベースのTiFlash の方がこの種の分析タスクの処理に適しているためです。TiKV の場合、主キーやインデックスを使用してクエリ対象の行数を減らすと、クエリ速度も向上し、 TiFlashと比較してリソース消費量も少なくなります。

### クエリエンジンを指定する {#specify-a-query-engine}

TiDBはコストベースオプティマイザー（CBO）を使用して、コスト見積もりに基づいてTiFlashレプリカを使用するかどうかを自動的に選択します。ただし、クエリがトランザクションクエリか分析クエリかが明確な場合は、 [オプティマイザヒント](/optimizer-hints.md)を使用して使用するクエリエンジンを指定できます。

クエリで使用するエンジンを指定するには、次のステートメントのように`/*+ read_from_storage(engine_name[table_name]) */`ヒントを使用できます。

> **注記：**
>
> -   テーブルに別名がある場合は、ヒントでテーブル名の代わりに別名を使用します。そうしないと、ヒントは機能しません。
> -   `read_from_storage`ヒントは[共通テーブル式](/develop/dev-guide-use-common-table-expression.md)には機能しません。

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

`EXPLAIN`ステートメントを使用して、上記のSQL文の実行プランを確認できます。タスク列に`cop[tiflash]`と`cop[tikv]`同時に表示される場合、 TiFlashと TiKV の両方がこのクエリを完了するようにスケジュールされていることを意味します。TiFlash とTiFlashのstorageエンジンは通常、異なる TiDB ノードを使用するため、2 つのクエリタイプは互いに影響を受けません。

TiDBがTiFlashをどのように使用するかの詳細については、 [TiDBを使用してTiFlashレプリカを読み取る](/tiflash/use-tidb-to-read-tiflash.md)参照してください。

## 続きを読む {#read-more}

<CustomContent platform="tidb">

-   [TiDB HTAPのクイックスタート](/quick-start-with-htap.md)
-   [HTAPを探索する](/explore-htap.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [TiDB Cloud HTAP クイックスタート](/tidb-cloud/tidb-cloud-htap-quickstart.md)

</CustomContent>

-   [ウィンドウ関数](/functions-and-operators/window-functions.md)
-   [TiFlashを使用する](/tiflash/tiflash-overview.md#use-tiflash)

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
