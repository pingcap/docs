---
title: TO_DECADES
summary: 指定した decades 数を Interval 型に変換します。
---

# TO_DECADES

指定した decades 数を Interval 型に変換します。

- 入力として、正の整数、0、負の整数を受け付けます。

## 構文 {#syntax}

```sql
TO_DECADES(<decades>)
```

## 戻り値の型 {#return-type}

Interval（年で表現されます）。

## 例 {#examples}

```sql
SELECT TO_DECADES(2), TO_DECADES(0), TO_DECADES((- 2));

┌─────────────────────────────────────────────────┐
│ to_decades(2) │ to_decades(0) │ to_decades(- 2) │
├───────────────┼───────────────┼─────────────────┤
│ 20 years      │ 00:00:00      │ -20 years       │
└─────────────────────────────────────────────────┘
```