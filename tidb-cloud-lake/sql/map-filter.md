---
title: MAP_FILTER
summary: 根据使用 [lambda 表达式](/tidb-cloud-lake/sql/stored-procedure-scripting.md#lambda-expressions) 定义的指定条件，过滤 JSON 对象中的键值对。
---

# MAP_FILTER

根据使用 [lambda 表达式](/tidb-cloud-lake/sql/stored-procedure-scripting.md#lambda-expressions) 定义的指定条件，过滤 JSON 对象中的键值对。

## 语法 {#syntax}

```sql
MAP_FILTER(<json_object>, (<key>, <value>) -> <condition>)
```

## 返回类型 {#return-type}

返回一个仅包含满足指定条件的键值对的 JSON 对象。

## 示例 {#examples}

以下示例从 JSON 对象中仅提取 `"status": "active"` 这一键值对，并过滤掉其他字段：

```sql
SELECT MAP_FILTER('{"status":"active", "user":"admin", "time":"2024-11-01"}'::VARIANT, (k, v) -> k = 'status') AS filtered_metadata;

┌─────────────────────┐
│  filtered_metadata  │
├─────────────────────┤
│ {"status":"active"} │
└─────────────────────┘
```