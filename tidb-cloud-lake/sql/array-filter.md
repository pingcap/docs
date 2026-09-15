---
title: ARRAY_FILTER
summary: 根据指定的 Lambda 表达式从 JSON 数组中过滤元素，仅返回满足条件的元素。有关 Lambda 表达式的更多信息，请参见 Lambda Expressions。
---

# ARRAY_FILTER

根据指定的 Lambda 表达式从 JSON 数组中过滤元素，仅返回满足条件的元素。有关 Lambda 表达式的更多信息，请参见 [Lambda 表达式](/tidb-cloud-lake/sql/stored-procedure-scripting.md#lambda-expressions)。

## 语法 {#syntax}

```sql
ARRAY_FILTER(<json_array>, <lambda_expression>)
```

## 返回类型 {#return-type}

JSON 数组。

## 示例 {#examples}

以下示例对数组进行过滤，仅返回以字母 `a` 开头的字符串，结果为 `["apple", "avocado"]`：

```sql
SELECT ARRAY_FILTER(
    ['apple', 'banana', 'avocado', 'grape'],
    d -> d::String LIKE 'a%'
);

-[ RECORD 1 ]-----------------------------------
array_filter(['apple', 'banana', 'avocado', 'grape'], d -> d::STRING LIKE 'a%'): ["apple","avocado"]
```