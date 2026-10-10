---
title: TO_SECOND
summary: 時刻を含む日付（timestamp/datetime）を、分内の秒数（0-59）を含む UInt8 数値に変換します。
---

# TO_SECOND

時刻を含む日付（timestamp/datetime）を、分内の秒数（0-59）を含む UInt8 数値に変換します。

## 構文 {#syntax}

```sql
TO_SECOND(<expr>)
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
    to_second('2023-11-12 09:38:18.165575');

┌─────────────────────────────────────────┐
│ to_second('2023-11-12 09:38:18.165575') │
├─────────────────────────────────────────┤
│                                      18 │
└─────────────────────────────────────────┘
```