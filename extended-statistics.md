---
title: Introduction to Extended Statistics
summary: Learn how to use extended statistics to guide the optimizer.
---

# Introduction to Extended Statistics

The statistics mentioned in the [Introduction to Statistics](/statistics.md) section, including histograms and Count-Min Sketch, are common statistics. This information is collected each time statistics are collected manually or automatically. Another class of statistics, as opposed to common statistics, is extended statistics, which are only helpful for optimizer estimation in a specific scenario.

Since they are only helpful in specific scenarios, extended statistics are not collected during the default manual or automatic `ANALYZE` to avoid the overhead of managing statistics. If you want to collect extended statistics, you need to "register" them with SQL commands first. Then TiDB will collect these registered extended statistics in addition to the common statistics the next time you manually or automatically `ANALYZE`.

# The registration of the Extended Statistics

If you want to register the extended statistics, you can use the SQL `ALTER TABLE ADD STATS_EXTENDED`. The grammar is shown below:

{{< copyable "sql" >}}

```sql
ALTER TABLE table_name ADD STATS_EXTENDED IF NOT EXISTS stats_name stats_type(column_name, column_name...);
```

This statement indicates that you want to collect the specified type of extended statistics on the specified columns of the table and name it.

- `table_name` is the table that you want to collect the extended statistics.
- `stats_name` is the name of the extended statistics. It should be unique for each table.
- `stats_type` is the type of the extended statistics. Now it only has one possible value `correlation`.
- `column_name` specifies the column group. It can be multiple columns. For `correlation` type, there should be and only be two columns.

The extended statistics will be collected if the `mysql.stats_extended` has the corresponding record when we run the `ANALYZE` command. And the `status` column will be set to `1`, and the `version` column will be set to the new timestamp.

## The type of the Extended Statistics

### Correlation

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

## The collection of the Extended Statistics

After registration, TiDB collects the extended statistic with the ANALYZE command manually or automatically, except below scenarios:

- Statistics collection on indexes only
- Statistics collection with `ANALYZE INCREMENTAL` command
- Statistics collection with variable `tidb_enable_fast_analyze` is true

## The deletion of the Extended Statistics

Each TiDB node will maintain a cache for the extended statistics to improve the efficiency of visiting the extended statistics. TiDB will load the table `mysql.stats_extended` periodically to ensure that the cache is kept the same as the data in the table. Each row in the table `mysql.stats_extended` records a column `version`. Once the row is updated, the value of the column `version` will be increased so that we can load the table into the memory incrementally instead of a full loading.

To delete a record of the extended statistics, TiDB provides the following command:

{{< copyable "sql" >}}

```sql
ALTER TABLE table_name DROP STATS_EXTENDED stats_name;
```

This command will mark the value of the corresponding record in the table `mysql.stats_extended`'s column `status` to `2`(meaning that the record is deleted) instead of deleting the record directly. Other TiDBs will read this change and delete the record in their memory cache. The background garbage collection will delete the record eventually.

Don't operate the table `mysql.stats_extended` directly. This can cause the inconsistency of the cache of each TiDB node. If you do such an operation wrongly, you can use the following command to load the data of the table fully instead of incrementally:

{{< copyable "sql" >}}

```sql
ADMIN RELOAD STATS_EXTENDED;
```

## The dump and load of the Extended Statistics

The way mentioned in the chapter [Introduction to Statistics](/statistics.md) is also suitable for extended statistics. The dump result is in the same JSON file as the normal statistics.

## The switch

You can use the following command to enable the feature: 

{{< copyable "sql" >}}

```sql
set global tidb_enable_extended_stats = on;
```

The default value of `tidb_enable_extended_stats` is `off`.
