---
title: TO_QUARTER
summary: 从给定的日期或时间戳中获取季度（1、2、3 或 4）。
---

# TO_QUARTER

从给定的日期或时间戳中获取季度（1、2、3 或 4）。

## 语法 {#syntax}

```sql
TO_QUARTER( <date_or_time_expr> )
```

## 别名 {#aliases}

- [QUARTER](/tidb-cloud-lake/sql/quarter.md)

## 返回类型 {#return-type}

整数型。

## 示例 {#examples}

```sql
SELECT NOW(), TO_QUARTER(NOW()), QUARTER(NOW());

┌─────────────────────────────────────────────────────────────────┐
│            now()           │ to_quarter(now()) │ quarter(now()) │
├────────────────────────────┼───────────────────┼────────────────┤
│ 2024-03-14 23:32:52.743133 │                 1 │              1 │
└─────────────────────────────────────────────────────────────────┘
```