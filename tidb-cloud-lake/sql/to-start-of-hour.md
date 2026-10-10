---
title: TO_START_OF_HOUR
summary: 時刻を含む日付（timestamp/datetime）を、その時間の開始時刻に切り捨てます。## 構文。
---

# TO_START_OF_HOUR

時刻を含む日付（timestamp/datetime）を、その時間の開始時刻に切り捨てます。

## 構文 {#syntax}

```sql
TO_START_OF_HOUR(<expr>)
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
  to_start_of_hour('2023-11-12 09:38:18.165575');

┌────────────────────────────────────────────────┐
│ to_start_of_hour('2023-11-12 09:38:18.165575') │
├────────────────────────────────────────────────┤
│ 2023-11-12 09:00:00                            │
└────────────────────────────────────────────────┘
```