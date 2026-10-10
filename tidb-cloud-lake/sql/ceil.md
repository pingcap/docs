---
title: CEIL
summary: 数値を切り上げます。
---

# CEIL

数値を切り上げます。

## 構文 {#syntax}

```sql
CEIL( <x> )
```

## エイリアス {#aliases}

- [CEILING](/tidb-cloud-lake/sql/ceiling.md)

## 例 {#examples}

```sql
SELECT CEILING(-1.23), CEIL(-1.23);

┌────────────────────────────────────┐
│ ceiling((- 1.23)) │ ceil((- 1.23)) │
├───────────────────┼────────────────┤
│                -1 │             -1 │
└────────────────────────────────────┘
```