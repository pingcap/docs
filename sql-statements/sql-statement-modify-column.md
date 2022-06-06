---
title: MODIFY COLUMN | TiDB SQL Statement Reference
summary: An overview of the usage of MODIFY COLUMN for the TiDB database.
---

# 列の変更 {#modify-column}

`ALTER TABLE.. MODIFY COLUMN`ステートメントは、既存のテーブルの列を変更します。変更には、データ型と属性の変更を含めることができます。同時に名前を変更するには、代わりに[`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)ステートメントを使用してください。

v5.1.0以降、TiDBはReorgデータのデータ型の変更をサポートしています。これには以下が含まれますが、これらに限定されません。

-   `VARCHAR`から`BIGINT`に変更
-   `DECIMAL`精度の変更
-   `VARCHAR(10)`から`VARCHAR(5)`の長さを圧縮します

## あらすじ {#synopsis}

```ebnf+diagram
AlterTableStmt ::=
    'ALTER' IgnoreOptional 'TABLE' TableName ( AlterTableSpecListOpt AlterTablePartitionOpt | 'ANALYZE' 'PARTITION' PartitionNameList ( 'INDEX' IndexNameList )? AnalyzeOptionListOpt )

AlterTableSpec ::=
    TableOptionList
|   'SET' 'TIFLASH' 'REPLICA' LengthNum LocationLabelList
|   'CONVERT' 'TO' CharsetKw ( CharsetName | 'DEFAULT' ) OptCollate
|   'ADD' ( ColumnKeywordOpt IfNotExists ( ColumnDef ColumnPosition | '(' TableElementList ')' ) | Constraint | 'PARTITION' IfNotExists NoWriteToBinLogAliasOpt ( PartitionDefinitionListOpt | 'PARTITIONS' NUM ) )
|   ( ( 'CHECK' | 'TRUNCATE' ) 'PARTITION' | ( 'OPTIMIZE' | 'REPAIR' | 'REBUILD' ) 'PARTITION' NoWriteToBinLogAliasOpt ) AllOrPartitionNameList
|   'COALESCE' 'PARTITION' NoWriteToBinLogAliasOpt NUM
|   'DROP' ( ColumnKeywordOpt IfExists ColumnName RestrictOrCascadeOpt | 'PRIMARY' 'KEY' | 'PARTITION' IfExists PartitionNameList | ( KeyOrIndex IfExists | 'CHECK' ) Identifier | 'FOREIGN' 'KEY' IfExists Symbol )
|   'EXCHANGE' 'PARTITION' Identifier 'WITH' 'TABLE' TableName WithValidationOpt
|   ( 'IMPORT' | 'DISCARD' ) ( 'PARTITION' AllOrPartitionNameList )? 'TABLESPACE'
|   'REORGANIZE' 'PARTITION' NoWriteToBinLogAliasOpt ReorganizePartitionRuleOpt
|   'ORDER' 'BY' AlterOrderItem ( ',' AlterOrderItem )*
|   ( 'DISABLE' | 'ENABLE' ) 'KEYS'
|   ( 'MODIFY' ColumnKeywordOpt IfExists | 'CHANGE' ColumnKeywordOpt IfExists ColumnName ) ColumnDef ColumnPosition
|   'ALTER' ( ColumnKeywordOpt ColumnName ( 'SET' 'DEFAULT' ( SignedLiteral | '(' Expression ')' ) | 'DROP' 'DEFAULT' ) | 'CHECK' Identifier EnforcedOrNot | 'INDEX' Identifier IndexInvisible )
|   'RENAME' ( ( 'COLUMN' | KeyOrIndex ) Identifier 'TO' Identifier | ( 'TO' | '='? | 'AS' ) TableName )
|   LockClause
|   AlgorithmClause
|   'FORCE'
|   ( 'WITH' | 'WITHOUT' ) 'VALIDATION'
|   'SECONDARY_LOAD'
|   'SECONDARY_UNLOAD'

ColumnKeywordOpt ::= 'COLUMN'?

ColumnDef ::=
    ColumnName ( Type | 'SERIAL' ) ColumnOptionListOpt

ColumnPosition ::=
    ( 'FIRST' | 'AFTER' ColumnName )?
```

## 例 {#examples}

### メタのみの変更 {#meta-only-change}

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
ALTER TABLE t1 MODIFY col1 BIGINT;
```

```
Query OK, 0 rows affected (0.09 sec)
```

{{< copyable "" >}}

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

### Reorg-データ変更 {#reorg-data-change}

{{< copyable "" >}}

```sql
CREATE TABLE t1 (id int not null primary key AUTO_INCREMENT, col1 INT);
```

```
Query OK, 0 rows affected (0.11 sec)
```

{{< copyable "" >}}

```sql
INSERT INTO t1 (col1) VALUES (12345),(67890);
```

```
Query OK, 2 rows affected (0.00 sec)
Records: 2  Duplicates: 0  Warnings: 0
```

{{< copyable "" >}}

```sql
ALTER TABLE t1 MODIFY col1 VARCHAR(5);
```

```
Query OK, 0 rows affected (2.52 sec)
```

{{< copyable "" >}}

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

> **ノート：**
>
> -   変更されたデータ型が既存のデータ行と競合する場合、TiDBはエラーを返します。上記の例では、TiDBは次のエラーを返します。
>
>     ```
>     alter table t1 modify column col1 varchar(4);
>     ERROR 1406 (22001): Data Too Long, field len 4, data len 5
>     ```
>
> -   非同期コミット機能との互換性により、DDLステートメントはReorg Dataへの処理を開始する前に一定期間（約2.5秒）待機します。
>
>     ```
>     Query OK, 0 rows affected (2.52 sec)
>     ```

## MySQLの互換性 {#mysql-compatibility}

-   単一の`ALTER TABLE`ステートメントを使用した複数の列の変更はサポートされていません。例えば：

    ```sql
    ALTER TABLE t1 MODIFY col1 BIGINT, MODIFY id BIGINT NOT NULL;
    ERROR 1105 (HY000): Unsupported multi schema change
    ```

-   主キー列のReorg-Dataタイプの変更はサポートしていませんが、Meta-Onlyタイプの変更はサポートしています。例えば：

    ```sql
    CREATE TABLE t (a int primary key);
    ALTER TABLE t MODIFY COLUMN a VARCHAR(10);
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

-   パーティションテーブルの列タイプの変更はサポートされていません。例えば：

    ```sql
    CREATE TABLE t (c1 INT, c2 INT, c3 INT) partition by range columns(c1) ( partition p0 values less than (10), partition p1 values less than (maxvalue));
    ALTER TABLE t MODIFY COLUMN c1 DATETIME;
    ERROR 8200 (HY000): Unsupported modify column: table is partition table
    ```

-   一部のデータ型（たとえば、一部のTIME型、ビット、セット、列挙型、JSON）の変更はサポートされていません。これは、TiDBとMySQL間の`cast`関数の動作の互換性の問題のためです。

    ```sql
    CREATE TABLE t (a DECIMAL(13, 7));
    ALTER TABLE t MODIFY COLUMN a DATETIME;
    ERROR 8200 (HY000): Unsupported modify column: change from original type decimal(13,7) to datetime is currently unsupported yet
    ```

## も参照してください {#see-also}

-   [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
-   [CREATETABLEを表示する](/sql-statements/sql-statement-show-create-table.md)
-   [列を追加](/sql-statements/sql-statement-add-column.md)
-   [ドロップ列](/sql-statements/sql-statement-drop-column.md)
-   [列を変更する](/sql-statements/sql-statement-change-column.md)
