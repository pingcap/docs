---
title: ARRAY_INDEXOF
summary: 返回数组中某个元素首次出现的位置索引。
---

# ARRAY_INDEXOF

返回数组中某个元素首次出现的位置索引。

## 语法 {#syntax}

```sql
ARRAY_INDEXOF(array, element)
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| array     | 要在其中搜索的数组。 |
| element   | 要搜索的元素。 |

## 返回类型 {#return-type}

INTEGER

## 关于索引的重要说明 {#important-note-on-indexing}

- 对于标准数组类型：索引从 **1** 开始（第一个元素的位置是 1）。
- 对于 variant 数组类型：索引从 **0** 开始（第一个元素的位置是 0），以兼容 Snowflake。

## 示例 {#examples}

### 示例 1：在标准数组中查找元素（索引从 1 开始） {#example-1-finding-an-element-in-a-standard-array-1-based-indexing}

```sql
SELECT ARRAY_INDEXOF([10, 20, 30, 20], 20);
```

结果：

```
2
```

### 示例 2：在 Variant 数组中查找元素（索引从 0 开始） {#example-2-finding-an-element-in-a-variant-array-0-based-indexing}

```sql
SELECT ARRAY_INDEXOF(PARSE_JSON('["apple", "banana", "orange"]'), 'banana');
```

结果：

```
1
```

### 示例 3：未找到元素 {#example-3-element-not-found}

```sql
SELECT ARRAY_INDEXOF([1, 2, 3], 4);
```

结果：

```
0
```