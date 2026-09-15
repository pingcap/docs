---
title: TO_DECADES
summary: 将指定的 decade 数转换为 Interval 类型。
---

# TO_DECADES

将指定的 decade 数转换为 Interval 类型。

- 接受正整数、零和负整数作为输入。

## 语法 {#syntax}

```sql
TO_DECADES(<decades>)
```

## 返回类型 {#return-type}

Interval（以年表示）。

## 示例 {#examples}

```sql
SELECT TO_DECADES(2), TO_DECADES(0), TO_DECADES((- 2));

┌─────────────────────────────────────────────────┐
│ to_decades(2) │ to_decades(0) │ to_decades(- 2) │
├───────────────┼───────────────┼─────────────────┤
│ 20 years      │ 00:00:00      │ -20 years       │
└─────────────────────────────────────────────────┘
```