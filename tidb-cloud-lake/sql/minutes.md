---
title: TO_MINUTES
summary: 指定した分数を Interval 型に変換します。
---

# TO_MINUTES

指定した分数を Interval 型に変換します。

- 入力として、正の整数、0、負の整数を受け付けます。

## 構文 {#syntax}

```sql
TO_MINUTES(<minutes>)
```

## 戻り値の型 {#return-type}

Interval（形式: `hh:mm:ss`）。

## 例 {#examples}

```sql
SELECT TO_MINUTES(2), TO_MINUTES(0), TO_MINUTES((- 2));

┌─────────────────────────────────────────────────┐
│ to_minutes(2) │ to_minutes(0) │ to_minutes(- 2) │
├───────────────┼───────────────┼─────────────────┤
│ 0:02:00       │ 00:00:00      │ -0:02:00        │
└─────────────────────────────────────────────────┘
```