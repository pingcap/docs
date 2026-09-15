---
title: IS_FLOAT
summary: 检查输入的 JSON 值是否为 float。
---

# IS_FLOAT

检查输入的 JSON 值是否为 float。

## 语法 {#syntax}

```sql
IS_FLOAT( <expr> )
```

## 返回类型 {#return-type}

如果输入的 JSON 值是 float，则返回 `true`；否则返回 `false`。

## 示例 {#examples}

```sql
SELECT
  IS_FLOAT(PARSE_JSON('1.23')),
  IS_FLOAT(PARSE_JSON('[1,2,3]'));

┌────────────────────────────────────────────────────────────────┐
│ is_float(parse_json('1.23')) │ is_float(parse_json('[1,2,3]')) │
├──────────────────────────────┼─────────────────────────────────┤
│ true                         │ false                           │
└────────────────────────────────────────────────────────────────┘
```