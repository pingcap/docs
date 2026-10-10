---
title: TO_START_OF_MINUTE
summary: 時刻を含む日付（timestamp/datetime）をその分の開始時刻に切り下げます。
---

# TO_START_OF_MINUTE

時刻を含む日付（timestamp/datetime）をその分の開始時刻に切り下げます。

## 構文 {#syntax}

```sql
TO_START_OF_MINUTE( <expr> )
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|-------------|
| `<expr>`  | timestamp   |

## 戻り値の型 {#return-type}

`TIMESTAMP`。日付を “YYYY-MM-DD hh:mm:ss.ffffff” 形式で返します。

## 例 {#examples}

```sql
SELECT
  to_start_of_minute('2023-11-12 09:38:18.165575');

┌──────────────────────────────────────────────────┐
│ to_start_of_minute('2023-11-12 09:38:18.165575') │
├──────────────────────────────────────────────────┤
│ 2023-11-12 09:38:00                              │
└──────────────────────────────────────────────────┘
```