---
title: TO_MINUTE
summary: 時刻を含む日付（timestamp/datetime）を、時の中の分数（0-59）を含む UInt8 数値に変換します。
---

# TO_MINUTE

時刻を含む日付（timestamp/datetime）を、時の中の分数（0-59）を含む UInt8 数値に変換します。

## 構文 {#syntax}

```sql
TO_MINUTE(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|-------------|
| `<expr>`  | timestamp   |

## 戻り値の型 {#return-type}

 `TINYINT`

## 例 {#examples}

```sql
SELECT
    to_minute('2023-11-12 09:38:18.165575');

┌─────────────────────────────────────────┐
│ to_minute('2023-11-12 09:38:18.165575') │
├─────────────────────────────────────────┤
│                                      38 │
└─────────────────────────────────────────┘
```