---
title: Tuple
summary: Tuple 是有序、不可变类型的集合。
---

# Tuple

## 概述 {#overview}

`TUPLE(T1, T2, …)` 用于存储一个具有已声明元素类型的固定有序值列表。每个 tuple 值都可以包含异构数据（例如，`TUPLE(DATETIME, STRING)`），其行为类似于紧凑的结构体。由于 tuple 是不可变的，因此当你需要更改其内容时，需要插入整个 tuple 值。

## 示例 {#examples}

### 创建并插入 {#create-and-insert}

```sql
CREATE TABLE events_tuple (
  event_info TUPLE(DATETIME, STRING)
);

INSERT INTO events_tuple VALUES
  (('2023-02-14 08:00:00', 'Valentine''s Day')),
  (('2023-03-17 19:30:00', 'Game Night'));

SELECT event_info FROM events_tuple;
```

结果：

```
┌──────────────────────────────────────────────────────┐
│ event_info                                           │
├──────────────────────────────────────────────────────┤
│ ["2023-02-14T08:00:00","Valentine's Day"]            │
│ ["2023-03-17T19:30:00","Game Night"]                 │
└──────────────────────────────────────────────────────┘
```

### 访问元素 {#access-elements}

Tuple 字段使用从 1 开始的序号访问方式（`tuple_column.1`），或者在你为元素命名时使用别名。

```sql
-- Ordinal access
SELECT
  event_info.1 AS event_time,
  event_info.2 AS description
FROM events_tuple;
```

结果：

```
┌──────────────────────────┬──────────────────┐
│ event_time               │ description      │
├──────────────────────────┼──────────────────┤
│ 2023-02-14T08:00:00      │ Valentine's Day  │
│ 2023-03-17T19:30:00      │ Game Night       │
└──────────────────────────┴──────────────────┘
```

当你需要在 SQL 表达式中传递成组的值，而又不想引入额外的表列时，tuple 会非常方便。