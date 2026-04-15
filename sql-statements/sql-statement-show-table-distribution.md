---
title: SHOW TABLE DISTRIBUTION
summary: TiDBデータベースにおけるSHOW TABLE DISTRIBUTIONの使用方法の概要。
---

# 表の分布を表示する<span class="version-mark">（v8.5.4の新機能）</span> {#show-table-distribution-span-class-version-mark-new-in-v8-5-4-span}

`SHOW TABLE DISTRIBUTION`ステートメントは、指定されたテーブルのリージョン分布情報を表示します。

<CustomContent platform="tidb-cloud">

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

</CustomContent>

## あらすじ {#synopsis}

```ebnf+diagram
ShowTableDistributionStmt ::=
    "SHOW" "TABLE" TableName "DISTRIBUTIONS"

TableName ::=
    (SchemaName ".")? Identifier
```

## 例 {#examples}

テーブル`t`のリージョン分布を表示します。

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

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文に対するTiDBの拡張機能です。

## 関連項目 {#see-also}

-   [`DISTRIBUTE TABLE`](/sql-statements/sql-statement-distribute-table.md)
-   [`SHOW DISTRIBUTION JOBS`](/sql-statements/sql-statement-show-distribution-jobs.md)
-   [`CANCEL DISTRIBUTION JOB`](/sql-statements/sql-statement-cancel-distribution-job.md)
