---
title: TO_WEEKS
summary: 指定した週数を Interval 型に変換します。
---

# TO_WEEKS

指定した週数を Interval 型に変換します。

- 入力として正の整数、0、負の整数を受け付けます。

## 構文 {#syntax}

```sql
TO_WEEKS(<weeks>)
```

## 戻り値の型 {#return-type}

Interval（days で表現されます）。

## 例 {#examples}

```sql
SELECT TO_WEEKS(2), TO_WEEKS(0), TO_WEEKS((- 2));

┌───────────────────────────────────────────┐
│ to_weeks(2) │ to_weeks(0) │ to_weeks(- 2) │
├─────────────┼─────────────┼───────────────┤
│ 14 days     │ 00:00:00    │ -14 days      │
└───────────────────────────────────────────┘
```