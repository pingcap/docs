---
title: HTAP Queries
---

# HTAP Queries

HTAP stands for Hybrid Transactional / Analytical Processing. Traditionally, databases are often designed for transactional or analytical scenarios, so the data platform often needs to be split into Transactional Processing and Analytical Processing, and the data needs to be replicated from the transactional database to the analytical database for quick response to analytical queries. TiDB databases can perform both transactional and analytical tasks, which greatly simplifies the construction of data platforms and allows users to use fresher data for analysis.

In TiDB, we have both TiKV, a row-store engine for online transactions, and TiFlash, a column-store engine for real-time analytics scenarios. Data exists in both the Row-Store and Columnar-Store, which are automatically synchronized for strong consistency. The Row-Store is optimized for online transactional OLTP, while the Columnar-Store is optimized for online analytical OLAP performance.

In the [Create Database](/develop/dev-guide-create-table.md#using-htap-capabilities) chapter, we have introduced how to enable the HTAP capability of TiDB. Below we'll take a closer look at how to use HTAP capabilities to analyze data faster.

## Data preparation

Before starting, you can import much larger sample data [via the `tiup demo` command](/develop/dev-guide-bookshop-schema-design.md#via-tiup-demo), for example:

{{< copyable "shell-regular" >}}

```shell
tiup demo bookshop prepare --users=200000 --books=500000 --authors=100000 --ratings=1000000 --orders=1000000 --host 127.0.0.1 --port 4000 --drop-tables
```

Or [using the Import function of TiDB Cloud](/develop/dev-guide-bookshop-schema-design.md#via-tidb-cloud-import) to import the pre-prepared sample data.

## Window function

When we use the database, in addition to the hope that it can store the data we want to record, and can realize business functions such as ordering and buying books, rating books, etc., we may also need to analyze our existing data, so as to make further decisions or take some operations based on the data.

In the [Single Table Read](/develop/dev-guide-get-data-from-single-table.md) section, we have introduced how to use aggregate queries to analyze the data as a whole. In more complex usage scenarios, we may want to aggregate the results of multiple aggregate queries in a single query. For example, if we want to know the historical trend of orders for a particular book, we may need to use aggregate function `sum` for all the orders every month, and then aggregate the `sum` results together to get the historical trend data.

In order to help users simplify the processing of such analysis, TiDB has supported window functions since version 3.0. Window functions provide cross-row data access capability for each row of data. Different from aggregation queries, window functions are used to aggregate data rows in the window range, but does not cause the result set to be merged into a single row of data.

Similar to aggregate functions, window functions also need to be used with a fixed set of syntax:

```sql
SELECT
    window_function() OVER ([partition_clause] [order_clause] [frame_clause]) AS alias
FROM
    table_name
```

### `ORDER BY` clause

For example, we can use the accumulation effect of the aggregation window function `sum()` to analyze the historical trend of the order volume of a certain book:

{{< copyable "sql" >}}

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

The `sum()` function will accumulate the data in order according to the ordering method specified by the `ORDER BY` clause in the `OVER` clause. The accumulated results are as follows:

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

By visualizing the data obtained through a line graph with time on the horizontal axis and accumulate orders on the vertical axis, we can easily get a macro view of the historical order growth trend of the book through the change in the slope of the line graph.

### `PARTITION BY` clause

Let's make our requirements a little more complicated. Suppose you want to analyze the historical order growth trend of different types of books, and you want to present this data in the same multi-series line chart.

We can use the `PARTITION BY` clause to group books according to their types and count their order accumulation history   separately for different types of books.

{{< copyable "sql" >}}

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

The query results are as follows:

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

### Non-aggregate window function

Besides, TiDB also provides us with some non-aggregated [window functions](/functions-and-operators/window-functions.md), with the help of which we can realize richer analysis queries.

For example, in the previous [Pagination Query](/develop/dev-guide-paginate-results.md) chapter, we have introduced how to use the `row_number()` function to achieve efficient pagination batch processing.

## Hybrid workload

### Enable column replica

TiDB's default storage engine, TiKV, is row-stored. Before proceeding to the next steps, you can read the section [Enable HTAP Capability](/develop/dev-guide-create-table.md#using-htap-capabilities) and add a TiFlash column-stored replica of the `books` and `orders` tables using the following SQL.

{{< copyable "sql" >}}

```sql
ALTER TABLE books SET TIFLASH REPLICA 1;
ALTER TABLE orders SET TIFLASH REPLICA 1;
```

By executing the following SQL statement, we can view the progress of TiDB creating a column-stored replica:

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'bookshop' and TABLE_NAME = 'books';
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'bookshop' and TABLE_NAME = 'orders';
```

A `PROGRESS` column of 1 indicates that the synchronization progress is 100% complete, and a `AVAILABLE` column of 1 indicates that the replica is currently available.

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

After the replica is added, you can view the execution plan of the above window function [example SQL](#partition-by-clause) by using the `EXPLAIN` statement. You will find that the words `cop[tiflash]` have appeared in the execution plan, indicating that the TiFlash engine has begun to function.

Query results as follow:

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

By comparing the two execution results before and after, you will find that the query speed is significantly improved by using TiFlash (when the amount of data is larger, the improvement will be more significant). 

This is because when using window functions, it is often necessary to perform a full table scan on the data of some columns. Compared with TiKV in row storage, TiFlash in column storage is more suitable for handling the load of such analytical tasks. For TiKV, if the number of rows to be queried can be quickly reduced through the primary key or index, the query speed is often very fast, and the resource consumption is generally less than that of TiFlash.

### Specify the query engine

TiDB will use the cost-based optimizer (CBO) to automatically choose whether to use TiFlash replicas based on cost estimates. However, in practice, if you are very sure about the type of query, it is recommended that you use [Optimizer Hints](/optimizer-hints.md) to explicitly specify the query engine used for the query to avoid fluctuations in application performance due to different optimization results from the optimizer.

You can use Hint `/*+ read_from_storage(engine_name[table_name]) */` to specify the query engine to be used when querying in the SELECT statement like the following SQL:

> **Notice:**
>
> 1. If your table uses aliases, you should replace table_name in Hints with alias_name, otherwise Hints will be invalid.
> 2. Also, setting read_from_storage Hint for [common table expression](/develop/dev-guide-use-common-table-expression.md) does not work.

{{< copyable "sql" >}}

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

If you check the execution plan of the above SQL with the `EXPLAIN` statement, you will see both `cop[tiflash]` and `cop[tikv]` in the task column, which means that TiDB is scheduling both the row-store query engine and the column-store query engine to complete the query when it processes this query. It is important to note that since the tiflash and tikv storage engines are usually part of different compute nodes, the two query types are not affected by each other.

You can learn more about how TiDB chooses to use TiFlash by reading the section [Reading TiFlash with TiDB](/tiflash/use-tiflash.md#use-tidb-to-read-tiflash-replicas) as a query engine.

## Read more

- [Quick Start Guide for TiDB HTAP](/quick-start-with-htap.md)
- [Explore HTAP](/explore-htap.md)
- [Window Functions](/functions-and-operators/window-functions.md)
- [Use TiFlash](/tiflash/use-tiflash.md)
