---
title: H3_IS_VALID
summary: Checks if the given H3 index is valid.
---

# H3_IS_VALID

Checks if the given [H3](https://h3geo.org/) index is valid.

## Syntax

```sql
H3_IS_VALID(h3)
```

## Examples

```sql
SELECT H3_IS_VALID(644325524701193974);

┌─────────────────────────────────┐
│ h3_is_valid(644325524701193974) │
├─────────────────────────────────┤
│ true                            │
└─────────────────────────────────┘
```
