---
title: TO_MINUTES
summary: 将指定的分钟数转换为 Interval 类型。
---

# TO_MINUTES

将指定的分钟数转换为 Interval 类型。

- 接受正整数、零和负整数作为输入。

## 语法 {#syntax}

```sql
TO_MINUTES(<minutes>)
```

## 返回类型 {#return-type}

Interval（格式为 `hh:mm:ss`）。

## 示例 {#examples}

```sql
SELECT TO_MINUTES(2), TO_MINUTES(0), TO_MINUTES((- 2));

┌─────────────────────────────────────────────────┐
│ to_minutes(2) │ to_minutes(0) │ to_minutes(- 2) │
├───────────────┼───────────────┼─────────────────┤
│ 0:02:00       │ 00:00:00      │ -0:02:00        │
└─────────────────────────────────────────────────┘
```