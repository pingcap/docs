---
title: ADD INDEX | TiDB SQL Statement Reference
summary: TiDBデータベースにおけるADD INDEXの使用方法の概要。
---

# ADD INDEX {#add-index}

`ALTER TABLE.. ADD INDEX`文は、既存のテーブルにインデックスを追加します。この操作は TiDB ではオンラインで実行されるため、インデックスの追加によってテーブルへの読み取りや書き込みがブロックされることはありません。

> **Tip:**
>
> [TiDB分散実行フレームワーク（DXF）](/tidb-distributed-execution-framework.md)を使用すると、このステートメントの操作を高速化できます。

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 4 vCPUを搭載した[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタの場合、インデックス作成中にリソース制限がクラスタの安定性に影響を与えないように、 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)を手動で無効にすることをお勧めします。この設定を無効にすることで、トランザクションを使用してインデックスを作成できるようになり、クラスタ全体への影響を軽減できます。

</CustomContent>

<CustomContent platform="tidb">

> **Warning:**
>
> - TiDB クラスターで DDL文が実行されている間は、TiDB クラスターをアップグレード**しないでください**(通常、 `ADD INDEX`や列型の変更など、時間のかかる DDL文の場合)。
> - アップグレードを行う前に、 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md)コマンドを使用して、TiDB クラスタで実行中の DDL ジョブがあるかどうかを確認することをお勧めします。クラスタで DDL ジョブが実行されている場合は、クラスタをアップグレードする前に、DDL ジョブの実行が完了するまで待つか、 [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)コマンドを使用して DDL ジョブをキャンセルしてください。
> - さらに、クラスタのアップグレード中は、DDL文を一切実行**しないでください**。実行すると、未定義の動作が発生する可能性があります。
>
> TiDB を v7.1.0 から以降のバージョンにアップグレードする場合は、前述の制限を無視できます。詳細については、 [TiDBのスムーズアップグレードの制限事項](/smooth-upgrade-tidb.md)を参照してください。

</CustomContent>

## 概要 {#synopsis}

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
           | 'WHERE' Expression

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

## 部分インデックス {#partial-indexes}

> **Note:**
>
> 部分インデックスは、TiDB Self-Managed および TiDB Cloud Dedicated では v8.5.7 以降、TiDB Cloud Essential および Premium では CLOUD.202603.1 以降でサポートされます。

部分インデックスは、テーブル内の行のサブセットに対して構築されるインデックスです。部分インデックスを追加する際には、条件式（述語とも呼ばれます）を指定して、その行のサブセットを定義できます。インデックスには、その述語を満たす行に対するエントリのみが含まれます。

### 使用シナリオ {#usage-scenarios}

次のシナリオでは、部分インデックスを使用することで、クエリ性能の向上やインデックス管理オーバーヘッドの削減に役立ちます。

- **選択的フィルタリング**: 特定の条件に基づいて少数の行のサブセットを頻繁にクエリする場合、部分インデックスを使用できます。部分インデックスの述語を満たすクエリでは、TiDB は部分インデックスを使用して無関係な行のスキャンを回避し、インデックスが占有するストレージ容量を削減できます。
- **条件付き一意性**: 特定の条件を満たす行に対してのみ一意性制約を適用する必要がある場合、ユニーク部分インデックスを使用して、テーブル全体に一意性制約を適用することを避けられます。
- **DML オーバーヘッドの削減**: 多数の `INSERT`、`UPDATE`、または `DELETE` 操作が、インデックス化する必要のない行に影響する場合、部分インデックスを使用できます。完全なインデックスを管理する場合と比べて、部分インデックスを管理することでインデックス管理オーバーヘッドを削減できます。

### 部分インデックスの追加 {#add-partial-indexes}

インデックス定義に `WHERE` 句を追加することで、部分インデックスを追加できます。例:

```sql
CREATE TABLE t1 (c1 INT, c2 INT, c3 TEXT);
ALTER TABLE t1 ADD INDEX idx1 (c1) WHERE c2 > 10;
```

ユニーク部分インデックスを追加することもできます。

