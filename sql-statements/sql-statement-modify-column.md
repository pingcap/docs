---
title: MODIFY COLUMN | TiDB SQL Statement Reference
summary: An overview of the usage of MODIFY COLUMN for the TiDB database.
---

# MODIFY COLUMN

The `ALTER TABLE ... MODIFY COLUMN` statement modifies a column on an existing table. The modification can include changing the data type and attributes. To rename the column at the same time, use the [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md) statement instead.

Starting from v5.1.0, TiDB supports column type changes that require Reorg-Data. When performing such changes, TiDB rebuilds all existing data in the table by reading the original data, converting it to the new column type, and then writing the converted data back to the table. Because all table data must be processed, Reorg-Data operations typically take a long time, and the execution time is proportional to the amount of data in the table.

The following are some common examples of column type changes that require Reorg-Data:

- Changing `VARCHAR` to `BIGINT`
- Modifying the `DECIMAL` precision
- Reducing the length of `VARCHAR(10)` to `VARCHAR(5)`

Starting from v8.5.5, TiDB optimizes some column type changes that previously required Reorg-Data. When the following conditions are met, TiDB rebuilds only the affected indexes instead of the entire table, thereby improving execution efficiency:

- The current session uses a strict [SQL mode](/sql-mode.md) (`sql_mode` includes `STRICT_TRANS_TABLES` or `STRICT_ALL_TABLES`).
- The table has no TiFlash replicas.
- There is no risk of data truncation during type conversion.

This optimization only applies to the following type change scenarios:

- Conversions between integer types, such as from `BIGINT` to `INT`
- Conversions between string types where the character set remains unchanged, such as from `VARCHAR(200)` to `VARCHAR(100)`

> **Note:**
>
> When converting from `VARCHAR` to `CHAR`, the original data must not contain trailing spaces. If the original data contains trailing spaces, TiDB still performs Reorg-Data to ensure that the converted values comply with the padding rules of the `CHAR` type.

## Synopsis

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

## Examples

### Meta-only change

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id int not null primary key AUTO_INCREMENT, col1 INT);
```

```
Query OK, 0 rows affected (0.11 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO t1 (col1) VALUES (1),(2),(3),(4),(5);
```

```
Query OK, 5 rows affected (0.02 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
ALTER TABLE t1 MODIFY col1 BIGINT;
```

```
Query OK, 0 rows affected (0.09 sec)
```

{{< copyable "sql" >}}

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

### Reorg-Data change

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id int not null primary key AUTO_INCREMENT, col1 INT);
```

```
Query OK, 0 rows affected (0.11 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO t1 (col1) VALUES (12345),(67890);
```

```
Query OK, 2 rows affected (0.00 sec)
Records: 2  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
ALTER TABLE t1 MODIFY col1 VARCHAR(5);
```

```
Query OK, 0 rows affected (2.52 sec)
```

{{< copyable "sql" >}}

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

> **Note:**
>
> - TiDB returns an error when the changed data type conflicts with an existing data row. In the above example, TiDB returns the following error:
>
>    ```
>    alter table t1 modify column col1 varchar(4);
>    ERROR 1406 (22001): Data Too Long, field len 4, data len 5
>    ```
>
> - Due to the compatibility with the Async Commit feature, when [Metadata lock](/metadata-lock.md) is disabled, the DDL statement waits for a period of time (about 2.5s) before starting to process into Reorg-Data.
>
>    ```
>    Query OK, 0 rows affected (2.52 sec)
>    ```

## MySQL compatibility

* Does not support modifying the Reorg-Data types on the primary key columns but supports modifying the Meta-Only types. For example:

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

* Does not support modifying the column types on generated columns. For example:

    ```sql
    CREATE TABLE t (a INT, b INT as (a+1));
    ALTER TABLE t MODIFY COLUMN b VARCHAR(10);
    ERROR 8200 (HY000): Unsupported modify column: column is generated
    ```

* Does not support modifying the column types on the partitioned tables. For example:

    ```sql
    CREATE TABLE t (c1 INT, c2 INT, c3 INT) partition by range columns(c1) ( partition p0 values less than (10), partition p1 values less than (maxvalue));
    ALTER TABLE t MODIFY COLUMN c1 DATETIME;
    ERROR 8200 (HY000): Unsupported modify column: table is partition table
    ```

* Does not support modifying from some data types (for example, some TIME types, BIT, SET, ENUM, JSON) to some other types due to some compatibility issues of the `cast` function's behavior between TiDB and MySQL.

    ```sql
    CREATE TABLE t (a DECIMAL(13, 7));
    ALTER TABLE t MODIFY COLUMN a DATETIME;
    ERROR 8200 (HY000): Unsupported modify column: change from original type decimal(13,7) to datetime is currently unsupported yet
    ```

## See also

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
* [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
* [DROP COLUMN](/sql-statements/sql-statement-drop-column.md)
* [CHANGE COLUMN](/sql-statements/sql-statement-change-column.md)
