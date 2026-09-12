---
title: ARRAY_CONTAINS
summary: 如果数组包含指定元素，则返回 true。
---

# ARRAY_CONTAINS

如果数组包含指定元素，则返回 true。

## 语法 {#syntax}

```sql
ARRAY_CONTAINS(array, element)
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| array     | 要在其中搜索的数组。 |
| element   | 要搜索的元素。 |

## 返回类型 {#return-type}

BOOLEAN

## 注意事项 {#notes}

此函数同时适用于标准数组类型和 variant 数组类型。

## 示例 {#examples}

### 示例 1：检查标准数组 {#example-1-checking-a-standard-array}

```sql
SELECT ARRAY_CONTAINS([1, 2, 3], 2);
```

结果：

```
true
```

### 示例 2：检查 variant 数组 {#example-2-checking-a-variant-array}

```sql
SELECT ARRAY_CONTAINS(PARSE_JSON('["apple", "banana", "orange"]'), 'banana');
```

结果：

```
true
```

### 示例 3：未找到元素 {#example-3-element-not-found}

```sql
SELECT ARRAY_CONTAINS([1, 2, 3], 4);
```

结果：

```
false
```