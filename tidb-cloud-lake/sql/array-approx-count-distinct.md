---
title: ARRAY_APPROX_COUNT_DISTINCT
summary: 返回数组中不同元素的近似计数，并忽略 `NULL` 值。它使用与 [`APPROX_COUNT_DISTINCT`](/tidb-cloud-lake/sql/approx-count-distinct.md) 相同的基于 HyperLogLog 的估算器。
---

# ARRAY_APPROX_COUNT_DISTINCT

返回数组中不同元素的近似计数，并忽略 `NULL` 值。它使用与 [`APPROX_COUNT_DISTINCT`](/tidb-cloud-lake/sql/approx-count-distinct.md) 相同的基于 HyperLogLog 的估算器。

## 语法 {#syntax}

```sql
ARRAY_APPROX_COUNT_DISTINCT(<array>)
```

## 返回类型 {#return-type}

`BIGINT`

## 示例 {#examples}

```sql
SELECT ARRAY_APPROX_COUNT_DISTINCT([1, 1, 2, 3, 3, 3]) AS approx_cnt;

┌────────────┐
│ approx_cnt │
├────────────┤
│          3 │
└────────────┘
```

```sql
SELECT ARRAY_APPROX_COUNT_DISTINCT([NULL, 'a', 'a', 'b']) AS approx_cnt_text;

┌──────────────────┐
│ approx_cnt_text  │
├──────────────────┤
│                2 │
└──────────────────┘
```