---
title: SQL Performance Tuning
summary: Introduces TiDB's SQL performance tuning scheme and analysis approach.
---

# SQL性能チューニング {#sql-performance-tuning}

このドキュメントでは、SQL ステートメントが遅くなる一般的な理由と、SQL パフォーマンスをチューニングするためのテクニックを紹介します。

## あなたが始める前に {#before-you-begin}

[`tiup demo`のインポート](/develop/dev-guide-bookshop-schema-design.md#method-1-via-tiup-demo)を使用してデータを準備できます。

```shell
tiup demo bookshop prepare --host 127.0.0.1 --port 4000 --books 1000000
```

または、事前に準備されたサンプル データをインポートするには[TiDB Cloudのインポート機能を使用する](/develop/dev-guide-bookshop-schema-design.md#method-2-via-tidb-cloud-import) 。

## 問題: 全テーブル スキャン {#issue-full-table-scan}

SQL クエリが遅くなる最も一般的な理由は、 `SELECT`ステートメントが全テーブル スキャンを実行するか、不適切なインデックスを使用することです。

TiDB が、プライマリ キーまたはセカンダリ インデックスではない列に基づいて大きなテーブルから少数の行を取得する場合、通常はパフォーマンスが低下します。

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

このクエリが遅い理由を理解するには、 `EXPLAIN`を使用して実行計画を確認します。

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

実行計画の`TableFullScan_5`からわかるように、TiDB は`books`テーブルに対してフル テーブル スキャンを実行し、 `title`各行の条件を満たすかどうかをチェックします。 `TableFullScan_5`の`estRows`値は`1000000.00`です。これは、オプティマイザーが、この全表スキャンに`1000000.00`行のデータが必要であると見積もることを意味します。

`EXPLAIN`の使用方法の詳細については、 [`EXPLAIN`ウォークスルー](/explain-walkthrough.md)を参照してください。

### 解決策: セカンダリ インデックスを使用する {#solution-use-secondary-index}

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

パフォーマンスが向上した理由を理解するには、 `EXPLAIN`使用して新しい実行計画を表示します。

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

実行計画の`IndexLookup_10`からわかるように、TiDB は`title_idx`インデックスでデータをクエリします。その`estRows`値は`1.27`です。これは、オプティマイザが`1.27`行のみがスキャンされると見積もることを意味します。スキャンされた推定行数は、全表スキャンの`1000000.00`行のデータよりもはるかに少なくなっています。

`IndexLookup_10`実行計画は、最初に`IndexRangeScan_8`演算子を使用して`title_idx`インデックスを介して条件を満たすインデックス データを読み取り、次に`TableLookup_9`演算子を使用して、インデックス データに格納されている行 ID に従って対応する行をクエリします。

TiDB 実行計画の詳細については、 [TiDB クエリ実行計画の概要](/explain-overview.md)を参照してください。

### 解決策: カバリング インデックスを使用する {#solution-use-covering-index}

インデックスが、SQL ステートメントによってクエリされるすべての列を含むカバリング インデックスである場合、クエリにはインデックス データのスキャンで十分です。

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

`title_idx`インデックスには`title`列のデータしか含まれていないため、TiDB は最初にインデックス データをスキャンしてから、テーブルの`price`列をクエリする必要があります。

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

パフォーマンスを最適化するには、 `title_idx`インデックスを削除して、新しいカバリング インデックス`title_price_idx`を作成します。

```sql
ALTER TABLE books DROP INDEX title_idx;
```

```sql
CREATE INDEX title_price_idx ON books (title, price);
```

`price`データは`title_price_idx`インデックスに格納されているため、次のクエリではインデックス データをスキャンするだけで済みます。

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

クエリが主キーを使用してデータをフィルター処理する場合、クエリは高速に実行されます。たとえば、 `books`テーブルの主キーは`id`列なので、 `id`列を使用してデータをクエリできます。

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

実行計画を表示するには、 `EXPLAIN`を使用します。

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

[JOIN実行計画](/explain-joins.md)を参照してください。

### こちらもご覧ください {#see-also}

-   [EXPLAIN コマンド](/explain-walkthrough.md)
-   [インデックスを使用するステートメントの説明](/explain-indexes.md)
