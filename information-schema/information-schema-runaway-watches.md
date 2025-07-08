---
title: RUNAWAY_WATCHES
summary: 了解 `RUNAWAY_WATCHES` INFORMATION_SCHEMA 表格。
---

# RUNAWAY_WATCHES

`RUNAWAY_WATCHES` 表显示了超出预期资源消耗的 runaway 查询的监控列表。更多信息请参见 [Runaway Queries](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries)。

> **Note:**
>
> 该表在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

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
+---------------------+--------------+------+------+---------+-------+
8 rows in set (0.00 sec)
```

## Examples

查询 runaway 查询的监控列表：

```sql
SELECT * FROM INFORMATION_SCHEMA.RUNAWAY_WATCHES\G
```

输出如下：

```sql
*************************** 1. row ***************************
                 ID: 20003
RESOURCE_GROUP_NAME: rg2
         START_TIME: 2023-07-28 13:06:08
           END_TIME: UNLIMITED
              WATCH: Similar
         WATCH_TEXT: 5b7fd445c5756a16f910192ad449c02348656a5e9d2aa61615e6049afbc4a82e
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
*************************** 2. row ***************************
                 ID: 16004
RESOURCE_GROUP_NAME: rg2
         START_TIME: 2023-07-28 01:45:30
           END_TIME: UNLIMITED
              WATCH: Similar
         WATCH_TEXT: 3d48fca401d8cbb31a9f29adc9c0f9d4be967ca80a34f59c15f73af94e000c84
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
2 rows in set (0.00 sec)
```

向资源组 `rg1` 添加监控项到列表中：

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
                 ID: 20003
RESOURCE_GROUP_NAME: rg2
         START_TIME: 2023-07-28 13:06:08
           END_TIME: UNLIMITED
              WATCH: Similar
         WATCH_TEXT: 5b7fd445c5756a16f910192ad449c02348656a5e9d2aa61615e6049afbc4a82e
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
*************************** 2. row ***************************
                 ID: 16004
RESOURCE_GROUP_NAME: rg2
         START_TIME: 2023-07-28 01:45:30
           END_TIME: UNLIMITED
              WATCH: Similar
         WATCH_TEXT: 3d48fca401d8cbb31a9f29adc9c0f9d4be967ca80a34f59c15f73af94e000c84
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
*************************** 3. row ***************************
                 ID: 20004
RESOURCE_GROUP_NAME: rg1
         START_TIME: 2023-07-28 14:23:04
           END_TIME: UNLIMITED
              WATCH: Exact
         WATCH_TEXT: select * from sbtest.sbtest1
             SOURCE: manual
             ACTION: NoneAction
3 rows in set (0.00 sec)
```

`RUNAWAY_WATCHES` 表中每个字段的含义如下：

- `ID`：监控项的编号。
- `RESOURCE_GROUP_NAME`：资源组的名称。
- `START_TIME`：开始时间。
- `END_TIME`：结束时间。`UNLIMITED` 表示该监控项具有无限有效期。
- `WATCH`：快速识别的匹配类型，值如下：
    - `Plan` 表示匹配 Plan Digest，此时 `WATCH_TEXT` 列显示 Plan Digest。
    - `Similar` 表示匹配 SQL Digest，此时 `WATCH_TEXT` 列显示 SQL Digest。
    - `Exact` 表示匹配 SQL 文本，此时 `WATCH_TEXT` 列显示 SQL 文本。
- `SOURCE`：监控项的来源。如果由 `QUERY_LIMIT` 规则识别，显示识别到的 TiDB IP 地址；如果是手动添加，则显示 `manual`。
- `ACTION`：识别后对应的操作。