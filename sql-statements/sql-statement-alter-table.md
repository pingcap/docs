---
title: ALTER TABLE | TiDB SQL Statement Reference
summary: An overview of the usage of ALTER TABLE for the TiDB database.
---

# 他の机 {#alter-table}

このステートメントは、新しいテーブル構造に適合するように既存のテーブルを変更します。ステートメント`ALTER TABLE`次の目的で使用できます。

-   [<a href="/sql-statements/sql-statement-add-index.md">`ADD`</a>](/sql-statements/sql-statement-add-index.md) 、 [<a href="/sql-statements/sql-statement-drop-index.md">`DROP`</a>](/sql-statements/sql-statement-drop-index.md) 、または[<a href="/sql-statements/sql-statement-rename-index.md">`RENAME`</a>](/sql-statements/sql-statement-rename-index.md)インデックス
-   [<a href="/sql-statements/sql-statement-add-column.md">`ADD`</a>](/sql-statements/sql-statement-add-column.md) 、 [<a href="/sql-statements/sql-statement-drop-column.md">`DROP`</a>](/sql-statements/sql-statement-drop-column.md) 、 [<a href="/sql-statements/sql-statement-modify-column.md">`MODIFY`</a>](/sql-statements/sql-statement-modify-column.md)または[<a href="/sql-statements/sql-statement-change-column.md">`CHANGE`</a>](/sql-statements/sql-statement-change-column.md)列
-   [<a href="/sql-statements/sql-statement-alter-table-compact.md">`COMPACT`</a>](/sql-statements/sql-statement-alter-table-compact.md)テーブルデータ

## あらすじ {#synopsis}

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
|   ( 'AUTO_INCREMENT' | 'AUTO_ID_CACHE' | 'AUTO_RANDOM_BASE' | 'SHARD_ROW_ID_BITS' ) EqOpt LengthNum
|   ( 'CACHE' | 'NOCACHE' )
|   (
        'TTL' EqOpt TimeColumnName '+' 'INTERVAL' Expression TimeUnit (TTLEnable EqOpt ( 'ON' | 'OFF' ))?
        | 'REMOVE' 'TTL'
        | TTLEnable EqOpt ( 'ON' | 'OFF' )
        | TTLJobInterval EqOpt stringLit
    )
|   PlacementPolicyOption

PlacementPolicyOption ::=
    "PLACEMENT" "POLICY" EqOpt PolicyName
|   "PLACEMENT" "POLICY" (EqOpt | "SET") "DEFAULT"
```

## 例 {#examples}

いくつかの初期データを含むテーブルを作成します。

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

次のクエリでは、列 c1 にインデックスが作成されていないため、テーブル全体のスキャンが必要です。

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

ステートメント[<a href="/sql-statements/sql-statement-add-index.md">`ALTER TABLE .. ADD INDEX`</a>](/sql-statements/sql-statement-add-index.md)は、テーブル t1 にインデックスを追加するために使用できます。 `EXPLAIN` 、元のクエリがより効率的なインデックス範囲スキャンを使用していることを確認します。

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

TiDB は、DDL 変更で`ALTER`のアルゴリズムが使用されることをアサートする機能をサポートしています。これは単なるアサーションであり、テーブルの変更に使用される実際のアルゴリズムは変更されません。これは、クラスターのピーク時間中にのみ DDL の即時変更を許可したい場合に便利です。

{{< copyable "" >}}

```sql
ALTER TABLE t1 DROP INDEX c1, ALGORITHM=INSTANT;
```

```sql
Query OK, 0 rows affected (0.24 sec)
```

`INPLACE`アルゴリズムを必要とする操作で`ALGORITHM=INSTANT`アサーションを使用すると、ステートメント エラーが発生します。

{{< copyable "" >}}

```sql
ALTER TABLE t1 ADD INDEX (c1), ALGORITHM=INSTANT;
```

```sql
ERROR 1846 (0A000): ALGORITHM=INSTANT is not supported. Reason: Cannot alter table by INSTANT. Try ALGORITHM=INPLACE.
```

ただし、 `INPLACE`操作に`ALGORITHM=COPY`アサーションを使用すると、エラーではなく警告が生成されます。これは、TiDB がアサーションを*このアルゴリズム以上のもの*として解釈するためです。 TiDB が使用するアルゴリズムは MySQL とは異なる可能性があるため、この動作の違いは MySQL の互換性にとって役立ちます。

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

TiDB の`ALTER TABLE`には、次の主要な制限が適用されます。

-   単一の`ALTER TABLE`ステートメントで複数のスキーマ オブジェクトを変更する場合:

    -   同じオブジェクトを複数回変更することはサポートされていません。
    -   TiDB は、**実行前に**テーブル スキーマに従ってステートメントを検証します。たとえば、列`c1`がテーブルに存在しないため、 `ALTER TABLE t ADD COLUMN c1 INT, ADD COLUMN c2 INT AFTER c1;`実行するとエラーが返されます。
    -   `ALTER TABLE`ステートメントの場合、TiDB での実行順序は左から右に次々と変更され、場合によっては MySQL と互換性がありません。

-   主キー列の[<a href="/sql-statements/sql-statement-modify-column.md#reorg-data-change">データの再編成</a>](/sql-statements/sql-statement-modify-column.md#reorg-data-change)タイプの変更はサポートされていません。

-   パーティション化されたテーブルの列タイプの変更はサポートされていません。

-   生成された列の列タイプの変更はサポートされていません。

-   一部のデータ型 (たとえば、一部の TIME、Bit、Set、Enum、および JSON 型) の変更は、TiDB と MySQL の間の`CAST`の動作の互換性の問題によりサポートされません。

-   空間データ型はサポートされていません。

-   `ALTER TABLE t CACHE | NOCACHE`は、MySQL 構文の TiDB 拡張機能です。詳細は[<a href="/cached-tables.md">キャッシュされたテーブル</a>](/cached-tables.md)を参照してください。

さらなる制限については、 [<a href="/mysql-compatibility.md#ddl">MySQL の互換性</a>](/mysql-compatibility.md#ddl)を参照してください。

## こちらも参照 {#see-also}

-   [<a href="/mysql-compatibility.md#ddl">MySQL の互換性</a>](/mysql-compatibility.md#ddl)
-   [<a href="/sql-statements/sql-statement-add-column.md">列の追加</a>](/sql-statements/sql-statement-add-column.md)
-   [<a href="/sql-statements/sql-statement-drop-column.md">ドロップカラム</a>](/sql-statements/sql-statement-drop-column.md)
-   [<a href="/sql-statements/sql-statement-add-index.md">インデックスの追加</a>](/sql-statements/sql-statement-add-index.md)
-   [<a href="/sql-statements/sql-statement-drop-index.md">ドロップインデックス</a>](/sql-statements/sql-statement-drop-index.md)
-   [<a href="/sql-statements/sql-statement-rename-index.md">インデックスの名前を変更</a>](/sql-statements/sql-statement-rename-index.md)
-   [<a href="/sql-statements/sql-statement-alter-index.md">インデックスの変更</a>](/sql-statements/sql-statement-alter-index.md)
-   [<a href="/sql-statements/sql-statement-create-table.md">テーブルの作成</a>](/sql-statements/sql-statement-create-table.md)
-   [<a href="/sql-statements/sql-statement-drop-table.md">ドロップテーブル</a>](/sql-statements/sql-statement-drop-table.md)
-   [<a href="/sql-statements/sql-statement-show-create-table.md">テーブルの作成を表示</a>](/sql-statements/sql-statement-show-create-table.md)
