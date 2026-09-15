---
title: TO_HOURS
summary: 将指定的小时数转换为 Interval 类型。
---

# TO_HOURS

将指定的小时数转换为 Interval 类型。

- 接受正整数、零和负整数作为输入。

## 语法 {#syntax}

```sql
TO_HOURS(<hours>)
```

## 返回类型 {#return-type}

Interval（格式为 `hh:mm:ss`）。

## 示例 {#examples}

```sql
SELECT TO_HOURS(2), TO_HOURS(0), TO_HOURS((- 2));

┌───────────────────────────────────────────┐
│ to_hours(2) │ to_hours(0) │ to_hours(- 2) │
├─────────────┼─────────────┼───────────────┤
│ 2:00:00     │ 00:00:00    │ -2:00:00      │
└───────────────────────────────────────────┘
```