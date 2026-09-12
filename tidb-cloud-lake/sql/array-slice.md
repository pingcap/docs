---
title: ARRAY_SLICE
summary: 使用 start 和 end 参数之间的切片提取子数组。
---

# ARRAY_SLICE

使用 start 和 end 参数之间的切片提取子数组。

## 语法 {#syntax}

```sql
ARRAY_SLICE(array, start, end)
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| array     | 要从中提取切片的源数组。 |
| start     | 切片的起始位置（包含）。 |
| end       | 切片的结束位置（不包含）。 |

## 返回类型 {#return-type}

数组（原数组的切片）。

## 关于索引的重要说明 {#important-note-on-indexing}

- 对于标准数组类型：索引从 **1** 开始（第一个元素的位置为 1）。
- 对于 variant 数组类型：索引从 **0** 开始（第一个元素的位置为 0），以兼容 Snowflake。

## 示例 {#examples}

### 示例 1：切片标准数组（1-based 索引） {#example-1-slicing-a-standard-array-1-based-indexing}

```sql
SELECT ARRAY_SLICE([10, 20, 30, 40, 50], 2, 4);
```

结果：

```
[20, 30]
```

### 示例 2：切片 Variant 数组（0-based 索引） {#example-2-slicing-a-variant-array-0-based-indexing}

```sql
SELECT ARRAY_SLICE(PARSE_JSON('["apple", "banana", "orange", "grape", "kiwi"]'), 1, 3);
```

结果：

```
["banana", "orange"]
```

### 示例 3：越界切片 {#example-3-out-of-bounds-slice}

```sql
SELECT ARRAY_SLICE([1, 2, 3], 4, 6);
```

结果：

```
[]
```