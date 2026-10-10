---
title: TO_START_OF_FIFTEEN_MINUTES
summary: 日時（timestamp/datetime）を15分間隔の開始時刻に切り捨てます。## Syntax.
---

# TO_START_OF_FIFTEEN_MINUTES

日時（timestamp/datetime）を15分間隔の開始時刻に切り捨てます。

## 構文 {#syntax}

```sql
TO_START_OF_FIFTEEN_MINUTES(<expr>)
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
  to_start_of_fifteen_minutes('2023-11-12 09:38:18.165575');

┌───────────────────────────────────────────────────────────┐
│ to_start_of_fifteen_minutes('2023-11-12 09:38:18.165575') │
├───────────────────────────────────────────────────────────┤
│ 2023-11-12 09:30:00                                       │
└───────────────────────────────────────────────────────────┘
```