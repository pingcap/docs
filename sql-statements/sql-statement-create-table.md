---
title: CREATE TABLE | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE TABLE for the TiDB database.
---

# テーブルの作成 {#create-table}

このステートメントは、現在選択されているデータベースに新しいテーブルを作成します。 MySQLの`CREATE TABLE`ステートメントと同様に動作します。

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

OnCommitOpt ::=
    ('ON' 'COMMIT' 'DELETE' 'ROWS')?
```

次の*table_options*がサポートされています。 `AVG_ROW_LENGTH` `ENGINE` `MIN_ROWS` `CONNECTION`の`DELAY_KEY_WRITE`は`MAX_ROWS` `ROW_FORMAT` `STATS_PERSISTENT` `CHECKSUM`が、 `KEY_BLOCK_SIZE`され`COMPRESSION` 。

| オプション                                        | 説明                                                                                | 例                                  |
| -------------------------------------------- | --------------------------------------------------------------------------------- | ---------------------------------- |
| `AUTO_INCREMENT`                             | 増分フィールドの初期値                                                                       | `AUTO_INCREMENT` = 5               |
| [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) | 暗黙の`_tidb_rowid`シャードのビット数を設定するには                                                  | `SHARD_ROW_ID_BITS` = 4            |
| `PRE_SPLIT_REGIONS`                          | テーブルを作成するときに`2^(PRE_SPLIT_REGIONS)`のリージョンを事前に分割するには                               | `PRE_SPLIT_REGIONS` = 4            |
| `AUTO_ID_CACHE`                              | TiDBインスタンスで自動IDキャッシュサイズを設定します。デフォルトでは、TiDBは自動IDの割り当て速度に応じてこのサイズを自動的に変更します         | `AUTO_ID_CACHE` = 200              |
| `AUTO_RANDOM_BASE`                           | auto_randomの初期増分パーツ値を設定します。このオプションは、内部インターフェースの一部と見なすことができます。ユーザーはこのパラメーターを無視できます | `AUTO_RANDOM_BASE` = 0             |
| `CHARACTER SET`                              | テーブルに[キャラクターセット](/character-set-and-collation.md)を指定するには                          | `CHARACTER SET` =&#39;utf8mb4&#39; |
| `COMMENT`                                    | コメント情報                                                                            | `COMMENT` =&#39;コメント情報&#39;        |

<CustomContent platform="tidb">

> **ノート：**
>
> `split-table`構成オプションはデフォルトで有効になっています。有効にすると、新しく作成されたテーブルごとに個別のリージョンが作成されます。詳細については、 [TiDB構成ファイル](/tidb-configuration-file.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> TiDBは、新しく作成されたテーブルごとに個別のリージョンを作成します。

</CustomContent>

## 例 {#examples}

単純なテーブルを作成し、1つの行を挿入します。

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

テーブルが存在する場合はドロップし、存在しない場合は条件付きでテーブルを作成します。

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

## MySQLの互換性 {#mysql-compatibility}

-   空間タイプを除くすべてのデータタイプがサポートされています。
-   `FULLTEXT` 、および`HASH`のインデックスはサポートさ`SPATIAL`ていません。

<CustomContent platform="tidb">

-   互換性のために、 `index_col_name`属性は、デフォルトで最大長制限が3072バイトの長さオプションをサポートします。長さの制限は、 `max-index-length`の構成オプションを使用して変更できます。詳細については、 [TiDB構成ファイル](/tidb-configuration-file.md#max-index-length)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   互換性のために、 `index_col_name`属性は、最大長制限が3072バイトの長さオプションをサポートします。

</CustomContent>

-   `index_col_name`の`[ASC | DESC]`は現在解析されていますが、無視されます（MySQL 5.7互換の動作）。
-   `COMMENT`属性は`WITH PARSER`オプションをサポートしていません。
-   TiDBは、1つのテーブルで最大512列をサポートします。 InnoDBの対応する数の制限は1017であり、MySQLのハード制限は4096です。詳細については、 [TiDBの制限](/tidb-limitations.md)を参照してください。
-   パーティションテーブルの場合、範囲、ハッシュ、および範囲列（単一列）のみがサポートされます。詳細については、 [パーティションテーブル](/partitioned-table.md)を参照してください。
-   `CHECK`の制約は解析されますが、無視されます（MySQL 5.7互換の動作）。詳細については、 [制約](/constraints.md)を参照してください。
-   `FOREIGN KEY`制約は解析および保存されますが、DMLステートメントによって強制されることはありません。詳細については、 [制約](/constraints.md)を参照してください。

## も参照してください {#see-also}

-   [データ型](/data-type-overview.md)
-   [ドロップテーブル](/sql-statements/sql-statement-drop-table.md)
-   [テーブルのようなものを作成](/sql-statements/sql-statement-create-table-like.md)
-   [作成テーブルを表示](/sql-statements/sql-statement-show-create-table.md)
