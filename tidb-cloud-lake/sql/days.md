---
title: TO_DAYS
summary: 将指定的天数转换为 Interval 类型。
---

# TO_DAYS

将指定的天数转换为 Interval 类型。

- 接受正整数、零和负整数作为输入。

## 语法 {#syntax}

```sql
TO_DAYS(<days>)
```

## 返回类型 {#return-type}

Interval（以天表示）。

## 示例 {#examples}

```sql
SELECT TO_DAYS(2), TO_DAYS(0), TO_DAYS(-2);

┌────────────────────────────────────────┐
│ to_days(2) │ to_days(0) │ to_days(- 2) │
├────────────┼────────────┼──────────────┤
│ 2 days     │ 00:00:00   │ -2 days      │
└────────────────────────────────────────┘
```