---
title: ARRAY_STDDEV_POP
summary: 数値配列の値の母標準偏差を計算します。`NULL` エントリは無視され、非数値エントリはエラーになります。
---

# ARRAY_STDDEV_POP

数値配列の値の母標準偏差を計算します。`NULL` エントリは無視され、非数値エントリはエラーになります。

## 構文 {#syntax}

```sql
ARRAY_STDDEV_POP(<array>)
```

## 戻り値の型 {#return-type}

浮動小数点数です。

## 例 {#examples}

```sql
SELECT ARRAY_STDDEV_POP([2, 4, 4, 4, 5, 5, 7, 9]) AS stddev_pop;

┌────────────┐
│ stddev_pop │
├────────────┤
│          2 │
└────────────┘
```

```sql
SELECT ARRAY_STDDEV_POP([1.5, 2.5, NULL, 3.5]) AS stddev_pop_null;

┌─────────────────┐
│ stddev_pop_null │
├─────────────────┤
│ 0.816496580927726 │
└─────────────────┘
```