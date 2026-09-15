---
title: IS_OBJECT
summary: 检查输入值是否为 JSON 对象。
---

# IS_OBJECT

检查输入值是否为 JSON 对象。

## 语法 {#syntax}

```sql
IS_OBJECT( <expr> )
```

## 返回类型 {#return-type}

如果输入的 JSON 值是 JSON 对象，则返回 `true`；否则返回 `false`。

## 示例 {#examples}

```sql
SELECT
  IS_OBJECT(PARSE_JSON('{"a":"b"}')), -- JSON Object
  IS_OBJECT(PARSE_JSON('["a","b","c"]')); --JSON Array

┌─────────────────────────────────────────────────────────────────────────────┐
│ is_object(parse_json('{"a":"b"}')) │ is_object(parse_json('["a","b","c"]')) │
├────────────────────────────────────┼────────────────────────────────────────┤
│ true                               │ false                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```