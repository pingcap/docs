---
title: TO_DAYS
summary: 指定した日数を Interval 型に変換します。
---

# TO_DAYS

指定した日数を Interval 型に変換します。

- 正の整数、0、負の整数を入力として受け付けます。

## 構文 {#syntax}

```sql
TO_DAYS(<days>)
```

## 戻り値の型 {#return-type}

Interval（day 単位で表現）。

## 例 {#examples}

```sql
SELECT TO_DAYS(2), TO_DAYS(0), TO_DAYS(-2);

┌────────────────────────────────────────┐
│ to_days(2) │ to_days(0) │ to_days(- 2) │
├────────────┼────────────┼──────────────┤
│ 2 days     │ 00:00:00   │ -2 days      │
└────────────────────────────────────────┘
```