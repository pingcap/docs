---
title: JSON_ARRAY_TRANSFORM
summary: 使用指定的转换 Lambda 表达式对 JSON 数组中的每个元素进行转换。有关 Lambda 表达式的更多信息，请参见 Lambda Expressions。
---

# JSON_ARRAY_TRANSFORM

使用指定的转换 Lambda 表达式对 JSON 数组中的每个元素进行转换。有关 Lambda 表达式的更多信息，请参见 [Lambda 表达式](/tidb-cloud-lake/sql/stored-procedure-scripting.md#lambda-expressions)。

## 语法 {#syntax}

```sql
ARRAY_TRANSFORM(<json_array>, <lambda_expression>)
```

## 返回类型 {#return-type}

JSON 数组。

## 示例 {#examples}

在此示例中，数组中的每个数值元素都乘以 10，将原始数组转换为 `[10, 20, 30, 40]`：

```sql
SELECT ARRAY_TRANSFORM(
    [1, 2, 3, 4],
    data -> (data::Int * 10)
);

-[ RECORD 1 ]-----------------------------------
array_transform([1, 2, 3, 4], data -> data::Int32 * 10): [10,20,30,40]
```