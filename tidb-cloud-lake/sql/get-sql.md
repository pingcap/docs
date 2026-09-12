---
title: GET
summary: 按索引（从 1 开始）从数组中返回一个元素。
---

# GET

按索引（从 1 开始）从数组中返回一个元素。

## 语法 {#syntax}

```sql
GET( <array>, <index> )
```

## 别名 {#aliases}

- [ARRAY_GET](/tidb-cloud-lake/sql/array-get.md)

## 示例 {#examples}

```sql
SELECT GET([1, 2], 2), ARRAY_GET([1, 2], 2);

┌───────────────────────────────────────┐
│ get([1, 2], 2) │ array_get([1, 2], 2) │
├────────────────┼──────────────────────┤
│              2 │                    2 │
└───────────────────────────────────────┘
```