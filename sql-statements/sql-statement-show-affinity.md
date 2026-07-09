---
title: SHOW AFFINITY
summary: An overview of the usage of SHOW AFFINITY for the TiDB database.
---

# SHOW AFFINITY <span class="version-mark">New in v8.5.5 and v9.0.0</span>

The `SHOW AFFINITY` statement shows [affinity](/table-affinity.md) scheduling information for tables configured with the `AFFINITY` option, as well as the target replica distribution currently recorded by PD.

## Synopsis

```ebnf+diagram
ShowAffinityStmt ::=
    "SHOW" "AFFINITY" ShowLikeOrWhereOpt
```

`SHOW AFFINITY` supports filtering table names using `LIKE` or `WHERE` clauses.

## Examples

The following examples create two tables with affinity scheduling enabled and show how to view their scheduling information:

```sql
CREATE TABLE t1 (a INT) AFFINITY = 'table';
CREATE TABLE tp1 (a INT) AFFINITY = 'partition' PARTITION BY HASH(a) PARTITIONS 2;

SHOW AFFINITY;
```

The example output is as follows:

```sql
+---------+------------+----------------+-----------------+------------------+----------+--------------+----------------------+
| Db_name | Table_name | Partition_name | Leader_store_id | Voter_store_ids  | Status   | Region_count | Affinity_region_count|
+---------+------------+----------------+-----------------+------------------+----------+--------------+----------------------+
| test    | t1         | NULL           | 1               | 1,2,3            | Stable   |            8 |                    8 |
| test    | tp1        | p0             | 4               | 4,5,6            | Preparing|            4 |                    2 |
| test    | tp1        | p1             | 4               | 4,5,6            | Preparing|            3 |                    2 |
+---------+------------+----------------+-----------------+------------------+----------+--------------+----------------------+
```

The meaning of each column is as follows:

- `Leader_store_id`, `Voter_store_ids`: the IDs of TiKV stores recorded by PD, indicating which stores host the target Leader and Voter replicas for the table or partitions. If the target replica locations for the affinity group are not determined, or if [`schedule.affinity-schedule-limit`](/pd-configuration-file.md#affinity-schedule-limit-new-in-v855-and-v900) is set to `0`, the value is displayed as `NULL`.
- `Status`: indicates the current status of affinity scheduling. Possible values are:
    - `Pending`: PD has not started affinity scheduling for the table or partition, such as when Leaders or Voters are not yet determined.
    - `Preparing`: PD is scheduling Regions to meet affinity requirements.
    - `Stable`: all Regions have reached the target distribution.
- `Region_count`: the current number of Regions in the affinity group.
- `Affinity_region_count`: the number of Regions that currently meet the affinity replica distribution requirements.
    - When `Affinity_region_count` is less than `Region_count`, it indicates that some Regions have not yet completed replica scheduling based on affinity.
    - When `Affinity_region_count` equals `Region_count`, it indicates that replica scheduling based on affinity is complete, meaning the distribution of all related Regions meets the affinity requirements. However, this does not indicate that related Region merge operations are complete.

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

- [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)
- [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)