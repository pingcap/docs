---
title: GET_BY_KEYPATH
summary: 使用 **key path** 字符串从 `VARIANT` 中提取嵌套值。`GET_BY_KEYPATH` 以 `VARIANT` 返回结果，而 `GET_BY_KEYPATH_STRING` 返回 `STRING`。
---

# GET_BY_KEYPATH

使用 **key path** 字符串从 `VARIANT` 中提取嵌套值。`GET_BY_KEYPATH` 以 `VARIANT` 返回结果，而 `GET_BY_KEYPATH_STRING` 返回 `STRING`。

key path 遵循 Postgres 风格的大括号语法：每个段都用 `{}` 包裹，段与段之间用逗号分隔，例如 `'{user,profile,name}'`。数组索引可以用数字指定，例如 `'{items,0}'`。

## 语法 {#syntax}

```sql
GET_BY_KEYPATH(<variant>, <keypath>)
GET_BY_KEYPATH_STRING(<variant>, <keypath>)
```

## 返回类型 {#return-type}

- `GET_BY_KEYPATH`: `VARIANT`
- `GET_BY_KEYPATH_STRING`: `STRING`

## 示例 {#examples}

```sql
SELECT GET_BY_KEYPATH(PARSE_JSON('{"user":{"name":"Ada","tags":["a","b"]}}'), '{user,name}') AS profile_name;

┌──────────────┐
│ profile_name │
├──────────────┤
│ "Ada"        │
└──────────────┘
```

```sql
SELECT GET_BY_KEYPATH(PARSE_JSON('[10, {"a":{"k1":[1,2,3]}}]'), '{1,a,k1}') AS inner_array;

┌─────────────┐
│ inner_array │
├─────────────┤
│ [1,2,3]     │
└─────────────┘
```

```sql
SELECT GET_BY_KEYPATH_STRING(PARSE_JSON('{"user":{"name":"Ada"}}'), '{user,name}') AS name_text;

┌──────────┐
│ name_text│
├──────────┤
│ Ada      │
└──────────┘
```

```sql
SELECT GET_BY_KEYPATH_STRING(PARSE_JSON('[10, {"scores":[100,98]}]'), '{1,scores,0}') AS first_score;

┌──────────────┐
│ first_score  │
├──────────────┤
│ 100          │
└──────────────┘
```

如果 key path 无法解析，这两个函数都返回 `NULL`。