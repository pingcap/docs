---
title: IS_NULL_VALUE
summary: Checks whether the input value is a JSON null. Please note that this function examines JSON null, not SQL NULL. To check if a value is SQL NULL, use IS_NULL.
---

# IS_NULL_VALUE

> **Note:**
>
> Introduced or updated in v1.2.368.

Checks whether the input value is a JSON `null`. Please note that this function examines JSON `null`, not SQL NULL. To check if a value is SQL NULL, use [IS_NULL](/tidb-cloud-lake/sql/is-null.md).

```json title='JSON null Example:'
{
  "name": "John",
  "age": null
}
```

## Syntax

```sql
IS_NULL_VALUE( <expr> )
```

## Return Type

Returns `true` if the input value is a JSON `null`, and `false` otherwise.

## Examples

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
