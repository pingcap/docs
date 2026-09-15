---
title: TO_MONTHS
summary: 将指定的月数转换为 Interval 类型。
---

# TO_MONTHS

将指定的月数转换为 Interval 类型。

- 接受正整数、零和负整数作为输入。

## 语法 {#syntax}

```sql
TO_MONTHS(<months>)
```

## 返回类型 {#return-type}

Interval（以月表示）。

## 示例 {#examples}

```sql
SELECT TO_MONTHS(2), TO_MONTHS(0), TO_MONTHS((- 2));

┌──────────────────────────────────────────────┐
│ to_months(2) │ to_months(0) │ to_months(- 2) │
├──────────────┼──────────────┼────────────────┤
│ 2 months     │ 00:00:00     │ -2 months      │
└──────────────────────────────────────────────┘
```