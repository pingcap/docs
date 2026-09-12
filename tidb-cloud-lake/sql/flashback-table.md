---
title: FLASHBACK TABLE
summary: 使用快照 ID 或时间戳将表闪回到以下版本，且仅涉及元信息操作，因此该过程非常快。
---

# FLASHBACK TABLE

使用快照 ID 或时间戳将表闪回到以下版本，且仅涉及元信息操作，因此该过程非常快。

通过命令中指定的快照 ID 或时间戳，{{{ .lake }}} 可以将表闪回到创建该快照时的先前状态。要获取表的快照 ID 和时间戳，请使用 [FUSE_SNAPSHOT](/tidb-cloud-lake/sql/fuse-snapshot.md)。

表闪回能力受以下条件限制：

- 该命令只能将现有表恢复到其先前状态。要恢复已删除的表，请使用 [UNDROP TABLE](/tidb-cloud-lake/sql/undrop-table.md)。

- 表闪回是 {{{ .lake }}} 时间旅行功能的一部分。在使用该命令前，请确保要闪回的表支持时间旅行。例如，该命令不适用于 transient tables，因为 {{{ .lake }}} 不会为这类表创建或存储快照。

- 将表闪回到先前状态后，不能再回滚该操作，但你可以再次将表闪回到更早的状态。

- {{{ .lake }}} 建议仅在紧急恢复场景中使用此命令。若要查询表的历史数据，请使用 [AT](/tidb-cloud-lake/sql/at.md) 子句。

## 语法 {#syntax}

```sql
-- Restore with a snapshot ID
ALTER TABLE <table> FLASHBACK TO (SNAPSHOT => '<snapshot-id>');

-- Restore with a snapshot timestamp
ALTER TABLE <table> FLASHBACK TO (TIMESTAMP => '<timestamp>'::TIMESTAMP);
```

## 示例 {#example}

### 步骤 1：创建示例 users 表并插入数据 {#step-1-create-a-sample-users-table-and-insert-data}

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

数据：

```sql
SELECT * FROM users;
+------+------------+-----------+----------------------+----------------------------+
| id   | first_name | last_name | email                | registration_date          |
+------+------------+-----------+----------------------+----------------------------+
|    1 | John       | Doe       | john.doe@example.com | 2023-01-01 00:00:00.000000 |
|    2 | Jane       | Doe       | jane.doe@example.com | 2023-01-02 00:00:00.000000 |
+------+------------+-----------+----------------------+----------------------------+
```

快照：

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

### 步骤 2：模拟一次误删除操作 {#step-2-simulate-an-accidental-delete-operation}

```sql
-- Simulate an accidental delete operation
DELETE FROM users WHERE id = 1;
```

数据：

```sql
+------+------------+-----------+----------------------+----------------------------+
| id   | first_name | last_name | email                | registration_date          |
+------+------------+-----------+----------------------+----------------------------+
|    2 | Jane       | Doe       | jane.doe@example.com | 2023-01-02 00:00:00.000000 |
+------+------------+-----------+----------------------+----------------------------+
```

快照：

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

### 步骤 3：找到删除操作之前的快照 ID {#step-3-find-the-snapshot-id-before-the-delete-operation}

```sql
-- Assume the snapshot_id from the previous query is 'xxxxxx'
-- Restore the table to the snapshot before the delete operation
ALTER TABLE users FLASHBACK TO (SNAPSHOT => 'c5c538d6b8bc42f483eefbddd000af7d');
```

数据：

```sql
SELECT * FROM users;
+------+------------+-----------+----------------------+----------------------------+
| id   | first_name | last_name | email                | registration_date          |
+------+------------+-----------+----------------------+----------------------------+
|    1 | John       | Doe       | john.doe@example.com | 2023-01-01 00:00:00.000000 |
|    2 | Jane       | Doe       | jane.doe@example.com | 2023-01-02 00:00:00.000000 |
+------+------------+-----------+----------------------+----------------------------+
```

快照：

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