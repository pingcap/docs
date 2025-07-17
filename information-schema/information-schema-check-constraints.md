---
title: CHECK_CONSTRAINTS
summary: 了解 `CHECK_CONSTRAINTS` INFORMATION_SCHEMA 表。
---

# CHECK\_CONSTRAINTS

`CHECK_CONSTRAINTS` 表提供有关表上的 [`CHECK` constraints](/constraints.md#check) 的信息。

```sql
USE INFORMATION_SCHEMA;
DESC CHECK_CONSTRAINTS;
```

输出结果如下：

```sql
+--------------------+-------------+------+-----+---------+-------+
| Field              | Type        | Null | Key | Default | Extra |
+--------------------+-------------+------+-----+---------+-------+
| CONSTRAINT_CATALOG | varchar(64) | NO   |     | NULL    |       |
| CONSTRAINT_SCHEMA  | varchar(64) | NO   |     | NULL    |       |
| CONSTRAINT_NAME    | varchar(64) | NO   |     | NULL    |       |
| CHECK_CLAUSE       | longtext    | NO   |     | NULL    |       |
+--------------------+-------------+------+-----+---------+-------+
4 rows in set (0.00 sec)
```

以下示例使用 `CREATE TABLE` 语句添加一个 `CHECK` constraint：

```sql
SET GLOBAL tidb_enable_check_constraint = ON;
CREATE TABLE test.t1 (id INT PRIMARY KEY, CHECK (id%2 = 0));
SELECT * FROM CHECK_CONSTRAINTS\G
```

输出结果如下：

```sql
*************************** 1. row ***************************
CONSTRAINT_CATALOG: def
 CONSTRAINT_SCHEMA: test
   CONSTRAINT_NAME: t1_chk_1
      CHECK_CLAUSE: (`id` % 2 = 0)
1 row in set (0.00 sec)
```

`CHECK_CONSTRAINTS` 表中的字段说明如下：

* `CONSTRAINT_CATALOG`: 约束的目录，始终为 `def`。
* `CONSTRAINT_SCHEMA`: 约束所在的模式。
* `CONSTRAINT_NAME`: 约束的名称。
* `CHECK_CLAUSE`: 检查约束的条件子句。