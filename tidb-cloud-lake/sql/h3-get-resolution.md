---
title: H3_GET_RESOLUTION
summary: Returns the resolution of the given H3 index.
---
Returns the resolution of the given [H3](https://eng.uber.com/h3/) index. 

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