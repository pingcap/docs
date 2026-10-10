---
title: SHOW STATISTICS
summary: テーブルとそのカラムに関する統計情報を表示します。統計情報は、データ分布、行数、一意な値に関する情報を提供することで、クエリオプティマイザがクエリ実行計画についてより適切な判断を行うのに役立ちます。
---

# SHOW STATISTICS

テーブルとそのカラムに関する統計情報を表示します。統計情報は、データ分布、行数、一意な値に関する情報を提供することで、クエリオプティマイザがクエリ実行計画についてより適切な判断を行うのに役立ちます。

{{{ .lake }}} は、データ挿入時に自動的に統計情報を生成します。このコマンドを使用すると、統計情報を確認し、実際のデータと比較して、クエリ性能に影響する可能性のある不一致を特定できます。

## 構文 {#syntax}

```sql
SHOW STATISTICS [ FROM DATABASE <database_name> | FROM TABLE <database_name>.<table_name> ]
```

| パラメータ | 説明                                                                                                                 |
|-----------|-----------------------------------------------------------------------------------------------------------------------------|
| FROM DATABASE | 指定したデータベース内のすべてのテーブルの統計情報を表示します。                                |
| FROM TABLE | 指定したテーブルのみの統計情報を表示します。                                |

パラメータを指定しない場合、このコマンドは現在のデータベース内のすべてのテーブルの統計情報を返します。

## 出力カラム {#output-columns}

このコマンドは、各テーブルの各カラムについて、以下のカラムを返します。

| カラム | 説明                                                                                                                 |
|--------|-----------------------------------------------------------------------------------------------------------------------------|
| database | データベース名。                                |
| table | テーブル名。                                |
| column_name | カラム名。                                |
| stats_row_count | 統計情報で考慮された累積行数。統計情報は insert 時に更新されますが、delete 時には減算されないため、この値は actual_row_count より **大きくなる** ことがあります。 |
| actual_row_count | 現在のスナップショットにおけるテーブルの実際の行数。 |
| distinct_count | HyperLogLog から計算された、一意な値の推定数（NDV）。 |
| null_count | カラム内の NULL 値の数。 |
| avg_size | カラム内の各値の平均サイズ（バイト単位）。 |

## 例 {#examples}

### 現在のデータベースの統計情報を表示する {#show-statistics-for-current-database}

```sql
CREATE DATABASE test_db;
USE test_db;

CREATE TABLE t1 (id INT, name VARCHAR(50));
INSERT INTO t1 VALUES (1, 'Alice'), (2, 'Bob');

SHOW STATISTICS;
```

出力:

```
database  table  column_name  stats_row_count  actual_row_count  distinct_count  null_count  avg_size
test_db   t1     id           2                2                 2               0           4
test_db   t1     name         2                2                 2               0           16
```

### 特定のテーブルの統計情報を表示する {#show-statistics-for-a-specific-table}

```sql
CREATE TABLE t2 (age INT, city VARCHAR(50));
INSERT INTO t2 VALUES (25, 'New York'), (30, 'London');

SHOW STATISTICS FROM TABLE test_db.t2;
```

出力:

```
database  table  column_name  stats_row_count  actual_row_count  distinct_count  null_count  avg_size
test_db   t2     age          2                2                 2               0           4
test_db   t2     city         2                2                 2               0           19
```

### データベース内のすべてのテーブルの統計情報を表示する {#show-statistics-for-all-tables-in-a-database}

```sql
SHOW STATISTICS FROM DATABASE test_db;
```

これにより、`test_db` データベース内のすべてのテーブル（`t1` と `t2`）の統計情報が表示されます。

## 関連コマンド {#related-commands}

- [SHOW TABLE STATUS](/tidb-cloud-lake/sql/show-table-status.md): テーブルのステータス情報を表示します