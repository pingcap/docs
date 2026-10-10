---
title: ARRAY_MEDIAN
summary: 配列内の数値の中央値を返します。NULL 要素は無視されます。
---

# ARRAY_MEDIAN

配列内の数値の中央値を返します。`NULL` 要素は無視されます。

## 構文 {#syntax}

```sql
ARRAY_MEDIAN(<array>)
```

## 戻り値の型 {#return-type}

数値型です。長さが偶数の入力では、中央の 2 つの値の平均が結果になります。

## 例 {#examples}

```sql
SELECT ARRAY_MEDIAN([1, 3, 2, 4]) AS med_even;

┌────────┐
│ med_even │
├────────┤
│    2.5 │
└────────┘
```

```sql
SELECT ARRAY_MEDIAN([1, 3, 5]) AS med_odd;

┌────────┐
│ med_odd│
├────────┤
│    3.0 │
└────────┘
```

```sql
SELECT ARRAY_MEDIAN([NULL, 10, 20, 30]) AS med_null;

┌────────┐
│ med_null│
├────────┤
│   20.0 │
└────────┘
```