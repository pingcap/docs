---
title: RUNAWAY_WATCHES
summary: Learn the `RUNAWAY_WATCHES` INFORMATION_SCHEMA table.
---

# RUNAWAY_WATCHES

The `RUNAWAY_WATCHES` table shows the watch list of runaway queries that consume more resources than expected. For more information, see [Runaway Queries](/tidb-resource-control-runaway-queries.md).

> **Note:**
>
> This table is not available on [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) clusters.

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

## Examples

Query the watch list of runaway queries:

```sql
SELECT * FROM INFORMATION_SCHEMA.RUNAWAY_WATCHES ORDER BY id\G
```

The output is as follows:

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

Add a watch item into list to the resource group `rg1`:

```sql
QUERY WATCH ADD RESOURCE GROUP rg1 SQL TEXT EXACT TO 'select * from sbtest.sbtest1';
```

Query the watch list of runaway queries again:

```sql
SELECT * FROM INFORMATION_SCHEMA.RUNAWAY_WATCHES\G
```

The output is as follows:

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

The meaning of each column field in the `RUNAWAY_WATCHES` table is as follows:

- `ID`: the ID of the watch item.
- `RESOURCE_GROUP_NAME`: the name of the resource group.
- `START_TIME`: the start time.
- `END_TIME`: the end time. `UNLIMITED` means that the watch item has an unlimited validity period.
- `WATCH`: the match type of the quick identification. The values are as follows:
    - `Plan` indicates that the Plan Digest is matched. In this case, the `WATCH_TEXT` column shows the Plan Digest.
    - `Similar` indicates that the SQL Digest is matched. In this case, the `WATCH_TEXT` column shows the SQL Digest.
    - `Exact` indicates that the SQL text is matched. In this case, the `WATCH_TEXT` column shows the SQL text.
- `SOURCE`: the source of the watch item. If it is identified by the `QUERY_LIMIT` rule, the identified TiDB IP address is displayed. If it is manually added, `manual` is displayed.
- `ACTION`: the corresponding operation after the identification.
- `RULE`: the identification rule. The current three rules are `ElapsedTime`, `ProcessedKeys`, and `RequestUnit`. The format is `ProcessedKeys = 666(10)`, where `666` is the actual value and `10` is the threshold.
