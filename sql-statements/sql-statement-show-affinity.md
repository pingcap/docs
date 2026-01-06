---
title: SHOW AFFINITY
summary: Overview of using SHOW AFFINITY in TiDB database.
---

# SHOW AFFINITY <span class="version-mark">Introduced in v8.5.5 and v9.0.0</span>

The `SHOW AFFINITY` statement is used to view the [affinity](/table-affinity.md) scheduling information of tables configured with the `AFFINITY` option, and the target replica distribution currently recorded by PD.

## Grammar Diagram

```ebnf+diagram
ShowAffinityStmt ::=
    "SHOW" "AFFINITY" ShowLikeOrWhereOpt
```

`SHOW AFFINITY` supports filtering table names using `LIKE` or `WHERE` clauses.

## Examples

The following examples create two tables with affinity scheduling enabled and view their scheduling information:

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

- `Leader_store_id`, `Voter_store_ids`: The TiKV Store IDs where PD records the target Leader replica and Voter replicas for this table or partition. If the affinity group has not yet determined the target replica locations or if [`schedule.affinity-schedule-limit`](/pd-configuration-file.md#affinity-schedule-limit-从-v855-和-v900-版本开始引入) is `0`, it displays as `NULL`.
- `Status`: Indicates the current status of affinity scheduling. Possible values are:
    - `Pending`: PD has not yet performed affinity scheduling for this table or partition (e.g., when Leader or Voter is not determined).
    - `Preparing`: PD is scheduling Regions to meet affinity requirements.
    - `Stable`: All Regions have reached the target distribution.
- `Region_count`: The current number of Regions in this affinity group.
- `Affinity_region_count`: The number of Regions that currently satisfy the affinity replica distribution requirements.
    - When `Affinity_region_count` is less than `Region_count`, it indicates that some Regions have not yet completed replica scheduling based on affinity.
    - When `Affinity_region_count` equals `Region_count`, it indicates that the Region replica migration scheduling based on affinity is complete, meaning that the distribution of all Regions meets the affinity requirements. However, this does not imply that related Region merge operations are complete.

## MySQL Compatibility

This statement is an extension of MySQL syntax by TiDB.

## See Also

- [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)
- [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md)