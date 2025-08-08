---
title: MODIFY COLUMN | TiDB SQL Statement Reference
summary: TiDB データベースの MODIFY COLUMN の使用法の概要。
---

# 列の変更 {#modify-column}

`ALTER TABLE.. MODIFY COLUMN`文は既存のテーブルの列を変更します。変更にはデータ型と属性の変更が含まれます。同時に列名を変更するには、代わりに[`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)文を使用してください。

バージョン 5.1.0 以降、TiDB は、Reorg データのデータ型の変更をサポートしています。これには以下が含まれますが、これらに限定されません。

-   `VARCHAR`を`BIGINT`に変更
-   `DECIMAL`精度の変更
-   `VARCHAR(10)`の長さを`VARCHAR(5)`に圧縮する

## 概要 {#synopsis}

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

## 例 {#examples}

### メタのみの変更 {#meta-only-change}

```sql
CREATE TABLE t1 (id int not null primary key AUTO_INCREMENT, col1 INT);
```

    Query OK, 0 rows affected (0.11 sec)

```sql
INSERT INTO t1 (col1) VALUES (1),(2),(3),(4),(5);
```

    Query OK, 5 rows affected (0.02 sec)
    Records: 5  Duplicates: 0  Warnings: 0

```sql
ALTER TABLE t1 MODIFY col1 BIGINT;
```

    Query OK, 0 rows affected (0.09 sec)

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

### 再編成データの変更 {#reorg-data-change}

```sql
CREATE TABLE t1 (id int not null primary key AUTO_INCREMENT, col1 INT);
```

    Query OK, 0 rows affected (0.11 sec)

```sql
INSERT INTO t1 (col1) VALUES (12345),(67890);
```

    Query OK, 2 rows affected (0.00 sec)
    Records: 2  Duplicates: 0  Warnings: 0

```sql
ALTER TABLE t1 MODIFY col1 VARCHAR(5);
```

    Query OK, 0 rows affected (2.52 sec)

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

> **注記：**
>
> -   TiDBは、変更されたデータ型が既存のデータ行と競合する場合にエラーを返します。上記の例では、TiDBは次のエラーを返します。
>
>         alter table t1 modify column col1 varchar(4);
>         ERROR 1406 (22001): Data Too Long, field len 4, data len 5
>
> -   非同期コミット機能との互換性のため、DDL ステートメントは、再編成データへの処理を開始する前に一定期間 (約 2.5 秒) 待機します。
>
>         Query OK, 0 rows affected (2.52 sec)

## MySQLの互換性 {#mysql-compatibility}

-   主キー列のReorg-Data型の変更はサポートされていませんが、Meta-Only型の変更はサポートされています。例：

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

-   生成された列の列型の変更はサポートされていません。例:

    ```sql
    CREATE TABLE t (a INT, b INT as (a+1));
    ALTER TABLE t MODIFY COLUMN b VARCHAR(10);
    ERROR 8200 (HY000): Unsupported modify column: column is generated
    ```

-   パーティションテーブルの列の型の変更はサポートされていません。例:

    ```sql
    CREATE TABLE t (c1 INT, c2 INT, c3 INT) partition by range columns(c1) ( partition p0 values less than (10), partition p1 values less than (maxvalue));
    ALTER TABLE t MODIFY COLUMN c1 DATETIME;
    ERROR 8200 (HY000): Unsupported modify column: table is partition table
    ```

-   TiDB と MySQL 間の`cast`関数の動作に関する互換性の問題により、一部のデータ型 (一部の TIME 型、BIT、SET、ENUM、JSON など) から他の型への変更はサポートされていません。

    ```sql
    CREATE TABLE t (a DECIMAL(13, 7));
    ALTER TABLE t MODIFY COLUMN a DATETIME;
    ERROR 8200 (HY000): Unsupported modify column: change from original type decimal(13,7) to datetime is currently unsupported yet
    ```

## 参照 {#see-also}

-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [表示テーブルの作成](/sql-statements/sql-statement-show-create-table.md)
-   [列を追加](/sql-statements/sql-statement-add-column.md)
-   [ドロップカラム](/sql-statements/sql-statement-drop-column.md)
-   [列の変更](/sql-statements/sql-statement-change-column.md)
