---
title: MODIFY COLUMN | TiDB SQL 语句参考
summary: TiDB 数据库中 MODIFY COLUMN 的用法概述。
---

# MODIFY COLUMN

`ALTER TABLE ... MODIFY COLUMN` 语句用于修改已存在表中的列。该修改可以包括更改数据类型和属性。如果需要同时重命名列，请使用 [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md) 语句。

从 v5.1.0 开始，TiDB 支持需要 Reorg-Data 的列类型变更。在执行此类变更时，TiDB 会通过读取原始数据、将其转换为新的列类型，然后将转换后的数据写回表中，从而重建表中所有现有数据。由于必须处理所有表数据，Reorg-Data 操作通常耗时较长，且执行时间与表中的数据量成正比。

以下是一些常见的需要 Reorg-Data 的列类型变更示例：

- 将 `VARCHAR` 更改为 `BIGINT`
- 修改 `DECIMAL` 精度
- 将 `VARCHAR(10)` 的长度缩短为 `VARCHAR(5)`

从 v8.5.5 开始，TiDB 对部分原本需要 Reorg-Data 的列类型变更进行了优化。当满足以下条件时，TiDB 只会重建受影响的索引，而不是整个表，从而提升执行效率：

- 当前会话使用严格的 [SQL 模式](/sql-mode.md)（`sql_mode` 包含 `STRICT_TRANS_TABLES` 或 `STRICT_ALL_TABLES`）。
- 表没有 TiFlash 副本。
- 类型转换过程中不存在数据截断风险。

该优化仅适用于以下类型变更场景：

- 整数型之间的转换，例如从 `BIGINT` 到 `INT`
- 字符串类型之间且字符集未变的转换，例如从 `VARCHAR(200)` 到 `VARCHAR(100)`

> **注意：**
>
> 当从 `VARCHAR` 转换为 `CHAR` 时，原始数据中不能包含尾随空格。如果原始数据包含尾随空格，TiDB 仍会执行 Reorg-Data，以确保转换后的值符合 `CHAR` 类型的填充规则。

## 语法

```ebnf+diagram
AlterTableStmt
         ::= 'ALTER' 'IGNORE'? 'TABLE' TableName ModifyColumnSpec ( ',' ModifyColumnSpec )*

ModifyColumnSpec
         ::= 'MODIFY' ColumnKeywordOpt 'IF EXISTS' ColumnName ColumnType ColumnOption* ( 'FIRST' | 'AFTER' ColumnName )?

ColumnType
         ::= NumericType
           | StringType
           | DateAndTimeType
           | 'SERIAL'

ColumnOption
         ::= 'NOT'? 'NULL'
           | 'AUTO_INCREMENT'
           | 'PRIMARY'? 'KEY' ( 'CLUSTERED' | 'NONCLUSTERED' )?
           | 'UNIQUE' 'KEY'?
           | 'DEFAULT' ( NowSymOptionFraction | SignedLiteral | NextValueForSequence )
           | 'SERIAL' 'DEFAULT' 'VALUE'
           | 'ON' 'UPDATE' NowSymOptionFraction
           | 'COMMENT' stringLit
           | ( 'CONSTRAINT' Identifier? )? 'CHECK' '(' Expression ')' ( 'NOT'? ( 'ENFORCED' | 'NULL' ) )?
           | 'GENERATED' 'ALWAYS' 'AS' '(' Expression ')' ( 'VIRTUAL' | 'STORED' )?
           | 'REFERENCES' TableName ( '(' IndexPartSpecificationList ')' )? Match? OnDeleteUpdateOpt
           | 'COLLATE' CollationName
           | 'COLUMN_FORMAT' ColumnFormat
           | 'STORAGE' StorageMedia
           | 'AUTO_RANDOM' ( '(' LengthNum ')' )?

ColumnName ::=
    Identifier ( '.' Identifier ( '.' Identifier )? )?
```

## 示例

### 仅元信息变更

```sql
CREATE TABLE t1 (id int not null primary key AUTO_INCREMENT, col1 INT);
```

```
Query OK, 0 rows affected (0.11 sec)
```

