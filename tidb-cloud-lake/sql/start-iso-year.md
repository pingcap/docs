---
title: TO_START_OF_ISO_YEAR
summary: 日付または時刻を含む日付（timestamp/datetime）に対して、ISO 年の最初の日を返します。
---

# TO_START_OF_ISO_YEAR

日付または時刻を含む日付（timestamp/datetime）に対して、ISO 年の最初の日を返します。

## 構文 {#syntax}

```sql
TO_START_OF_ISO_YEAR(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|----------------|
| `<expr>`  | 日付/タイムスタンプ |

## 戻り値の型 {#return-type}

`DATE`。`YYYY-MM-DD` 形式の日付を返します。

## 例 {#examples}

```sql
SELECT
  to_start_of_iso_year('2023-11-12 09:38:18.165575');

┌────────────────────────────────────────────────────┐
│ to_start_of_iso_year('2023-11-12 09:38:18.165575') │
├────────────────────────────────────────────────────┤
│ 2023-01-02                                         │
└────────────────────────────────────────────────────┘
```