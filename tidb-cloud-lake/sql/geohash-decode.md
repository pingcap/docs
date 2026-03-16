---
title: GEOHASH_DECODE
---

Converts a [Geohash](https://en.wikipedia.org/wiki/Geohash)-encoded string into latitude/longitude coordinates.

## Syntax

```sql
GEOHASH_DECODE('<geohashed-string\>')
```

## Examples

```sql
SELECT GEOHASH_DECODE('ezs42');

┌─────────────────────────────────┐
│     geohash_decode('ezs42')     │
├─────────────────────────────────┤
│ (-5.60302734375,42.60498046875) │
└─────────────────────────────────┘
```