---
title: SQL Performance Tuning
summary: TiDB の SQL パフォーマンス チューニング スキームと分析アプローチを紹介します。
---

# SQL性能チューニング {#sql-performance-tuning}

このドキュメントでは、SQL ステートメントが遅くなる一般的な理由と、SQL パフォーマンスをチューニングする手法について説明します。

## あなたが始める前に {#before-you-begin}

[`tiup demo`インポート](/develop/dev-guide-bookshop-schema-design.md#method-1-via-tiup-demo)使用してデータを準備できます。

```shell
tiup demo bookshop prepare --host 127.0.0.1 --port 4000 --books 1000000
```

または、事前に準備されたサンプル データをインポートする場合は[TiDB Cloudのインポート機能を使用する](/develop/dev-guide-bookshop-schema-design.md#method-2-via-tidb-cloud-import) 。

## 問題: テーブル全体のスキャン {#issue-full-table-scan}

SQL クエリが遅くなる最も一般的な理由は、 `SELECT`ステートメントが完全なテーブル スキャンを実行するか、間違ったインデックスを使用することです。

TiDB が主キーではない列またはセカンダリ インデックス内の列に基づいて大規模なテーブルから少数の行を取得する場合、通常はパフォーマンスが低下します。

```sql
SELECT * FROM books WHERE title = 'Marian Yost';
```

```sql
+------------+-------------+-----------------------+---------------------+-------+--------+
| id         | title       | type                  | published_at        | stock | price  |
+------------+-------------+-----------------------+---------------------+-------+--------+
| 65670536   | Marian Yost | Arts                  | 1950-04-09 06:28:58 | 542   | 435.01 |
| 1164070689 | Marian Yost | Education & Reference | 1916-05-27 12:15:35 | 216   | 328.18 |
| 1414277591 | Marian Yost | Arts                  | 1932-06-15 09:18:14 | 303   | 496.52 |
| 2305318593 | Marian Yost | Arts                  | 2000-08-15 19:40:58 | 398   | 402.90 |
| 2638226326 | Marian Yost | Sports                | 1952-04-02 12:40:37 | 191   | 174.64 |
+------------+-------------+-----------------------+---------------------+-------+--------+
5 rows in set
Time: 0.582s
```

このクエリが遅い理由を理解するには、 `EXPLAIN`使用して実行プランを確認します。

```sql
EXPLAIN SELECT * FROM books WHERE title = 'Marian Yost';
```

```sql
+---------------------+------------+-----------+---------------+-----------------------------------------+
| id                  | estRows    | task      | access object | operator info                           |
+---------------------+------------+-----------+---------------+-----------------------------------------+
| TableReader_7       | 1.27       | root      |               | data:Selection_6                        |
| └─Selection_6       | 1.27       | cop[tikv] |               | eq(bookshop.books.title, "Marian Yost") |
|   └─TableFullScan_5 | 1000000.00 | cop[tikv] | table:books   | keep order:false                        |
+---------------------+------------+-----------+---------------+-----------------------------------------+
```

実行プランの`TableFullScan_5`からわかるように、TiDB は`books`テーブルの全テーブル スキャンを実行し、各行の`title`条件を満たしているかどうかを確認します。 `TableFullScan_5`の`estRows`値は`1000000.00`であり、これはオプティマイザがこの全テーブル スキャンで`1000000.00`行のデータが必要になると見積もっていることを意味します。

`EXPLAIN`の使用方法の詳細については、 [`EXPLAIN`ウォークスルー](/explain-walkthrough.md)を参照してください。

### 解決策: セカンダリインデックスを使用する {#solution-use-secondary-index}

上記のクエリを高速化するには、 `books.title`列にセカンダリ インデックスを追加します。

```sql
CREATE INDEX title_idx ON books (title);
```

クエリの実行ははるかに高速です。

```sql
SELECT * FROM books WHERE title = 'Marian Yost';
```

```sql
+------------+-------------+-----------------------+---------------------+-------+--------+
| id         | title       | type                  | published_at        | stock | price  |
+------------+-------------+-----------------------+---------------------+-------+--------+
| 1164070689 | Marian Yost | Education & Reference | 1916-05-27 12:15:35 | 216   | 328.18 |
| 1414277591 | Marian Yost | Arts                  | 1932-06-15 09:18:14 | 303   | 496.52 |
| 2305318593 | Marian Yost | Arts                  | 2000-08-15 19:40:58 | 398   | 402.90 |
| 2638226326 | Marian Yost | Sports                | 1952-04-02 12:40:37 | 191   | 174.64 |
| 65670536   | Marian Yost | Arts                  | 1950-04-09 06:28:58 | 542   | 435.01 |
+------------+-------------+-----------------------+---------------------+-------+--------+
5 rows in set
Time: 0.007s
```

パフォーマンスが向上した理由を理解するには、 `EXPLAIN`使用して新しい実行プランを確認します。

```sql
EXPLAIN SELECT * FROM books WHERE title = 'Marian Yost';
```

```sql
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
| id                        | estRows | task      | access object                       | operator info                                         |
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
| IndexLookUp_10            | 1.27    | root      |                                     |                                                       |
| ├─IndexRangeScan_8(Build) | 1.27    | cop[tikv] | table:books, index:title_idx(title) | range:["Marian Yost","Marian Yost"], keep order:false |
| └─TableRowIDScan_9(Probe) | 1.27    | cop[tikv] | table:books                         | keep order:false                                      |
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
```

実行プランの`IndexLookup_10`からわかるように、TiDB は`title_idx`インデックスでデータをクエリします。その`estRows`値は`1.27`で、これはオプティマイザが`1.27`行のみがスキャンされると見積もっていることを意味します。推定されるスキャン行数は、フル テーブル スキャンの`1000000.00`行のデータよりはるかに少なくなります。

`IndexLookup_10`実行プランは、まず`IndexRangeScan_8`演算子を使用して`title_idx`インデックスを通じて条件を満たすインデックス データを読み取り、次に`TableLookup_9`演算子を使用して、インデックス データに格納されている行 ID に従って対応する行をクエリすることです。

TiDB 実行プランの詳細については、 [TiDB クエリ実行プランの概要](/explain-overview.md)参照してください。

### 解決策: カバーインデックスを使用する {#solution-use-covering-index}

インデックスが、SQL ステートメントによってクエリされるすべての列を含むカバーリング インデックスである場合、インデックス データをスキャンするだけでクエリに十分です。

たとえば、次のクエリでは、 `title`に基づいて対応する`price`クエリするだけで済みます。

```sql
SELECT title, price FROM books WHERE title = 'Marian Yost';
```

```sql
+-------------+--------+
| title       | price  |
+-------------+--------+
| Marian Yost | 435.01 |
| Marian Yost | 328.18 |
| Marian Yost | 496.52 |
| Marian Yost | 402.90 |
| Marian Yost | 174.64 |
+-------------+--------+
5 rows in set
Time: 0.007s
```

`title_idx`インデックスには`title`列目のデータのみが含まれているため、TiDB は最初にインデックス データをスキャンし、次にテーブルから`price`列目をクエリする必要があります。

```sql
EXPLAIN SELECT title, price FROM books WHERE title = 'Marian Yost';
```

```sql
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
| id                        | estRows | task      | access object                       | operator info                                         |
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
| IndexLookUp_10            | 1.27    | root      |                                     |                                                       |
| ├─IndexRangeScan_8(Build) | 1.27    | cop[tikv] | table:books, index:title_idx(title) | range:["Marian Yost","Marian Yost"], keep order:false |
| └─TableRowIDScan_9(Probe) | 1.27    | cop[tikv] | table:books                         | keep order:false                                      |
+---------------------------+---------+-----------+-------------------------------------+-------------------------------------------------------+
```

パフォーマンスを最適化するには、インデックス`title_idx`を削除し、新しいカバー インデックス`title_price_idx`を作成します。

```sql
ALTER TABLE books DROP INDEX title_idx;
```

```sql
CREATE INDEX title_price_idx ON books (title, price);
```

`price`データは`title_price_idx`インデックスに格納されているため、次のクエリではインデックス データのスキャンのみが必要です。

```sql
EXPLAIN SELECT title, price FROM books WHERE title = 'Marian Yost';
```

```sql
--------------------+---------+-----------+--------------------------------------------------+-------------------------------------------------------+
| id                 | estRows | task      | access object                                    | operator info                                         |
+--------------------+---------+-----------+--------------------------------------------------+-------------------------------------------------------+
| IndexReader_6      | 1.27    | root      |                                                  | index:IndexRangeScan_5                                |
| └─IndexRangeScan_5 | 1.27    | cop[tikv] | table:books, index:title_price_idx(title, price) | range:["Marian Yost","Marian Yost"], keep order:false |
+--------------------+---------+-----------+--------------------------------------------------+-------------------------------------------------------+
```

このクエリはより高速に実行されます:

```sql
SELECT title, price FROM books WHERE title = 'Marian Yost';
```

```sql
+-------------+--------+
| title       | price  |
+-------------+--------+
| Marian Yost | 174.64 |
| Marian Yost | 328.18 |
| Marian Yost | 402.90 |
| Marian Yost | 435.01 |
| Marian Yost | 496.52 |
+-------------+--------+
5 rows in set
Time: 0.004s
```

`books`テーブルは後の例で使用されるため、 `title_price_idx`インデックスを削除します。

```sql
ALTER TABLE books DROP INDEX title_price_idx;
```

### 解決策: プライマリインデックスを使用する {#solution-use-primary-index}

クエリが主キーを使用してデータをフィルター処理する場合、クエリは高速に実行されます。たとえば、 `books`テーブルの主キーは`id`列目なので、 `id`列目を使用してデータをクエリできます。

```sql
SELECT * FROM books WHERE id = 896;
```

```sql
+-----+----------------+----------------------+---------------------+-------+--------+
| id  | title          | type                 | published_at        | stock | price  |
+-----+----------------+----------------------+---------------------+-------+--------+
| 896 | Kathryne Doyle | Science & Technology | 1969-03-18 01:34:15 | 468   | 281.32 |
+-----+----------------+----------------------+---------------------+-------+--------+
1 row in set
Time: 0.004s
```

実行プランを表示するには`EXPLAIN`使用します。

```sql
EXPLAIN SELECT * FROM books WHERE id = 896;
```

```sql
+-------------+---------+------+---------------+---------------+
| id          | estRows | task | access object | operator info |
+-------------+---------+------+---------------+---------------+
| Point_Get_1 | 1.00    | root | table:books   | handle:896    |
+-------------+---------+------+---------------+---------------+
```

`Point_Get`非常に高速な実行プランです。

## 適切な結合タイプを使用する {#use-the-right-join-type}

[JOIN 実行プラン](/explain-joins.md)参照。

### 参照 {#see-also}

-   [EXPLAIN コマンド](/explain-walkthrough.md)
-   [インデックスを使用するステートメントを説明する](/explain-indexes.md)
