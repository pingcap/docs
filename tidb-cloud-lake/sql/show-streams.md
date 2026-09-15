---
title: SHOW STREAMS
summary: 列出与特定数据库关联的 streams。
---

# SHOW STREAMS

列出与特定数据库关联的 streams。

## 语法 {#syntax}

```sql
SHOW [ FULL ] STREAMS
     [ { FROM | IN } <database_name> ]
     [ LIKE '<pattern>' | WHERE <expr> ]
```

| 参数 | 描述 |
|-----------|----------------------------------------------------------------------------------------------|
| FULL      | 列出包含附加信息的结果。更多详情请参见[示例](#examples)。   |
| FROM / IN | 指定一个数据库。如果省略，该命令返回当前数据库中的结果。 |
| LIKE      | 使用大小写敏感的模式匹配并结合 `%` 通配符来过滤 stream 名称。        |
| WHERE     | 使用 WHERE 子句中的表达式来过滤 stream 名称。                            |

## 示例 {#examples}

以下示例显示属于当前数据库的 streams：

```sql
SHOW STREAMS;

┌──────────────────────────────────────────────────────────┐
│ Streams_in_default │        table_on       │     mode    │
├────────────────────┼───────────────────────┼─────────────┤
│ order_changes      │ default.orders        │ append_only │
│ s_append_only      │ default.t_append_only │ append_only │
│ s_standard         │ default.t_standard    │ standard    │
└──────────────────────────────────────────────────────────┘
```

以下示例显示当前数据库中 streams 的详细信息：

```sql
SHOW FULL STREAMS;

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│         created_on         │      name     │ database │ catalog │        table_on       │       owner      │ comment │     mode    │ invalid_reason │
├────────────────────────────┼───────────────┼──────────┼─────────┼───────────────────────┼──────────────────┼─────────┼─────────────┼────────────────┤
│ 2024-05-12 14:28:33.886271 │ order_changes │ default  │ default │ default.orders        │ NULL             │         │ append_only │                │
│ 2024-05-12 14:35:05.992050 │ s_append_only │ default  │ default │ default.t_append_only │ NULL             │         │ append_only │                │
│ 2024-05-12 14:35:05.981121 │ s_standard    │ default  │ default │ default.t_standard    │ NULL             │         │ standard    │                │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```