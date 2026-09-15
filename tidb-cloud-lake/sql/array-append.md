---
title: ARRAY_APPEND
summary: 将一个元素追加到数组末尾。
---

# ARRAY_APPEND

将一个元素追加到数组末尾。

## 语法 {#syntax}

```sql
ARRAY_APPEND(array, element)
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| array     | 要向其追加元素的源数组。 |
| element   | 要追加到数组中的元素。 |

## 返回类型 {#return-type}

追加元素后的数组。

## 注意事项 {#notes}

此函数同时适用于标准数组类型和 variant 数组类型。

## 示例 {#examples}

### 示例 1：追加到标准数组 {#example-1-appending-to-a-standard-array}

```sql
SELECT ARRAY_APPEND([1, 2, 3], 4);
```

结果：

```
[1, 2, 3, 4]
```

### 示例 2：追加到 variant 数组 {#example-2-appending-to-a-variant-array}

```sql
SELECT ARRAY_APPEND(PARSE_JSON('[1, 2, 3]'), 4);
```

结果：

```
[1, 2, 3, 4]
```

### 示例 3：追加不同的数据类型 {#example-3-appending-different-data-types}

```sql
SELECT ARRAY_APPEND(['a', 'b'], 'c');
```

结果：

```
["a", "b", "c"]
```

## 相关函数 {#related-functions}

- [ARRAY_PREPEND](/tidb-cloud-lake/sql/array-prepend.md)：将一个元素前置到数组开头
- [ARRAY_CONCAT](/tidb-cloud-lake/sql/array-concat.md)：连接两个数组