---
title: TO_MILLENNIA
summary: 将指定的千年数转换为 Interval 类型。
---

# TO_MILLENNIA

将指定的千年数转换为 Interval 类型。

- 接受正整数、零和负整数作为输入。

## 语法 {#syntax}

```sql
TO_MILLENNIA(<millennia>)
```

## 返回类型 {#return-type}

Interval（以年表示）。

## 示例 {#examples}

```sql
SELECT TO_MILLENNIA(2), TO_MILLENNIA(0), TO_MILLENNIA((- 2));

┌───────────────────────────────────────────────────────┐
│ to_millennia(2) │ to_millennia(0) │ to_millennia(- 2) │
├─────────────────┼─────────────────┼───────────────────┤
│ 2000 years      │ 00:00:00        │ -2000 years       │
└───────────────────────────────────────────────────────┘
```