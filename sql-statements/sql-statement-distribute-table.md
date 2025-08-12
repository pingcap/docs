---
title: DISTRIBUTE TABLE
summary: An overview of the usage of DISTRIBUTE TABLE for the TiDB database.
---

# DISTRIBUTE TABLE

<span class="version-mark">New in v9.0.0</span>

> **Warning:**
>
> - This feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.
> - This feature is not available on [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) clusters.

The `DISTRIBUTE TABLE` statement redistributes and reschedules Regions of a specified table to achieve a balanced distribution at the table level. Executing this statement helps prevent Regions from being concentrated on a few TiFlash or TiKV nodes, addressing the issue of uneven region distribution in the table.

## Synopsis

```ebnf+diagram
DistributeTableStmt ::=
    "DISTRIBUTE" "TABLE" TableName PartitionNameListOpt "RULE" EqOrAssignmentEq Identifier "ENGINE" EqOrAssignmentEq Identifier "TIMEOUT" EqOrAssignmentEq Identifier

TableName ::=
    (SchemaName ".")? Identifier

PartitionNameList ::=
    "PARTITION" "(" PartitionName ("," PartitionName)* ")"
```

## Parameter description

When redistributing Regions in a table using the `DISTRIBUTE TABLE` statement, you can specify the storage engine (such as TiFlash or TiKV) and different Raft roles (such as Leader, Learner, or Voter) for balanced distribution.

- `RULE`: specifies which Raft role's Region to balance and schedule. Optional values are `"leader-scatter"`, `"peer-scatter"`, and `"learner-scatter"`.
- `ENGINE`: specifies the storage engine. Optional values are `"tikv"` and `"tiflash"`.
- `TIMEOUT`: specifies the timeout limit for the scatter operation. If PD does not complete the scatter within this time, the scatter task will automatically exit. When this parameter is not specified, the default value is `"30m"`.

## Examples

Redistribute the Regions of the Leaders in the table `t1` on TiKV:

```sql
CREATE TABLE t1 (a INT);
...
DISTRIBUTE TABLE t1 RULE = "leader-scatter" ENGINE = "tikv" TIMEOUT = "1h";
```

```
+--------+
| JOB_ID |
+--------+
|    100 |
+--------+
```

Redistribute the Regions of the Learners in the table `t2` on TiFlash:

```sql
CREATE TABLE t2 (a INT);
...
DISTRIBUTE TABLE t2 RULE = "learner-scatter" ENGINE = "tiflash";
```

```
+--------+
| JOB_ID |
+--------+
|    101 |
+--------+
```

Redistribute the Regions of the Peers in the table `t3`'s `p1` and `p2` partitions on TiKV:

```sql
CREATE TABLE t3 ( a INT, b INT, INDEX idx(b)) PARTITION BY RANGE( a ) (
    PARTITION p1 VALUES LESS THAN (10000),
    PARTITION p2 VALUES LESS THAN (20000),
    PARTITION p3 VALUES LESS THAN (MAXVALUE) );
...
DISTRIBUTE TABLE t3 PARTITION (p1, p2) RULE = "peer-scatter" ENGINE = "tikv";
```

```
+--------+
| JOB_ID |
+--------+
|    102 |
+--------+
```

Redistribute the Regions of the Learner in the table `t4`'s `p1` and `p2` partitions on TiFlash:

```sql
CREATE TABLE t4 ( a INT, b INT, INDEX idx(b)) PARTITION BY RANGE( a ) (
    PARTITION p1 VALUES LESS THAN (10000),
    PARTITION p2 VALUES LESS THAN (20000),
    PARTITION p3 VALUES LESS THAN (MAXVALUE) );
...
DISTRIBUTE TABLE t4 PARTITION (p1, p2) RULE = "learner-scatter" ENGINE="tiflash";
```

```
+--------+
| JOB_ID |
+--------+
|    103 |
+--------+
```

## Notes

When you execute the `DISTRIBUTE TABLE` statement to redistribute Regions of a table, the Region distribution result might be affected by the PD hotspot scheduler. After the redistribution, the Region distribution of this table might become imbalanced again over time.

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

- [`SHOW DISTRIBUTION JOBS`](/sql-statements/sql-statement-show-distribution-jobs.md)
- [`SHOW TABLE DISTRIBUTION`](/sql-statements/sql-statement-show-table-distribution.md)
- [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)
- [`CANCEL DISTRIBUTION JOB`](/sql-statements/sql-statement-cancel-distribution-job.md)