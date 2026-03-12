---
title: SIPHASH64
---

Produces a 64-bit [SipHash](https://en.wikipedia.org/wiki/SipHash) hash value.

## Syntax

```sql
SIPHASH64(<expr>)
```

## Aliases

- [SIPHASH](siphash.md)

## Examples

```sql
SELECT SIPHASH('1234567890'), SIPHASH64('1234567890');

┌─────────────────────────────────────────────────┐
│ siphash('1234567890') │ siphash64('1234567890') │
├───────────────────────┼─────────────────────────┤
│  18110648197875983073 │    18110648197875983073 │
└─────────────────────────────────────────────────┘
```