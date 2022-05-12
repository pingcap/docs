---
title: SQL Performance Tuning
summary: Introducing TiDB's SQL performance tuning scheme and analysis approach.
---

# SQL Performance Tuning

This section introduce some common reasons for slow SQL statements, and you will learn some SQL performance tuning skills.

## Before you begin

You can use [`tiup demo` Import](/develop/dev-bookshop-schema-design.md#method-1-through-tiup-demo-command-line) to prepare data:

{{< copyable "shell-regular" >}}

```shell
tiup demo bookshop prepare --host 127.0.0.1 --port 4000 --books 1000000
```

Or [using the Import function of TiDB Cloud](/develop/dev-bookshop-schema-design.md#method-2-through-the-tidb-cloud-import-function) to import the pre-prepared sample data.

## Issue: Full Table Scan

The most common reason for slow SQL is that the `SELECT` statements that include full table scan and incorrect use of indexes.

You'll get poor performance when retrieving a small number of rows from a large table based on a column that is not in the primary key or any secondary index:

{{< copyable "sql" >}}

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

We can use `EXPLAIN` to see the execution plan of the SQL and see why the SQL is so slow:

{{< copyable "sql" >}}

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

As can be seen from `TableFullScan_5` in the execution plan, TiDB will perform a full table scan of table `books` and then check whether `title` satisfies the condition for each row. The `estRows` value of `TableFullScan_5` is `1000000.00`, indicating that the optimizer estimates that this full table scan will scan `1000000.00` rows of data.

For more information about the usage of `EXPLAIN`, see [EXPLAIN Walkthrough](/explain-walkthrough.md).

### Solution: Use Secondary Index

To speed up this query, add a secondary index on `books.title`:

{{< copyable "sql" >}}

```sql
CREATE INDEX title_idx ON books (title);
```

The query will now return much faster:

{{< copyable "sql" >}}

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

To understand why the performance improved, use `EXPLAIN` to see the new execution plan:

{{< copyable "sql" >}}

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

As can be seen from `IndexLookup_10` in the execution plan, TiDB will query the data by index `title_idx`. Its `estRows` value is `1.27`, indicating that the optimizer estimates that only `1.27` rows will be scanned, which is much smaller than the `1000000.00` row data in the full table scan.

The execution process of the `IndexLookup_10` is to first use the `IndexRangeScan_8` operator to read the index data that meets the condition through the `title_idx` index, and then query the corresponding row data according to the Row ID stored in the index data by `TableLookup_9` operator.

For more information on the TiDB execution plan, see [TiDB Query Execution Plan Overview](/explain-overview.md).

### Solution: Use Covering Index

If the index is covering index, which contains all the columns required by the SQL statements, then just scan the index data.

For example, in the following query, you only need to query the corresponding `price` based on `title`:

{{< copyable "sql" >}}

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

Since the index `title_idx` only contains the `title` column data, TiDB still needs to scan the index data first, then query the `price` column data from the table row data.

{{< copyable "sql" >}}

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

Let's drop the `title_idx` index and create a new covering index `title_price_idx`:

{{< copyable "sql" >}}

```sql
ALTER TABLE books DROP INDEX title_idx;
```

{{< copyable "sql" >}}

```sql
CREATE INDEX title_price_idx ON books (title, price);
```

Now that the `price` data is stored in the index `title_price_idx`, so the following query only needs to scan the index data:

{{< copyable "sql" >}}

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

Now this query will run faster:

{{< copyable "sql" >}}

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

Since table `books` will be used in later examples, let's drop the `title_price_idx` index.

{{< copyable "sql" >}}

```sql
ALTER TABLE books DROP INDEX title_price_idx;
```

### Solution: Use Primary Index

If the query uses the primary key to filter data, the query will run very fast. For example, the primary key of the table `books` is the column `id`, and then use the column `id` to query the data:

{{< copyable "sql" >}}

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

We can use `EXPLAIN` to see the execution plan:

{{< copyable "sql" >}}

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

`Point_Get` is a very fast execute plan.

## Use Right Join Type

See [JOIN Execution Plan](/explain-joins.md)。

### See Also

* [EXPLAIN Walkthrough](/explain-walkthrough.md)
* [Explain Statements That Use Indexes](/explain-indexes.md)