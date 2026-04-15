---
title: CREATE TABLE | TiDB SQL Statement Reference
summary: TiDBデータベースにおけるCREATE TABLEの使用方法の概要。
---

# テーブルを作成する {#create-table}

このステートメントは、現在選択されているデータベースに新しいテーブルを作成します。MySQL の`CREATE TABLE`ステートメントと同様の動作をします。

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
|   'AFFINITY' EqOpt StringName
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

以下の*テーブルオプション*がサポートされています。 `AVG_ROW_LENGTH` 、 `CHECKSUM` 、 `COMPRESSION` 、 `CONNECTION` 、 `DELAY_KEY_WRITE` 、 {{B `ENGINE` 、 `KEY_BLOCK_SIZE` 、 `MAX_ROWS` 、 `MIN_ROWS`および`STATS_PERSISTENT` `ROW_FORMAT`のその他のオプションは解析されますが無視されます。

| オプション                                        | 説明                                                                                                                                                                          | 例                                   |
| -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| `AUTO_INCREMENT`                             | 増分フィールドの初期値                                                                                                                                                                 | `AUTO_INCREMENT` = 5                |
| [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) | 暗黙の`_tidb_rowid`シャードのビット数を設定するには                                                                                                                                            | `SHARD_ROW_ID_BITS` = 4             |
| `PRE_SPLIT_REGIONS`                          | テーブル作成時に`2^(PRE_SPLIT_REGIONS)`領域を事前に分割するには                                                                                                                                 | `PRE_SPLIT_REGIONS` = 4             |
| `AUTO_ID_CACHE`                              | TiDBインスタンスで自動IDキャッシュサイズを設定します。デフォルトでは、TiDBは自動IDの割り当て速度に応じてこのサイズを自動的に変更します。                                                                                                  | `AUTO_ID_CACHE` = 200               |
| `AUTO_RANDOM_BASE`                           | auto_randomの初期増分値を設定します。このオプションは内部インターフェースの一部とみなすことができます。ユーザーはこのパラメータを無視できます。                                                                                               | `AUTO_RANDOM_BASE` = 0              |
| `CHARACTER SET`                              | テーブルの[文字セット](/character-set-and-collation.md)を指定するには                                                                                                                        | `CHARACTER SET` = &#39;utf8mb4&#39; |
| `COLLATE`                                    | テーブルの文字セット照合順序を指定するには                                                                                                                                                       | `COLLATE` = &#39;utf8mb4_bin&#39;   |
| `COMMENT`                                    | コメント情報                                                                                                                                                                      | `COMMENT` = &#39;コメント情報&#39;        |
| `AFFINITY`                                   | テーブルまたはパーティションのアフィニティスケジューリングを有効にするには、この設定を使用します。パーティション化されていないテーブルの場合は`'table'`に、パーティション化されたテーブルの場合は`'partition'`に設定できます。 `'none'`に設定するか、空欄のままにすると、アフィニティスケジューリングが無効になります。 | `AFFINITY` = &#39;テーブル&#39;         |

<CustomContent platform="tidb">

> **注記：**
>
> -   `split-table`設定オプションはデフォルトで有効になっています。このオプションを有効にすると、新しく作成されるテーブルごとに個別のリージョンが作成されます。詳細は、 [TiDB設定ファイル](/tidb-configuration-file.md)参照してください。
> -   `AFFINITY`を使用する前に、アフィニティが有効になっているテーブルのパーティショニング スキームの変更 (パーティションの追加、削除、再編成、または交換など) はサポートされておらず、一時テーブルまたはビューで`AFFINITY`を構成することもサポートされていないことに注意してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> -   TiDBは、新しく作成されたテーブルごとに個別のリージョンを作成します。
> -   `AFFINITY`を使用する前に、アフィニティが有効になっているテーブルのパーティショニング スキームの変更 (パーティションの追加、削除、再編成、または交換など) はサポートされておらず、一時テーブルまたはビューで`AFFINITY`を構成することもサポートされていないことに注意してください。

</CustomContent>

## 例 {#examples}

シンプルな表を作成し、1行を挿入する：

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

テーブルが存在する場合は削除し、存在しない場合は条件付きでテーブルを作成する。

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

## MySQLとの互換性 {#mysql-compatibility}

-   空間型を除くすべてのデータ型がサポートされています。

-   TiDB は、MySQL との互換性のために、 `HASH` 、 `BTREE` 、 `RTREE`などのインデックス タイプを構文で受け入れますが、それらを無視します。

-   TiDB Self-Managed およびTiDB Cloud Dedicatedは`FULLTEXT`構文の解析をサポートしていますが、 `FULLTEXT`インデックスの使用はサポートしていません。

    > **注記：**
    >
    > 現在、特定の AWS リージョンのTiDB Cloud StarterとTiDB Cloud Essentialインスタンスのみが[`FULLTEXT`構文と索引](https://docs.pingcap.com/tidbcloud/vector-search-full-text-search-sql)をサポートしています。

-   `PRIMARY KEY`インデックス オプションを使用して、 `UNIQUE INDEX`または`GLOBAL`グローバル インデックスとして[グローバルインデックス](/global-indexes.md)ことは、パーティション化[パーティション化されたテーブル](/partitioned-table.md)の TiDB 拡張機能であり、MySQL とは互換性がありません。

<CustomContent platform="tidb">

-   互換性のために、 `index_col_name`属性は、デフォルトで最大長3072バイトの長さオプションをサポートしています。長さの制限は`max-index-length`設定オプションで変更できます。詳細は、 [TiDB設定ファイル](/tidb-configuration-file.md#max-index-length)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   互換性のために、 `index_col_name`属性は、最大長制限3072バイトの長さオプションをサポートしています。

</CustomContent>

-   `[ASC | DESC]`内の`index_col_name`は現在解析されますが無視されます (MySQL 5.7互換の動作)。
-   `COMMENT`属性は`WITH PARSER`オプションをサポートしていません。
-   TiDBは、デフォルトでは1つのテーブルで1017列、最大4096列をサポートします。InnoDBにおける対応する列数の制限は1017列、MySQLにおけるハードリミットは4096列です。詳細は[TiDBの制限事項](/tidb-limitations.md)を参照してください。
-   TiDB は`HASH` 、 `RANGE` 、 `LIST` 、および`KEY`サポートしています[パーティショニングの種類](/partitioned-table.md#partitioning-types)されていないパーティション タイプの場合、TiDB は`Warning: Unsupported partition type %s, treat as normal table`を返します。ここで、 `%s`はサポートされていない特定のパーティション タイプです。

## 関連項目 {#see-also}

-   [データ型](/data-type-overview.md)
-   [テーブルを削除する](/sql-statements/sql-statement-drop-table.md)
-   [テーブルを作成する](/sql-statements/sql-statement-create-table-like.md)
-   [テーブルの作成を表示する](/sql-statements/sql-statement-show-create-table.md)
