---
title: ARRAY_MIN
summary: 配列内の最小の数値を返します。`NULL` 要素はスキップされ、非数値の値があるとエラーになります。
---

# ARRAY_MIN

配列内の最小の数値を返します。`NULL` 要素はスキップされ、非数値の値があるとエラーになります。

## 構文 {#syntax}

```sql
ARRAY_MIN(<array>)
```

## 戻り値の型 {#return-type}

配列要素と同じ数値型です。

## 例 {#examples}

```sql
SELECT ARRAY_MIN([5, 2, 9, -1]) AS min_int;

┌─────────┐
│ min_int │
├─────────┤
│      -1 │
└─────────┘
```

```sql
SELECT ARRAY_MIN([1.5, -2.25, 3.0]) AS min_decimal;

┌──────────────┐
│ min_decimal  │
├──────────────┤
│       -2.25  │
└──────────────┘
```

```sql
SELECT ARRAY_MIN([NULL, 10, 4]) AS min_with_null;

┌──────────────┐
│ min_with_null│
├──────────────┤
│            4 │
└──────────────┘
```