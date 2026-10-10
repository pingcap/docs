---
title: UNNEST
summary: 配列をアンネストし、要素の集合を返します。
---

# UNNEST

配列をアンネストし、要素の集合を返します。

## 構文 {#syntax}

```sql
UNNEST( <array> )
```

## 例 {#examples}

```sql
SELECT UNNEST([1, 2]);

┌─────────────────┐
│  unnest([1, 2]) │
├─────────────────┤
│               1 │
│               2 │
└─────────────────┘

-- UNNEST(array) can be used as a table function.
SELECT * FROM UNNEST([1, 2]);

┌─────────────────┐
│      value      │
├─────────────────┤
│               1 │
│               2 │
└─────────────────┘
```