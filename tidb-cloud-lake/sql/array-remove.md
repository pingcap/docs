---
title: ARRAY_REMOVE
summary: 从数组中移除某个元素的所有出现项。
---

# ARRAY_REMOVE

从数组中移除某个元素的所有出现项。

## 语法 {#syntax}

```sql
ARRAY_REMOVE(array, element)
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| array     | 要从中移除元素的源数组。 |
| element   | 要从数组中移除的元素。 |

## 返回类型 {#return-type}

返回移除了指定元素所有出现项后的数组。

## 注意事项 {#notes}

此函数同时适用于标准数组类型和 variant 数组类型。

## 示例 {#examples}

### 示例 1：从标准数组中移除元素 {#example-1-removing-from-a-standard-array}

```sql
SELECT ARRAY_REMOVE([1, 2, 2, 3, 2], 2);
```

结果：

```
[1, 3]
```

### 示例 2：从 variant 数组中移除元素 {#example-2-removing-from-a-variant-array}

```sql
SELECT ARRAY_REMOVE(PARSE_JSON('["apple", "banana", "apple", "orange"]'), 'apple');
```

结果：

```
["banana", "orange"]
```

### 示例 3：未找到元素 {#example-3-element-not-found}

```sql
SELECT ARRAY_REMOVE([1, 2, 3], 4);
```

结果：

```
[1, 2, 3]
```