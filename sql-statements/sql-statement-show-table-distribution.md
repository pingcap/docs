---
title: SHOW TABLE DISTRIBUTION
summary: An overview of the usage of SHOW TABLE DISTRIBUTION for the TiDB database.
---

# SHOW TABLE DISTRIBUTION

The `SHOW TABLE DISTRIBUTION` statement shows the Region distribution information for a specified table.

## Syntax

```ebnf+diagram
ShowTableDistributionStmt ::=
    "SHOW" "TABLE" "DISTRIBUTION" TableName

TableName ::=
    (SchemaName ".")? Identifier
```

## Examples

Show the Region distribution of the table `t1`:

```sql
SHOW TABLE DISTRIBUTION t1;
```

```
+---------+------------+----------------+----------+------------+-------------------+--------------------+-----------------+------------------+
| DB_NAME | TABLE_NAME | PARTITION_NAME | STORE_ID | STORE_TYPE | REGION_LEADER_NUM | REGION_LEADER_BYTE | REGION_PEER_NUM | REGION_PEER_BYTE |
+---------+------------+----------------+----------+------------+-------------------+--------------------+-----------------+------------------+
| db_1    |     t1     |                | 1        | TiKV       |               315 |        24057934521 |            1087 |      86938746542 |
| db_1    |     t1     |                | 2        | TiKV       |               324 |        28204839240 |            1104 |      91039476832 |
| db_1    |     t1     |                | 3        | TiKV       |               319 |        25986274812 |            1091 |      89405367423 |
| db_1    |     t1     |                | 4        | TiKV       |               503 |        41039587625 |            1101 |      90482317797 |
+---------+------------+----------------+----------+------------+-------------------+--------------------+-----------------+------------------+
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

- [`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md)
- [`SHOW DISTRIBUTION JOBS`](/sql-statements/sql-statement-show-distribution-jobs.md)