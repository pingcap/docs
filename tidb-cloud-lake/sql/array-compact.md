---
title: ARRAY_COMPACT
summary: 从数组中移除所有 NULL 值。
---

# ARRAY_COMPACT

从数组中移除所有 NULL 值。

## 语法 {#syntax}

```sql
ARRAY_COMPACT(array)
```

## 参数 {#parameters}

| 参数 | 描述 |
|-----------|-------------|
| array     | 要从中移除 NULL 值的数组。 |

## 返回类型 {#return-type}

不包含 NULL 值的数组。

## 注意事项 {#notes}

此函数同时适用于标准数组类型和 variant 数组类型。

## 示例 {#examples}

### 示例 1：从标准数组中移除 NULL 值 {#example-1-removing-nulls-from-a-standard-array}

```sql
SELECT ARRAY_COMPACT([1, NULL, 2, NULL, 3]);
```

结果：

```
[1, 2, 3]
```

### 示例 2：从 variant 数组中移除 NULL 值 {#example-2-removing-nulls-from-a-variant-array}

```sql
SELECT ARRAY_COMPACT(PARSE_JSON('["apple", null, "banana", null, "orange"]'));
```

结果：

```
["apple", "banana", "orange"]
```

### 示例 3：不包含 NULL 值的数组 {#example-3-array-with-no-nulls}

```sql
SELECT ARRAY_COMPACT([1, 2, 3]);
```

结果：

```
[1, 2, 3]
```