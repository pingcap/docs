---
title: COLLATIONS
summary: 了解 `COLLATIONS` information_schema 表。
---

# COLLATIONS

`COLLATIONS` 表提供了与 `CHARACTER_SETS` 表中的字符集对应的排序规则列表。目前，该表仅用于与 MySQL 的兼容性。

```sql
USE information_schema;
DESC collations;
```

```sql
+--------------------+-------------+------+------+---------+-------+
| Field              | Type        | Null | Key  | Default | Extra |
+--------------------+-------------+------+------+---------+-------+
| COLLATION_NAME     | varchar(32) | YES  |      | NULL    |       |
| CHARACTER_SET_NAME | varchar(32) | YES  |      | NULL    |       |
| ID                 | bigint      | YES  |      | NULL    |       |
| IS_DEFAULT         | varchar(3)  | YES  |      | NULL    |       |
| IS_COMPILED        | varchar(3)  | YES  |      | NULL    |       |
| SORTLEN            | bigint      | YES  |      | NULL    |       |
| PAD_ATTRIBUTE      | varchar(9)  | YES  |      | NULL    |       |
+--------------------+-------------+------+------+---------+-------+
7 rows in set (0.001 sec)
```

```sql
SELECT * FROM collations WHERE character_set_name='utf8mb4';
```

```sql
+--------------------+--------------------+------+------------+-------------+---------+---------------+
| COLLATION_NAME     | CHARACTER_SET_NAME | ID   | IS_DEFAULT | IS_COMPILED | SORTLEN | PAD_ATTRIBUTE |
+--------------------+--------------------+------+------------+-------------+---------+---------------+
| utf8mb4_0900_ai_ci | utf8mb4            |  255 |            | Yes         |       0 | NO PAD        |
| utf8mb4_0900_bin   | utf8mb4            |  309 |            | Yes         |       1 | NO PAD        |
| utf8mb4_bin        | utf8mb4            |   46 | Yes        | Yes         |       1 | PAD SPACE     |
| utf8mb4_general_ci | utf8mb4            |   45 |            | Yes         |       1 | PAD SPACE     |
| utf8mb4_unicode_ci | utf8mb4            |  224 |            | Yes         |       8 | PAD SPACE     |
+--------------------+--------------------+------+------------+-------------+---------+---------------+
5 rows in set (0.001 sec)
```

`COLLATIONS` 表中各列的描述如下：

* `COLLATION_NAME`：排序规则的名称。
* `CHARACTER_SET_NAME`：所属字符集的名称。
* `ID`：排序规则的 ID。
* `IS_DEFAULT`：该排序规则是否为所属字符集的默认排序规则。
* `IS_COMPILED`：字符集是否已编译到服务器中。
* `SORTLEN`：排序规则在排序字符时分配的最小内存长度。
* `PAD_ATTRIBUTE`：在字符串比较时是否忽略尾部空格。`PAD SPACE` 表示忽略尾部空格（例如， `'abc'` 等于 `'abc   '`），而 `NO PAD` 表示尾部空格是有意义的（例如， `'abc'` 不等于 `'abc   '`）。

## 相关链接

- [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md)
- [`SHOW COLLATION`](/sql-statements/sql-statement-show-collation.md)
- [`INFORMATION_SCHEMA.CHARACTER_SETS`](/information-schema/information-schema-character-sets.md)
- [`INFORMATION_SCHEMA.COLLATION_CHARACTER_SET_APPLICABILITY`](/information-schema/information-schema-collation-character-set-applicability.md)