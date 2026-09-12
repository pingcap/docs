---
title: POW
summary: 返回 `x` 的 `y` 次幂值。
---

# POW

返回 `x` 的 `y` 次幂值。

## 语法 {#syntax}

```sql
POW( <x, y> )
```

## 别名 {#aliases}

- [POWER](/tidb-cloud-lake/sql/power.md)

## 示例 {#examples}

```sql
SELECT POW(-2, 2), POWER(-2, 2);

┌─────────────────────────────────┐
│ pow((- 2), 2) │ power((- 2), 2) │
├───────────────┼─────────────────┤
│             4 │               4 │
└─────────────────────────────────┘
```