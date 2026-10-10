---
title: TO_MONTH
summary: 日付または日時（timestamp/datetime）を、月番号（1-12）を含む UInt8 数値に変換します。
---

# TO_MONTH

日付または日時（timestamp/datetime）を、月番号（1-12）を含む UInt8 数値に変換します。

## 構文 {#syntax}

```sql
TO_MONTH(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|----------------|
| `<expr>`  | 日付/タイムスタンプ |

## エイリアス {#aliases}

- [MONTH](/tidb-cloud-lake/sql/month.md)

## 戻り値の型 {#return-type}

 `TINYINT`

## 例 {#examples}

```sql
SELECT NOW(), TO_MONTH(NOW()), MONTH(NOW());

┌─────────────────────────────────────────────────────────────┐
│            now()           │ to_month(now()) │ month(now()) │
├────────────────────────────┼─────────────────┼──────────────┤
│ 2024-03-14 23:34:02.161291 │               3 │            3 │
└─────────────────────────────────────────────────────────────┘
```