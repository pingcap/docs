---
title: DATABASE
summary: 返回当前已选择数据库的名称。如果未选择数据库，则此函数返回 default。
---

# DATABASE

返回当前已选择数据库的名称。如果未选择数据库，则此函数返回 `default`。

## 语法 {#syntax}

```sql
DATABASE()
```

## 示例 {#examples}

```sql
SELECT DATABASE();

┌────────────┐
│ database() │
├────────────┤
│ default    │
└────────────┘
```