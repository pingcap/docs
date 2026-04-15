---
title: ADD INDEX | TiDB SQL Statement Reference
summary: TiDBデータベースにおけるADD INDEXの使用方法の概要。
---

# インデックスを追加 {#add-index}

`ALTER TABLE.. ADD INDEX`ステートメントは、既存のテーブルにインデックスを追加します。この操作は TiDB ではオンラインで実行されるため、インデックスの追加によってテーブルへの読み取りや書き込みがブロックされることはありません。

> **ヒント：**
>
> [TiDB分散実行フレームワーク（DXF）](/tidb-distributed-execution-framework.md)使用すると、このステートメントの操作を高速化できます。

<CustomContent platform="tidb-cloud">

> **注記：**
>
> 4 vCPUを搭載した[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタの場合、インデックス作成中にリソース制限がクラスタの安定性に影響を与えないように、 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)手動で無効にすることをお勧めします。この設定を無効にすることで、トランザクションを使用してインデックスを作成できるようになり、クラスタ全体への影響を軽減できます。

</CustomContent>

<CustomContent platform="tidb">

> **警告：**
>
> -   TiDB クラスターで DDL ステートメントが実行されている間は、TiDB クラスターをアップグレード**しないでください**(通常、 `ADD INDEX`や列型の変更など、時間のかかる DDL ステートメントの場合)。
> -   アップグレードを行う前に、 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md)コマンドを使用して、TiDB クラスタで実行中の DDL ジョブがあるかどうかを確認することをお勧めします。クラスタで DDL ジョブが実行されている場合は、クラスタをアップグレードする前に、DDL ジョブの実行が完了するまで待つか、 [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)コマンドを使用して DDL ジョブをキャンセルしてください。
> -   さらに、クラスタのアップグレード中は、DDLステートメントを一切実行**しないでください**。実行すると、未定義の動作が発生する可能性があります。
>
> TiDB を v7.1.0 から以降のバージョンにアップグレードする場合は、前述の制限を無視できます。詳細については、 [TiDBのスムーズアップグレードの制限事項](/smooth-upgrade-tidb.md)を参照してください。

</CustomContent>

## あらすじ {#synopsis}

```ebnf+diagram
AlterTableStmt
         ::= 'ALTER' 'IGNORE'? 'TABLE' TableName AddIndexSpec ( ',' AddIndexSpec )*

AddIndexSpec
         ::= 'ADD' ( ( 'PRIMARY' 'KEY' | ( 'KEY' | 'INDEX' ) 'IF NOT EXISTS'? | 'UNIQUE' ( 'KEY' | 'INDEX' )? ) ( ( Identifier? 'USING' | Identifier 'TYPE' ) IndexType )? | 'FULLTEXT' ( 'KEY' | 'INDEX' )? IndexName ) '(' IndexPartSpecification ( ',' IndexPartSpecification )* ')' IndexOption*

IndexPartSpecification
         ::= ( ColumnName ( '(' LengthNum ')' )? | '(' Expression ')' ) ( 'ASC' | 'DESC' )

IndexOption
         ::= 'KEY_BLOCK_SIZE' '='? LengthNum
           | 'USING' IndexType
           | 'WITH' 'PARSER' Identifier
           | 'COMMENT' stringLit
           | 'VISIBLE'
           | 'INVISIBLE'
           | 'GLOBAL'
           | 'LOCAL'

IndexType
         ::= 'BTREE'
           | 'HASH'
           | 'RTREE'
```

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_7           | 10.00    | root      |               | data:Selection_6               |
| └─Selection_6           | 10.00    | cop[tikv] |               | eq(test.t1.c1, 3)              |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)

mysql> ALTER TABLE t1 ADD INDEX (c1);
Query OK, 0 rows affected (0.30 sec)

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| id                     | estRows | task      | access object          | operator info                               |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| IndexReader_6          | 0.01    | root      |                        | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 0.01    | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
2 rows in set (0.00 sec)
```

## MySQLとの互換性 {#mysql-compatibility}

-   TiDB は、MySQL との互換性のために、 `HASH` 、 `BTREE` 、 `RTREE`などのインデックス タイプを構文で受け入れますが、それらを無視します。

-   `SPATIAL`インデックスはサポートされていません。

-   TiDB Self-Managed およびTiDB Cloud Dedicated は`FULLTEXT`構文の解析をサポートしていますが、 `FULLTEXT`インデックスの使用はサポートしていません。

    > **注記：**
    >
    > 現在、特定の AWS リージョンのTiDB Cloud StarterとTiDB Cloud Essentialインスタンスのみが[`FULLTEXT`構文と索引](https://docs.pingcap.com/tidbcloud/vector-search-full-text-search-sql)をサポートしています。

-   降順インデックスはサポートされていません（ MySQL 5.7と同様）。

-   `CLUSTERED`タイプの主キーをテーブルに追加することはサポートされていません。 `CLUSTERED`タイプの主キーの詳細については、[クラスター化インデックス](/clustered-indexes.md)を参照してください。

-   `PRIMARY KEY`インデックス オプションを使用して、 `UNIQUE INDEX`または`GLOBAL`グローバル インデックスとして[グローバルインデックス](/global-indexes.md)ことは、パーティション化[パーティション化されたテーブル](/partitioned-table.md)の TiDB 拡張機能であり、MySQL とは互換性がありません。

## 関連項目 {#see-also}

-   [インデックス選択](/choose-index.md)
-   [インデックス問題の解決方法](/wrong-index-solution.md)
-   [インデックスを作成する](/sql-statements/sql-statement-create-index.md)
-   [インデックスを削除](/sql-statements/sql-statement-drop-index.md)
-   [インデックス名の変更](/sql-statements/sql-statement-rename-index.md)
-   [インデックスの変更](/sql-statements/sql-statement-alter-index.md)
-   [列を追加](/sql-statements/sql-statement-add-column.md)
-   [テーブルを作成する](/sql-statements/sql-statement-create-table.md)
-   [EXPLAIN](/sql-statements/sql-statement-explain.md)
-   [TiDB分散実行フレームワーク（DXF）](/tidb-distributed-execution-framework.md)
