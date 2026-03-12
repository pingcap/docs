---
title: LEFT
---

Returns the leftmost `len` characters from the string `str`, or NULL if any argument is NULL. If `len` is greater than the length of `str`, the entire `str` is returned.

## Syntax

```sql
LEFT(<str>, <len>);
```

## Arguments

| Arguments | Description                                              |
|-----------|----------------------------------------------------------|
| `<str>`   | The main string from where the character to be extracted |
| `<len>`   | The count of characters                                  |

## Return Type

`VARCHAR`

## Examples

```sql
SELECT LEFT('foobarbar', 5), LEFT('foobarbar', 10);

┌──────────────────────────────────────────────┐
│ left('foobarbar', 5) │ left('foobarbar', 10) │
├──────────────────────┼───────────────────────┤
│ fooba                │ foobarbar             │
└──────────────────────────────────────────────┘
```