---
title: ARRAY_SIZE
title_includes: ARRAY_LENGTH
---

Returns the length of an array, counting `NULL` elements.

Alias: `ARRAY_LENGTH`

## Syntax

```sql
ARRAY_SIZE(<array>)
```

## Return Type

`BIGINT`

## Examples

```sql
SELECT ARRAY_SIZE([1, 2, 3]) AS size_plain;

┌──────────┐
│ size_plain │
├──────────┤
│        3 │
└──────────┘
```

```sql
SELECT ARRAY_SIZE([1, NULL, 3]) AS size_with_null;

┌──────────────┐
│ size_with_null│
├──────────────┤
│            3 │
└──────────────┘
```
