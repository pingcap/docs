---
title: ARRAY_UNIQUE
summary: 返回数组中唯一元素的数量。
---

# ARRAY_UNIQUE

返回数组中唯一元素的数量。

## 语法 {#syntax}

```sql
ARRAY_UNIQUE(array)
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| array     | 要分析其唯一元素的数组。 |

## 返回类型 {#return-type}

INTEGER

## 注意事项 {#notes}

此函数同时适用于标准数组类型和 variant 数组类型。

## 示例 {#examples}

### 示例 1：统计标准数组中的唯一元素 {#example-1-counting-unique-elements-in-a-standard-array}

```sql
SELECT ARRAY_UNIQUE([1, 2, 2, 3, 3, 3]);
```

结果：

```
3
```

### 示例 2：统计 variant 数组中的唯一元素 {#example-2-counting-unique-elements-in-a-variant-array}

```sql
SELECT ARRAY_UNIQUE(PARSE_JSON('["apple", "banana", "apple", "orange", "banana"]'));
```

结果：

```
3
```

### 示例 3：空数组 {#example-3-empty-array}

```sql
SELECT ARRAY_UNIQUE([]);
```

结果：

```
0
```