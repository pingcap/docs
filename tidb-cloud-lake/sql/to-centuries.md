---
title: TO_CENTURIES
summary: 指定した世紀数を Interval 型に変換します。
---

# TO_CENTURIES

指定した世紀数を Interval 型に変換します。

- 正の整数、0、負の整数を入力として受け付けます。

## 構文 {#syntax}

```sql
TO_CENTURIES(<centuries>)
```

## 戻り値の型 {#return-type}

Interval（年で表現されます）。

## 例 {#examples}

```sql
SELECT TO_CENTURIES(2), TO_CENTURIES(0), TO_CENTURIES(-2);

┌───────────────────────────────────────────────────────┐
│ to_centuries(2) │ to_centuries(0) │ to_centuries(- 2) │
├─────────────────┼─────────────────┼───────────────────┤
│ 200 years       │ 00:00:00        │ -200 years        │
└───────────────────────────────────────────────────────┘
```