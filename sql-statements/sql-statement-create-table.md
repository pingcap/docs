---
title: CREATE TABLE | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE TABLE for the TiDB database.
---

# テーブルを作成 {#create-table}

このステートメントは、現在選択されているデータベースに新しいテーブルを作成します。 MySQL の`CREATE TABLE`ステートメントと同様に動作します。

## あらすじ {#synopsis}

```ebnf+diagram
CreateTableStmt ::=
    'CREATE' OptTemporary 'TABLE' IfNotExists TableName ( TableElementListOpt CreateTableOptionListOpt PartitionOpt DuplicateOpt AsOpt CreateTableSelectOpt | LikeTableWithOrWithoutParen ) OnCommitOpt

OptTemporary ::=
    ( 'TEMPORARY' | ('GLOBAL' 'TEMPORARY') )?

IfNotExists ::=
    ('IF' 'NOT' 'EXISTS')?

TableName ::=
    Identifier ('.' Identifier)?

TableElementListOpt ::=
    ( '(' TableElementList ')' )?

TableElementList ::=
    TableElement ( ',' TableElement )*

TableElement ::=
    ColumnDef
|   Constraint

ColumnDef ::=
    ColumnName ( Type | 'SERIAL' ) ColumnOptionListOpt

ColumnOptionListOpt ::=
    ColumnOption*

ColumnOptionList ::=
    ColumnOption*

ColumnOption ::=
    'NOT'? 'NULL'
|   'AUTO_INCREMENT'
|   PrimaryOpt 'KEY'
|   'UNIQUE' 'KEY'?
|   'DEFAULT' DefaultValueExpr
|   'SERIAL' 'DEFAULT' 'VALUE'
|   'ON' 'UPDATE' NowSymOptionFraction
|   'COMMENT' stringLit
|   ConstraintKeywordOpt 'CHECK' '(' Expression ')' EnforcedOrNotOrNotNullOpt
|   GeneratedAlways 'AS' '(' Expression ')' VirtualOrStored
|   ReferDef
|   'COLLATE' CollationName
|   'COLUMN_FORMAT' ColumnFormat
|   'STORAGE' StorageMedia
|   'AUTO_RANDOM' OptFieldLen

CreateTableOptionListOpt ::=
    TableOptionList?

PartitionOpt ::=
    ( 'PARTITION' 'BY' PartitionMethod PartitionNumOpt SubPartitionOpt PartitionDefinitionListOpt )?

DuplicateOpt ::=
    ( 'IGNORE' | 'REPLACE' )?

TableOptionList ::=
    TableOption ( ','? TableOption )*

TableOption ::=
    PartDefOption
|   DefaultKwdOpt ( CharsetKw EqOpt CharsetName | 'COLLATE' EqOpt CollationName )
|   ( 'AUTO_INCREMENT' | 'AUTO_ID_CACHE' | 'AUTO_RANDOM_BASE' | 'AVG_ROW_LENGTH' | 'CHECKSUM' | 'TABLE_CHECKSUM' | 'KEY_BLOCK_SIZE' | 'DELAY_KEY_WRITE' | 'SHARD_ROW_ID_BITS' | 'PRE_SPLIT_REGIONS' ) EqOpt LengthNum
|   ( 'CONNECTION' | 'PASSWORD' | 'COMPRESSION' ) EqOpt stringLit
|   RowFormat
|   ( 'STATS_PERSISTENT' | 'PACK_KEYS' ) EqOpt StatsPersistentVal
|   ( 'STATS_AUTO_RECALC' | 'STATS_SAMPLE_PAGES' ) EqOpt ( LengthNum | 'DEFAULT' )
|   'STORAGE' ( 'MEMORY' | 'DISK' )
|   'SECONDARY_ENGINE' EqOpt ( 'NULL' | StringName )
|   'UNION' EqOpt '(' TableNameListOpt ')'
|   'ENCRYPTION' EqOpt EncryptionOpt
| 'TTL' EqOpt TimeColumnName '+' 'INTERVAL' Expression TimeUnit (TTLEnable EqOpt ( 'ON' | 'OFF' ))?
|   PlacementPolicyOption

OnCommitOpt ::=
    ('ON' 'COMMIT' 'DELETE' 'ROWS')?

PlacementPolicyOption ::=
    "PLACEMENT" "POLICY" EqOpt PolicyName
|   "PLACEMENT" "POLICY" (EqOpt | "SET") "DEFAULT"
```

次の*table_options が*サポートされています。 `AVG_ROW_LENGTH` 、 `CHECKSUM` 、 `COMPRESSION` 、 `CONNECTION` 、 `DELAY_KEY_WRITE` 、 `ENGINE` 、 `KEY_BLOCK_SIZE` 、 `MAX_ROWS` 、 `MIN_ROWS` 、 `ROW_FORMAT` 、 `STATS_PERSISTENT`などのその他のオプションは解析されますが、無視されます。

