---
title: IS_NULL_VALUE
summary: 检查输入值是否为 JSON `null`。请注意，此函数检查的是 JSON `null`，而不是 SQL NULL。要检查某个值是否为 SQL NULL，请使用 IS_NULL。
---

# IS_NULL_VALUE

检查输入值是否为 JSON `null`。请注意，此函数检查的是 JSON `null`，而不是 SQL NULL。要检查某个值是否为 SQL NULL，请使用 [IS_NULL](/tidb-cloud-lake/sql/is-null.md)。

```json title='JSON null Example:'
{
  "name": "John",
  "age": null
}
```

## 语法 {#syntax}

```sql
IS_NULL_VALUE( <expr> )
```

## 返回类型 {#return-type}

如果输入值是 JSON `null`，则返回 `true`；否则返回 `false`。

## 示例 {#examples}

```sql
SELECT
  IS_NULL_VALUE(PARSE_JSON('{"name":"John", "age":null}') :age), --JSON null
  IS_NULL(NULL); --SQL NULL

┌──────────────────────────────────────────────────────────────────────────────┐
│ is_null_value(parse_json('{"name":"john", "age":null}'):age) │ is_null(null) │
├──────────────────────────────────────────────────────────────┼───────────────┤
│ true                                                         │ true          │
└──────────────────────────────────────────────────────────────────────────────┘
```