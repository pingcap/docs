---
title: "`ANALYZE` Embedded in DDL Statements"
summary: このドキュメントでは、新しく作成または再編成されたインデックスの DDL ステートメントに埋め込まれた ANALYZE` 機能について説明します。この機能により、新しいインデックスの統計がすぐに更新されるようになります。
---

# DDL ステートメントに埋め込まれた<code>ANALYZE</code> <span class="version-mark">(v8.5.4 で導入)</span> {#code-analyze-code-embedded-in-ddl-statements-span-class-version-mark-introduced-in-v8-5-4-span}

このドキュメントでは、次の 2 種類の DDL ステートメントに組み込まれている`ANALYZE`機能について説明します。

-   新しいインデックスを作成するDDL文: [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)
-   既存のインデックスを再編成する DDL ステートメント: [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md)と[`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)

この機能を有効にすると、TiDBは新規または再編成されたインデックスがユーザーに表示される前に、自動的に`ANALYZE` （統計収集）操作を実行します。これにより、インデックスの作成または再編成後に一時的に統計が利用できなくなることによる、オプティマイザの推定値の不正確さや潜在的なプラン変更を防止できます。

## 使用シナリオ {#usage-scenarios}

DDL操作によってインデックスが交互に追加または変更されるシナリオでは、新しいインデックスに統計情報がないため、既存の安定したクエリに推定バイアスが生じ、オプティマイザーが最適ではないプランを選択する可能性があります。詳細については、 [問題 #57948](https://github.com/pingcap/tidb/issues/57948)参照してください。

例えば：

```sql
CREATE TABLE t (a INT, b INT);
INSERT INTO t VALUES (1, 1), (2, 2), (3, 3);
INSERT INTO t SELECT * FROM t; -- * N times

ALTER TABLE t ADD INDEX idx_a (a);

EXPLAIN SELECT * FROM t WHERE a > 4;
```

    +-------------------------+-----------+-----------+---------------+--------------------------------+
    | id                      | estRows   | task      | access object | operator info                  |
    +-------------------------+-----------+-----------+---------------+--------------------------------+
    | TableReader_8           | 131072.00 | root      |               | data:Selection_7               |
    | └─Selection_7           | 131072.00 | cop[tikv] |               | gt(test.t.a, 4)                |
    |   └─TableFullScan_6     | 393216.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
    +-------------------------+-----------+-----------+---------------+--------------------------------+
    3 rows in set (0.002 sec)

前のプランでは、新しく作成されたインデックスにはまだ統計情報がないため、TiDB はパス推定にヒューリスティック ルールのみに頼ることができます。インデックス アクセス パスでテーブル検索が不要でコストが大幅に低い場合を除き、オプティマイザはより安定した既存のパスを選択する傾向があります。前の例では、フル テーブル スキャンが選択されています。ただし、データ分散の観点から見ると、 `t.a > 4`実際には 0 行を返します。新しいインデックス`idx_a`が使用された場合、クエリは関連する行をすばやく見つけて、フル テーブル スキャンを回避できます。この例では、DDL がインデックスを作成した後、統計がすぐに収集されないため、生成されたプランは最適ではありませんが、オプティマイザは元のプランを引き続き使用するため、クエリのパフォーマンスは大幅に低下しません。ただし、 [問題 #57948](https://github.com/pingcap/tidb/issues/57948)によると、場合によってはヒューリスティックによって古いインデックスと新しいインデックスが不当に比較され、元のプランが依存しているインデックスが削除され、最終的にフル テーブル スキャンにフォールバックすることがあります。

v8.5.0以降、TiDBはインデックス間のヒューリスティック比較と、統計情報が欠落している場合の動作を改善しました。それでもなお、複雑なシナリオでは、DDLに`ANALYZE`を埋め込むことがプラン変更を防ぐ最善の方法です。システム変数[`tidb_stats_update_during_ddl`](/system-variables.md#tidb_stats_update_during_ddl-new-in-v854)を使用して、インデックス作成時または再編成時に埋め込み`ANALYZE`実行するかどうかを制御できます。デフォルト値は`OFF`です。

## <code>ADD INDEX</code> DDL {#code-add-index-code-ddl}

`tidb_stats_update_during_ddl`が`ON`の場合、 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)実行すると、再編成フェーズの終了後に埋め込まれた`ANALYZE`操作が自動的に実行されます。この`ANALYZE`操作は、新しく作成されたインデックスがユーザーに表示される前に、その統計情報を収集し、その後`ADD INDEX`残りのフェーズに進みます。

`ANALYZE`時間がかかる可能性があることを考慮して、TiDB は最初の Reorg の実行時間に基づいてタイムアウトしきい値を設定します。3 `ANALYZE`タイムアウトすると、 `ADD INDEX` `ANALYZE`完了を同期的に待つのをやめ、後続のプロセスを続行します。これにより、インデックスがユーザーにとってより早く表示されます。つまり、インデックス統計は`ANALYZE`非同期的に完了した後に更新されます。

例えば：

```sql
CREATE TABLE t (a INT, b INT, c INT);
Query OK, 0 rows affected (0.011 sec)

INSERT INTO t VALUES (1, 1, 1), (2, 2, 2), (3, 3, 3);
Query OK, 3 rows affected (0.003 sec)
Records: 3  Duplicates: 0  Warnings: 0

SET @@tidb_stats_update_during_ddl = 1;
Query OK, 0 rows affected (0.001 sec)

ALTER TABLE t ADD INDEX idx (a, b);
Query OK, 0 rows affected (0.049 sec)
```

```sql
EXPLAIN SELECT a FROM t WHERE a > 1;
```

    +------------------------+---------+-----------+--------------------------+----------------------------------+
    | id                     | estRows | task      | access object            | operator info                    |
    +------------------------+---------+-----------+--------------------------+----------------------------------+
    | IndexReader_7          | 4.00    | root      |                          | index:IndexRangeScan_6           |
    | └─IndexRangeScan_6     | 4.00    | cop[tikv] | table:t, index:idx(a, b) | range:(1,+inf], keep order:false |
    +------------------------+---------+-----------+--------------------------+----------------------------------+
    2 rows in set (0.002 sec)

```sql
SHOW STATS_HISTOGRAMS WHERE table_name = "t";
```

    +---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
    | Db_name | Table_name | Partition_name | Column_name | Is_index | Update_time         | Distinct_count | Null_count | Avg_col_size | Correlation | Load_status | Total_mem_usage | Hist_mem_usage | Topn_mem_usage | Cms_mem_usage |
    +---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
    | test    | t          |                | a           |        0 | 2025-10-30 20:17:57 |              3 |          0 |          0.5 |           1 | allLoaded   |             155 |              0 |            155 |             0 |
    | test    | t          |                | idx         |        1 | 2025-10-30 20:17:57 |              3 |          0 |            0 |           0 | allLoaded   |             182 |              0 |            182 |             0 |
    +---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
    2 rows in set (0.013 sec)

```sql
ADMIN SHOW DDL JOBS 1;
```

    +--------+---------+--------------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+----------------------------------------+
    | JOB_ID | DB_NAME | TABLE_NAME               | JOB_TYPE      | SCHEMA_STATE         | SCHEMA_ID | TABLE_ID | ROW_COUNT | CREATE_TIME                | START_TIME                 | END_TIME                   | STATE   | COMMENTS                               |
    +--------+---------+--------------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+----------------------------------------+
    |    151 | test    | t                        | add index     | write reorganization |         2 |      148 |   6291456 | 2025-10-29 00:14:47.181000 | 2025-10-29 00:14:47.183000 | NULL                       | running | analyzing, txn-merge, max_node_count=3 |
    +--------+---------+--------------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+----------------------------------------+
    1 rows in set (0.001 sec)

`ADD INDEX`例では、 `tidb_stats_update_during_ddl`が`ON`場合、 `ADD INDEX` DDL文の実行後、後続の`EXPLAIN`出力でインデックス`idx`の統計情報が自動的に収集され、メモリにロードされたことがわかります（ `SHOW STATS_HISTOGRAMS`を実行することで確認できます）。その結果、オプティマイザはこれらの統計情報を範囲スキャンにすぐに使用できます。インデックスの作成や再編成、および`ANALYZE`に時間がかかる場合は、 `ADMIN SHOW DDL JOBS`を実行してDDLジョブのステータスを確認できます。出力の`COMMENTS`列に`analyzing`含まれている場合、DDLジョブが統計情報を収集していることを意味します。

## 既存のインデックスを再編成するための DDL {#ddl-for-reorganizing-existing-indexes}

`tidb_stats_update_during_ddl`が`ON`の場合、インデックスの再編成を行う[`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md)または[`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)を実行すると、Reorg フェーズの完了後に埋め込まれた`ANALYZE`操作も実行されます。このメカニズムは`ADD INDEX`の場合と同じです。

-   インデックスが表示される前に統計の収集を開始します。
-   `ANALYZE`がタイムアウトすると、 [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md)と[`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md) `ANALYZE`完了を同期的に待つのをやめ、後続の処理を続行します。これにより、インデックスがユーザーにとってより早く表示されます。つまり、 `ANALYZE`非同期的に完了すると、インデックス統計が更新されます。

例えば：

```sql
CREATE TABLE s (a VARCHAR(10), INDEX idx (a));
Query OK, 0 rows affected (0.012 sec)

INSERT INTO s VALUES (1), (2), (3);
Query OK, 3 rows affected (0.003 sec)
Records: 3  Duplicates: 0  Warnings: 0

SET @@tidb_stats_update_during_ddl = 1;
Query OK, 0 rows affected (0.001 sec)

ALTER TABLE s MODIFY COLUMN a INT;
Query OK, 0 rows affected (0.056 sec)

EXPLAIN SELECT * FROM s WHERE a > 1;
```

    +------------------------+---------+-----------+-----------------------+----------------------------------+
    | id                     | estRows | task      | access object         | operator info                    |
    +------------------------+---------+-----------+-----------------------+----------------------------------+
    | IndexReader_7          | 2.00    | root      |                       | index:IndexRangeScan_6           |
    | └─IndexRangeScan_6     | 2.00    | cop[tikv] | table:s, index:idx(a) | range:(1,+inf], keep order:false |
    +------------------------+---------+-----------+-----------------------+----------------------------------+
    2 rows in set (0.005 sec)

```sql
SHOW STATS_HISTOGRAMS WHERE table_name = "s";
```

    +---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
    | Db_name | Table_name | Partition_name | Column_name | Is_index | Update_time         | Distinct_count | Null_count | Avg_col_size | Correlation | Load_status | Total_mem_usage | Hist_mem_usage | Topn_mem_usage | Cms_mem_usage |
    +---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
    | test    | s          |                | a           |        0 | 2025-10-30 20:10:18 |              3 |          0 |            2 |           1 | allLoaded   |             158 |              0 |            158 |             0 |
    | test    | s          |                | a           |        0 | 2025-10-30 20:10:18 |              3 |          0 |            1 |           1 | allLoaded   |             155 |              0 |            155 |             0 |
    | test    | s          |                | idx         |        1 | 2025-10-30 20:10:18 |              3 |          0 |            0 |           0 | allLoaded   |             158 |              0 |            158 |             0 |
    | test    | s          |                | idx         |        1 | 2025-10-30 20:10:18 |              3 |          0 |            0 |           0 | allLoaded   |             155 |              0 |            155 |             0 |
    +---------+------------+----------------+-------------+----------+---------------------+----------------+------------+--------------+-------------+-------------+-----------------+----------------+----------------+---------------+
    4 rows in set (0.008 sec)

```sql
ADMIN SHOW DDL JOBS 1;
```

    +--------+---------+------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+-----------------------------+
    | JOB_ID | DB_NAME | TABLE_NAME       | JOB_TYPE      | SCHEMA_STATE         | SCHEMA_ID | TABLE_ID | ROW_COUNT | CREATE_TIME                | START_TIME                 | END_TIME                   | STATE   | COMMENTS                    |
    +--------+---------+------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+-----------------------------+
    |    153 | test    | s                | modify column | write reorganization |         2 |      148 |  12582912 | 2025-10-29 00:26:49.240000 | 2025-10-29 00:26:49.244000 | NULL                       | running | analyzing                   |
    +--------+---------+------------------+---------------+----------------------+-----------+----------+-----------+----------------------------+----------------------------+----------------------------+---------+-----------------------------+
    1 rows in set (0.001 sec)

`MODIFY COLUMN`例では、 `tidb_stats_update_during_ddl`が`ON`場合、 `MODIFY COLUMN` DDL文の実行後、後続の`EXPLAIN`出力でインデックス`idx`の統計情報が自動的に収集され、メモリにロードされたことがわかります（ `SHOW STATS_HISTOGRAMS`を実行することで確認できます）。その結果、オプティマイザはこれらの統計情報を範囲スキャンにすぐに使用できます。インデックスの作成や再編成、および`ANALYZE`に時間がかかる場合は、 `ADMIN SHOW DDL JOBS`を実行してDDLジョブのステータスを確認できます。出力の`COMMENTS`列に`analyzing`含まれている場合、DDLジョブが統計情報を収集していることを意味します。
