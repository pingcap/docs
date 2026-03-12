---
title: JSON_EXISTS_KEY
title_includes: JSON_EXISTS_ANY_KEYS, JSON_EXISTS_ALL_KEYS
---

Checks whether a JSON object contains one or more keys.

- `JSON_EXISTS_KEY` tests a single key.
- `JSON_EXISTS_ANY_KEYS` accepts an array of keys and returns `TRUE` when at least one key exists.
- `JSON_EXISTS_ALL_KEYS` returns `TRUE` only when every key in the array exists.

## Syntax

```sql
JSON_EXISTS_KEY(<variant>, <key>)
JSON_EXISTS_ANY_KEYS(<variant>, <array_of_keys>)
JSON_EXISTS_ALL_KEYS(<variant>, <array_of_keys>)
```

## Return Type

`BOOLEAN`

## Examples

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
