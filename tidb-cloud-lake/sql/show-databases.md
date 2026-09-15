---
title: SHOW DATABASES
summary: 显示实例中存在的数据库列表。
---

# SHOW DATABASES

显示实例中存在的数据库列表。

另请参阅：[system.databases](/tidb-cloud-lake/sql/system-databases.md)

## 语法 {#syntax}

```sql
SHOW [ FULL ] DATABASES
    [ LIKE '<pattern>' | WHERE <expr> ]
```

| 参数 | 描述 |
|-----------|-----------------------------------------------------------------------------------------------------------------------------|
| FULL      | 列出包含附加信息的结果。更多详情请参阅[示例](#examples)。 |
| LIKE      | 使用大小写敏感的模式匹配按名称过滤结果。 |
| WHERE     | 使用 WHERE 子句中的表达式过滤结果。 |

## 示例 {#examples}

```sql
SHOW DATABASES;

┌──────────────────────┐
│ databases_in_default │
├──────────────────────┤
│ canada               │
│ china                │
│ default              │
│ information_schema   │
│ system               │
│ test                 │
└──────────────────────┘

SHOW FULL DATABASES;

┌───────────────────────────────────────────────────┐
│ catalog │       owner      │ databases_in_default │
├─────────┼──────────────────┼──────────────────────┤
│ default │ account_admin    │ canada               │
│ default │ account_admin    │ china                │
│ default │ NULL             │ default              │
│ default │ NULL             │ information_schema   │
│ default │ NULL             │ system               │
│ default │ account_admin    │ test                 │
└───────────────────────────────────────────────────┘
```