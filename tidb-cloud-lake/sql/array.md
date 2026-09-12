---
title: 数组
summary: 已定义数据类型的数组。
---

# 数组

## 概述 {#overview}

`ARRAY(T)` 用于存储变长集合，其中所有元素都具有相同的类型 `T`。在创建表时定义元素类型，并使用数组函数来读或转换这些值。

> **注意：**
>
> {{{ .lake }}} 数组从 1 开始计数。`arr[1]` 返回第一个元素，`arr[n]` 返回最后一个元素。

## 示例 {#examples}

```sql
CREATE TABLE array_samples (arr ARRAY(INT64));

INSERT INTO array_samples VALUES ([1, 2, 3]), ([10, 20]);

SELECT
  arr,
  arr[1]   AS first_elem,
  arr[2]   AS second_elem
FROM array_samples;
```

结果：

```
┌────────────┬────────────┬──────────────┐
│ arr        │ first_elem │ second_elem │
├────────────┼────────────┼──────────────┤
│ [1,2,3]    │          1 │            2 │
│ [10,20]    │         10 │           20 │
└────────────┴────────────┴──────────────┘
```

```sql
-- Index 0 always returns NULL because arrays are 1-based.
SELECT arr[0] AS zeroth_elem FROM array_samples;
```

结果：

```
┌─────────────┐
│ zeroth_elem │
├─────────────┤
│ NULL        │
│ NULL        │
└─────────────┘
```