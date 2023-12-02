---
title: TABLE_CONSTRAINTS
summary: Learn the `TABLE_CONSTRAINTS` information_schema table.
---

# TABLE_CONSTRAINTS {#table-constraints}

`TABLE_CONSTRAINTS`表は、どのテーブルに制約があるかを示しています。

```sql
USE information_schema;
DESC table_constraints;
```

```sql
+--------------------+--------------+------+------+---------+-------+
| Field              | Type         | Null | Key  | Default | Extra |
+--------------------+--------------+------+------+---------+-------+
| CONSTRAINT_CATALOG | varchar(512) | YES  |      | NULL    |       |
| CONSTRAINT_SCHEMA  | varchar(64)  | YES  |      | NULL    |       |
| CONSTRAINT_NAME    | varchar(64)  | YES  |      | NULL    |       |
| TABLE_SCHEMA       | varchar(64)  | YES  |      | NULL    |       |
| TABLE_NAME         | varchar(64)  | YES  |      | NULL    |       |
| CONSTRAINT_TYPE    | varchar(64)  | YES  |      | NULL    |       |
+--------------------+--------------+------+------+---------+-------+
6 rows in set (0.00 sec)
```

```sql
SELECT * FROM table_constraints WHERE constraint_type='UNIQUE';
```

```sql
+--------------------+--------------------+-------------------------+--------------------+-------------------------------------+-----------------+
| CONSTRAINT_CATALOG | CONSTRAINT_SCHEMA  | CONSTRAINT_NAME         | TABLE_SCHEMA       | TABLE_NAME                          | CONSTRAINT_TYPE |
+--------------------+--------------------+-------------------------+--------------------+-------------------------------------+-----------------+
| def                | mysql              | name                    | mysql              | help_topic                          | UNIQUE          |
| def                | mysql              | tbl                     | mysql              | stats_meta                          | UNIQUE          |
| def                | mysql              | tbl                     | mysql              | stats_histograms                    | UNIQUE          |
| def                | mysql              | tbl                     | mysql              | stats_buckets                       | UNIQUE          |
| def                | mysql              | delete_range_index      | mysql              | gc_delete_range                     | UNIQUE          |
| def                | mysql              | delete_range_done_index | mysql              | gc_delete_range_done                | UNIQUE          |
| def                | PERFORMANCE_SCHEMA | SCHEMA_NAME             | PERFORMANCE_SCHEMA | events_statements_summary_by_digest | UNIQUE          |
+--------------------+--------------------+-------------------------+--------------------+-------------------------------------+-----------------+
7 rows in set (0.01 sec)
```

`TABLE_CONSTRAINTS`テーブルのフィールドは次のように説明されています。

-   `CONSTRAINT_CATALOG` : 制約が属するカタログの名前。この値は常に`def`です。
-   `CONSTRAINT_SCHEMA` : 制約が属するデータベースの名前。
-   `CONSTRAINT_NAME` : 制約の名前。
-   `TABLE_NAME` : テーブルの名前。
-   `CONSTRAINT_TYPE` : 制約のタイプ。値は`UNIQUE` 、 `PRIMARY KEY`または`FOREIGN KEY`です。 `UNIQUE`と`PRIMARY KEY`情報は、 `SHOW INDEX`ステートメントの実行結果と同様です。
