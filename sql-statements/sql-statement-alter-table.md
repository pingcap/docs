---
title: ALTER TABLE | TiDB SQL Statement Reference
summary: An overview of the usage of ALTER TABLE for the TiDB database.
---

# 他の机 {#alter-table}

このステートメントは、新しいテーブル構造に準拠するように既存のテーブルを変更します。ステートメント`ALTER TABLE`は、次の目的で使用できます。

-   [`ADD`](/sql-statements/sql-statement-add-index.md) 、または[`RENAME`](/sql-statements/sql-statement-rename-index.md) [`DROP`](/sql-statements/sql-statement-drop-index.md)インデックス
-   [`ADD`](/sql-statements/sql-statement-add-column.md) [`MODIFY`](/sql-statements/sql-statement-modify-column.md) [`DROP`](/sql-statements/sql-statement-drop-column.md) [`CHANGE`](/sql-statements/sql-statement-change-column.md)

## あらすじ {#synopsis}

```ebnf+diagram
AlterTableStmt ::=
    'ALTER' IgnoreOptional 'TABLE' TableName ( AlterTableSpecListOpt AlterTablePartitionOpt | 'ANALYZE' 'PARTITION' PartitionNameList ( 'INDEX' IndexNameList )? AnalyzeOptionListOpt )

TableName ::=
    Identifier ('.' Identifier)?

AlterTableSpec ::=
    TableOptionList
|   'SET' 'TIFLASH' 'REPLICA' LengthNum LocationLabelList
|   'CONVERT' 'TO' CharsetKw ( CharsetName | 'DEFAULT' ) OptCollate
|   'ADD' ( ColumnKeywordOpt IfNotExists ( ColumnDef ColumnPosition | '(' TableElementList ')' ) | Constraint | 'PARTITION' IfNotExists NoWriteToBinLogAliasOpt ( PartitionDefinitionListOpt | 'PARTITIONS' NUM ) )
|   ( ( 'CHECK' | 'TRUNCATE' ) 'PARTITION' | ( 'OPTIMIZE' | 'REPAIR' | 'REBUILD' ) 'PARTITION' NoWriteToBinLogAliasOpt ) AllOrPartitionNameList
|   'COALESCE' 'PARTITION' NoWriteToBinLogAliasOpt NUM
|   'DROP' ( ColumnKeywordOpt IfExists ColumnName RestrictOrCascadeOpt | 'PRIMARY' 'KEY' |  'PARTITION' IfExists PartitionNameList | ( KeyOrIndex IfExists | 'CHECK' ) Identifier | 'FOREIGN' 'KEY' IfExists Symbol )
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
| ( 'AUTO_INCREMENT' | 'AUTO_ID_CACHE' | 'AUTO_RANDOM_BASE' | 'SHARD_ROW_ID_BITS' ) EqOpt LengthNum
```

## 例 {#examples}

いくつかの初期データを使用してテーブルを作成します。

{{< copyable "" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
```

```sql
Query OK, 0 rows affected (0.11 sec)

Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

次のクエリでは、列c1にインデックスが付けられていないため、全表スキャンが必要です。

{{< copyable "" >}}

```sql
EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
```

```sql
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_7           | 10.00    | root      |               | data:Selection_6               |
| └─Selection_6           | 10.00    | cop[tikv] |               | eq(test.t1.c1, 3)              |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

ステートメント[`ALTER TABLE .. ADD INDEX`](/sql-statements/sql-statement-add-index.md)を使用して、テーブルt1にインデックスを追加できます。 `EXPLAIN`は、元のクエリがインデックス範囲スキャンを使用していることを確認します。これはより効率的です。

{{< copyable "" >}}

```sql
ALTER TABLE t1 ADD INDEX (c1);
EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
```

```sql
Query OK, 0 rows affected (0.30 sec)

+------------------------+---------+-----------+------------------------+---------------------------------------------+
| id                     | estRows | task      | access object          | operator info                               |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| IndexReader_6          | 10.00   | root      |                        | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 10.00   | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
2 rows in set (0.00 sec)
```

TiDBは、DDLの変更が特定の`ALTER`アルゴリズムを使用することを表明する機能をサポートしています。これは単なるアサーションであり、テーブルの変更に使用される実際のアルゴリズムを変更するものではありません。クラスタのピーク時にのみインスタントDDL変更を許可する場合に便利です。

{{< copyable "" >}}

```sql
ALTER TABLE t1 DROP INDEX c1, ALGORITHM=INSTANT;
```

```sql
Query OK, 0 rows affected (0.24 sec)
```

`INPLACE`アルゴリズムを必要とする操作で`ALGORITHM=INSTANT`アサーションを使用すると、ステートメントエラーが発生します。

{{< copyable "" >}}

```sql
ALTER TABLE t1 ADD INDEX (c1), ALGORITHM=INSTANT;
```

```sql
ERROR 1846 (0A000): ALGORITHM=INSTANT is not supported. Reason: Cannot alter table by INSTANT. Try ALGORITHM=INPLACE.
```

ただし、 `INPLACE`操作に`ALGORITHM=COPY`アサーションを使用すると、エラーではなく警告が生成されます。これは、TiDBがアサーションを*このアルゴリズム以上として解釈するためです*。 TiDBが使用するアルゴリズムはMySQLとは異なる可能性があるため、この動作の違いはMySQLの互換性に役立ちます。

{{< copyable "" >}}

```sql
ALTER TABLE t1 ADD INDEX (c1), ALGORITHM=COPY;
SHOW WARNINGS;
```

```sql
Query OK, 0 rows affected, 1 warning (0.25 sec)

+-------+------+---------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                     |
+-------+------+---------------------------------------------------------------------------------------------+
| Error | 1846 | ALGORITHM=COPY is not supported. Reason: Cannot alter table by COPY. Try ALGORITHM=INPLACE. |
+-------+------+---------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

次の主な制限は、TiDBの`ALTER TABLE`に適用されます。

-   現在、 `ALTER TABLE`のステートメントで複数の変更を行うことはサポートされていません。

-   主キー列の[Reorg-データ](/sql-statements/sql-statement-modify-column.md#reorg-data-change)タイプの変更はサポートされていません。

-   パーティション表の列タイプの変更はサポートされていません。

-   生成された列の列タイプの変更はサポートされていません。

-   一部のデータ型（たとえば、一部のTIME、Bit、Set、Enum、およびJSON型）の変更は、TiDBとMySQL間の`CAST`関数の動作の互換性の問題のためにサポートされていません。

-   空間データ型はサポートされていません。

さらなる制限については、 [MySQLの互換性](/mysql-compatibility.md#ddl)を参照してください。

## も参照してください {#see-also}

-   [MySQLの互換性](/mysql-compatibility.md#ddl)
-   [列を追加](/sql-statements/sql-statement-add-column.md)
-   [ドロップ列](/sql-statements/sql-statement-drop-column.md)
-   [インデックスを追加](/sql-statements/sql-statement-add-index.md)
-   [ドロップインデックス](/sql-statements/sql-statement-drop-index.md)
-   [インデックスの名前を変更](/sql-statements/sql-statement-rename-index.md)
-   [ALTER INDEX](/sql-statements/sql-statement-alter-index.md)
-   [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
-   [ドロップテーブル](/sql-statements/sql-statement-drop-table.md)
-   [CREATETABLEを表示する](/sql-statements/sql-statement-show-create-table.md)
