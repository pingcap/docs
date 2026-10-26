---
title: TiFlash Late Materialization
summary: Describe how to use the TiFlash late materialization feature to accelerate queries in OLAP scenarios.
---

# TiFlash Late Materialization

> **Note:**
>
> TiFlash late materialization does not take effect in the [fast scan mode](/tiflash/use-fastscan.md).

TiFlash late materialization is an optimization method to accelerate queries in OLAP scenarios. You can use the [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700) system variable to control whether to enable or disable TiFlash late materialization.

- When it is disabled, to process a `SELECT` statement with filter conditions (`WHERE` clause), TiFlash reads all the data from the columns required by the query, and then filters and aggregates the data based on the query conditions.
- When it is enabled, TiFlash supports pushing down part of the filter conditions to the TableScan operator. That is, TiFlash first scans the column data related to the filter conditions that are pushed down to the TableScan operator, filters the rows that meet the condition, and then scans the other column data of these rows for further calculation, thereby reducing IO scans and computations of data processing.

To improve the performance of certain queries in OLAP scenarios, starting from v7.1.0, the TiFlash late materialization feature is enabled by default. The TiDB optimizer can determine which filter conditions to be pushed down based on statistics and filter conditions, and prioritize pushing down the filter conditions with high filtration rates. For detailed algorithms, see the [RFC document](https://github.com/pingcap/tidb/tree/master/docs/design/2022-12-06-support-late-materialization.md).

For example:

```sql
EXPLAIN SELECT a, b, c FROM t1 WHERE a < 1;
```

```
+-------------------------+----------+--------------+---------------+-------------------------------------------------------+
| id                      | estRows  | task         | access object | operator info                                         |
+-------------------------+----------+--------------+---------------+-------------------------------------------------------+
| TableReader_12          | 12288.00 | root         |               | MppVersion: 1, data:ExchangeSender_11                 |
| └─ExchangeSender_11     | 12288.00 | mpp[tiflash] |               | ExchangeType: PassThrough                             |
|   └─TableFullScan_9     | 12288.00 | mpp[tiflash] | table:t1      | pushed down filter:lt(test.t1.a, 1), keep order:false |
+-------------------------+----------+--------------+---------------+-------------------------------------------------------+
```

In this example, the filter condition `a < 1` is pushed down to the TableScan operator. TiFlash first reads all data from column `a`, and then filters the rows that meet the `a < 1` condition. Next, TiFlash reads columns `b` and `c` from these filtered rows.

## Enable or disable TiFlash late materialization

By default, the `tidb_opt_enable_late_materialization` system variable is `ON` at both the session and global levels, which means that the TiFlash late materialization feature is enabled. You can use the following statement to view the corresponding variable information:

```sql
SHOW VARIABLES LIKE 'tidb_opt_enable_late_materialization';
```

```
+--------------------------------------+-------+
| Variable_name                        | Value |
+--------------------------------------+-------+
| tidb_opt_enable_late_materialization | ON    |
+--------------------------------------+-------+
```

```sql
SHOW GLOBAL VARIABLES LIKE 'tidb_opt_enable_late_materialization';
```

```
+--------------------------------------+-------+
| Variable_name                        | Value |
+--------------------------------------+-------+
| tidb_opt_enable_late_materialization | ON    |
+--------------------------------------+-------+
```

You can modify the `tidb_opt_enable_late_materialization` variable at the session level or at the global level.

- To disable TiFlash late materialization in the current session, use the following statement:

    ```sql
    SET SESSION tidb_opt_enable_late_materialization=OFF;
    ```

- To disable TiFlash late materialization at the global level, use the following statement:

    ```sql
    SET GLOBAL tidb_opt_enable_late_materialization=OFF;
    ```

    After this setting, the `tidb_opt_enable_late_materialization` variable will be enabled by default for both session and global levels in new sessions.

To enable TiFlash late materialization, use the following statements:

```sql
SET SESSION tidb_opt_enable_late_materialization=ON;
```

```sql
SET GLOBAL tidb_opt_enable_late_materialization=ON;
```

## Specify filter columns with a hint

To control which filter conditions are evaluated during late materialization, use the [`TIFLASH_LM_FILTER`](/optimizer-hints.md#tiflash_lm_filtert1_name-col1_name--col2_name-) optimizer hint. This hint is useful when the optimizer's cost-based selection does not choose the desired filter conditions.

Before using the hint, ensure that the table has an [available TiFlash replica](/tiflash/create-tiflash-replicas.md#check-replication-progress) and that `tidb_opt_enable_late_materialization` is `ON`.

For example, for a table `t1` with integer columns `a`, `b`, and `c`, you can push the filter condition `a + b > 100` down to the TableScan operator while keeping `c IN (1, 2, 3)` in the Selection operator:

```sql
SET SESSION tidb_opt_enable_late_materialization = ON;

EXPLAIN SELECT /*+ READ_FROM_STORAGE(TIFLASH[t1]), TIFLASH_LM_FILTER(t1, a, b) */
    * FROM t1 WHERE a + b > 100 AND c IN (1, 2, 3);
```

The hint lists both columns referenced by `a + b > 100`, so TiFlash evaluates this condition during late materialization. TiFlash first reads columns `a` and `b`, filters the rows, and then reads column `c` for the surviving rows. The condition on `c` remains in the Selection operator because `c` is not listed in the hint. `READ_FROM_STORAGE(TIFLASH[t1])` requests a TiFlash scan; `TIFLASH_LM_FILTER` controls only the late materialization filters.

In the `EXPLAIN` output, check for `pushed down filter:gt(plus(test.t1.a, test.t1.b), 100)` in the TableFullScan operator and the condition on `c` in the Selection operator. The database qualifier depends on the database containing `t1`.

To select only a filter on a single column, list that column:

```sql
EXPLAIN SELECT /*+ READ_FROM_STORAGE(TIFLASH[t1]), TIFLASH_LM_FILTER(t1, a) */
    * FROM t1 WHERE a > 1 AND b > 1;
```

In this example, `a > 1` is evaluated during late materialization, and `b > 1` remains in the Selection operator. A condition that references multiple columns must have all those columns listed in the hint. For example, listing only `a` does not select `a + b > 100` for late materialization.

The hint replaces cost-based late materialization filter selection for the scan, including on small tables. If no filter conditions match the listed columns, TiDB does not select other late materialization filters automatically. The hint still requires late materialization to be enabled and does not take effect for scans that preserve order (`keep order:true`) or in fast scan mode. For query-block syntax and warnings, see [`TIFLASH_LM_FILTER`](/optimizer-hints.md#tiflash_lm_filtert1_name-col1_name--col2_name-).

## Implementation mechanism

When filter conditions are pushed down to the TableScan operator, the execution process of the TableScan operator mainly includes the following steps:

1. Reads the three columns `<handle, del_mark, version>`, performs multi-version concurrency control (MVCC) filtering, and then generates the MVCC Bitmap.
2. Reads the columns related to the filter conditions, filters the rows that meet the conditions, and then generates the Filter Bitmap.
3. Performs an `AND` operation between the MVCC Bitmap and Filter Bitmap to generate the Final Bitmap.
4. Reads the corresponding rows of the remaining columns according to the Final Bitmap.
5. Merges the data read in steps 2 and 4, and then returns the results.
