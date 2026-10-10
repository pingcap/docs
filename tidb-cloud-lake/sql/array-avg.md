---
title: ARRAY_AVG
summary: 配列内の数値項目の平均を返します。`NULL` 要素は無視され、数値以外の値があるとエラーになります。
---

# ARRAY_AVG

配列内の数値項目の平均を返します。`NULL` 要素は無視され、数値以外の値があるとエラーになります。

## 構文 {#syntax}

```sql
ARRAY_AVG(<array>)
```

## 戻り値の型 {#return-type}

数値型（結果を表現できる最小の数値型が使用されます）。

## 例 {#examples}

```sql
SELECT ARRAY_AVG([1, 2, 3, 4]) AS avg_int;

┌─────────┐
│ avg_int │
├─────────┤
│     2.5 │
└─────────┘
```

```sql
SELECT ARRAY_AVG([1.5, 2.5, 3.5]) AS avg_decimal;

┌──────────────┐
│ avg_decimal  │
├──────────────┤
│       2.5000 │
└──────────────┘
```

```sql
SELECT ARRAY_AVG([10, NULL, 4]) AS avg_with_null;

┌──────────────┐
│ avg_with_null│
├──────────────┤
│          7.0 │
└──────────────┘
```