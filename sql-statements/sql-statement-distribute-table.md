---
title: DISTRIBUTE TABLE
summary: An overview of the usage of DISTRIBUTE TABLE for the TiDB database.
---

# DISTRIBUTE TABLE

The `DISTRIBUTE TABLE` statement redistributes and reschedules Regions of a specified table to achieve a balanced distribution at the table level. Executing this statement helps prevent Regions from being concentrated on a few TiFlash or TiKV nodes, addressing the issue of uneven region distribution in the table.

## Syntax

```ebnf+diagram
DistributeTableStmt ::=
    "DISTRIBUTE"  "TABLE" TableName PartitionNameList?  EngineOption? RoleOption?

TableName ::=
    (SchemaName ".")? Identifier

PartitionNameList ::=
    "PARTITION" "(" PartitionName ("," PartitionName)* ")"

EngineOption ::=
    "ENGINE" Expression

RoleOption ::=
    "Role" Expression
```

## Examples

When redistributing Regions using the `DISTRIBUTE TABLE` statement, you can specify the storage engine (such as TiFlash or TiKV) and different Raft roles (such as Leader, Learner, or Voter) for balanced distribution.

Redistribute the Regions of the Leaders in the table `t1` on TiKV:

```sql
CREATE TABLE t1 (a INT);
...
DISTRIBUTE TABLE t1 engine tikv role leader
```

```
+---------+
| JOB_ID  |
100
+---------+
```

Redistribute the Regions of the Learners in the table `t2` on TiFlash:

```sql
CREATE TABLE t2 (a INT);
...
DISTRIBUTE TABLE t2 ENGINE tiflash role learner;
```

```
+---------+
| JOB_ID  |
101
+---------+
```

Redistribute the Regions of the Leaders in the table `t3`'s `p1` and `p2` partitions on TiKV:

```sql
CREATE TABLE t3 (a INT);
...
DISTRIBUTE TABLE t3 PARTITION (p1, p2) ENGINE tikv role leader;
```

```
+---------+
| JOB_ID  |
102
+---------+
```

Execute the [`SHOW DISTRIBUTION JOBS`](/sql-statements/sql-statement-show-distribution-jobs.md) statement to view all distribution jobs:

```sql
SHOW DISTRIBUTION JOBS;
```

```
+---------+------------+------------+-----------------+------------+-----------+----------+-------------+---------------+
| JOB_ID  |  DB_NAME   | TABLE_NAME | PARTITION_NAMES | ENGINE_TYPE | ROLE_TYPE | STATUS  | CREATE_USER | CREATE_TIME   |
+---------+------------+------------+-----------------+------------+-----------+--------+---------------+---------------+
|    1    |   db_1     |    t1      |                 | TIKV       | LEADER    | RUNNING  | ADMIN       | 20240712      |
|    2    |   db_1     |    t2      |                 | TIFLASH    | LEARNER   | FINISHED | ADMIN       | 20240715      |
|    3    |   db_1     |    t3      |                 | TiKV       | VOTER     | STOPPED  | ADMIN       | 20240713      |
|    4    |   db_1     |    t4      |                 | TIFLASH    | LEARNER   | FINISHED | ADMIN       | 20240713      |
+---------+------------+------------+-----------------+------------+-----------+----------+-------------+---------------+
```

Execute the [`SHOW TABLE DISTRIBUTION`](/sql-statements/sql-statement-show-table-distribution.md) statement to view the Region distribution of the table `t1`:

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

## Notes

When you execute the `DISTRIBUTE TABLE` statement to redistribute Regions of a table, the Region distribution result might be affected by the PD hotspot scheduler. After the redistribution, the Region distribution of this table might become imbalanced again over time.

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

- [`SHOW DISTRIBUTION JOBS`](/sql-statements/sql-statement-show-distribution-jobs.md)
- [`SHOW TABLE DISTRIBUTION`](/sql-statements/sql-statement-show-table-distribution.md)
- [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)