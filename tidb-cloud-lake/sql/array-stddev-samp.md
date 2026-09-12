---
title: ARRAY_STDDEV_SAMP
summary: 计算数值数组值的样本标准差。`NULL` 项会被忽略；非数值条目会引发错误。
---

# ARRAY_STDDEV_SAMP

计算数值数组值的样本标准差。`NULL` 项会被忽略；非数值条目会引发错误。

## 语法 {#syntax}

```sql
ARRAY_STDDEV_SAMP(<array>)
```

## 返回类型 {#return-type}

浮点型。

## 示例 {#examples}

```sql
SELECT ARRAY_STDDEV_SAMP([2, 4, 4, 4, 5, 5, 7, 9]) AS stddev_samp;

┌─────────────┐
│ stddev_samp │
├─────────────┤
│ 2.138089935299395 │
└─────────────┘
```

```sql
SELECT ARRAY_STDDEV_SAMP([1.5, 2.5, NULL, 3.5]) AS stddev_samp_null;

┌─────────────────┐
│ stddev_samp_null │
├─────────────────┤
│              1  │
└─────────────────┘
```