```sql
INSERT INTO t1 (col1) VALUES (1),(2),(3),(4),(5);
```

```
Query OK, 5 rows affected (0.02 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

```sql
ALTER TABLE t1 MODIFY col1 BIGINT;
```

```
Query OK, 0 rows affected (0.09 sec)
```

```sql
SHOW CREATE TABLE t1\G
```

```sql
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col1` bigint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=30001
1 row in set (0.00 sec)
```

### Reorg-Data 变更

```sql
CREATE TABLE t1 (id int not null primary key AUTO_INCREMENT, col1 INT);
```

```
Query OK, 0 rows affected (0.11 sec)
```

```sql
INSERT INTO t1 (col1) VALUES (12345),(67890);
```

```
Query OK, 2 rows affected (0.00 sec)
Records: 2  Duplicates: 0  Warnings: 0
```

```sql
ALTER TABLE t1 MODIFY col1 VARCHAR(5);
```

```
Query OK, 0 rows affected (2.52 sec)
```

```sql
SHOW CREATE TABLE t1\G
```

```sql
*************************** 1. row ***************************
       Table: t1
CREATE TABLE `t1` (
  `id` int NOT NULL AUTO_INCREMENT,
  `col1` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=30001
1 row in set (0.00 sec)
```

> **注意：**
>
> - 当更改后的数据类型与已有数据行发生冲突时，TiDB 会返回错误。在上述示例中，TiDB 返回如下错误：
>
>    ```
>    alter table t1 modify column col1 varchar(4);
>    ERROR 1406 (22001): Data Too Long, field len 4, data len 5
>    ```
>
> - 由于与 Async Commit 特性的兼容性，当 [元信息锁](/metadata-lock.md) 被禁用时，DDL 语句会在开始进入 Reorg-Data 处理前等待一段时间（约 2.5 秒）。
>
>    ```
>    Query OK, 0 rows affected (2.52 sec)
>    ```

## MySQL 兼容性

* 不支持对主键列进行 Reorg-Data 类型的修改，但支持 Meta-Only 类型的修改。例如：

    ```sql
    CREATE TABLE t (a int primary key);
    ALTER TABLE t MODIFY COLUMN a VARCHAR(10);
    ERROR 8200 (HY000): Unsupported modify column: column has primary key flag
    ```

    ```sql
    CREATE TABLE t (a int primary key);
    ALTER TABLE t MODIFY COLUMN a int UNSIGNED;
    ERROR 8200 (HY000): Unsupported modify column: column has primary key flag
    ```

    ```sql
    CREATE TABLE t (a int primary key);
    ALTER TABLE t MODIFY COLUMN a bigint;
    Query OK, 0 rows affected (0.01 sec)
    ```

* 不支持对生成列的列类型进行修改。例如：

    ```sql
    CREATE TABLE t (a INT, b INT as (a+1));
    ALTER TABLE t MODIFY COLUMN b VARCHAR(10);
    ERROR 8200 (HY000): Unsupported modify column: column is generated
    ```

* 不支持对分区表的列类型进行修改。例如：

    ```sql
    CREATE TABLE t (c1 INT, c2 INT, c3 INT) partition by range columns(c1) ( partition p0 values less than (10), partition p1 values less than (maxvalue));
    ALTER TABLE t MODIFY COLUMN c1 DATETIME;
    ERROR 8200 (HY000): Unsupported modify column: table is partition table
    ```

* 由于 TiDB 与 MySQL 在 `cast` 函数行为上的兼容性问题，不支持从某些数据类型（如部分 TIME 类型、BIT、SET、ENUM、JSON）转换为其他类型。

    ```sql
    CREATE TABLE t (a DECIMAL(13, 7));
    ALTER TABLE t MODIFY COLUMN a DATETIME;
    ERROR 8200 (HY000): Unsupported modify column: change from original type decimal(13,7) to datetime is currently unsupported yet
    ```

## 另请参阅

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
* [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
* [DROP COLUMN](/sql-statements/sql-statement-drop-column.md)
* [CHANGE COLUMN](/sql-statements/sql-statement-change-column.md)
