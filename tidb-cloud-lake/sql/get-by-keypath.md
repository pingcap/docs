---
title: GET_BY_KEYPATH
title_includes: GET_BY_KEYPATH_STRING
---

Extracts a nested value from a `VARIANT` using a **key path** string. `GET_BY_KEYPATH` returns the result as `VARIANT`, while `GET_BY_KEYPATH_STRING` returns a `STRING`.

Key paths follow the Postgres-style braces syntax: each segment is wrapped in `{}` and segments are separated by commas, for example `'{user,profile,name}'`. Array indexes can be specified as numbers, e.g. `'{items,0}'`.

## Syntax

```sql
GET_BY_KEYPATH(<variant>, <keypath>)
GET_BY_KEYPATH_STRING(<variant>, <keypath>)
```

## Return Type

- `GET_BY_KEYPATH`: `VARIANT`
- `GET_BY_KEYPATH_STRING`: `STRING`

## Examples

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

If the key path cannot be resolved, both functions return `NULL`.
