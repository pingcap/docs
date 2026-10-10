---
title: TO_YYYYMMDD
summary: 日付または時刻を含む日付（timestamp/datetime）を、年・月・日を含む UInt32 の数値（YYYY * 10000 + MM * 100 + DD）に変換します。## Syntax.
---

# TO_YYYYMMDD

日付または時刻を含む日付（timestamp/datetime）を、年・月・日を含む UInt32 の数値（YYYY *10000 + MM* 100 + DD）に変換します。

## 構文 {#syntax}

```sql
TO_YYYYMMDD(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|---------------|
| `<expr>`  | 日付/日時 |

## 戻り値の型 {#return-type}

`INT`。`YYYYMMDD` 形式で返します。

## 例 {#examples}

```sql
SELECT
  to_yyyymmdd('2023-11-12 09:38:18.165575');

┌───────────────────────────────────────────┐
│ to_yyyymmdd('2023-11-12 09:38:18.165575') │
├───────────────────────────────────────────┤
│                                  20231112 │
└───────────────────────────────────────────┘
```