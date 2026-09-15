---
title: ARRAY_GENERATE_RANGE
summary: 构建一个由起始值到结束值之间按固定间隔排列的整数数组。结束边界为排他。
---

# ARRAY_GENERATE_RANGE

构建一个由起始值到结束值之间按固定间隔排列的整数数组。`end` 边界为排他。

## 语法 {#syntax}

```sql
ARRAY_GENERATE_RANGE(<start>, <end>[, <step>])
```

- `<start>`：要包含的第一个值。
- `<end>`：排他的上界（或下界）。
- `<step>`：可选的增量（默认为 `1`）。负步长会生成降序序列。

## 返回类型 {#return-type}

`ARRAY`

## 示例 {#examples}

```sql
SELECT ARRAY_GENERATE_RANGE(1, 5) AS seq;

┌──────────┐
│ seq      │
├──────────┤
│ [1,2,3,4]│
└──────────┘
```

```sql
SELECT ARRAY_GENERATE_RANGE(0, 6, 2) AS seq_step;

┌────────────┐
│ seq_step   │
├────────────┤
│ [0,2,4]    │
└────────────┘
```

```sql
SELECT ARRAY_GENERATE_RANGE(5, 0, -2) AS seq_down;

┌────────────┐
│ seq_down   │
├────────────┤
│ [5,3,1]    │
└────────────┘
```