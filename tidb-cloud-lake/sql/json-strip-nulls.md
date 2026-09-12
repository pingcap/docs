---
title: JSON_STRIP_NULLS
summary: 从 JSON 对象中移除所有值为 null 的属性。
---

# JSON_STRIP_NULLS

从 JSON 对象中移除所有值为 null 的属性。

## 语法 {#syntax}

```sql
JSON_STRIP_NULLS(<variant_expr>)
```

## 参数 {#arguments}

一个 VARIANT 类型的表达式。

## 返回类型 {#return-type}

VARIANT。

## 示例 {#examples}

```sql
SELECT JSON_STRIP_NULLS(PARSE_JSON('{"name": "Alice", "age": 30, "city": null}')) AS value;

╭───────────────────────────╮
│           value           │
├───────────────────────────┤
│ {"age":30,"name":"Alice"} │
╰───────────────────────────╯
```