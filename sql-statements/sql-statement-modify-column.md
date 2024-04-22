---
title: MODIFY COLUMN | TiDB SQL Statement Reference
summary: ALTER TABLE.. MODIFY COLUMNステートメントは、既存のテーブルの列を変更します。データ型と属性の変更が含まれる場合があります。TiDB v5.1.0 以降、Reorg データのデータ型の変更をサポートしています。例えば、VARCHARをBIGINTに変更することができます。また、DECIMAL精度を変更したり、VARCHARの長さを圧縮することも可能です。MySQLの互換性に関して、一部のデータ型の変更はサポートされていません。
---

# 列の変更 {#modify-column}

`ALTER TABLE.. MODIFY COLUMN`ステートメントは、既存のテーブルの列を変更します。変更には、データ型と属性の変更が含まれる場合があります。同時に名前を変更するには、代わりに[`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)ステートメントを使用します。

v5.1.0 以降、TiDB は、以下を含む (ただしこれらに限定されない) Reorg データのデータ型の変更をサポートしています。

-   `VARCHAR`を`BIGINT`に変更する
-   `DECIMAL`精度を変更する
-   `VARCHAR(10)` ～ `VARCHAR(5)`の長さを圧縮する

## あらすじ {#synopsis}

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
SHOW CREATE TABLE t1\G;
```

```sql
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `col1` bigint(20) DEFAULT NULL,
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
SHOW CREATE TABLE t1\G;
```

```sql
*************************** 1. row ***************************
       Table: t1
CREATE TABLE `t1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `col1` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=30001
1 row in set (0.00 sec)
```

> **注記：**
>
> -   変更されたデータ型が既存のデータ行と競合する場合、TiDB はエラーを返します。上記の例では、TiDB は次のエラーを返します。
>
>         alter table t1 modify column col1 varchar(4);
>         ERROR 1406 (22001): Data Too Long, field len 4, data len 5
>
> -   Async Commit 機能との互換性のため、DDL ステートメントは、Reorg Data への処理を開始する前に一定時間 (約 2.5 秒) 待機します。
>
>         Query OK, 0 rows affected (2.52 sec)

## MySQLの互換性 {#mysql-compatibility}

-   主キー列の Reorg-Data タイプの変更はサポートされていませんが、Meta-Only タイプの変更はサポートされています。例えば：

    ```sql
    CREATE TABLE t (a int primary key);
    ALTER TABLE t MODIFY COLUMN a VARCHAR(10);
    ERROR 8200 (HY000): Unsupported modify column: column has primary key flag
    ```

    ```sql
    CREATE TABLE t (a int primary key);
    ALTER TABLE t MODIFY COLUMN a INT(10) UNSIGNED;
    ERROR 8200 (HY000): Unsupported modify column: column has primary key flag
    ```

    ```sql
    CREATE TABLE t (a int primary key);
    ALTER TABLE t MODIFY COLUMN a bigint;
    Query OK, 0 rows affected (0.01 sec)
    ```

-   生成された列の列タイプの変更はサポートされていません。例えば：

    ```sql
    CREATE TABLE t (a INT, b INT as (a+1));
    ALTER TABLE t MODIFY COLUMN b VARCHAR(10);
    ERROR 8200 (HY000): Unsupported modify column: column is generated
    ```

-   パーティション化されたテーブルの列タイプの変更はサポートされていません。例えば：

    ```sql
    CREATE TABLE t (c1 INT, c2 INT, c3 INT) partition by range columns(c1) ( partition p0 values less than (10), partition p1 values less than (maxvalue));
    ALTER TABLE t MODIFY COLUMN c1 DATETIME;
    ERROR 8200 (HY000): Unsupported modify column: table is partition table
    ```

-   一部のデータ型 (たとえば、一部の TIME 型、Bit、Set、Enum、JSON) の変更はサポートされていません。これは、TiDB と MySQL の間の`cast`の動作の互換性の問題によりサポートされていません。

    ```sql
    CREATE TABLE t (a DECIMAL(13, 7));
    ALTER TABLE t MODIFY COLUMN a DATETIME;
    ERROR 8200 (HY000): Unsupported modify column: change from original type decimal(13,7) to datetime is currently unsupported yet
    ```

## こちらも参照 {#see-also}

-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [テーブルの作成を表示](/sql-statements/sql-statement-show-create-table.md)
-   [列の追加](/sql-statements/sql-statement-add-column.md)
-   [ドロップカラム](/sql-statements/sql-statement-drop-column.md)
-   [列の変更](/sql-statements/sql-statement-change-column.md)