```sql
ALTER TABLE t1 ADD UNIQUE INDEX idx2 (c1, c2) WHERE c3 = 'abc';
```

### 使用例 {#usage-examples}

以下の例は、部分インデックスを効果的に使用する方法を示しています。

ユーザーデータを含むテーブルを作成します。

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    status VARCHAR(20),
    created_at DATETIME,
    score INT
);
```

一般的なクエリパターンに対して部分インデックスを追加します。

```sql
ALTER TABLE users ADD INDEX idx_active_users (name) WHERE status = 'active';
ALTER TABLE users ADD INDEX idx_high_score_users (created_at) WHERE score > 1000;
ALTER TABLE users ADD INDEX idx_pending_status (status) WHERE status = 'pending';
```

その後、次のクエリで部分インデックスを使用できます。

```sql
mysql> EXPLAIN SELECT * FROM users WHERE status = 'active' AND name = 'John';
+-------------------------------+---------+-----------+-------------------------------------------+-------------------------------------------------------+
| id                            | estRows | task      | access object                             | operator info                                         |
+-------------------------------+---------+-----------+-------------------------------------------+-------------------------------------------------------+
| IndexLookUp_9                 | 1.00    | root      |                                           |                                                       |
| ├─IndexRangeScan_6(Build)     | 10.00   | cop[tikv] | table:users, index:idx_active_users(name) | range:["John","John"], keep order:false, stats:pseudo |
| └─Selection_8(Probe)          | 1.00    | cop[tikv] |                                           | eq(test.users.status, "active")                       |
|   └─TableRowIDScan_7          | 10.00   | cop[tikv] | table:users                               | keep order:false, stats:pseudo                        |
+-------------------------------+---------+-----------+-------------------------------------------+-------------------------------------------------------+
4 rows in set (0.00 sec)

mysql> EXPLAIN SELECT * FROM users WHERE status = 'active' ORDER BY name;
+-------------------------------+----------+-----------+-------------------------------------------+---------------------------------+
| id                            | estRows  | task      | access object                             | operator info                   |
+-------------------------------+----------+-----------+-------------------------------------------+---------------------------------+
| IndexLookUp_18                | 10.00    | root      |                                           |                                 |
| ├─IndexFullScan_15(Build)     | 10000.00 | cop[tikv] | table:users, index:idx_active_users(name) | keep order:true, stats:pseudo   |
| └─Selection_17(Probe)         | 10.00    | cop[tikv] |                                           | eq(test.users.status, "active") |
|   └─TableRowIDScan_16         | 10000.00 | cop[tikv] | table:users                               | keep order:false, stats:pseudo  |
+-------------------------------+----------+-----------+-------------------------------------------+---------------------------------+
4 rows in set (0.00 sec)

mysql> EXPLAIN SELECT * FROM users WHERE score > 10000 ORDER BY created_at;
+-------------------------------+----------+-----------+-----------------------------------------------------+--------------------------------+
| id                            | estRows  | task      | access object                                       | operator info                  |
+-------------------------------+----------+-----------+-----------------------------------------------------+--------------------------------+
| IndexLookUp_18                | 3333.33  | root      |                                                     |                                |
| ├─IndexFullScan_15(Build)     | 10000.00 | cop[tikv] | table:users, index:idx_high_score_users(created_at) | keep order:true, stats:pseudo  |
| └─Selection_17(Probe)         | 3333.33  | cop[tikv] |                                                     | gt(test.users.score, 10000)     |
|   └─TableRowIDScan_16         | 10000.00 | cop[tikv] | table:users                                         | keep order:false, stats:pseudo |
+-------------------------------+----------+-----------+-----------------------------------------------------+--------------------------------+
4 rows in set (0.00 sec)

