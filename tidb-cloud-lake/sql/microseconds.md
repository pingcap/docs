---
title: TO_MICROSECONDS
summary: 将指定数量的微秒转换为 Interval 类型。
---

# TO_MICROSECONDS

将指定数量的微秒转换为 Interval 类型。

- 接受正整数、零和负整数作为输入。

## 语法 {#syntax}

```sql
TO_MICROSECONDS(<microseconds>)
```

## 返回类型 {#return-type}

Interval（格式为 `hh:mm:ss.sssssss`）。

## 示例 {#examples}

```sql
SELECT TO_MICROSECONDS(2), TO_MICROSECONDS(0), TO_MICROSECONDS((- 2));

┌────────────────────────────────────────────────────────────────┐
│ to_microseconds(2) │ to_microseconds(0) │ to_microseconds(- 2) │
├────────────────────┼────────────────────┼──────────────────────┤
│ 0:00:00.000002     │ 00:00:00           │ -0:00:00.000002      │
└────────────────────────────────────────────────────────────────┘
```