---
title: TO_SECONDS
summary: 指定した秒数を Interval 型に変換します。
---

# TO_SECONDS

指定した秒数を Interval 型に変換します。

- 入力として正の整数、0、負の整数を受け付けます。

## 構文 {#syntax}

```sql
TO_SECONDS(<seconds>)
```

## エイリアス {#aliases}

- [EPOCH](/tidb-cloud-lake/sql/epoch.md)

## 戻り値の型 {#return-type}

Interval（形式は `hh:mm:ss`）。

## 例 {#examples}

```sql
SELECT TO_SECONDS(2), TO_SECONDS(0), TO_SECONDS((- 2));

┌─────────────────────────────────────────────────┐
│ to_seconds(2) │ to_seconds(0) │ to_seconds(- 2) │
├───────────────┼───────────────┼─────────────────┤
│ 0:00:02       │ 00:00:00      │ -0:00:02        │
└─────────────────────────────────────────────────┘
```