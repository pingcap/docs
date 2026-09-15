---
title: ARRAY_SIZE
summary: 返回数组的长度，`NULL` 元素也会计入。
---

# ARRAY_SIZE

返回数组的长度，`NULL` 元素也会计入。

别名：`ARRAY_LENGTH`

## 语法 {#syntax}

```sql
ARRAY_SIZE(<array>)
```

## 返回类型 {#return-type}

`BIGINT`

## 示例 {#examples}

```sql
SELECT ARRAY_SIZE([1, 2, 3]) AS size_plain;

┌──────────┐
│ size_plain │
├──────────┤
│        3 │
└──────────┘
```

```sql
SELECT ARRAY_SIZE([1, NULL, 3]) AS size_with_null;

┌──────────────┐
│ size_with_null│
├──────────────┤
│            3 │
└──────────────┘
```