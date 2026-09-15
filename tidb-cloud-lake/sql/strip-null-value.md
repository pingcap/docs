---
title: STRIP_NULL_VALUE
summary: 将 JSON null 值转换为 SQL NULL 值。所有其他 variant 值均保持不变并直接返回。
---

# STRIP_NULL_VALUE

将 JSON null 值转换为 SQL NULL 值。所有其他 variant 值均保持不变并直接返回。

## 语法 {#syntax}

```sql
STRIP_NULL_VALUE(<variant_expr>)
```

## 参数 {#arguments}

一个 VARIANT 类型的表达式。

## 返回类型 {#return-type}

- 如果该表达式是 JSON null 值，该函数返回 SQL NULL。
- 如果该表达式不是 JSON null 值，该函数返回输入值。

## 示例 {#examples}

```sql
SELECT STRIP_NULL_VALUE(PARSE_JSON('null')) AS value;

╭───────╮
│ value │
├───────┤
│ NULL  │
╰───────╯

SELECT STRIP_NULL_VALUE(PARSE_JSON('{"name": "Alice", "age": 30, "city": null}')) AS value;

╭───────────────────────────────────────╮
│                 value                 │
├───────────────────────────────────────┤
│ {"age":30,"city":null,"name":"Alice"} │
╰───────────────────────────────────────╯
```