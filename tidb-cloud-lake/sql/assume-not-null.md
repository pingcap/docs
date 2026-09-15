---
title: ASSUME_NOT_NULL
summary: 对于 Nullable 类型，返回等价的非 Nullable 值。如果原始值为 NULL，则结果未定义。
---

# ASSUME_NOT_NULL

对于 Nullable 类型，返回等价的非 `Nullable` 值。如果原始值为 `NULL`，则结果未定义。

## 语法 {#syntax}

```sql
ASSUME_NOT_NULL(<x>)
```

## 别名 {#aliases}

- [REMOVE_NULLABLE](/tidb-cloud-lake/sql/remove-nullable.md)

## 返回类型 {#return-type}

对于非 `Nullable` 类型，返回原始数据类型；对于 `Nullable` 类型，返回其内部嵌套的非 `Nullable` 数据类型。

## 示例 {#examples}

```sql
CREATE TABLE default.t_null ( x int,  y int null);

INSERT INTO default.t_null values (1, null), (2, 3);

SELECT ASSUME_NOT_NULL(y), REMOVE_NULLABLE(y) FROM t_null;

┌─────────────────────────────────────────┐
│ assume_not_null(y) │ remove_nullable(y) │
├────────────────────┼────────────────────┤
│                  0 │                  0 │
│                  3 │                  3 │
└─────────────────────────────────────────┘
```