| オプション                                        | 説明                                                                                 | 例                                   |
| -------------------------------------------- | ---------------------------------------------------------------------------------- | ----------------------------------- |
| `AUTO_INCREMENT`                             | インクリメント フィールドの初期値                                                                  | `AUTO_INCREMENT` = 5                |
| [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) | 暗黙の`_tidb_rowid`シャードのビット数を設定するには                                                   | `SHARD_ROW_ID_BITS` = 4             |
| `PRE_SPLIT_REGIONS`                          | テーブルの作成時に`2^(PRE_SPLIT_REGIONS)`リージョンを事前に分割するには                                    | `PRE_SPLIT_REGIONS` = 4             |
| `AUTO_ID_CACHE`                              | TiDB インスタンスで自動 ID キャッシュ サイズを設定するには。デフォルトでは、TiDB は自動 ID の割り当て速度に応じてこのサイズを自動的に変更します。 | `AUTO_ID_CACHE` = 200               |
| `AUTO_RANDOM_BASE`                           | auto_random の増分部分の初期値を設定します。このオプションは、内部インターフェースの一部と見なすことができます。ユーザーはこのパラメータを無視できます  | `AUTO_RANDOM_BASE` = 0              |
| `CHARACTER SET`                              | テーブルに[キャラクターセット](/character-set-and-collation.md)指定するには                            | `CHARACTER SET` = &#39;utf8mb4&#39; |
| `COMMENT`                                    | コメント情報                                                                             | `COMMENT` = &#39;コメント情報&#39;        |

<CustomContent platform="tidb">

> **ノート：**
>
> `split-table`構成オプションはデフォルトで有効になっています。有効にすると、新しく作成されたテーブルごとに個別のリージョンが作成されます。詳細については、 [TiDB 構成ファイル](/tidb-configuration-file.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> TiDB は、新しく作成されたテーブルごとに個別のリージョンを作成します。

</CustomContent>

## 例 {#examples}

単純なテーブルを作成し、1 行を挿入します。

{{< copyable "" >}}

```sql
CREATE TABLE t1 (a int);
DESC t1;
SHOW CREATE TABLE t1\G
INSERT INTO t1 (a) VALUES (1);
SELECT * FROM t1;
```

```
mysql> drop table if exists t1;
Query OK, 0 rows affected (0.23 sec)

mysql> CREATE TABLE t1 (a int);
Query OK, 0 rows affected (0.09 sec)

mysql> DESC t1;
+-------+---------+------+------+---------+-------+
| Field | Type    | Null | Key  | Default | Extra |
+-------+---------+------+------+---------+-------+
| a     | int(11) | YES  |      | NULL    |       |
+-------+---------+------+------+---------+-------+
1 row in set (0.00 sec)

mysql> SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `a` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)

mysql> INSERT INTO t1 (a) VALUES (1);
Query OK, 1 row affected (0.03 sec)

mysql> SELECT * FROM t1;
+------+
| a    |
+------+
|    1 |
+------+
1 row in set (0.00 sec)
```

存在する場合はテーブルを削除し、存在しない場合は条件付きでテーブルを作成します。

{{< copyable "" >}}

```sql
DROP TABLE IF EXISTS t1;
CREATE TABLE IF NOT EXISTS t1 (
 id BIGINT NOT NULL PRIMARY KEY auto_increment,
 b VARCHAR(200) NOT NULL
);
DESC t1;
```

```sql
mysql> DROP TABLE IF EXISTS t1;
Query OK, 0 rows affected (0.22 sec)

mysql> CREATE TABLE IF NOT EXISTS t1 (
    ->  id BIGINT NOT NULL PRIMARY KEY auto_increment,
    ->  b VARCHAR(200) NOT NULL
    -> );
Query OK, 0 rows affected (0.08 sec)

mysql> DESC t1;
+-------+--------------+------+------+---------+----------------+
| Field | Type         | Null | Key  | Default | Extra          |
+-------+--------------+------+------+---------+----------------+
| id    | bigint(20)   | NO   | PRI  | NULL    | auto_increment |
| b     | varchar(200) | NO   |      | NULL    |                |
+-------+--------------+------+------+---------+----------------+
2 rows in set (0.00 sec)
```

## MySQL の互換性 {#mysql-compatibility}

-   空間型を除くすべてのデータ型がサポートされています。
-   `FULLTEXT` 、 `HASH`および`SPATIAL`インデックスはサポートされていません。

<CustomContent platform="tidb">

-   互換性のために、 `index_col_name`属性は、デフォルトで最大長が 3072 バイトに制限された長さオプションをサポートします。長さ制限は、 `max-index-length`構成オプションで変更できます。詳細については、 [TiDB 構成ファイル](/tidb-configuration-file.md#max-index-length)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   互換性のために、 `index_col_name`属性は、最大長が 3072 バイトに制限された長さオプションをサポートします。

</CustomContent>

-   `index_col_name`分の`[ASC | DESC]`現在解析されていますが、無視されます (MySQL 5.7互換の動作)。
-   `COMMENT`属性は`WITH PARSER`オプションをサポートしません。
-   TiDB は、デフォルトで 1 つのテーブルで 1017 列をサポートし、最大で 4096 列をサポートします。 InnoDB での対応する数の制限は 1017 列であり、MySQL でのハード リミットは 4096 列です。詳細については、 [TiDB の制限事項](/tidb-limitations.md)を参照してください。
-   分割されたテーブルでは、範囲、ハッシュ、および範囲列 (単一列) のみがサポートされます。詳細については、 [パーティションテーブル](/partitioned-table.md)を参照してください。
-   `CHECK`制約は解析されますが無視されます (MySQL 5.7互換の動作)。詳細については、 [制約](/constraints.md)を参照してください。
-   `FOREIGN KEY`制約は解析および保存されますが、DML ステートメントによって適用されません。詳細については、 [制約](/constraints.md)を参照してください。

## こちらもご覧ください {#see-also}

-   [データ型](/data-type-overview.md)
-   [ドロップテーブル](/sql-statements/sql-statement-drop-table.md)
-   [次のようなテーブルを作成](/sql-statements/sql-statement-create-table-like.md)
-   [テーブルの作成を表示](/sql-statements/sql-statement-show-create-table.md)
