---
title: ARRAY_MAX
summary: 配列内の最大の数値を返します。`NULL` 要素はスキップされ、数値以外の値があるとエラーになります。
---

# ARRAY_MAX

配列内の最大の数値を返します。`NULL` 要素はスキップされ、数値以外の値があるとエラーになります。

## 構文 {#syntax}

```sql
ARRAY_MAX(<array>)
```

## 戻り値の型 {#return-type}

配列要素と同じ数値型です。

## 例 {#examples}

```sql
SELECT ARRAY_MAX([5, 2, 9, -1]) AS max_int;

┌─────────┐
│ max_int │
├─────────┤
│       9 │
└─────────┘
```

```sql
SELECT ARRAY_MAX([1.5, -2.25, 3.0]) AS max_decimal;

┌─────────────┐
│ max_decimal │
├─────────────┤
│      3.00   │
└─────────────┘
```

```sql
SELECT ARRAY_MAX([NULL, 10, 4]) AS max_with_null;

┌───────────────┐
│ max_with_null │
├───────────────┤
│           10  │
└───────────────┘
```