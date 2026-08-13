---
title: FLUSH STATS_DELTA
summary: TiDB データベースにおける FLUSH STATS_DELTA の使用方法の概要。
---

# FLUSH STATS_DELTA <span class="version-mark">v8.5.7 で新規追加</span>

`FLUSH STATS_DELTA` は、TiDB のメモリにバッファされている保留中の統計デルタを、[`mysql.stats_meta`](/mysql-schema/mysql-schema.md#statistics-system-tables) システムテーブルに即座に永続化します。

`INSERT`、`UPDATE`、`DELETE` などの DML 文を使用してデータを変更すると、TiDB は影響を受けた各テーブルの総行数と変更行数の変化を記録し、これらの変更（統計デルタと呼ばれます）を、その文を実行した TiDB ノードのメモリにバッファします。デフォルトでは、TiDB は 20 * [`stats-lease`](/tidb-configuration-file.md#stats-lease) ごと（デフォルトでは 60 秒ごと）に統計デルタを `mysql.stats_meta` システムテーブルへ永続化します。詳細は、[自動更新](/statistics.md#automatic-update) を参照してください。

[テーブルの統計ヘルス状態](/sql-statements/sql-statement-show-stats-healthy.md)、[`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md) の出力、および自動統計収集のスケジューリングは、永続化された統計メタデータに依存します。そのため、オプティマイザの動作を検証するテストシナリオなど、永続化された統計メタデータに最近のデータ変更を即座に反映させる必要がある場合に、`FLUSH STATS_DELTA` は有用です。[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) を実行する前に `FLUSH STATS_DELTA` を実行する必要はありません。TiDB は、テーブルの統計を収集する前に、そのテーブルの保留中の統計デルタを自動的にフラッシュするためです。

## 概要 {#synopsis}

```ebnf+diagram
FlushStatsDeltaStmt ::=
    'FLUSH' 'STATS_DELTA' FlushTargetList ClusterOption?

FlushTargetList ::=
    FlushTarget (',' FlushTarget)*

FlushTarget ::=
    TableName
  | SchemaWildcard
  | GlobalWildcard

TableName ::=
    Identifier ('.' Identifier)?

SchemaWildcard ::=
    Identifier '.' '*'

GlobalWildcard ::=
    '*' '.' '*'

ClusterOption ::=
    'CLUSTER'
```

## オプション {#options}

- **Targets (`FlushTargetList`)**: 統計デルタをフラッシュする対象テーブルを指定します。少なくとも 1 つの対象を指定する必要があります。
    - `table_name`: 現在のデータベース内の特定のテーブルの統計デルタをフラッシュします。データベースを選択していない場合、TiDB は `No database selected` エラーを返します。
    - `db_name.table_name`: 指定したデータベース内の特定のテーブルの統計デルタをフラッシュします。
    - `db_name.*`: 指定したデータベース内のすべてのテーブルの統計デルタをフラッシュします。
    - `*.*`: すべてのテーブルの統計デルタをフラッシュします。
- **`CLUSTER`**: クラスター内のすべての TiDB ノードでこの文を実行します。各 TiDB ノードは、自身が実行した DML 文の統計デルタをバッファします。このオプションを指定しない場合、TiDB は接続先の TiDB ノードにバッファされているデルタのみを永続化します。

次の動作に注意してください。

- TiDB は、フラッシュ対象として指定された重複または包含関係にあるターゲットを重複排除します。たとえば、`FLUSH STATS_DELTA *.*, test.t` では、`*.*` がすでにすべてのテーブルを含んでいるため、`test.t` は無視されます。同様に、`FLUSH STATS_DELTA test.*, test.t` では、`test.*` が `test` データベース内のすべてのテーブルをすでに含んでいるため、`test.t` は無視されます。
- パーティションテーブルの場合、TiDB はそのテーブル本体とすべてのパーティションの統計デルタを永続化します。
- 指定したデータベースまたはテーブルが存在しない場合、TiDB は警告を返し、そのターゲットをスキップします。

## 例 {#examples}

データ変更の直後に、単一テーブルの統計デルタを即座に永続化します。

```sql
USE test;
CREATE TABLE t (a INT, b INT);
INSERT INTO t VALUES (1, 1), (2, 2), (3, 3);
FLUSH STATS_DELTA t;
```

```
Query OK, 0 rows affected (0.01 sec)
```

これで TiDB は、テーブルの行数変更を `mysql.stats_meta` システムテーブルに永続化しました。永続化された値は `SHOW STATS_META` を使用して確認できます。`SHOW STATS_META` は、接続先の TiDB ノードのメモリから統計情報を読み取る点に注意してください。この TiDB ノードは、[`stats-lease`](/tidb-configuration-file.md#stats-lease) ごと（デフォルトでは `3s` ごと）に永続化された値を読み込むため、フラッシュされた値が出力に反映されるまでに短い遅延が生じる場合があります。

```sql
SHOW STATS_META WHERE table_name = 't';
```

```
+---------+------------+----------------+---------------------+--------------+-----------+-------------------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count | Last_analyze_time |
+---------+------------+----------------+---------------------+--------------+-----------+-------------------+
| test    | t          |                | 2026-07-13 15:30:00 |            3 |         3 | NULL              |
+---------+------------+----------------+---------------------+--------------+-----------+-------------------+
1 row in set (0.01 sec)
```

現在のデータベース内のテーブルと、`sales` データベース内のすべてのテーブルの統計デルタを永続化します。

```sql
FLUSH STATS_DELTA t, sales.*;
```

クラスター内のすべての TiDB ノードにバッファされている、すべてのテーブルの統計デルタを永続化します。

```sql
FLUSH STATS_DELTA *.* CLUSTER;
```

## 権限 {#privileges}

`FLUSH STATS_DELTA` を実行するには、対象オブジェクトに対する `SELECT` 権限が必要です。

- `table_name` または `db_name.table_name` の場合、対象テーブルに対する `SELECT` 権限が必要です。
- `db_name.*` の場合、対象データベースに対する `SELECT` 権限が必要です。
- `*.*` の場合、グローバルな `SELECT` 権限が必要です。

他の `FLUSH` 文とは異なり、`FLUSH STATS_DELTA` には `RELOAD` 権限は不要です。

## MySQLとの互換性 {#mysql-compatibility}

`FLUSH STATS_DELTA` は、MySQL 構文に対する TiDB 独自の拡張です。

## 参照 {#see-also}

- [統計](/statistics.md)
- [`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md)
- [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)