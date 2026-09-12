---
title: ARRAY_REVERSE
summary: 反转数组中元素的顺序。
---

# ARRAY_REVERSE

反转数组中元素的顺序。

## 语法 {#syntax}

```sql
ARRAY_REVERSE(array)
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| array     | 要反转的数组。 |

## 返回类型 {#return-type}

返回元素顺序被反转后的数组。

## 注意事项 {#notes}

此函数同时适用于标准数组类型和 variant 数组类型。

## 示例 {#examples}

### 示例 1：反转标准数组 {#example-1-reversing-a-standard-array}

```sql
SELECT ARRAY_REVERSE([1, 2, 3, 4, 5]);
```

结果：

```
[5, 4, 3, 2, 1]
```

### 示例 2：反转 variant 数组 {#example-2-reversing-a-variant-array}

```sql
SELECT ARRAY_REVERSE(PARSE_JSON('["apple", "banana", "orange"]'));
```

结果：

```
["orange", "banana", "apple"]
```

### 示例 3：反转空数组 {#example-3-reversing-an-empty-array}

```sql
SELECT ARRAY_REVERSE([]);
```

结果：

```
[]
```