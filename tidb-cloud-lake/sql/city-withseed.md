---
title: CITY64WITHSEED
---

Calculates a City64WithSeed 64-bit hash for a string.

## Syntax

```sql
CITY64WITHSEED(<expr1>, <expr2>)
```

## Examples

```sql
SELECT CITY64WITHSEED('1234567890', 12);

┌──────────────────────────────────┐
│ city64withseed('1234567890', 12) │
├──────────────────────────────────┤
│             10660895976650300430 │
└──────────────────────────────────┘
```