---
title: TO_MILLISECONDS
summary: 指定したミリ秒数を Interval 型に変換します。
---

# TO_MILLISECONDS

指定したミリ秒数を Interval 型に変換します。

- 入力として正の整数、0、負の整数を受け付けます。

## 構文 {#syntax}

```sql
TO_MILLISECONDS(<milliseconds>)
```

## 戻り値の型 {#return-type}

Interval（形式: `hh:mm:ss.sss`）。

## 例 {#examples}

```sql
SELECT TO_MILLISECONDS(2), TO_MILLISECONDS(0), TO_MILLISECONDS((- 2));

┌────────────────────────────────────────────────────────────────┐
│ to_milliseconds(2) │ to_milliseconds(0) │ to_milliseconds(- 2) │
├────────────────────┼────────────────────┼──────────────────────┤
│ 0:00:00.002        │ 00:00:00           │ -0:00:00.002         │
└────────────────────────────────────────────────────────────────┘
```