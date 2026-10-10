---
title: ARRAY_STDDEV_SAMP
summary: 数値配列の値の標本標準偏差を計算します。`NULL` 項目は無視され、非数値エントリがあるとエラーになります。
---

# ARRAY_STDDEV_SAMP

数値配列の値の標本標準偏差を計算します。`NULL` 項目は無視され、非数値エントリがあるとエラーになります。

## 構文 {#syntax}

```sql
ARRAY_STDDEV_SAMP(<array>)
```

## 戻り値の型 {#return-type}

浮動小数点数です。

## 例 {#examples}

```sql
SELECT ARRAY_STDDEV_SAMP([2, 4, 4, 4, 5, 5, 7, 9]) AS stddev_samp;

┌─────────────┐
│ stddev_samp │
├─────────────┤
│ 2.138089935299395 │
└─────────────┘
```

```sql
SELECT ARRAY_STDDEV_SAMP([1.5, 2.5, NULL, 3.5]) AS stddev_samp_null;

┌─────────────────┐
│ stddev_samp_null │
├─────────────────┤
│              1  │
└─────────────────┘
```