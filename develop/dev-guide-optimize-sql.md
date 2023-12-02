---
title: SQL Performance Tuning
summary: Introduces TiDB's SQL performance tuning scheme and analysis approach.
---

# SQL性能チューニング {#sql-performance-tuning}

このドキュメントでは、SQL ステートメントが遅い一般的な理由と、SQL パフォーマンスをチューニングするためのテクニックを紹介します。

## あなたが始める前に {#before-you-begin}

[`tiup demo`のインポート](/develop/dev-guide-bookshop-schema-design.md#method-1-via-tiup-demo)を使用してデータを準備できます。

```shell
tiup demo bookshop prepare --host 127.0.0.1 --port 4000 --books 1000000
```

または、 [TiDB Cloudのインポート機能を使用する](/develop/dev-guide-bookshop-schema-design.md#method-2-via-tidb-cloud-import)を使用して、事前に準備されたサンプル データをインポートします。

## 問題: フルテーブルスキャン {#issue-full-table-scan}

SQL クエリが遅くなる最も一般的な理由は、 `SELECT`ステートメントがテーブル全体のスキャンを実行するか、間違ったインデックスを使用することです。

TiDB が主キーではない列またはセカンダリ インデックスにある列に基づいて大きなテーブルから少数の行を取得する場合、通常はパフォーマンスが低下します。

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

このクエリが遅い理由を理解するには、 `EXPLAIN`使用して実行計画を確認します。

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

実行計画の`TableFullScan_5`からわかるように、TiDB は`books`テーブルに対してフル テーブル スキャンを実行し、 `title`各行の条件を満たすかどうかをチェックします。 `TableFullScan_5`の`estRows`値は`1000000.00`です。これは、オプティマイザがこのテーブル全体のスキャンには`1000000.00`行のデータが必要であると推定することを意味します。

`EXPLAIN`の使用法の詳細については、 [`EXPLAIN`ウォークスルー](/explain-walkthrough.md)を参照してください。

### 解決策: セカンダリ インデックスを使用する {#solution-use-secondary-index}

上記のクエリを高速化するには、 `books.title`列にセカンダリ インデックスを追加します。

```sql
CREATE INDEX title_idx ON books (title);
```

クエリの実行がはるかに高速になります。

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

パフォーマンスが向上する理由を理解するには、 `EXPLAIN`使用して新しい実行計画を確認します。

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

実行計画の`IndexLookup_10`からわかるように、TiDB は`title_idx`インデックスによってデータをクエリします。その`estRows`値は`1.27`です。これは、オプティマイザが`1.27`行のみがスキャンされると推定することを意味します。スキャンされる推定行数は、テーブル全体のスキャンの`1000000.00`行のデータよりもはるかに少なくなります。

`IndexLookup_10`実行プランでは、まず`IndexRangeScan_8`演算子を使用して、 `title_idx`インデックスを通じて条件を満たすインデックス データを読み取り、次に`TableLookup_9`演算子を使用して、インデックス データに格納されている行 ID に従って対応する行をクエリします。

TiDB 実行計画の詳細については、 [TiDB クエリ実行計画の概要](/explain-overview.md)を参照してください。

### 解決策: カバリングインデックスを使用する {#solution-use-covering-index}

インデックスが SQL ステートメントによってクエリされるすべての列を含むカバーインデックスである場合、クエリにはインデックス データをスキャンするだけで十分です。

たとえば、次のクエリでは、 `title`に基づいて対応する`price`をクエリするだけで済みます。

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

`title_idx`インデックスには`title`列のデータのみが含まれるため、TiDB は引き続き最初にインデックス データをスキャンしてから、テーブルの`price`列をクエリする必要があります。

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

パフォーマンスを最適化するには、インデックス`title_idx`を削除し、新しいカバーインデックス`title_price_idx`を作成します。

```sql
ALTER TABLE books DROP INDEX title_idx;
```

```sql
CREATE INDEX title_price_idx ON books (title, price);
```

`price`データは`title_price_idx`インデックスに格納されているため、次のクエリはインデックス データをスキャンするだけで済みます。

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

このクエリはより高速に実行されるようになりました。

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

### 解決策: プライマリ インデックスを使用する {#solution-use-primary-index}

クエリで主キーを使用してデータをフィルタリングすると、クエリは高速に実行されます。たとえば、 `books`テーブルの主キーは`id`列であるため、 `id`列を使用してデータをクエリできます。

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

実行計画を表示するには`EXPLAIN`を使用します。

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

`Point_Get`非常に高速に実行されるプランです。

## 適切な結合タイプを使用する {#use-the-right-join-type}

[JOIN実行計画](/explain-joins.md)を参照してください。

### こちらも参照 {#see-also}

-   [EXPLAIN コマンド](/explain-walkthrough.md)
-   [インデックスを使用する Explain ステートメント](/explain-indexes.md)
