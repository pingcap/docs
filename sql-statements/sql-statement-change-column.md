---
title: CHANGE COLUMN | TiDB SQL Statement Reference
summary: An overview of the usage of CHANGE COLUMN for the TiDB database.
---

# 列を変更する {#change-column}

`ALTER TABLE.. CHANGE COLUMN`ステートメントは、既存のテーブルの列を変更します。変更には、列の名前の変更と、データ型の互換性のある型への変更の両方が含まれる場合があります。

v5.1.0以降、TiDBはReorgデータ型の変更をサポートしています。これには以下が含まれますが、これらに限定されません。

-   `VARCHAR`から`BIGINT`に変更
-   `DECIMAL`精度の変更
-   `VARCHAR(10)`から`VARCHAR(5)`の長さを圧縮します

## あらすじ {#synopsis}

```ebnf+diagram
AlterTableStmt
         ::= 'ALTER' 'IGNORE'? 'TABLE' TableName ChangeColumnSpec ( ',' ChangeColumnSpec )*

ChangeColumnSpec
         ::= 'CHANGE' ColumnKeywordOpt 'IF EXISTS' ColumnName ColumnName ColumnType ColumnOption* ( 'FIRST' | 'AFTER' ColumnName )?

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

{{< copyable "" >}}

```sql
CREATE TABLE t1 (id int not null primary key AUTO_INCREMENT, col1 INT);
```

```
Query OK, 0 rows affected (0.11 sec)
```

{{< copyable "" >}}

```sql
INSERT INTO t1 (col1) VALUES (1),(2),(3),(4),(5);
```

```
Query OK, 5 rows affected (0.02 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

{{< copyable "" >}}

```sql
ALTER TABLE t1 CHANGE col1 col2 INT;
```

```
Query OK, 0 rows affected (0.09 sec)
```

{{< copyable "" >}}

```sql
ALTER TABLE t1 CHANGE col2 col3 BIGINT, ALGORITHM=INSTANT;
```

```
Query OK, 0 rows affected (0.08 sec)
```

{{< copyable "" >}}

```sql
ALTER TABLE t1 CHANGE col3 col4 BIGINT, CHANGE id id2 INT NOT NULL;
```

```
ERROR 1105 (HY000): can't run multi schema change
```

{{< copyable "" >}}

```sql
CREATE TABLE t (a int primary key);
ALTER TABLE t CHANGE COLUMN a a VARCHAR(10);
```

```
ERROR 8200 (HY000): Unsupported modify column: column has primary key flag
```

{{< copyable "" >}}

```sql
CREATE TABLE t (c1 INT, c2 INT, c3 INT) partition by range columns(c1) ( partition p0 values less than (10), partition p1 values less than (maxvalue));
ALTER TABLE t CHANGE COLUMN c1 c1 DATETIME;
```

```
ERROR 8200 (HY000): Unsupported modify column: table is partition table
```

{{< copyable "" >}}

```sql
CREATE TABLE t (a INT, b INT as (a+1));
ALTER TABLE t CHANGE COLUMN b b VARCHAR(10);
```

```
ERROR 8200 (HY000): Unsupported modify column: column is generated
```

{{< copyable "" >}}

```sql
CREATE TABLE t (a DECIMAL(13, 7));
ALTER TABLE t CHANGE COLUMN a a DATETIME;
```

```
ERROR 8200 (HY000): Unsupported modify column: change from original type decimal(13,7) to datetime is currently unsupported yet
```

## MySQLの互換性 {#mysql-compatibility}

-   現在、 `ALTER TABLE`のステートメントで複数の変更を行うことはサポートされていません。
-   主キー列の[Reorg-データ](/sql-statements/sql-statement-modify-column.md#reorg-data-change)タイプの変更はサポートされていません。
-   パーティション表の列タイプの変更はサポートされていません。
-   生成された列の列タイプの変更はサポートされていません。
-   一部のデータ型（たとえば、一部のTIME、Bit、Set、Enum、およびJSON型）の変更は、TiDBとMySQL間の`CAST`関数の動作の互換性の問題のためにサポートされていません。

## も参照してください {#see-also}

-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [作成テーブルを表示](/sql-statements/sql-statement-show-create-table.md)
-   [列を追加](/sql-statements/sql-statement-add-column.md)
-   [ドロップ列](/sql-statements/sql-statement-drop-column.md)
-   [列の変更](/sql-statements/sql-statement-modify-column.md)
