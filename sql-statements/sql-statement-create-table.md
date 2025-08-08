---
title: CREATE TABLE | TiDB SQL Statement Reference
summary: TiDB データベースの CREATE TABLE の使用法の概要。
---

# テーブルの作成 {#create-table}

この文は、現在選択されているデータベースに新しいテーブルを作成します。MySQLの`CREATE TABLE`文と同様に動作します。

## 概要 {#synopsis}

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
|   PrimaryOpt 'KEY' ( 'GLOBAL' | 'LOCAL' )?
|   'UNIQUE' 'KEY'? ( 'GLOBAL' | 'LOCAL' )?
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

Constraint ::=
    IndexDef
|   ForeignKeyDef

IndexDef ::=
    ( 'INDEX' | 'KEY' ) IndexName? '(' KeyPartList ')' IndexOption?

KeyPartList ::=
    KeyPart ( ',' KeyPart )*

KeyPart ::=
    ColumnName ( '(' Length ')')? ( 'ASC' | 'DESC' )?
|   '(' Expression ')' ( 'ASC' | 'DESC' )?

IndexOption ::=
    'COMMENT' String
|   ( 'VISIBLE' | 'INVISIBLE' )
|   ('USING' | 'TYPE') ('BTREE' | 'RTREE' | 'HASH')
|   ( 'GLOBAL' | 'LOCAL' )

ForeignKeyDef
         ::= ( 'CONSTRAINT' Identifier )? 'FOREIGN' 'KEY'
             Identifier? '(' ColumnName ( ',' ColumnName )* ')'
             'REFERENCES' TableName '(' ColumnName ( ',' ColumnName )* ')'
             ( 'ON' 'DELETE' ReferenceOption )?
             ( 'ON' 'UPDATE' ReferenceOption )?

ReferenceOption
         ::= 'RESTRICT'
           | 'CASCADE'
           | 'SET' 'NULL'
           | 'SET' 'DEFAULT'
           | 'NO' 'ACTION'

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
|    'TTL' EqOpt TimeColumnName '+' 'INTERVAL' Expression TimeUnit (TTLEnable EqOpt ( 'ON' | 'OFF' ))? (TTLJobInterval EqOpt stringLit)?
|   PlacementPolicyOption

OnCommitOpt ::=
    ('ON' 'COMMIT' 'DELETE' 'ROWS')?

PlacementPolicyOption ::=
    "PLACEMENT" "POLICY" EqOpt PolicyName
|   "PLACEMENT" "POLICY" (EqOpt | "SET") "DEFAULT"

DefaultValueExpr ::=
    NowSymOptionFractionParentheses
|   SignedLiteral
|   NextValueForSequenceParentheses
|   BuiltinFunction

BuiltinFunction ::=
    '(' BuiltinFunction ')'
|   identifier '(' ')'
|   identifier '(' ExpressionList ')'
|   "REPLACE" '(' ExpressionList ')'

NowSymOptionFractionParentheses ::=
    '(' NowSymOptionFractionParentheses ')'
|   NowSymOptionFraction

NowSymOptionFraction ::=
    NowSym
|   NowSymFunc '(' ')'
|   NowSymFunc '(' NUM ')'
|   CurdateSym '(' ')'
|   "CURRENT_DATE"

NextValueForSequenceParentheses ::=
    '(' NextValueForSequenceParentheses ')'
|   NextValueForSequence

NextValueForSequence ::=
    "NEXT" "VALUE" forKwd TableName
