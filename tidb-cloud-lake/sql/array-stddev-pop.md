---
title: ARRAY_STDDEV_POP
summary: 计算数值数组值的总体标准差。忽略 `NULL` 条目；非数值条目会引发错误。
---

# ARRAY_STDDEV_POP

计算数值数组值的总体标准差。忽略 `NULL` 条目；非数值条目会引发错误。

## 语法 {#syntax}

```sql
ARRAY_STDDEV_POP(<array>)
```

## 返回类型 {#return-type}

浮点型。

## 示例 {#examples}

```sql
SELECT ARRAY_STDDEV_POP([2, 4, 4, 4, 5, 5, 7, 9]) AS stddev_pop;

┌────────────┐
│ stddev_pop │
├────────────┤
│          2 │
└────────────┘
```

```sql
SELECT ARRAY_STDDEV_POP([1.5, 2.5, NULL, 3.5]) AS stddev_pop_null;

┌─────────────────┐
│ stddev_pop_null │
├─────────────────┤
│ 0.816496580927726 │
└─────────────────┘
```