---
title: ARRAY_COUNT
summary: 配列内の非NULL要素をカウントします。
---

# ARRAY_COUNT

配列内の非`NULL`要素をカウントします。

## 構文 {#syntax}

```sql
ARRAY_COUNT(<array>)
```

## 戻り値の型 {#return-type}

`BIGINT`

## 例 {#examples}

```sql
SELECT ARRAY_COUNT([1, 2, 3]) AS cnt;

┌─────┐
│ cnt │
├─────┤
│   3 │
└─────┘
```

```sql
SELECT ARRAY_COUNT([1, NULL, 3]) AS cnt_with_null;

┌──────────────┐
│ cnt_with_null│
├──────────────┤
│            2 │
└──────────────┘
```

```sql
SELECT ARRAY_COUNT(['a', 'b', NULL]) AS cnt_text;

┌─────────┐
│ cnt_text│
├─────────┤
│       2 │
└─────────┘
```