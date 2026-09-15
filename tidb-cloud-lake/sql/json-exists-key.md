---
title: JSON_EXISTS_KEY
summary: 检查 JSON 对象是否包含一个或多个键。
---

# JSON_EXISTS_KEY

检查 JSON 对象是否包含一个或多个键。

- `JSON_EXISTS_KEY` 测试单个键。
- `JSON_EXISTS_ANY_KEYS` 接受一个键数组，并在至少存在一个键时返回 `TRUE`。
- `JSON_EXISTS_ALL_KEYS` 仅在数组中的每个键都存在时返回 `TRUE`。

## 语法 {#syntax}

```sql
JSON_EXISTS_KEY(<variant>, <key>)
JSON_EXISTS_ANY_KEYS(<variant>, <array_of_keys>)
JSON_EXISTS_ALL_KEYS(<variant>, <array_of_keys>)
```

## 返回类型 {#return-type}

`BOOLEAN`

## 示例 {#examples}

```sql
SELECT JSON_EXISTS_KEY(PARSE_JSON('{"a":1,"b":2}'), 'b') AS has_b;

┌──────┐
│ has_b│
├──────┤
│ true │
└──────┘
```

```sql
SELECT JSON_EXISTS_ANY_KEYS(PARSE_JSON('{"a":1,"b":2}'), ['x','b']) AS any_key;

┌────────┐
│ any_key│
├────────┤
│ true   │
└────────┘
```

```sql
SELECT JSON_EXISTS_ALL_KEYS(PARSE_JSON('{"a":1,"b":2}'), ['a','b','c']) AS all_keys;

┌────────┐
│ all_keys│
├────────┤
│ false  │
└────────┘
```

```sql
SELECT JSON_EXISTS_ALL_KEYS(PARSE_JSON('{"a":1,"b":2}'), ['a','b']) AS all_keys;

┌────────┐
│ all_keys│
├────────┤
│ true   │
└────────┘
```