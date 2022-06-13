---
title: SQL Performance Tuning
summary: Introduces TiDB's SQL performance tuning scheme and analysis approach.
---

# SQL性能チューニング {#sql-performance-tuning}

このドキュメントでは、SQLステートメントが遅い一般的な理由とSQLパフォーマンスを調整するための手法を紹介します。

## あなたが始める前に {#before-you-begin}

[`tiup demo`のインポート](/develop/dev-guide-bookshop-schema-design.md#via-tiup-demo)を使用してデータを準備できます。

{{< copyable "" >}}

```shell
tiup demo bookshop prepare --host 127.0.0.1 --port 4000 --books 1000000
```

または[TiDB Cloudのインポート機能を使用する](/develop/dev-guide-bookshop-schema-design.md#via-tidb-cloud-import)を使用して、事前に準備されたサンプルデータをインポートします。

## 問題：全表スキャン {#issue-full-table-scan}

SQLクエリが遅い最も一般的な理由は、 `SELECT`ステートメントが全表スキャンを実行するか、誤ったインデックスを使用することです。

TiDBが主キーまたは二次インデックスではない列に基づいて大きなテーブルから少数の行を取得する場合、通常、パフォーマンスは低下します。

{{< copyable "" >}}

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

このクエリが遅い理由を理解するには、 `EXPLAIN`を使用して実行プランを確認します。

{{< copyable "" >}}

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

実行プランの`TableFullScan_5`からわかるように、TiDBは`books`のテーブルに対して全表スキャンを実行し、 `title`が各行の条件を満たすかどうかをチェックします。 `TableFullScan_5`の`estRows`の値は`1000000.00`です。これは、オプティマイザーがこの全表スキャンで`1000000.00`行のデータが必要であると推定していることを意味します。

`EXPLAIN`の使用法の詳細については、 [`EXPLAIN`ウォークスルー](/explain-walkthrough.md)を参照してください。

### 解決策：セカンダリインデックスを使用する {#solution-use-secondary-index}

上記のこのクエリを高速化するには、 `books.title`列にセカンダリインデックスを追加します。

{{< copyable "" >}}

```sql
CREATE INDEX title_idx ON books (title);
```

クエリの実行ははるかに高速です。

{{< copyable "" >}}

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

パフォーマンスが向上する理由を理解するには、 `EXPLAIN`を使用して新しい実行プランを確認します。

{{< copyable "" >}}

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

実行プランの`IndexLookup_10`からわかるように、TiDBは`title_idx`インデックスでデータをクエリします。その`estRows`の値は`1.27`です。これは、オプティマイザーが`1.27`行のみがスキャンされると推定することを意味します。スキャンされた推定行は、全表スキャンの`1000000.00`行のデータよりもはるかに少なくなります。

`IndexLookup_10`の実行プランでは、最初に`IndexRangeScan_8`演算子を使用して、 `title_idx`インデックスを介して条件を満たすインデックスデータを読み取り、次に`TableLookup_9`演算子を使用して、インデックスデータに格納されている行IDに従って対応する行をクエリします。

TiDB実行プランの詳細については、 [TiDBクエリ実行プランの概要](/explain-overview.md)を参照してください。

### 解決策：カバーインデックスを使用する {#solution-use-covering-index}

インデックスがカバーインデックスであり、SQLステートメントによってクエリされたすべての列が含まれている場合、クエリにはインデックスデータをスキャンするだけで十分です。

たとえば、次のクエリでは、 `title`に基づいて対応する`price`をクエリするだけで済みます。

{{< copyable "" >}}

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

`title_idx`インデックスには`title`列のデータしか含まれていないため、TiDBは最初にインデックスデータをスキャンしてから、テーブルから`price`列をクエリする必要があります。

{{< copyable "" >}}

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

パフォーマンスを最適化するには、 `title_idx`のインデックスを削除し、新しいカバーインデックス`title_price_idx`を作成します。

{{< copyable "" >}}

```sql
ALTER TABLE books DROP INDEX title_idx;
```

{{< copyable "" >}}

```sql
CREATE INDEX title_price_idx ON books (title, price);
```

`price`のデータは`title_price_idx`のインデックスに格納されているため、次のクエリではインデックスデータをスキャンするだけで済みます。

{{< copyable "" >}}

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

これで、このクエリはより高速に実行されます。

{{< copyable "" >}}

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

`books`のテーブルは後の例で使用されるため、 `title_price_idx`のインデックスを削除します。

{{< copyable "" >}}

```sql
ALTER TABLE books DROP INDEX title_price_idx;
```

### 解決策：プライマリインデックスを使用する {#solution-use-primary-index}

クエリが主キーを使用してデータをフィルタリングする場合、クエリは高速に実行されます。たとえば、 `books`テーブルの主キーは`id`列であるため、 `id`列を使用してデータをクエリできます。

{{< copyable "" >}}

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

`EXPLAIN`を使用して、実行プランを確認します。

{{< copyable "" >}}

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

`Point_Get`は非常に高速な実行プランです。

## 適切な結合タイプを使用する {#use-the-right-join-type}

[JOIN実行プラン](/explain-joins.md)を参照してください。

### も参照してください {#see-also}

-   [EXPLAIN コマンド / EXPLAIN機能](/explain-walkthrough.md)
-   [インデックスを使用するステートメントを説明する](/explain-indexes.md)
