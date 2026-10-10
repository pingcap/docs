---
title: TO_MONTHS
summary: 指定した月数を Interval 型に変換します。
---

# TO_MONTHS

指定した月数を Interval 型に変換します。

- 正の整数、0、負の整数を入力として受け付けます。

## 構文 {#syntax}

```sql
TO_MONTHS(<months>)
```

## 戻り値の型 {#return-type}

Interval（months で表現）。

## 例 {#examples}

```sql
SELECT TO_MONTHS(2), TO_MONTHS(0), TO_MONTHS((- 2));

┌──────────────────────────────────────────────┐
│ to_months(2) │ to_months(0) │ to_months(- 2) │
├──────────────┼──────────────┼────────────────┤
│ 2 months     │ 00:00:00     │ -2 months      │
└──────────────────────────────────────────────┘
```