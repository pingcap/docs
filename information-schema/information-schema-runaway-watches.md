---
title: RUNAWAY_WATCHES
summary: 了解 `RUNAWAY_WATCHES` INFORMATION_SCHEMA 表。
---

# RUNAWAY_WATCHES

`RUNAWAY_WATCHES` 表展示了消耗资源超出预期的 runaway 查询的监控列表。更多信息，参见 [Runaway Queries](/tidb-resource-control-runaway-queries.md)。

> **Note:**
>
> 该表在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。

```sql
USE INFORMATION_SCHEMA;
DESC RUNAWAY_WATCHES;
```

```sql
+---------------------+--------------+------+------+---------+-------+
| Field               | Type         | Null | Key  | Default | Extra |
+---------------------+--------------+------+------+---------+-------+
| ID                  | bigint(64)   | NO   |      | NULL    |       |
| RESOURCE_GROUP_NAME | varchar(32)  | NO   |      | NULL    |       |
| START_TIME          | varchar(32)  | NO   |      | NULL    |       |
| END_TIME            | varchar(32)  | YES  |      | NULL    |       |
| WATCH               | varchar(12)  | NO   |      | NULL    |       |
| WATCH_TEXT          | text         | NO   |      | NULL    |       |
| SOURCE              | varchar(128) | NO   |      | NULL    |       |
| ACTION              | varchar(12)  | NO   |      | NULL    |       |
| RULE                | varchar(128) | NO   |      | NULL    |       |
+---------------------+--------------+------+------+---------+-------+
9 rows in set (0.00 sec)
```

## 示例

查询 runaway 查询的监控列表：

```sql
SELECT * FROM INFORMATION_SCHEMA.RUNAWAY_WATCHES ORDER BY id\G
```

输出如下：

```sql
*************************** 1. row ***************************
                 ID: 1
RESOURCE_GROUP_NAME: default
         START_TIME: 2024-09-11 07:20:48
           END_TIME: 2024-09-11 07:30:48
              WATCH: Exact
         WATCH_TEXT: select count(*) from `tpch1`.`supplier`
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
               RULE: ProcessedKeys = 10000(100)
*************************** 2. row ***************************
                 ID: 2
RESOURCE_GROUP_NAME: default
         START_TIME: 2024-09-11 07:20:51
           END_TIME: 2024-09-11 07:30:51
              WATCH: Exact
         WATCH_TEXT: select count(*) from `tpch1`.`partsupp`
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
               RULE: RequestUnit = RRU:143.369959, WRU:0.000000, WaitDuration:0s(10)
*************************** 3. row ***************************
                 ID: 3
RESOURCE_GROUP_NAME: default
         START_TIME: 2024-09-11 07:21:16
           END_TIME: 2024-09-11 07:31:16
              WATCH: Exact
         WATCH_TEXT: select sleep(2) from t
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
               RULE: ElapsedTime = 2024-09-11T15:21:16+08:00(2024-09-11T15:21:16+08:00)
3 rows in set (0.00 sec)
```

向资源组 `rg1` 添加一个监控项：

```sql
QUERY WATCH ADD RESOURCE GROUP rg1 SQL TEXT EXACT TO 'select * from sbtest.sbtest1';
```

再次查询 runaway 查询的监控列表：

```sql
SELECT * FROM INFORMATION_SCHEMA.RUNAWAY_WATCHES\G
```

输出如下：

```sql
*************************** 1. row ***************************
                 ID: 1
RESOURCE_GROUP_NAME: default
         START_TIME: 2024-09-11 07:20:48
           END_TIME: 2024-09-11 07:30:48
              WATCH: Exact
         WATCH_TEXT: select count(*) from `tpch1`.`supplier`
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
               RULE: ProcessedKeys = 10000(100)
*************************** 2. row ***************************
                 ID: 2
RESOURCE_GROUP_NAME: default
         START_TIME: 2024-09-11 07:20:51
           END_TIME: 2024-09-11 07:30:51
              WATCH: Exact
         WATCH_TEXT: select count(*) from `tpch1`.`partsupp`
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
               RULE: RequestUnit = RRU:143.369959, WRU:0.000000, WaitDuration:0s(10)
*************************** 3. row ***************************
                 ID: 3
RESOURCE_GROUP_NAME: default
         START_TIME: 2024-09-11 07:21:16
           END_TIME: 2024-09-11 07:31:16
              WATCH: Exact
         WATCH_TEXT: select sleep(2) from t
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
               RULE: ElapsedTime = 2024-09-11T15:21:16+08:00(2024-09-11T15:21:16+08:00)
*************************** 4. row ***************************
                 ID: 4
RESOURCE_GROUP_NAME: default
         START_TIME: 2024-09-11 07:23:10
           END_TIME: UNLIMITED
              WATCH: Exact
         WATCH_TEXT: select * from sbtest.sbtest1
             SOURCE: manual
             ACTION: Kill
               RULE: None
3 row in set (0.00 sec)
```

`RUNAWAY_WATCHES` 表中每个字段的含义如下：

- `ID`：监控项的 ID。
- `RESOURCE_GROUP_NAME`：资源组名称。
- `START_TIME`：开始时间。
- `END_TIME`：结束时间。`UNLIMITED` 表示该监控项有效期无限。
- `WATCH`：快速识别的匹配类型。取值如下：
    - `Plan` 表示匹配 Plan Digest，此时 `WATCH_TEXT` 列显示 Plan Digest。
    - `Similar` 表示匹配 SQL Digest，此时 `WATCH_TEXT` 列显示 SQL Digest。
    - `Exact` 表示匹配 SQL 文本，此时 `WATCH_TEXT` 列显示 SQL 文本。
- `SOURCE`：监控项的来源。如果是通过 `QUERY_LIMIT` 规则识别，则显示被识别的 TiDB IP 地址；如果是手动添加，则显示 `manual`。
- `ACTION`：识别后对应的操作。
- `RULE`：识别规则。目前有三种规则：`ElapsedTime`、`ProcessedKeys` 和 `RequestUnit`。格式为 `ProcessedKeys = 666(10)`，其中 `666` 为实际值，`10` 为阈值。