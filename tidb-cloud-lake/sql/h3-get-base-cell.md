---
title: H3_GET_BASE_CELL
summary: Returns the base cell number of the given H3 index.
---

# H3_GET_BASE_CELL

Returns the base cell number of the given [H3](https://h3geo.org/) index.

## Syntax

```sql
H3_GET_BASE_CELL(h3)
```

## Examples

```sql
SELECT H3_GET_BASE_CELL(644325524701193974);

┌──────────────────────────────────────┐
│ h3_get_base_cell(644325524701193974) │
├──────────────────────────────────────┤
│                                    8 │
└──────────────────────────────────────┘
```
