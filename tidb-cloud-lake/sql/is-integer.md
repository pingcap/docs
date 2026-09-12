---
title: IS_INTEGER
summary: 检查输入的 JSON 值是否为整数。
---

# IS_INTEGER

检查输入的 JSON 值是否为整数。

## 语法 {#syntax}

```sql
IS_INTEGER( <expr> )
```

## 返回类型 {#return-type}

如果输入的 JSON 值是整数，则返回 `true`；否则返回 `false`。

## 示例 {#examples}

```sql
SELECT
  IS_INTEGER(PARSE_JSON('123')),
  IS_INTEGER(PARSE_JSON('[1,2,3]'));

┌───────────────────────────────────────────────────────────────────┐
│ is_integer(parse_json('123')) │ is_integer(parse_json('[1,2,3]')) │
├───────────────────────────────┼───────────────────────────────────┤
│ true                          │ false                             │
└───────────────────────────────────────────────────────────────────┘
```