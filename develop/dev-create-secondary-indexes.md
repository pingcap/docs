---
title: Create Secondary Indexes
summary: The ways, best practices and examples for creating secondary indexes.
---

# Create Secondary Indexes

Indexes are logical objects in a cluster that help TiDB cluster queries find data more efficiently. When you create a secondary index, TiDB creates a reference to each row in the table and sorts it by the selected column. More information about secondary indexes can be found in [TiDB Best Practices](/best-practices/tidb-best-practices.md#secondary-index).

This page provides a best practice guide for creating secondary indexes and provides an example of a TiDB-based [bookshop](/develop/dev-bookshop-schema-design.md) database.

## Before you start

Before reading this page, you need to prepare the following:

- [Build a TiDB Cluster in TiDB Cloud(DevTier)](/develop/dev-build-cluster-in-cloud.md).
- Read [Schema Design Overview](/develop/dev-schema-design-overview.md).
- [Create a Database](/develop/dev-create-database.md).
- [Create a Table](/develop/dev-create-table.md)。

## How to create secondary index

### Adding a secondary index to an existing table

If you need to add a secondary index to an existing table, you can use the [CREATE INDEX](/common/sql-statements/sql-statement-create-index.md) statement. In TiDB, `CREATE INDEX` is an online operation, it indicated the statement does not block data reads or writes to the table. Secondary indexes are typically created in the following form.

{{< copyable "sql" >}}

```sql
CREATE INDEX {index_name} ON {table_name} ({column_names});
```

|      Parameter      |               Description               |
| :--------------: | :----------------------------------: |
|  `{index_name}`  |              Secondary Index Name              |
|  `{table_name}`  |                 Table name                 |
| `{column_names}` | List the names of the columns to be indexed, separated by semi-colon commas |

### Create a secondary index while creating a new table

If you want to create a secondary index at the same time as the table, use a clause containing the KEY keyword at the end of [CREATE TABLE](/common/sql-statements/sql-statement-create-table.md) to create the secondary index:

{{< copyable "sql" >}}

```sql
KEY `{index_name}` (`{column_names}`)
```

|      Parameter      |               Description               |
| :--------------: | :----------------------------------: |
|  `{index_name}`  |              Secondary Index Name              |
| `{column_names}` | List the names of the columns to be indexed, separated by semi-colon commas |

## Best Practices

Please refer to the [Best Practices for Indexing](/develop/dev-index-best-practice.md).

## Example

Suppose you want the `bookshop` application to have the ability to **search for all books published in a given year**. Our `books` table looks like this:

| Field name   | Type          | Explain                                                          |
|--------------|---------------|------------------------------------------------------------------|
| id           | bigint(20)    | Unique ID of the book                                            |
| title        | varchar(100)  | Book title                                                       |
| type         | enum          | Types of books (eg: magazines / animation / teaching aids, etc.) |
| stock        | bigint(20)    | Stock                                                            |
| price        | decimal(15,2) | Price                                                            |
| published_at | datetime      | Date of publish                                                  |

{{< copyable "sql" >}}

```sql
CREATE TABLE `bookshop`.`books` (
  `id` bigint(20) AUTO_RANDOM NOT NULL,
  `title` varchar(100) NOT NULL,
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports') NOT NULL,
  `published_at` datetime NOT NULL,
  `stock` int(11) DEFAULT '0',
  `price` decimal(15,2) DEFAULT '0.0',
  PRIMARY KEY (`id`) CLUSTERED
) DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

Then we need to write the SQL for **search for all books published in a given year**, using 2022 as an example, as follows:

{{< copyable "sql" >}}

```sql
SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

We can use [EXPLAIN](/common/sql-statements/sql-statement-explain.md) to check the execution plan of a SQL statement.

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT * FROM `bookshop`.`books` WHERE `published_at` >= '2022-01-01 00:00:00' AND `published_at` < '2023-01-01 00:00:00';
```

Running results:

```
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
| id                      | estRows  | task      | access object | operator info                                                                                                            |
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
| TableReader_7           | 346.32   | root      |               | data:Selection_6                                                                                                         |
| └─Selection_6           | 346.32   | cop[tikv] |               | ge(bookshop.books.published_at, 2022-01-01 00:00:00.000000), lt(bookshop.books.published_at, 2023-01-01 00:00:00.000000) |
|   └─TableFullScan_5     | 20000.00 | cop[tikv] | table:books   | keep order:false                                                                                                         |
+-------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------------------+
3 rows in set (0.61 sec)
```

You can see something like **TableFullScan** in the returned plan, which means TiDB is ready to do a full table scan of the `books` table in this query, which can be almost fatal in the case of a large amount of data.

So we need to add an index to the `books` table for the `published_at` column.

{{< copyable "sql" >}}

```sql
CREATE INDEX `idx_book_published_at` ON `bookshop`.`books` (`bookshop`.`books`.`published_at`);
```

After adding the index, run the `EXPLAIN` statement again to check the execution plan.

```
+-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
| id                            | estRows | task      | access object                                          | operator info                                                     |
+-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
| IndexLookUp_10                | 146.01  | root      |                                                        |                                                                   |
| ├─IndexRangeScan_8(Build)     | 146.01  | cop[tikv] | table:books, index:idx_book_published_at(published_at) | range:[2022-01-01 00:00:00,2023-01-01 00:00:00), keep order:false |
| └─TableRowIDScan_9(Probe)     | 146.01  | cop[tikv] | table:books                                            | keep order:false                                                  |
+-------------------------------+---------+-----------+--------------------------------------------------------+-------------------------------------------------------------------+
3 rows in set (0.18 sec)
```

Instead of **TableFullScan** in the execution plan, you can see **IndexRangeScan**, which means that TiDB is ready to use indexes when doing this query.

> **Note:**
>
> The **TableFullScan**, **IndexRangeScan**, etc. in the execution plan above are called [operators](/explain-overview.md#operator-overview) within TiDB. If you are interested, you can go to the [TiDB Query Execution Plan Overview](/explain-overview.md) document to learn more about execution plans and operators.
>
> The execution plan does not return the same operator every time, because TiDB uses a **Cost-Based Optimization (CBO)** approach. It means execution plan is not only rule-dependent, but also data distribution-dependent. You can go to the [SQL Tuning Overview](/sql-tuning-overview.md) documentation for a more detailed description of TiDB SQL performance.
>
> TiDB also supports explicit use of indexes when querying, and you can use [Optimizer Hints](/optimizer-hints.md) or [SQL Plan Management (SPM)](/sql-plan-management.md) to artificially control the use of indexes. But if you don't understand what's going on inside it, please **_don't use it yet_**.

We can query the indexes in the table using the [SHOW INDEXES](/common/sql-statements/sql-statement-show-indexes.md) statement:

{{< copyable "sql" >}}

```sql
SHOW INDEXES FROM `bookshop`.`books`;
```

Running result:

```
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| Table | Non_unique | Key_name              | Seq_in_index | Column_name  | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression | Clustered |
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
| books |          0 | PRIMARY               |            1 | id           | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | YES       |
| books |          1 | idx_book_published_at |            1 | published_at | A         |           0 |     NULL | NULL   |      | BTREE      |         |               | YES     | NULL       | NO        |
+-------+------------+-----------------------+--------------+--------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------+
2 rows in set (1.63 sec)
```

At this point, you have completed the creation of the **database**, **tables**, and **secondary indexes**. Next, the database schema is ready to give your application the ability to [write](/develop/dev-insert-data.md) to and [read](/develop/dev-get-data-from-single-table.md) from it.
