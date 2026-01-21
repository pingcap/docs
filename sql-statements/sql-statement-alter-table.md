---
title: ALTER TABLE | TiDB SQL Statement Reference
summary: TiDB データベースの ALTER TABLE の使用法の概要。
---

# テーブルの変更 {#alter-table}

この文は、既存のテーブルを新しいテーブル構造に適合するように変更します。文`ALTER TABLE`は次の目的で使用できます。

-   [`ADD`](/sql-statements/sql-statement-add-index.md) 、 [`DROP`](/sql-statements/sql-statement-drop-index.md) 、または[`RENAME`](/sql-statements/sql-statement-rename-index.md)インデックス
-   [`ADD`](/sql-statements/sql-statement-add-column.md) [`DROP`](/sql-statements/sql-statement-drop-column.md)または[`MODIFY`](/sql-statements/sql-statement-modify-column.md) [`CHANGE`](/sql-statements/sql-statement-change-column.md)
-   [`COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)テーブルデータ

## 概要 {#synopsis}

```ebnf+diagram
AlterTableStmt ::=
    'ALTER' IgnoreOptional 'TABLE' TableName (
        AlterTableSpecListOpt AlterTablePartitionOpt |
        'ANALYZE' 'PARTITION' PartitionNameList ( 'INDEX' IndexNameList )? AnalyzeOptionListOpt |
        'COMPACT' ( 'PARTITION' PartitionNameList )? 'TIFLASH' 'REPLICA'
    )

TableName ::=
    Identifier ('.' Identifier)?

AlterTableSpec ::=
    TableOptionList
|   'SET' 'TIFLASH' 'REPLICA' LengthNum LocationLabelList
|   'CONVERT' 'TO' CharsetKw ( CharsetName | 'DEFAULT' ) OptCollate
|   'ADD' ( ColumnKeywordOpt IfNotExists ( ColumnDef ColumnPosition | '(' TableElementList ')' ) | Constraint | 'PARTITION' IfNotExists NoWriteToBinLogAliasOpt ( PartitionDefinitionListOpt | 'PARTITIONS' NUM ) )
|   ( ( 'CHECK' | 'TRUNCATE' ) 'PARTITION' | ( 'OPTIMIZE' | 'REPAIR' | 'REBUILD' ) 'PARTITION' NoWriteToBinLogAliasOpt ) AllOrPartitionNameList
|   'COALESCE' 'PARTITION' NoWriteToBinLogAliasOpt NUM
|   'DROP' ( ColumnKeywordOpt IfExists ColumnName RestrictOrCascadeOpt | 'PRIMARY' 'KEY' |  'PARTITION' IfExists PartitionNameList | ( KeyOrIndex IfExists | 'CHECK' ) Identifier | 'FOREIGN' 'KEY' Symbol )
|   'EXCHANGE' 'PARTITION' Identifier 'WITH' 'TABLE' TableName WithValidationOpt
|   ( 'IMPORT' | 'DISCARD' ) ( 'PARTITION' AllOrPartitionNameList )? 'TABLESPACE'
|   'REORGANIZE' 'PARTITION' NoWriteToBinLogAliasOpt ReorganizePartitionRuleOpt
|   'ORDER' 'BY' AlterOrderItem ( ',' AlterOrderItem )*
|   ( 'DISABLE' | 'ENABLE' ) 'KEYS'
|   ( 'MODIFY' ColumnKeywordOpt IfExists | 'CHANGE' ColumnKeywordOpt IfExists ColumnName ) ColumnDef ColumnPosition
|   'ALTER' ( ColumnKeywordOpt ColumnName ( 'SET' 'DEFAULT' ( SignedLiteral | '(' Expression ')' ) | 'DROP' 'DEFAULT' ) | 'CHECK' Identifier EnforcedOrNot | 'INDEX' Identifier ("VISIBLE" | "INVISIBLE") )
|   'RENAME' ( ( 'COLUMN' | KeyOrIndex ) Identifier 'TO' Identifier | ( 'TO' | '='? | 'AS' ) TableName )
|   LockClause
|   AlgorithmClause
|   'FORCE'
|   ( 'WITH' | 'WITHOUT' ) 'VALIDATION'
|   'SECONDARY_LOAD'
|   'SECONDARY_UNLOAD'
|   ( 'AUTO_INCREMENT' | 'AUTO_ID_CACHE' | 'AUTO_RANDOM_BASE' | 'SHARD_ROW_ID_BITS' ) EqOpt LengthNum
|   ( 'CACHE' | 'NOCACHE' )
|   (
        'TTL' EqOpt TimeColumnName '+' 'INTERVAL' Expression TimeUnit (TTLEnable EqOpt ( 'ON' | 'OFF' ))?
        | 'REMOVE' 'TTL'
        | TTLEnable EqOpt ( 'ON' | 'OFF' )
        | TTLJobInterval EqOpt stringLit
    )
|   'AFFINITY' EqOpt stringLit
|   PlacementPolicyOption

PlacementPolicyOption ::=
    "PLACEMENT" "POLICY" EqOpt PolicyName
|   "PLACEMENT" "POLICY" (EqOpt | "SET") "DEFAULT"
```

## 例 {#examples}

初期データを含むテーブルを作成します。

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
```

```sql
Query OK, 0 rows affected (0.11 sec)

Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

次のクエリでは、列 c1 にインデックスが付いていないため、完全なテーブルスキャンが必要です。

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

ステートメント[`ALTER TABLE .. ADD INDEX`](/sql-statements/sql-statement-add-index.md)は、テーブル t1 にインデックスを追加するために使用できます。3 `EXPLAIN`元のクエリでインデックス範囲スキャンが使用されるようになり、より効率的になっていることを確認します。

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

TiDBは、DDL変更が`ALTER`のアルゴリズムを使用していることをアサートする機能をサポートしています。これは単なるアサーションであり、テーブルの変更に使用される実際のアルゴリズムは変更されないことに注意してください。

```sql
ALTER TABLE t1 DROP INDEX c1, ALGORITHM=INSTANT;
```

```sql
Query OK, 0 rows affected (0.24 sec)
```

`INPLACE`アルゴリズムを必要とする操作で`ALGORITHM=INSTANT`アサーションを使用すると、ステートメント エラーが発生します。

```sql
ALTER TABLE t1 ADD INDEX (c1), ALGORITHM=INSTANT;
```

```sql
ERROR 1846 (0A000): ALGORITHM=INSTANT is not supported. Reason: Cannot alter table by INSTANT. Try ALGORITHM=INPLACE.
```

ただし、 `ALGORITHM=COPY`アサーションを`INPLACE`操作に使用すると、エラーではなく警告が生成されます。これは、TiDB がアサーションを「*このアルゴリズム以上」*と解釈するためです。TiDB が使用するアルゴリズムは MySQL と異なる可能性があるため、この動作の違いは MySQL との互換性を保つために役立ちます。

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

TiDB の`ALTER TABLE`には次の主な制限が適用されます。

-   `ALTER TABLE`つのステートメントで複数のスキーマ オブジェクトを変更する場合:

    -   同じオブジェクトを複数回変更することはサポートされていません。
    -   TiDBは**実行前に**テーブルスキーマに従ってステートメントを検証します。例えば、 `ALTER TABLE t ADD COLUMN c1 INT, ADD COLUMN c2 INT AFTER c1;`を実行すると、列`c1`テーブルに存在しないためエラーが返されます。
    -   `ALTER TABLE`ステートメントの場合、TiDB での実行順序は左から右への変更が 1 つずつ順番に実行されるため、場合によっては MySQL と互換性がありません。

-   主キー列の[再編成データ](/sql-statements/sql-statement-modify-column.md#reorg-data-change)種類の変更はサポートされていません。

-   パーティション化されたテーブル上の列タイプの変更はサポートされていません。

-   生成された列の列タイプの変更はサポートされていません。

-   一部のデータ型 (たとえば、一部の TIME、Bit、Set、Enum、JSON 型) の変更は、TiDB と MySQL 間の`CAST`関数の動作の互換性の問題によりサポートされていません。

-   `AFFINITY`オプションは TiDB 拡張構文です。テーブルで`AFFINITY`有効にすると、パーティションの追加、削除、再編成、スワップなど、そのテーブルのパーティションスキームを変更できなくなります。パーティションスキームを変更するには、まず`AFFINITY`削除する必要があります。

-   空間データ型はサポートされていません。

-   `ALTER TABLE t CACHE | NOCACHE`はMySQL構文に対するTiDB拡張です。詳細については[キャッシュされたテーブル](/cached-tables.md)参照してください。

詳細な制限については[MySQLの互換性](/mysql-compatibility.md#ddl-operations)参照してください。

## 参照 {#see-also}

-   [MySQLの互換性](/mysql-compatibility.md#ddl-operations)
-   [列を追加](/sql-statements/sql-statement-add-column.md)
-   [ドロップカラム](/sql-statements/sql-statement-drop-column.md)
-   [インデックスを追加](/sql-statements/sql-statement-add-index.md)
-   [インデックスを削除](/sql-statements/sql-statement-drop-index.md)
-   [インデックス名の変更](/sql-statements/sql-statement-rename-index.md)
-   [インデックスの変更](/sql-statements/sql-statement-alter-index.md)
-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [テーブルを削除](/sql-statements/sql-statement-drop-table.md)
-   [表示テーブルの作成](/sql-statements/sql-statement-show-create-table.md)
