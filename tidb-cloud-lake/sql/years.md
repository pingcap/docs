---
title: TO_YEARS
summary: 指定した年数を Interval 型に変換します。
---

# TO_YEARS

指定した年数を Interval 型に変換します。

- 正の整数、0、負の整数を入力として受け付けます。

## 構文 {#syntax}

```sql
TO_YEARS(<years>)
```

## 戻り値の型 {#return-type}

Interval（年で表現されます）。

## 例 {#examples}

```sql
SELECT TO_YEARS(2), TO_YEARS(0), TO_YEARS((- 2));

┌───────────────────────────────────────────┐
│ to_years(2) │ to_years(0) │ to_years(- 2) │
├─────────────┼─────────────┼───────────────┤
│ 2 years     │ 00:00:00    │ -2 years      │
└───────────────────────────────────────────┘
```