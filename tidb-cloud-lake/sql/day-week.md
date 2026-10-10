---
title: TO_DAY_OF_WEEK
summary: 日付または時刻を含む日付（timestamp/datetime）を、曜日番号を表す UInt8 の数値に変換します（Monday は 1、Sunday は 7）。
---

# TO_DAY_OF_WEEK

日付または時刻を含む日付（timestamp/datetime）を、曜日番号を表す UInt8 の数値に変換します（Monday は 1、Sunday は 7）。

## 構文 {#syntax}

```sql
TO_DAY_OF_WEEK(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|----------------|
| `<expr>`  | 日付/タイムスタンプ |

## 戻り値の型 {#return-type}

`TINYINT`

## 例 {#examples}

```sql

SELECT
    to_day_of_week('2023-11-12 09:38:18.165575');

┌──────────────────────────────────────────────┐
│ to_day_of_week('2023-11-12 09:38:18.165575') │
├──────────────────────────────────────────────┤
│                                            7 │
└──────────────────────────────────────────────┘
```