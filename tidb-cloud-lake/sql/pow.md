---
title: POW
summary: x の y 乗の値を返します。
---

# POW

`x` の `y` 乗の値を返します。

## 構文 {#syntax}

```sql
POW( <x, y> )
```

## エイリアス {#aliases}

- [POWER](/tidb-cloud-lake/sql/power.md)

## 例 {#examples}

```sql
SELECT POW(-2, 2), POWER(-2, 2);

┌─────────────────────────────────┐
│ pow((- 2), 2) │ power((- 2), 2) │
├───────────────┼─────────────────┤
│             4 │               4 │
└─────────────────────────────────┘
```