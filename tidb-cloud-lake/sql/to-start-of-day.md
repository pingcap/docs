---
title: TO_START_OF_DAY
summary: 時刻を含む日付（timestamp/datetime）をその日の開始時刻に切り下げます。## 構文。
---

# TO_START_OF_DAY

時刻を含む日付（timestamp/datetime）をその日の開始時刻に切り下げます。

## 構文 {#syntax}

```sql
TO_START_OF_DAY( <expr> )
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|-------------|
| `<expr>`  | timestamp   |

## 戻り値の型 {#return-type}

`TIMESTAMP`。日付を `YYYY-MM-DD hh:mm:ss.ffffff` 形式で返します。

## 例 {#examples}

```sql
SELECT
  to_start_of_day('2023-11-12 09:38:18.165575');

┌───────────────────────────────────────────────┐
│ to_start_of_day('2023-11-12 09:38:18.165575') │
├───────────────────────────────────────────────┤
│ 2023-11-12 00:00:00                           │
└───────────────────────────────────────────────┘
```