---
title: VIEWS
summary: Learn the `VIEWS` information_schema table.
---

# VIEWS

The `VIEWS` table provides information about SQL views.

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC views;
```

```
+----------------------+--------------+------+------+---------+-------+
| Field                | Type         | Null | Key  | Default | Extra |
+----------------------+--------------+------+------+---------+-------+
| TABLE_CATALOG        | varchar(512) | NO   |      | NULL    |       |
| TABLE_SCHEMA         | varchar(64)  | NO   |      | NULL    |       |
| TABLE_NAME           | varchar(64)  | NO   |      | NULL    |       |
| VIEW_DEFINITION      | longblob     | NO   |      | NULL    |       |
| CHECK_OPTION         | varchar(8)   | NO   |      | NULL    |       |
| IS_UPDATABLE         | varchar(3)   | NO   |      | NULL    |       |
| DEFINER              | varchar(77)  | NO   |      | NULL    |       |
| SECURITY_TYPE        | varchar(7)   | NO   |      | NULL    |       |
| CHARACTER_SET_CLIENT | varchar(32)  | NO   |      | NULL    |       |
| COLLATION_CONNECTION | varchar(32)  | NO   |      | NULL    |       |
+----------------------+--------------+------+------+---------+-------+
10 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
CREATE VIEW test.v1 AS SELECT 1;
SELECT * FROM views\G
```

```
*************************** 1. row ***************************
       TABLE_CATALOG: def
        TABLE_SCHEMA: test
          TABLE_NAME: v1
     VIEW_DEFINITION: SELECT 1
        CHECK_OPTION: CASCADED
        IS_UPDATABLE: NO
             DEFINER: root@127.0.0.1
       SECURITY_TYPE: DEFINER
CHARACTER_SET_CLIENT: utf8mb4
COLLATION_CONNECTION: utf8mb4_0900_ai_ci
1 row in set (0.00 sec)
```