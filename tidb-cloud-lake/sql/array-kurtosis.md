---
title: ARRAY_KURTOSIS
summary: 配列内の数値の過剰尖度を返します。`NULL` 要素は無視され、非数値要素があるとエラーになります。
---

# ARRAY_KURTOSIS

配列内の数値の過剰尖度を返します。`NULL` 要素は無視され、非数値要素があるとエラーになります。

## 構文 {#syntax}

```sql
ARRAY_KURTOSIS(<array>)
```

## 戻り値の型 {#return-type}

浮動小数点数です。

## 例 {#examples}

```sql
SELECT ARRAY_KURTOSIS([1, 2, 3, 4]) AS kurt;

┌────────────────────────┐
│ kurt                   │
├────────────────────────┤
│ -1.200000000000001     │
└────────────────────────┘
```

```sql
SELECT ARRAY_KURTOSIS([1.5, 2.5, 3.5, 4.5]) AS kurt_decimal;

┌────────────────────────┐
│ kurt_decimal           │
├────────────────────────┤
│ -1.200000000000001     │
└────────────────────────┘
```

```sql
SELECT ARRAY_KURTOSIS([NULL, 2, 3, 4]) AS kurt_null;

┌────────────────┐
│ kurt_null      │
├────────────────┤
│ 0              │
└────────────────┘
```