|   "NEXTVAL" '(' TableName ')'
```

`ROW_FORMAT`の*table_options*がサポートさ`MAX_ROWS` `KEY_BLOCK_SIZE` `ENGINE` `DELAY_KEY_WRITE` 。その他の`CONNECTION` （ `AVG_ROW_LENGTH`など`CHECKSUM` `COMPRESSION`解析されますが無視`STATS_PERSISTENT`れます`MIN_ROWS`

| オプション                                        | 説明                                                                            | 例                                   |
| -------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------- |
| `AUTO_INCREMENT`                             | 増分フィールドの初期値                                                                   | `AUTO_INCREMENT` = 5                |
| [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) | 暗黙の`_tidb_rowid`シャードのビット数を設定するには                                              | `SHARD_ROW_ID_BITS` = 4             |
| `PRE_SPLIT_REGIONS`                          | テーブルを作成するときに`2^(PRE_SPLIT_REGIONS)`リージョンを事前に分割するには                            | `PRE_SPLIT_REGIONS` = 4             |
| `AUTO_ID_CACHE`                              | TiDBインスタンスの自動IDキャッシュサイズを設定します。デフォルトでは、TiDBは自動IDの割り当て速度に応じてこのサイズを自動的に変更します。    | `AUTO_ID_CACHE` = 200               |
| `AUTO_RANDOM_BASE`                           | auto_randomの初期増分値を設定します。このオプションは内部インターフェースの一部とみなすことができます。ユーザーはこのパラメータを無視できます。 | `AUTO_RANDOM_BASE` = 0              |
| `CHARACTER SET`                              | テーブルの[文字セット](/character-set-and-collation.md)指定するには                           | `CHARACTER SET` = &#39;utf8mb4&#39; |
| `COMMENT`                                    | コメント情報                                                                        | `COMMENT` = &#39;コメント情報&#39;        |

<CustomContent platform="tidb">

> **注記：**
>
> `split-table`設定オプションはデフォルトで有効になっています。有効にすると、新しく作成されたテーブルごとに個別のリージョンが作成されます。詳細については、 [TiDB構成ファイル](/tidb-configuration-file.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> TiDB は、新しく作成されたテーブルごとに個別のリージョンを作成します。

</CustomContent>

## 例 {#examples}

簡単なテーブルを作成し、 1 行を挿入します。

```sql
CREATE TABLE t1 (a int);
DESC t1;
SHOW CREATE TABLE t1\G
INSERT INTO t1 (a) VALUES (1);
SELECT * FROM t1;
```

    mysql> drop table if exists t1;
    Query OK, 0 rows affected (0.23 sec)

    mysql> CREATE TABLE t1 (a int);
    Query OK, 0 rows affected (0.09 sec)

    mysql> DESC t1;
    +-------+------+------+------+---------+-------+
    | Field | Type | Null | Key  | Default | Extra |
    +-------+------+------+------+---------+-------+
    | a     | int  | YES  |      | NULL    |       |
    +-------+------+------+------+---------+-------+
    1 row in set (0.00 sec)

    mysql> SHOW CREATE TABLE t1\G
    *************************** 1. row ***************************
           Table: t1
    Create Table: CREATE TABLE `t1` (
      `a` int DEFAULT NULL
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

テーブルが存在する場合は削除し、存在しない場合は条件付きでテーブルを作成します。

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
         id BIGINT NOT NULL PRIMARY KEY auto_increment,
         b VARCHAR(200) NOT NULL
        );
Query OK, 0 rows affected (0.08 sec)

mysql> DESC t1;
+-------+--------------+------+------+---------+----------------+
| Field | Type         | Null | Key  | Default | Extra          |
+-------+--------------+------+------+---------+----------------+
| id    | bigint       | NO   | PRI  | NULL    | auto_increment |
| b     | varchar(200) | NO   |      | NULL    |                |
+-------+--------------+------+------+---------+----------------+
2 rows in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

-   空間型を除くすべてのデータ型がサポートされています。
-   TiDB `RTREE` `BTREE` `HASH`インデックス タイプを受け入れますが、それらを無視します。
-   TiDB は`FULLTEXT`構文の解析をサポートしますが、 `FULLTEXT`インデックスの使用はサポートしません。
-   `GLOBAL`インデックス オプションを使用して`PRIMARY KEY`または`UNIQUE INDEX` [グローバルインデックス](/partitioned-table.md#global-indexes)として設定することは、 [パーティションテーブル](/partitioned-table.md)の TiDB 拡張であり、MySQL と互換性がありません。

<CustomContent platform="tidb">

-   互換性のため、 `index_col_name`属性は長さオプションをサポートしており、デフォルトで最大3072バイトの長さ制限があります。長さ制限は`max-index-length`設定オプションで変更できます。詳細については[TiDB構成ファイル](/tidb-configuration-file.md#max-index-length)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   互換性のために、 `index_col_name`属性は、最大長が 3072 バイトに制限された長さオプションをサポートします。

</CustomContent>

-   `index_col_name`のうち`[ASC | DESC]`は現在解析されていますが無視されます (MySQL 5.7互換の動作)。
-   `COMMENT`属性は`WITH PARSER`オプションをサポートしていません。
-   TiDBは、デフォルトで1つのテーブルあたり1017列、最大4096列をサポートします。InnoDBにおける対応する列数制限は1017列、MySQLにおけるハードリミットは4096列です。詳細については、 [TiDB の制限](/tidb-limitations.md)参照してください。
-   TiDBは`HASH` 、 `RANGE` 、 `LIST` 、および`KEY` [パーティションタイプ](/partitioned-table.md#partitioning-types)をサポートします。サポートされていないパーティションタイプの場合、TiDBは`Warning: Unsupported partition type %s, treat as normal table`返します。ここで、 `%s`サポートされていない特定のパーティションタイプです。

## 参照 {#see-also}

-   [データ型](/data-type-overview.md)
-   [テーブルを削除](/sql-statements/sql-statement-drop-table.md)
-   [次のようなテーブルを作成する](/sql-statements/sql-statement-create-table-like.md)
-   [表示テーブルの作成](/sql-statements/sql-statement-show-create-table.md)
