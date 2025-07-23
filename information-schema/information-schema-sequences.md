---
title: SEQUENCES
summary: 了解 `SEQUENCES` INFORMATION_SCHEMA 表。
---

# SEQUENCES

`SEQUENCES` 表提供关于序列的信息。[sequences feature](/sql-statements/sql-statement-create-sequence.md) 模仿了 MariaDB 中的类似功能。

```sql
USE INFORMATION_SCHEMA;
DESC SEQUENCES;
```

输出结果如下：

```sql
+-----------------+--------------+------+------+---------+-------+
| Field           | Type         | Null | Key  | Default | Extra |
+-----------------+--------------+------+------+---------+-------+
| TABLE_CATALOG   | varchar(512) | NO   |      | NULL    |       |
| SEQUENCE_SCHEMA | varchar(64)  | NO   |      | NULL    |       |
| SEQUENCE_NAME   | varchar(64)  | NO   |      | NULL    |       |
| CACHE           | tinyint(0)   | NO   |      | NULL    |       |
| CACHE_VALUE     | bigint(21)   | YES  |      | NULL    |       |
| CYCLE           | tinyint(0)   | NO   |      | NULL    |       |
| INCREMENT       | bigint(21)   | NO   |      | NULL    |       |
| MAX_VALUE       | bigint(21)   | YES  |      | NULL    |       |
| MIN_VALUE       | bigint(21)   | YES  |      | NULL    |       |
| START           | bigint(21)   | YES  |      | NULL    |       |
| COMMENT         | varchar(64)  | YES  |      | NULL    |       |
+-----------------+--------------+------+------+---------+-------+
11 行，耗时 0.00 秒
```

创建一个序列 `test.seq` 并查询序列的下一个值：

```sql
CREATE SEQUENCE test.seq;
SELECT NEXTVAL(test.seq);
SELECT * FROM sequences\G
```

输出结果如下：

```sql
+-------------------+
| NEXTVAL(test.seq) |
+-------------------+
|                 1 |
+-------------------+
1 行，耗时 0.01 秒
```

查看所有序列：

```sql
SELECT * FROM SEQUENCES\G
```

输出结果如下：

```sql
*************************** 1. row ***************************
  TABLE_CATALOG: def
SEQUENCE_SCHEMA: test
  SEQUENCE_NAME: seq
          CACHE: 1
    CACHE_VALUE: 1000
          CYCLE: 0
      INCREMENT: 1
      MAX_VALUE: 9223372036854775806
      MIN_VALUE: 1
          START: 1
        COMMENT:
1 行，耗时 0.00 秒
```

## See also

- [`CREATE SEQUENCE`](/sql-statements/sql-statement-create-sequence.md)
- [`SHOW CREATE SEQUENCE`](/sql-statements/sql-statement-show-create-sequence.md)
- [`ALTER SEQUENCE`](/sql-statements/sql-statement-alter-sequence.md)
- [`DROP SEQUENCE`](/sql-statements/sql-statement-drop-sequence.md)
- [Sequence functions](/functions-and-operators/sequence-functions.md)