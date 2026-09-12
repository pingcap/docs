---
title: CONNECTION_ID
summary: 返回当前连接的连接 ID。
---

# CONNECTION_ID

返回当前连接的连接 ID。

## 语法 {#syntax}

```sql
CONNECTION_ID()
```

## 示例 {#examples}

```sql
SELECT CONNECTION_ID();

┌──────────────────────────────────────┐
│            connection_id()           │
├──────────────────────────────────────┤
│ 23cb06ec-583e-4eba-b790-7c8cf72a53f8 │
└──────────────────────────────────────┘
```