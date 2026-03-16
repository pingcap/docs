---
title: H3_TO_GEO
---

Returns the longitude and latitude corresponding to the given [H3](https://eng.uber.com/h3/) index. 

## Syntax

```sql
H3_TO_GEO(h3)
```

## Examples

```sql
SELECT H3_TO_GEO(644325524701193974);

┌────────────────────────────────────────┐
│      h3_to_geo(644325524701193974)     │
├────────────────────────────────────────┤
│ (37.79506616830255,55.712902431456676) │
└────────────────────────────────────────┘
```