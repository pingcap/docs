---
title: TO_DAY_OF_MONTH
summary: 日付または時刻を含む日付（timestamp/datetime）を、月の日（1-31）を表す UInt8 数値に変換します。
---

# TO_DAY_OF_MONTH

日付または時刻を含む日付（timestamp/datetime）を、月の日（1-31）を表す UInt8 数値に変換します。

## 構文 {#syntax}

```sql
TO_DAY_OF_MONTH(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|----------------|
| `<expr>`  | 日付/タイムスタンプ |

## エイリアス {#aliases}

- [DAY](/tidb-cloud-lake/sql/day.md)

## 戻り値の型 {#return-type}

`TINYINT`

## 例 {#examples}

```sql
SELECT NOW(), TO_DAY_OF_MONTH(NOW()), DAY(NOW());

┌──────────────────────────────────────────────────────────────────┐
│            now()           │ to_day_of_month(now()) │ day(now()) │
├────────────────────────────┼────────────────────────┼────────────┤
│ 2024-03-14 23:35:41.947962 │                     14 │         14 │
└──────────────────────────────────────────────────────────────────┘
```