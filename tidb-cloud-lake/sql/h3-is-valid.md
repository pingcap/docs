---
title: H3_IS_VALID
---

Checks if the given [H3](https://eng.uber.com/h3/) index is valid.

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