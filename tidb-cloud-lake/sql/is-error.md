---
title: IS_ERROR
summary: 返回一个布尔值，指示表达式是否为错误值。
---

# IS_ERROR

返回一个布尔值，指示表达式是否为错误值。

另请参阅：[IS_NOT_ERROR](/tidb-cloud-lake/sql/is-not-error.md)

## 语法 {#syntax}

```sql
IS_ERROR( <expr> )
```

## 返回类型 {#return-type}

如果表达式是错误，则返回 `true`；否则返回 `false`。

## 示例 {#examples}

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