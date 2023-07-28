---
title: RUNAWAY_WATCHES
summary: Learn the `RUNAWAY_WATCHES` information_schema table。
---

# RUNAWAY_WATCHES

The `RUNAWAY_WATCHES` table shows a list of all identified runaway queries. See [Runaway Queries](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries).

```sql
USE information_schema;
DESC runaway_watches;
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

> **Warning:**
>
> This feature is an experimental feature. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

## Examples

```sql
select * from information_schema.runaway_watches\G; -- Query runaway query identification list
```

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

```sql
query watch add resource group rg1 sql text exact to 'select * from sbtest.sbtest1'; -- Add identification list
```

```sql
select * from information_schema.runaway_watches\G; -- Query runaway query identification list
```

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
3 row in set (0.00 sec)
```

The meanings of the columns in the `RUNAWAY_WATCHES` table are as follows:

- ID: the ID of the identification item.
- RESOURCE_GROUP_NAME: the name of the resource group.
- START_TIME: the start time.
- END_TIME: the end time. `UNLIMITED` means that the identification item is valid forever.
- WATCH: the type of the fast identification. The values are as follows:
    - `Plan` indicates that the Plan Digest is matched. In this case, the `WATCH_TEXT` column shows the Plan Digest.
    - `Similar` indicates that the SQL Digest is matched. In this case, the `WATCH_TEXT` column shows the SQL Digest.
    - `Exact` indicates that the SQL text is matched. In this case, the `WATCH_TEXT` column shows the SQL text.
- `SOURCE` indicates the source of the identification item. If it is identified by the `QUERY_LIMIT` rule, the identified TiDB IP address is displayed. If it is manually added, `manual` is displayed.
- `ACTION` indicates the corresponding operation after the identification. If it is `NoneAction`, the `ACTION` configured in `QUERY_LIMIT` in the resource group is used.
