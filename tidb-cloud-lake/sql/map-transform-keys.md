---
title: MAP_TRANSFORM_KEYS
summary: 使用 [lambda 表达式](/tidb-cloud-lake/sql/stored-procedure-scripting.md#lambda-expressions) 对 JSON 对象中的每个键应用转换。
---

# MAP_TRANSFORM_KEYS

使用 [lambda 表达式](/tidb-cloud-lake/sql/stored-procedure-scripting.md#lambda-expressions) 对 JSON 对象中的每个键应用转换。

## 语法 {#syntax}

```sql
MAP_TRANSFORM_KEYS(<json_object>, (<key>, <value>) -> <key_transformation>)
```

## 返回类型 {#return-type}

返回一个 JSON 对象，其值与输入 JSON 对象相同，但键会根据指定的 lambda 转换进行修改。

## 示例 {#examples}

以下示例为每个键追加 `"_v1"`，从而创建一个键已修改的新 JSON 对象：

```sql
SELECT MAP_TRANSFORM_KEYS('{"name":"John", "role":"admin"}'::VARIANT, (k, v) -> CONCAT(k, '_v1')) AS versioned_metadata;

┌──────────────────────────────────────┐
│          versioned_metadata          │
├──────────────────────────────────────┤
│ {"name_v1":"John","role_v1":"admin"} │
└──────────────────────────────────────┘
```