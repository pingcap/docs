---
title: CEIL
summary: 将数字向上取整。
---

# CEIL

将数字向上取整。

## 语法 {#syntax}

```sql
CEIL( <x> )
```

## 别名 {#aliases}

- [CEILING](/tidb-cloud-lake/sql/ceiling.md)

## 示例 {#examples}

```sql
SELECT CEILING(-1.23), CEIL(-1.23);

┌────────────────────────────────────┐
│ ceiling((- 1.23)) │ ceil((- 1.23)) │
├───────────────────┼────────────────┤
│                -1 │             -1 │
└────────────────────────────────────┘
```