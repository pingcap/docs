---
title: TO_WEEKS
summary: 将指定的周数转换为 Interval 类型。
---

# TO_WEEKS

将指定的周数转换为 Interval 类型。

- 接受正整数、零和负整数作为输入。

## 语法 {#syntax}

```sql
TO_WEEKS(<weeks>)
```

## 返回类型 {#return-type}

Interval（以天表示）。

## 示例 {#examples}

```sql
SELECT TO_WEEKS(2), TO_WEEKS(0), TO_WEEKS((- 2));

┌───────────────────────────────────────────┐
│ to_weeks(2) │ to_weeks(0) │ to_weeks(- 2) │
├─────────────┼─────────────┼───────────────┤
│ 14 days     │ 00:00:00    │ -14 days      │
└───────────────────────────────────────────┘
```