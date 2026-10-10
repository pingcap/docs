---
title: IS_NOT_ERROR
summary: 式がエラー値であるかどうかを示す Boolean 値を返します。
---

# IS_NOT_ERROR

式がエラー値であるかどうかを示す Boolean 値を返します。

関連情報: [IS_ERROR](/tidb-cloud-lake/sql/is-error.md)

## 構文 {#syntax}

```sql
IS_NOT_ERROR( <expr> )
```

## 戻り値の型 {#return-type}

式がエラーでない場合は `true`、それ以外の場合は `false` を返します。

## 例 {#examples}

```sql
-- Indicates division by zero, hence an error
SELECT IS_ERROR(1/0), IS_NOT_ERROR(1/0);

┌───────────────────────────────────────────┐
│ is_error((1 / 0)) │ is_not_error((1 / 0)) │
├───────────────────┼───────────────────────┤
│ true              │ false                 │
└───────────────────────────────────────────┘

-- The conversion to DATE is successful, hence not an error
SELECT IS_ERROR('2024-03-17'::DATE), IS_NOT_ERROR('2024-03-17'::DATE);

┌─────────────────────────────────────────────────────────────────┐
│ is_error('2024-03-17'::date) │ is_not_error('2024-03-17'::date) │
├──────────────────────────────┼──────────────────────────────────┤
│ false                        │ true                             │
└─────────────────────────────────────────────────────────────────┘
```