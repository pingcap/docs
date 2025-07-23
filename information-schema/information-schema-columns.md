---
title: COLUMNS
summary: 了解 `COLUMNS` INFORMATION_SCHEMA 表。
---

# COLUMNS

`COLUMNS` 表提供关于表中列的详细信息。

```sql
USE INFORMATION_SCHEMA;
DESC COLUMNS;
```

输出如下：

```sql
+--------------------------+---------------+------+------+---------+-------+
| Field                    | Type          | Null | Key  | Default | Extra |
+--------------------------+---------------+------+------+---------+-------+
| TABLE_CATALOG            | varchar(512)  | YES  |      | NULL    |       |
| TABLE_SCHEMA             | varchar(64)   | YES  |      | NULL    |       |
| TABLE_NAME               | varchar(64)   | YES  |      | NULL    |       |
| COLUMN_NAME              | varchar(64)   | YES  |      | NULL    |       |
| ORDINAL_POSITION         | bigint(64)    | YES  |      | NULL    |       |
| COLUMN_DEFAULT           | text          | YES  |      | NULL    |       |
| IS_NULLABLE              | varchar(3)    | YES  |      | NULL    |       |
| DATA_TYPE                | varchar(64)   | YES  |      | NULL    |       |
| CHARACTER_MAXIMUM_LENGTH | bigint(21)    | YES  |      | NULL    |       |
| CHARACTER_OCTET_LENGTH   | bigint(21)    | YES  |      | NULL    |       |
| NUMERIC_PRECISION        | bigint(21)    | YES  |      | NULL    |       |
| NUMERIC_SCALE            | bigint(21)    | YES  |      | NULL    |       |
| DATETIME_PRECISION       | bigint(21)    | YES  |      | NULL    |       |
| CHARACTER_SET_NAME       | varchar(32)   | YES  |      | NULL    |       |
| COLLATION_NAME           | varchar(32)   | YES  |      | NULL    |       |
| COLUMN_TYPE              | text          | YES  |      | NULL    |       |
| COLUMN_KEY               | varchar(3)    | YES  |      | NULL    |       |
| EXTRA                    | varchar(30)   | YES  |      | NULL    |       |
| PRIVILEGES               | varchar(80)   | YES  |      | NULL    |       |
| COLUMN_COMMENT           | varchar(1024) | YES  |      | NULL    |       |
| GENERATION_EXPRESSION    | text          | NO   |      | NULL    |       |
+--------------------------+---------------+------+------+---------+-------+
21 行，耗时 0.00 秒
```

创建表 `test.t1` 并查询 `COLUMNS` 表中的信息：

```sql
CREATE TABLE test.t1 (a int);
SELECT * FROM COLUMNS WHERE table_schema='test' AND TABLE_NAME='t1'\G
```

输出如下：

```sql
*************************** 1. row ***************************
           TABLE_CATALOG: def
            TABLE_SCHEMA: test
              TABLE_NAME: t1
             COLUMN_NAME: a
        ORDINAL_POSITION: 1
          COLUMN_DEFAULT: NULL
             IS_NULLABLE: YES
               DATA_TYPE: int
CHARACTER_MAXIMUM_LENGTH: NULL
  CHARACTER_OCTET_LENGTH: NULL
       NUMERIC_PRECISION: 11
           NUMERIC_SCALE: 0
      DATETIME_PRECISION: NULL
      CHARACTER_SET_NAME: NULL
          COLLATION_NAME: NULL
             COLUMN_TYPE: int(11)
              COLUMN_KEY:
                   EXTRA:
              PRIVILEGES: select,insert,update,references
          COLUMN_COMMENT:
   GENERATION_EXPRESSION:
1 行，耗时 0.02 秒
```

`COLUMNS` 表中列的描述如下：

* `TABLE_CATALOG`：所属表所在的目录（catalog）名称，值始终为 `def`。
* `TABLE_SCHEMA`：所在的模式（schema）名称。
* `TABLE_NAME`：表的名称。
* `COLUMN_NAME`：列的名称。
* `ORDINAL_POSITION`：列在表中的位置。
* `COLUMN_DEFAULT`：列的默认值。如果显式默认值为 `NULL`，或列定义中未包含 `default` 子句，则此值为 `NULL`。
* `IS_NULLABLE`：列是否允许存储空值。允许为空则为 `YES`，否则为 `NO`。
* `DATA_TYPE`：列的数据类型。
* `CHARACTER_MAXIMUM_LENGTH`：字符串列的最大长度（字符数）。
* `CHARACTER_OCTET_LENGTH`：字符串列的最大长度（字节数）。
* `NUMERIC_PRECISION`：数值类型列的数值精度。
* `NUMERIC_SCALE`：数值类型列的小数位数。
* `DATETIME_PRECISION`：时间类型列的秒数精度。
* `CHARACTER_SET_NAME`：字符串列的字符集名称。
* `COLLATION_NAME`：字符串列的排序规则名称。
* `COLUMN_TYPE`：列的类型。
* `COLUMN_KEY`：是否为索引列。可能的值包括：
    * 空：此列未被索引，或为多列非唯一索引中的第二列。
    * `PRI`：此列为主键或多列主键之一。
    * `UNI`：此列为唯一索引的第一列。
    * `MUL`：此列为非唯一索引的第一列，允许多个相同值。
* `EXTRA`：关于此列的其他信息。
* `PRIVILEGES`：当前用户在此列上的权限。目前在 TiDB 中，此值固定为 `select,insert,update,references`。
* `COLUMN_COMMENT`：列定义中的注释。
* `GENERATION_EXPRESSION`：对于生成列，此值显示用于计算列值的表达式。非生成列时为空。

对应的 `SHOW` 语句如下：

```sql
SHOW COLUMNS FROM t1 FROM test;
```

输出如下：

```sql
+-------+---------+------+------+---------+-------+
| Field | Type    | Null | Key  | Default | Extra |
+-------+---------+------+------+---------+-------+
| a     | int(11) | YES  |      | NULL    |       |
+-------+---------+------+------+---------+-------+
1 行，耗时 0.00 秒
```

## 相关链接

- [`SHOW COLUMNS FROM`](/sql-statements/sql-statement-show-columns-from.md)