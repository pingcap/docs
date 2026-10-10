---
title: ARRAY_SKEWNESS
summary: 配列内の数値の歪度を返します。`NULL` 項目は無視され、数値以外の項目があるとエラーになります。
---

# ARRAY_SKEWNESS

配列内の数値の歪度を返します。`NULL` 項目は無視され、数値以外の項目があるとエラーになります。

## 構文 {#syntax}

```sql
ARRAY_SKEWNESS(<array>)
```

## 戻り値の型 {#return-type}

浮動小数点数です。

## 例 {#examples}

```sql
SELECT ARRAY_SKEWNESS([1, 2, 3, 4]) AS skew;

┌──────┐
│ skew │
├──────┤
│    0 │
└──────┘
```

```sql
SELECT ARRAY_SKEWNESS([1.5, 2.5, 3.5, 4.5]) AS skew_decimal;

┌────────────┐
│ skew_decimal│
├────────────┤
│          0 │
└────────────┘
```

```sql
SELECT ARRAY_SKEWNESS([NULL, 2, 3, 10]) AS skew_null;

┌────────────────────┐
│ skew_null          │
├────────────────────┤
│ 1.6300591617118865 │
└────────────────────┘
```