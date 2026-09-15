---
title: ARRAY_PREPEND
summary: 将一个元素添加到数组的开头。
---

# ARRAY_PREPEND

将一个元素添加到数组的开头。

## 语法 {#syntax}

```sql
ARRAY_PREPEND(element, array)
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| element   | 要添加到数组开头的元素。 |
| array     | 将在其开头添加该元素的源数组。 |

## 返回类型 {#return-type}

返回添加了前置元素后的数组。

## 注意事项 {#notes}

此函数同时适用于标准数组类型和 variant 数组类型。

## 示例 {#examples}

### 示例 1：向标准数组开头添加元素 {#example-1-prepending-to-a-standard-array}

```sql
SELECT ARRAY_PREPEND(0, [1, 2, 3]);
```

结果：

```
[0, 1, 2, 3]
```

### 示例 2：向 variant 数组开头添加元素 {#example-2-prepending-to-a-variant-array}

```sql
SELECT ARRAY_PREPEND('apple', PARSE_JSON('["banana", "orange"]'));
```

结果：

```
["apple", "banana", "orange"]
```

### 示例 3：添加复杂元素到数组开头 {#example-3-prepending-a-complex-element}

```sql
SELECT ARRAY_PREPEND(PARSE_JSON('{"value": 0}'), [1, 2, 3]);
```

结果：

```
[{"value": 0}, 1, 2, 3]
```