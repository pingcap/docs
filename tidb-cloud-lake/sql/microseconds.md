---
title: TO_MICROSECONDS
summary: 指定したマイクロ秒数を Interval 型に変換します。
---

# TO_MICROSECONDS

指定したマイクロ秒数を Interval 型に変換します。

- 正の整数、0、負の整数を入力として受け付けます。

## 構文 {#syntax}

```sql
TO_MICROSECONDS(<microseconds>)
```

## 戻り値の型 {#return-type}

Interval（形式: `hh:mm:ss.sssssss`）。

## 例 {#examples}

```sql
SELECT TO_MICROSECONDS(2), TO_MICROSECONDS(0), TO_MICROSECONDS((- 2));

┌────────────────────────────────────────────────────────────────┐
│ to_microseconds(2) │ to_microseconds(0) │ to_microseconds(- 2) │
├────────────────────┼────────────────────┼──────────────────────┤
│ 0:00:00.000002     │ 00:00:00           │ -0:00:00.000002      │
└────────────────────────────────────────────────────────────────┘
```