---
title: TO_MILLENNIA
summary: 指定した millennia 数を Interval 型に変換します。
---

# TO_MILLENNIA

指定した millennia 数を Interval 型に変換します。

- 入力として、正の整数、0、負の整数を受け付けます。

## 構文 {#syntax}

```sql
TO_MILLENNIA(<millennia>)
```

## 戻り値の型 {#return-type}

Interval（年で表現されます）。

## 例 {#examples}

```sql
SELECT TO_MILLENNIA(2), TO_MILLENNIA(0), TO_MILLENNIA((- 2));

┌───────────────────────────────────────────────────────┐
│ to_millennia(2) │ to_millennia(0) │ to_millennia(- 2) │
├─────────────────┼─────────────────┼───────────────────┤
│ 2000 years      │ 00:00:00        │ -2000 years       │
└───────────────────────────────────────────────────────┘
```