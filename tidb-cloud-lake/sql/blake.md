---
title: BLAKE3
---

Calculates a BLAKE3 256-bit checksum for a string. The value is returned as a string of 64 hexadecimal digits or NULL if the argument was NULL.

## Syntax

```sql
BLAKE3(<expr>)
```

## Examples

```sql
SELECT BLAKE3('1234567890');

┌──────────────────────────────────────────────────────────────────┐
│                       blake3('1234567890')                       │
├──────────────────────────────────────────────────────────────────┤
│ d12e417e04494572b561ba2c12c3d7f9e5107c4747e27b9a8a54f8480c63e841 │
└──────────────────────────────────────────────────────────────────┘
```