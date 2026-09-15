---
title: CURRENT_CATALOG
summary: 返回当前会话正在使用的 catalog 名称。
---

# CURRENT_CATALOG

返回当前会话正在使用的 catalog 名称。

## 语法 {#syntax}

```sql
CURRENT_CATALOG()
```

## 示例 {#examples}

```sql
SELECT CURRENT_CATALOG();

┌───────────────────┐
│ current_catalog() │
├───────────────────┤
│ default           │
└───────────────────┘
```