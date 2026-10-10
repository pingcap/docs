---
title: ARRAY_ANY
summary: 配列から最初の非NULL要素を返します。`ARRAY_AGGREGATE(<array>, 'ANY')` と同等です。
---

# ARRAY_ANY

配列から最初の非`NULL`要素を返します。`ARRAY_AGGREGATE(<array>, 'ANY')` と同等です。

## 構文 {#syntax}

```sql
ARRAY_ANY(<array>)
```

## 戻り値の型 {#return-type}

配列要素の型と同じです。

## 例 {#examples}

```sql
SELECT ARRAY_ANY(['a', 'b', 'c']) AS first_item;

┌────────────┐
│ first_item │
├────────────┤
│ a          │
└────────────┘
```

```sql
SELECT ARRAY_ANY([NULL, 'x', 'y']) AS first_non_null;

┌────────────────┐
│ first_non_null │
├────────────────┤
│ x              │
└────────────────┘
```

```sql
SELECT ARRAY_ANY([NULL, 10, 20]) AS first_number;

┌──────────────┐
│ first_number │
├──────────────┤
│           10 │
└──────────────┘
```