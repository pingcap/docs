---
title: TRY_CAST
summary: あるデータ型の値を別のデータ型に変換します。エラー時には NULL を返します。
---

# TRY_CAST

あるデータ型の値を別のデータ型に変換します。エラー時には NULL を返します。

関連情報: [CAST](/tidb-cloud-lake/sql/cast.md)

## 構文 {#syntax}

```sql
TRY_CAST( <expr> AS <data_type> )
```

## 例 {#examples}

```sql
SELECT TRY_CAST(1 AS VARCHAR);

┌───────────────────────┐
│ try_cast(1 as string) │
├───────────────────────┤
│ 1                     │
└───────────────────────┘
```