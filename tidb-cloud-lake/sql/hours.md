---
title: TO_HOURS
summary: 指定した時間数を Interval 型に変換します。
---

# TO_HOURS

指定した時間数を Interval 型に変換します。

- 入力として、正の整数、0、負の整数を受け付けます。

## 構文 {#syntax}

```sql
TO_HOURS(<hours>)
```

## 戻り値の型 {#return-type}

Interval（形式: `hh:mm:ss`）。

## 例 {#examples}

```sql
SELECT TO_HOURS(2), TO_HOURS(0), TO_HOURS((- 2));

┌───────────────────────────────────────────┐
│ to_hours(2) │ to_hours(0) │ to_hours(- 2) │
├─────────────┼─────────────┼───────────────┤
│ 2:00:00     │ 00:00:00    │ -2:00:00      │
└───────────────────────────────────────────┘
```