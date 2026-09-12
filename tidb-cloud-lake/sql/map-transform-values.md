---
title: MAP_TRANSFORM_VALUES
summary: 使用 [Lambda 表达式](/tidb-cloud-lake/sql/stored-procedure-scripting.md#lambda-expressions) 对 JSON 对象中的每个值应用转换。
---

# MAP_TRANSFORM_VALUES

使用 [Lambda 表达式](/tidb-cloud-lake/sql/stored-procedure-scripting.md#lambda-expressions) 对 JSON 对象中的每个值应用转换。

## 语法 {#syntax}

```sql
MAP_TRANSFORM_VALUES(<json_object>, (<key>, <value>) -> <value_transformation>)
```

## 返回类型 {#return-type}

返回一个 JSON 对象，其键与输入的 JSON 对象相同，但值会根据指定的 lambda 转换进行修改。

## 示例 {#examples}

以下示例将每个数值乘以 10，把原始对象转换为 `{"a":10,"b":20}`：

```sql
SELECT MAP_TRANSFORM_VALUES('{"a":1,"b":2}'::VARIANT, (k, v) -> v * 10) AS transformed_values;

┌────────────────────┐
│ transformed_values │
├────────────────────┤
│ {"a":10,"b":20}    │
└────────────────────┘
```