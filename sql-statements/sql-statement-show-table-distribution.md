---
title: SHOW TABLE DISTRIBUTION
summary: An overview of the usage of SHOW TABLE DISTRIBUTION for the TiDB database.
---

# SHOW TABLE DISTRIBUTION

<!-- New in v9.0.0 -->

The `SHOW TABLE DISTRIBUTION` statement shows the Region distribution information for a specified table.

## Synopsis

```ebnf+diagram
ShowTableDistributionStmt ::=
    "SHOW" "TABLE" TableName "DISTRIBUTIONS"

TableName ::=
    (SchemaName ".")? Identifier
```

## Examples

Show the Region distribution of the table `t1`:

```sql
CREATE TABLE `t` (
  `a` int DEFAULT NULL,
  `b` int DEFAULT NULL,
  KEY `idx` (`b`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin 
PARTITION BY RANGE (`a`)
(PARTITION `p1` VALUES LESS THAN (10000),
 PARTITION `p2` VALUES LESS THAN (MAXVALUE)) |
SHOW TABLE t1 DISTRIBUTIONS;
```

```
+----------------+----------+------------+---------------------+-------------------+--------------------+-------------------+--------------------+--------------------------+-------------------------+--------------------------+------------------------+-----------------------+------------------------+
| PARTITION_NAME | STORE_ID | STORE_TYPE | REGION_LEADER_COUNT | REGION_PEER_COUNT | REGION_WRITE_BYTES | REGION_WRITE_KEYS | REGION_WRITE_QUERY | REGION_LEADER_READ_BYTES | REGION_LEADER_READ_KEYS | REGION_LEADER_READ_QUERY | REGION_PEER_READ_BYTES | REGION_PEER_READ_KEYS | REGION_PEER_READ_QUERY |
+----------------+----------+------------+---------------------+-------------------+--------------------+-------------------+--------------------+--------------------------+-------------------------+--------------------------+------------------------+-----------------------+------------------------+
| p1             |        1 | tikv       |                   0 |                 0 |                  0 |                 0 |                  0 |                        0 |                       0 |                        0 |                      0 |                     0 |                      0 |
| p1             |       15 | tikv       |                   0 |                 0 |                  0 |                 0 |                  0 |                        0 |                       0 |                        0 |                      0 |                     0 |                      0 |
| p1             |        4 | tikv       |                   1 |                 1 |                  0 |                 0 |                  0 |                        0 |                       0 |                        0 |                      0 |                     0 |                      0 |
| p1             |        5 | tikv       |                   0 |                 1 |                  0 |                 0 |                  0 |                        0 |                       0 |                        0 |                      0 |                     0 |                      0 |
| p1             |        6 | tikv       |                   0 |                 1 |                  0 |                 0 |                  0 |                        0 |                       0 |                        0 |                      0 |                     0 |                      0 |
| p2             |        1 | tikv       |                   0 |                 0 |                  0 |                 0 |                  0 |                        0 |                       0 |                        0 |                      0 |                     0 |                      0 |
| p2             |       15 | tikv       |                   0 |                 0 |                  0 |                 0 |                  0 |                        0 |                       0 |                        0 |                      0 |                     0 |                      0 |
| p2             |        4 | tikv       |                   0 |                 1 |                  0 |                 0 |                  0 |                        0 |                       0 |                        0 |                      0 |                     0 |                      0 |
| p2             |        5 | tikv       |                   1 |                 1 |                  0 |                 0 |                  0 |                        0 |                       0 |                        0 |                      0 |                     0 |                      0 |
| p2             |        6 | tikv       |                   0 |                 1 |                  0 |                 0 |                  0 |                        0 |                       0 |                        0 |                      0 |                     0 |                      0 |
+----------------+----------+------------+---------------------+-------------------+--------------------+-------------------+--------------------+--------------------------+-------------------------+--------------------------+------------------------+-----------------------+------------------------+
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

- [`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md)
- [`SHOW DISTRIBUTION JOBS`](/sql-statements/sql-statement-show-distribution-jobs.md)
- [`CANCEL DISTRIBUTION JOB`](/sql-statements/sql-statement-cancel-distribution-job.md)