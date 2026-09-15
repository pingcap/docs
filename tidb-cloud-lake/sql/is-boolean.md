---
title: IS_BOOLEAN
summary: 检查输入的 JSON 值是否为布尔值。
---

# IS_BOOLEAN

检查输入的 JSON 值是否为布尔值。

## 语法 {#syntax}

```sql
IS_BOOLEAN( <expr> )
```

## 返回类型 {#return-type}

如果输入的 JSON 值是布尔值，则返回 `true`；否则返回 `false`。

## 示例 {#examples}

```sql
SELECT
  IS_BOOLEAN(PARSE_JSON('true')),
  IS_BOOLEAN(PARSE_JSON('[1,2,3]'));

┌────────────────────────────────────────────────────────────────────┐
│ is_boolean(parse_json('true')) │ is_boolean(parse_json('[1,2,3]')) │
├────────────────────────────────┼───────────────────────────────────┤
│ true                           │ false                             │
└────────────────────────────────────────────────────────────────────┘
```