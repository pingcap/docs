---
title: H3_GET_RESOLUTION
summary: Returns the resolution of the given H3 index.
---

# H3_GET_RESOLUTION

Returns the resolution of the given [H3](https://h3geo.org/) index.

## Syntax

```sql
H3_GET_RESOLUTION(h3)
```

## Examples

```sql
SELECT H3_GET_RESOLUTION(644325524701193974);

┌───────────────────────────────────────┐
│ h3_get_resolution(644325524701193974) │
├───────────────────────────────────────┤
│                                    15 │
└───────────────────────────────────────┘
```
