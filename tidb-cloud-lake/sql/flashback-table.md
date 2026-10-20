---
title: FLASHBACK TABLE
summary: スナップショット ID またはタイムスタンプを使用してテーブルを以前のバージョンにフラッシュバックします。メタデータ操作のみを伴うため、高速に実行できます。
---

# FLASHBACK TABLE

スナップショット ID またはタイムスタンプを使用してテーブルを以前のバージョンにフラッシュバックします。メタデータ操作のみを伴うため、高速に実行できます。

コマンドで指定したスナップショット ID またはタイムスタンプに基づいて、{{{ .lake }}} はそのスナップショットが作成された時点の以前の状態にテーブルをフラッシュバックします。テーブルのスナップショット ID とタイムスタンプを取得するには、[FUSE_SNAPSHOT](/tidb-cloud-lake/sql/fuse-snapshot.md) を使用します。

テーブルをフラッシュバックできるのは、次の条件を満たす場合に限られます。

- このコマンドは、既存のテーブルのみを以前の状態に戻します。削除されたテーブルをリカバリするには、[UNDROP TABLE](/tidb-cloud-lake/sql/undrop-table.md) を使用します。

- テーブルのフラッシュバックは、{{{ .lake }}} の time travel 機能の一部です。このコマンドを使用する前に、フラッシュバックしたいテーブルが time travel の対象であることを確認してください。たとえば、transient table では {{{ .lake }}} がそのようなテーブルのスナップショットを作成または保存しないため、このコマンドは機能しません。

- テーブルを以前の状態にフラッシュバックした後でロールバックすることはできませんが、さらに以前の状態へ再度フラッシュバックすることはできます。

- {{{ .lake }}} では、このコマンドは緊急時のリカバリにのみ使用することを推奨しています。テーブルの履歴データをクエリするには、[AT](/tidb-cloud-lake/sql/at.md) 句を使用します。

## 構文 {#syntax}

```sql
-- Restore with a snapshot ID
ALTER TABLE <table> FLASHBACK TO (SNAPSHOT => '<snapshot-id>');

-- Restore with a snapshot timestamp
ALTER TABLE <table> FLASHBACK TO (TIMESTAMP => '<timestamp>'::TIMESTAMP);
```

## 例 {#example}

### ステップ 1: サンプルの users テーブルを作成してデータを挿入する {#step-1-create-a-sample-users-table-and-insert-data}

```sql
-- Create a sample users table
CREATE TABLE users (
    id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    registration_date TIMESTAMP
);

-- Insert sample data
INSERT INTO users (id, first_name, last_name, email, registration_date)
VALUES (1, 'John', 'Doe', 'john.doe@example.com', '2023-01-01 00:00:00'),
       (2, 'Jane', 'Doe', 'jane.doe@example.com', '2023-01-02 00:00:00');
```

データ:

```sql
SELECT * FROM users;
+------+------------+-----------+----------------------+----------------------------+
| id   | first_name | last_name | email                | registration_date          |
+------+------------+-----------+----------------------+----------------------------+
|    1 | John       | Doe       | john.doe@example.com | 2023-01-01 00:00:00.000000 |
|    2 | Jane       | Doe       | jane.doe@example.com | 2023-01-02 00:00:00.000000 |
+------+------------+-----------+----------------------+----------------------------+
```

スナップショット:

```sql
SELECT * FROM Fuse_snapshot('default', 'users')\G;
*************************** 1. row ***************************
         snapshot_id: c5c538d6b8bc42f483eefbddd000af7d
   snapshot_location: 29356/44446/_ss/c5c538d6b8bc42f483eefbddd000af7d_v2.json
      format_version: 2
previous_snapshot_id: NULL
       segment_count: 1
         block_count: 1
           row_count: 2
  bytes_uncompressed: 150
    bytes_compressed: 829
          index_size: 1028
           timestamp: 2023-04-19 04:20:25.062854
```

### ステップ 2: 誤った削除操作をシミュレートする {#step-2-simulate-an-accidental-delete-operation}

```sql
-- Simulate an accidental delete operation
DELETE FROM users WHERE id = 1;
```

データ:

```sql
+------+------------+-----------+----------------------+----------------------------+
| id   | first_name | last_name | email                | registration_date          |
+------+------------+-----------+----------------------+----------------------------+
|    2 | Jane       | Doe       | jane.doe@example.com | 2023-01-02 00:00:00.000000 |
+------+------------+-----------+----------------------+----------------------------+
```

スナップショット:

```sql
SELECT * FROM Fuse_snapshot('default', 'users')\G;
*************************** 1. row ***************************
         snapshot_id: 7193af51a4c9423ebd6ddbb04327b280
   snapshot_location: 29356/44446/_ss/7193af51a4c9423ebd6ddbb04327b280_v2.json
      format_version: 2
previous_snapshot_id: c5c538d6b8bc42f483eefbddd000af7d
       segment_count: 1
         block_count: 1
           row_count: 1
  bytes_uncompressed: 87
    bytes_compressed: 778
          index_size: 1028
           timestamp: 2023-04-19 04:22:20.390430
*************************** 2. row ***************************
         snapshot_id: c5c538d6b8bc42f483eefbddd000af7d
   snapshot_location: 29356/44446/_ss/c5c538d6b8bc42f483eefbddd000af7d_v2.json
      format_version: 2
previous_snapshot_id: NULL
       segment_count: 1
         block_count: 1
           row_count: 2
  bytes_uncompressed: 150
    bytes_compressed: 829
          index_size: 1028
           timestamp: 2023-04-19 04:20:25.062854
```

### ステップ 3: 削除操作前の snapshot ID を見つける {#step-3-find-the-snapshot-id-before-the-delete-operation}

```sql
-- Assume the snapshot_id from the previous query is 'xxxxxx'
-- Restore the table to the snapshot before the delete operation
ALTER TABLE users FLASHBACK TO (SNAPSHOT => 'c5c538d6b8bc42f483eefbddd000af7d');
```

データ:

```sql
SELECT * FROM users;
+------+------------+-----------+----------------------+----------------------------+
| id   | first_name | last_name | email                | registration_date          |
+------+------------+-----------+----------------------+----------------------------+
|    1 | John       | Doe       | john.doe@example.com | 2023-01-01 00:00:00.000000 |
|    2 | Jane       | Doe       | jane.doe@example.com | 2023-01-02 00:00:00.000000 |
+------+------------+-----------+----------------------+----------------------------+
```

Snapshot:

```sql
SELECT * FROM Fuse_snapshot('default', 'users')\G;
*************************** 1. row ***************************
         snapshot_id: c5c538d6b8bc42f483eefbddd000af7d
   snapshot_location: 29356/44446/_ss/c5c538d6b8bc42f483eefbddd000af7d_v2.json
      format_version: 2
previous_snapshot_id: NULL
       segment_count: 1
         block_count: 1
           row_count: 2
  bytes_uncompressed: 150
    bytes_compressed: 829
          index_size: 1028
           timestamp: 2023-04-19 04:20:25.062854
```