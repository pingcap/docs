---
title: SHOW TABLE DISTRIBUTION
summary: TiDB 数据库中 SHOW TABLE DISTRIBUTION 的用法概述。
---

# SHOW TABLE DISTRIBUTION <span class="version-mark">New in v8.5.4</span>

`SHOW TABLE DISTRIBUTION` 语句用于显示指定表的 Region 分布信息。

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 此功能不适用于 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群。

</CustomContent>

## 语法

```ebnf+diagram
ShowTableDistributionStmt ::=
    "SHOW" "TABLE" TableName "DISTRIBUTIONS"

TableName ::=
    (SchemaName ".")? Identifier
```

## 示例

显示表 `t` 的 Region 分布信息：

```sql
CREATE TABLE `t` (
  `a` int DEFAULT NULL,
  `b` int DEFAULT NULL,
  KEY `idx` (`b`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin 
PARTITION BY RANGE (`a`)
(PARTITION `p1` VALUES LESS THAN (10000),
 PARTITION `p2` VALUES LESS THAN (MAXVALUE));
SHOW TABLE t DISTRIBUTIONS;
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

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

- [`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md)
- [`SHOW DISTRIBUTION JOBS`](/sql-statements/sql-statement-show-distribution-jobs.md)
- [`CANCEL DISTRIBUTION JOB`](/sql-statements/sql-statement-cancel-distribution-job.md)