---
title: AT
summary: AT 子句支持通过指定 snapshot ID、时间戳、stream 名称或时间间隔来检索数据的历史版本。
---

# AT

AT 子句支持通过指定 snapshot ID、时间戳、stream 名称或时间间隔来检索数据的历史版本。

{{{ .lake }}} 会在数据发生修改时自动创建快照，因此可以将快照视为过去某一时间点的数据视图。你可以通过 snapshot ID 或创建该快照时的时间戳来访问快照。关于如何获取 snapshot ID 和时间戳，请参见[获取 Snapshot ID 和时间戳](#obtaining-snapshot-id-and-timestamp)。

这是 {{{ .lake }}} Time Travel 功能的一部分。该功能允许你在保留时间内（默认 24 小时）对数据的历史版本进行查询、备份和恢复。

## 语法 {#syntax}

```sql
SELECT ...
FROM ...
AT (
       SNAPSHOT => '<snapshot_id>' |
       TIMESTAMP => <timestamp> |
       STREAM => <stream_name> |
       OFFSET => <time_interval>
   )
```

| 参数 | 描述 |
|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SNAPSHOT  | 指定一个特定的 snapshot ID，用于查询历史数据。 |
| TIMESTAMP | 指定一个特定的时间戳，用于检索该时间点的数据。 |
| STREAM    | 表示查询指定 stream 创建时刻的数据。 |
| OFFSET    | 指定从当前时间向前回溯的秒数。其形式应为负整数，绝对值表示以秒为单位的时间差。例如，`-3600` 表示回到 1 小时前（3,600 秒）。 |
| TAG       | 指定通过 `ALTER TABLE ... CREATE TAG` 创建的命名 tag，以查询与该 tag 关联的快照。这是一个实验特性，需要执行 `SET enable_experimental_table_ref = 1`。参见 [快照标签操作](/tidb-cloud-lake/sql/alter-table.md#snapshot-tag-operations)。 |

## 获取 Snapshot ID 和时间戳 {#obtaining-snapshot-id-and-timestamp}

如需返回某个表所有快照的 snapshot ID 和时间戳，请使用 [FUSE_SNAPSHOT](/tidb-cloud-lake/sql/fuse-snapshot.md) 函数：

```sql
SELECT snapshot_id,
       timestamp
FROM   FUSE_SNAPSHOT('<database_name>', '<table_name>');
```

## 示例 {#examples}

以下示例演示了 AT 子句如何基于 snapshot ID、时间戳和 stream 检索数据的历史版本：

1. 创建一个名为 `t` 的表，该表只有一列 `a`，然后向表中插入两行数据，值分别为 1 和 2。

    ```sql
    CREATE TABLE t(a INT);

    INSERT INTO t VALUES(1);
    INSERT INTO t VALUES(2);
    ```

2. 在表 `t` 上创建一个名为 `s` 的 stream，然后向表中额外插入一行值为 3 的数据。

    ```sql
    CREATE STREAM s ON TABLE t;

    INSERT INTO t VALUES(3);
    ```

3. 执行时间旅行查询以检索历史数据版本。

```sql
-- Return snapshot IDs and corresponding timestamps for table 't'
SELECT snapshot_id, timestamp FROM FUSE_SNAPSHOT('default', 't');
┌───────────────────────────────────────────────────────────────┐
│            snapshot_id           │          timestamp         │
├──────────────────────────────────┼────────────────────────────┤
│ 296349da841d4fa8820bbf8e228d75f3 │ 2024-04-02 15:25:21.456574 │
│ aaa4857c5935401790db2c9f0f2818be │ 2024-04-02 15:19:02.484304 │
│ e66ad2bc3f21416e87903dc9cd0388a3 │ 2024-04-02 15:18:40.766361 │
└───────────────────────────────────────────────────────────────┘

-- These queries retrieve the same data but using different methods:
-- by snapshot_id:
SELECT * FROM t AT (SNAPSHOT => 'aaa4857c5935401790db2c9f0f2818be');
-- by timestamp:
SELECT * FROM t AT (TIMESTAMP => '2024-04-02 15:19:02.484304'::TIMESTAMP);
-- by stream:
SELECT * FROM t AT (STREAM => s);

┌─────────────────┐
│        a        │
├─────────────────┤
│               1 │
│               2 │
└─────────────────┘

-- Retrieve all columns from table 't' with data from 60 seconds ago
SELECT * FROM t AT (OFFSET => -60);
```