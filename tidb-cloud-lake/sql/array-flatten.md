---
title: ARRAY_FLATTEN
summary: 将嵌套数组展平为单维数组。
---

# ARRAY_FLATTEN

将嵌套数组展平为单维数组。

## 语法 {#syntax}

```sql
ARRAY_FLATTEN(array)
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| array     | 要展平的嵌套数组。 |

## 返回类型 {#return-type}

数组（展平后）。

## 注意事项 {#notes}

此函数同时适用于标准数组类型和 variant 数组类型。

## 示例 {#examples}

### 示例 1：展平嵌套数组 {#example-1-flattening-a-nested-array}

```sql
SELECT ARRAY_FLATTEN([[1, 2], [3, 4]]);
```

结果：

```
[1, 2, 3, 4]
```

### 示例 2：展平 variant 数组 {#example-2-flattening-a-variant-array}

```sql
SELECT ARRAY_FLATTEN(PARSE_JSON('[["a", "b"], ["c", "d"]]'));
```

结果：

```
["a", "b", "c", "d"]
```