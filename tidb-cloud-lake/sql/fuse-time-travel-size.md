---
title: FUSE_TIME_TRAVEL_SIZE
summary: 计算表的历史数据（用于 Time Travel）的存储大小。
---

# FUSE_TIME_TRAVEL_SIZE

计算表的历史数据（用于 Time Travel）的存储大小。

## 语法 {#syntax}

```sql
-- Calculate historical data size for all tables in all databases
SELECT ...
FROM fuse_time_travel_size();

-- Calculate historical data size for all tables in a specified database
SELECT ...
FROM fuse_time_travel_size('<database_name>');

-- Calculate historical data size for a specified table in a specified database
SELECT ...
FROM fuse_time_travel_size('<database_name>', '<table_name>');
```

## 输出 {#output}

该函数返回一个结果集，包含以下列：

| 列 | 描述 |
|----------------------------------|-------------------------------------------------------------------------------------------------------|
| `database_name`                  | 表所在数据库的名称。                                                                                  |
| `table_name`                     | 表名。                                                                                                |
| `is_dropped`                     | 表示该表是否已被删除（已删除的表为 `true`，否则为 `false`）。                                        |
| `time_travel_size`               | 该表历史数据（用于 Time Travel）的总存储大小，单位为字节。                                            |
| `latest_snapshot_size`           | 该表最新快照的存储大小，单位为字节。                                                                  |
| `data_retention_period_in_hours` | Time Travel 数据的保留时间（单位为小时）（`NULL` 表示使用默认保留策略）。                             |
| `error`                          | 检索存储大小时遇到的错误（如果未发生错误，则为 `NULL`）。                                             |

## 示例 {#examples}

以下示例计算 `default` 数据库中所有表的历史数据大小：

```sql
SELECT * FROM fuse_time_travel_size('default')

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ database_name │ table_name │ is_dropped │ time_travel_size │ latest_snapshot_size │ data_retention_period_in_hours │       error      │
├───────────────┼────────────┼────────────┼──────────────────┼──────────────────────┼────────────────────────────────┼──────────────────┤
│ default       │ books      │ true       │             2810 │                 1490 │                           NULL │ NULL             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```