mysql> EXPLAIN SELECT * FROM users WHERE status = 'pending';
+-------------------------------+---------+-----------+-----------------------------------------------+-------------------------------------------------------------+
| id                            | estRows | task      | access object                                 | operator info                                               |
+-------------------------------+---------+-----------+-----------------------------------------------+-------------------------------------------------------------+
| IndexLookUp_7                 | 10.00   | root      |                                               |                                                             |
| ├─IndexRangeScan_5(Build)     | 10.00   | cop[tikv] | table:users, index:idx_pending_status(status) | range:["pending","pending"], keep order:false, stats:pseudo |
| └─TableRowIDScan_6(Probe)     | 10.00   | cop[tikv] | table:users                                   | keep order:false, stats:pseudo                              |
+-------------------------------+---------+-----------+-----------------------------------------------+-------------------------------------------------------------+
3 rows in set (0.00 sec)
```

クエリの述語が部分インデックスで定義された条件を満たさない場合、TiDB はヒントを指定していても部分インデックスを選択しません。たとえば、次のステートメントでは部分インデックス `idx_high_score_users` を使用できません。これは、クエリ述語 `score > 100` が部分インデックス定義 `score > 1000` を満たさないためです。

```sql
mysql> EXPLAIN SELECT * FROM users USE INDEX(idx_high_score_users) WHERE score > 100 ORDER BY created_at;
+---------------------------+----------+-----------+---------------+--------------------------------+
| id                        | estRows  | task      | access object | operator info                  |
+---------------------------+----------+-----------+---------------+--------------------------------+
| Sort_5                    | 3333.33  | root      |               | test.users.created_at          |
| └─TableReader_10          | 3333.33  | root      |               | data:Selection_9               |
|   └─Selection_9           | 3333.33  | cop[tikv] |               | gt(test.users.score, 100)      |
|     └─TableFullScan_8     | 10000.00 | cop[tikv] | table:users   | keep order:false, stats:pseudo |
+---------------------------+----------+-----------+---------------+--------------------------------+
```

### 制限事項 {#limitations}

- 部分インデックスの `WHERE` 句では、基本的な比較演算子（`=`、`!=`、`<`、`<=`、`>`、`>=`）、`IS NULL`、`IS NOT NULL`、および定数値を使用した `IN` 述語をサポートします。
- 述語内のカラムと定数値は、同じデータ型である必要があります。
- 述語は同じテーブルのカラムのみを参照できます。
- 式インデックスに部分インデックスを作成することはできません。

## MySQLとの互換性 {#mysql-compatibility}

- TiDB は、MySQL との互換性のために、 `HASH` 、 `BTREE` 、 `RTREE`などのインデックス タイプを構文で受け入れますが、それらを無視します。

- `SPATIAL`インデックスはサポートされていません。

- TiDB Self-Managed およびTiDB Cloud Dedicated は`FULLTEXT`構文の解析をサポートしていますが、 `FULLTEXT`インデックスの使用はサポートしていません。

    > **Note:**
    >
    > 現在、特定の AWS リージョンのTiDB Cloud Starterインスタンスのみが[`FULLTEXT`構文と索引](https://docs.pingcap.com/tidbcloud/vector-search-full-text-search-sql)をサポートしています。

- 降順インデックスはサポートされていません（ MySQL 5.7と同様）。

- `CLUSTERED`タイプの主キーをテーブルに追加することはサポートされていません。 `CLUSTERED`タイプの主キーの詳細については、[クラスター化インデックス](/clustered-indexes.md)を参照してください。

- `GLOBAL`インデックスオプションを使用して`PRIMARY KEY`または`UNIQUE INDEX`を[グローバルインデックス](/global-indexes.md)として設定することは、[パーティション化されたテーブル](/partitioned-table.md)に対するTiDBの拡張機能であり、MySQLとは互換性がありません。

## 参照 {#see-also}

- [インデックス選択](/choose-index.md)
- [インデックス問題の解決方法](/wrong-index-solution.md)
- [CREATE INDEX](/sql-statements/sql-statement-create-index.md)
- [DROP INDEX](/sql-statements/sql-statement-drop-index.md)
- [RENAME INDEX](/sql-statements/sql-statement-rename-index.md)
- [ALTER INDEX](/sql-statements/sql-statement-alter-index.md)
- [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
- [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
- [EXPLAIN](/sql-statements/sql-statement-explain.md)
- [TiDB分散実行フレームワーク（DXF）](/tidb-distributed-execution-framework.md)
