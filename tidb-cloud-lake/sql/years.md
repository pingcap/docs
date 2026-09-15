---
title: TO_YEARS
summary: 将指定的年数转换为 Interval 类型。
---

# TO_YEARS

将指定的年数转换为 Interval 类型。

- 接受正整数、零和负整数作为输入。

## 语法 {#syntax}

```sql
TO_YEARS(<years>)
```

## 返回类型 {#return-type}

Interval（以年表示）。

## 示例 {#examples}

```sql
SELECT TO_YEARS(2), TO_YEARS(0), TO_YEARS((- 2));

┌───────────────────────────────────────────┐
│ to_years(2) │ to_years(0) │ to_years(- 2) │
├─────────────┼─────────────┼───────────────┤
│ 2 years     │ 00:00:00    │ -2 years      │
└───────────────────────────────────────────┘
```