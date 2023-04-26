---
title: ALTER TABLE | TiDB SQL Statement Reference
summary: An overview of the usage of ALTER TABLE for the TiDB database.
---

# 他の机 {#alter-table}

このステートメントは、新しいテーブル構造に準拠するように既存のテーブルを変更します。ステートメント`ALTER TABLE`は、次の目的で使用できます。

-   [`ADD`](/sql-statements/sql-statement-add-index.md) 、 [`DROP`](/sql-statements/sql-statement-drop-index.md) 、または[`RENAME`](/sql-statements/sql-statement-rename-index.md)インデックス
-   [`ADD`](/sql-statements/sql-statement-add-column.md) 、 [`DROP`](/sql-statements/sql-statement-drop-column.md) 、 [`MODIFY`](/sql-statements/sql-statement-modify-column.md)または[`CHANGE`](/sql-statements/sql-statement-change-column.md)列
-   [`COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)テーブル データ

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
    )
|   PlacementPolicyOption

PlacementPolicyOption ::=
    "PLACEMENT" "POLICY" EqOpt PolicyName
|   "PLACEMENT" "POLICY" (EqOpt | "SET") "DEFAULT"
```

## 例 {#examples}

初期データを含むテーブルを作成します。

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

次のクエリでは、列 c1 にインデックスが付けられていないため、完全なテーブル スキャンが必要です。

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

ステートメント[`ALTER TABLE .. ADD INDEX`](/sql-statements/sql-statement-add-index.md)使用して、テーブル t1 にインデックスを追加できます。 `EXPLAIN` 、元のクエリがより効率的なインデックス レンジ スキャンを使用するようになったことを確認します。

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

TiDB は、DDL の変更が特定の`ALTER`アルゴリズムを使用することをアサートする機能をサポートしています。これは単なるアサーションであり、テーブルの変更に使用される実際のアルゴリズムを変更するものではありません。クラスターのピーク時に即時の DDL 変更のみを許可する場合に役立ちます。

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

ただし、 `INPLACE`操作に`ALGORITHM=COPY`アサーションを使用すると、エラーではなく警告が生成されます。これは、TiDB がアサーションを*このアルゴリズム以上のもの*として解釈するためです。 TiDB が使用するアルゴリズムは MySQL とは異なる可能性があるため、この動作の違いは MySQL の互換性に役立ちます。

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

## MySQL の互換性 {#mysql-compatibility}

次の主要な制限が TiDB の`ALTER TABLE`に適用されます。

-   単一の`ALTER TABLE`ステートメントで複数のスキーマ オブジェクトを変更する場合:

    -   複数の変更で同じオブジェクトを変更することはサポートされていません。
    -   TiDB は、**実行前に**テーブル スキーマに従ってステートメントを検証します。たとえば、インデックス`i`テーブルに存在しないため、 `ALTER TABLE ADD INDEX i(b), DROP INDEX i;`実行するとエラーが返されます。
    -   `ALTER TABLE`ステートメントの場合、TiDB での実行順序は左から右に次々と変更されます。これは、場合によっては MySQL と互換性がありません。

-   主キー列の[再編成データ](/sql-statements/sql-statement-modify-column.md#reorg-data-change)型の変更はサポートされていません。

-   分割されたテーブルでの列の型の変更はサポートされていません。

-   生成された列の列タイプの変更はサポートされていません。

-   TiDB と MySQL 間の`CAST`関数の動作の互換性の問題により、一部のデータ型 (たとえば、一部の TIME、Bit、Set、Enum、および JSON 型) の変更はサポートされていません。

-   空間データ型はサポートされていません。

-   `ALTER TABLE t CACHE | NOCACHE`は、MySQL 構文に対する TiDB 拡張です。詳細については、 [キャッシュされたテーブル](/cached-tables.md)を参照してください。

その他の制限については、 [MySQL の互換性](/mysql-compatibility.md#ddl)を参照してください。

## こちらもご覧ください {#see-also}

-   [MySQL の互換性](/mysql-compatibility.md#ddl)
-   [列を追加](/sql-statements/sql-statement-add-column.md)
-   [ドロップ カラム](/sql-statements/sql-statement-drop-column.md)
-   [インデックスを追加](/sql-statements/sql-statement-add-index.md)
-   [ドロップインデックス](/sql-statements/sql-statement-drop-index.md)
-   [インデックスの名前を変更](/sql-statements/sql-statement-rename-index.md)
-   [インデックスの変更](/sql-statements/sql-statement-alter-index.md)
-   [テーブルを作成](/sql-statements/sql-statement-create-table.md)
-   [ドロップテーブル](/sql-statements/sql-statement-drop-table.md)
-   [テーブルの作成を表示](/sql-statements/sql-statement-show-create-table.md)
