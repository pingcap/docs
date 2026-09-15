---
title: ARRAY_REDUCE
summary: 通过应用指定的 Lambda 表达式，将 JSON 数组归约为单个值。有关 Lambda 表达式的更多信息，请参见 Lambda Expressions。
---

# ARRAY_REDUCE

通过应用指定的 Lambda 表达式，将 JSON 数组归约为单个值。有关 Lambda 表达式的更多信息，请参见 [Lambda 表达式](/tidb-cloud-lake/sql/stored-procedure-scripting.md#lambda-expressions)。

## 语法 {#syntax}

```sql
ARRAY_REDUCE(<json_array>, <lambda_expression>)
```

## 示例 {#examples}

以下示例将数组中的所有元素相乘（2 _3_ 4）：

```sql
SELECT ARRAY_REDUCE(
    [2, 3, 4],
    (acc, d) -> acc::Int * d::Int
);

-[ RECORD 1 ]-----------------------------------
array_reduce([2, 3, 4], (acc, d) -> acc::Int32 * d::Int32): 24
```