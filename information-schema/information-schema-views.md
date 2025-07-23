---
title: VIEWS
summary: 了解 `VIEWS` INFORMATION_SCHEMA 表。
---

# VIEWS

`VIEWS` 表提供关于 [SQL 视图](/views.md) 的信息。

```sql
USE INFORMATION_SCHEMA;
DESC VIEWS;
```

输出结果如下：

```sql
+----------------------+--------------+------+------+---------+-------+
| Field                | Type         | Null | Key  | Default | Extra |
+----------------------+--------------+------+------+---------+-------+
| TABLE_CATALOG        | varchar(512) | NO   |      | NULL    |       |
| TABLE_SCHEMA         | varchar(64)  | NO   |      | NULL    |       |
| TABLE_NAME           | varchar(64)  | NO   |      | NULL    |       |
| VIEW_DEFINITION      | longtext     | NO   |      | NULL    |       |
| CHECK_OPTION         | varchar(8)   | NO   |      | NULL    |       |
| IS_UPDATABLE         | varchar(3)   | NO   |      | NULL    |       |
| DEFINER              | varchar(77)  | NO   |      | NULL    |       |
| SECURITY_TYPE        | varchar(7)   | NO   |      | NULL    |       |
| CHARACTER_SET_CLIENT | varchar(32)  | NO   |      | NULL    |       |
| COLLATION_CONNECTION | varchar(32)  | NO   |      | NULL    |       |
+----------------------+--------------+------+------+---------+-------+
10 rows in set (0.00 sec)
```

创建视图并查询 `VIEWS` 表：

```sql
CREATE VIEW test.v1 AS SELECT 1;
SELECT * FROM VIEWS\G
```

输出结果如下：

```sql
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

`VIEWS` 表中的字段说明如下：

* `TABLE_CATALOG`: 视图所属的目录名。该值始终为 `def`。
* `TABLE_SCHEMA`: 视图所属的模式（schema）名。
* `TABLE_NAME`: 视图名称。
* `VIEW_DEFINITION`: 视图的定义，即创建视图时所用的 `SELECT` 语句。
* `CHECK_OPTION`: `CHECK_OPTION` 的值。取值选项为 `NONE`、`CASCADE` 和 `LOCAL`。
* `IS_UPDATABLE`: 是否允许对视图进行 `UPDATE`/`INSERT`/`DELETE` 操作。在 TiDB 中，该值始终为 `NO`。
* `DEFINER`: 创建视图的用户名，格式为 `'user_name'@'host_name'`。
* `SECURITY_TYPE`: `SQL SECURITY` 的值。取值选项为 `DEFINER` 和 `INVOKER`。
* `CHARACTER_SET_CLIENT`: 创建视图时的 `character_set_client` 会话变量值。
* `COLLATION_CONNECTION`: 创建视图时的 `collation_connection` 会话变量值。

## 相关链接

- [`CREATE VIEW`](/sql-statements/sql-statement-create-view.md)
- [`DROP VIEW`](/sql-statements/sql-statement-drop-view.md)