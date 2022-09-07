---
title: Introduction to Extended Statistics
summary: Learn how to use extended statistics to guide the optimizer.
---

# Introduction to Extended Statistics

TiDB can collect the following two types of statistics:

- Regular statistics: statistics such as histograms and Count-Min Sketch. See [Introduction to Statistics](/statistics.md) for details.
- Extended statistics: statistics filtered by tables and columns.

Because the extended statistics are only used for optimizer estimates in specific scenarios, when the `ANALYZE` statement is executed manually or automatically, to reduce the overhead of managing statistics, TiDB only collects the regular statistics and does not collect the extended statistics by default.

Extended statistics are disabled by default. To collect extended statistics, you need to enable and register the extended statistics first.

After the registration, the next time the `ANALYZE` statement is executed manually or automatically, TiDB collects both the regular statistics and the registered extended statistics.

## Limitations

Extended statistics are not collected in the following scenarios:

- Statistics collection on indexes only
- Statistics collection with the `ANALYZE INCREMENTAL` command
- Statistics collection with the value of the `tidb_enable_fast_analyze` system variable set to `true`

## Common operations

### Enable extended statistics

To enable extended statistics, set the system variable `tidb_enable_extended_stats` to `ON`:

```sql
SET GLOBAL tidb_enable_extended_stats = ON;
```

The default value of this variable is `OFF`.

### Register extended statistics

To register the extended statistics, use the SQL statement `ALTER TABLE ADD STATS_EXTENDED`. The syntax is as follows:

```sql
ALTER TABLE table_name ADD STATS_EXTENDED IF NOT EXISTS stats_name stats_type(column_name, column_name...);
```

In the statement, you can specify the table name, statistics type, statistics type, and column name of the extended statistics to be collected.

- `table_name` specifies the name of the table from which the extended statistics are collected.
- `stats_name` specifies the name of the statistics, which must be unique for each table.
- `stats_type` specifies the type of the statistics. Currently, only the correlation type is supported.
- `column_name` specifies the column group, which might have multiple columns. Currently, you can only specify two column names.

Each TiDB node maintains a cache in the system table `mysql.stats_extended` for extended statistics, which improve access performance. After you register the extended statistics, if the system table `mysql.stats_extended` has the corresponding records, the next time the `ANALYZE` statement is executed, TiDB will collect the extended statistics.

Each row in the `mysql.stats_extended` table records a `version` column. Once a row is updated, the value of the column `version` is increased, so that TiDB can load the table into the memory incrementally instead of fully.

TiDB loads `mysql.stats_extended` periodically to ensure that the cache is kept the same as the data in the table.

### Delete extended statistics

To delete a record of the extended statistics, use the following statement:

```sql
ALTER TABLE table_name DROP STATS_EXTENDED stats_name;
```

After you execute the statement, TiDB marks the value of the corresponding record in `mysql.stats_extended`'s column `status` to `2`, which means that the record is deleted, instead of deleting the record directly.

Other TiDB nodes will read this change and delete the record in their memory cache. The background garbage collection will delete the record eventually.

### Flush the cache of one TiDB node

It is not recommended to directly operate on the `mysql.stats_extended` system table. The direct operation on the table causes inconsistent caches on different TiDB nodes.

If you have mistakenly operated on the table, you can use the following statement on each TiDB node. Then the current cache will be cleared and the `mysql.stats_extended` table will be fully reloaded:

```sql
ADMIN RELOAD STATS_EXTENDED;
```

## Export and import extended statistics

The way of exporting or importing extended statistics is the same as the regular statistics. See [Introduction to Statistics - Import and export statistics](/statistics.md#import-and-export-statistics) for details.

## Usage scenarios and examples

Currently, only the correlation type is supported. This type is used to estimate the number of rows in the range query. The following example shows how to use the correlation type to estimate the number of rows in the range query.

The registration SQL is like the following:

{{< copyable "sql" >}}

```sql
ALTER TABLE t ADD STATS_EXTENDED s1 correlation(col1, col2);
```

When we run the `ANALYZE` after the registration, TiDB will calculate the [Pearson correlation coefficient](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient) of the `col` and `col2` of the table `t` and write the record into the table `mysql.stats_extended`.

It's used to improve TiDB's index selection for the following scenario:

For a table `t` described below：

{{< copyable "sql" >}}

```sql
CREATE TABLE t(col1 INT, col2 INT, KEY(col1), KEY(col2));
```

Suppose that the `col1` and `col2` of the table `t` both obey monotonically increasing constraints in row order, i.e., the values of `col1` and `col2` are strictly correlated in order (the value of the correlation is 1):

{{< copyable "sql" >}}

```sql
SELECT * FROM t WHERE col1 > 1 ORDER BY col2 LIMIT 1;
```

For the above query, the optimizer has two choices to access the table `t`: one uses the index on `col1` to access the table and then sorts the result by `col2` to calculate the `Top-1`. Another is that access the table by index on `col2` to meet the first row that satisfies `col1 > 1`. The latter's cost mainly depends on how many rows are filtered out when we scan the table in `col2`'s order. Usually, the optimizer can only suppose that `col1` and `col2` are independent, leading to a significant estimation error.

After the TiDB has the extended statistics for correlation, the optimizer can estimate how many rows we need to scan more precisely. Since the `col1` and `col2` are strictly correlated in order, the optimizer will equivalently translate the row count estimate for option two above into:

{{< copyable "sql" >}}

```sql
SELECT * FROM t WHERE col1 <= 1 OR col1 IS NULL;
```

The above estimation plus one will be the final estimation for the condition. This way, we don't need to use the independent assumption to get a significant estimation error.
The optimizer will use the independent assumption if the correlation factor is less than the system variable `tidb_opt_correlation_threshold`. But it will increase the estimation heuristically. The larger the system variable `tidb_opt_correlation_exp_factor` is, the larger the estimation result is. The larger the absolute value of the correlation factor is, the larger the estimation result is.


