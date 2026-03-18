---
title: CRC32
summary: Returns the CRC32 checksum of x, where 'x' is expected to be a string and (if possible) is treated as one if it is not.
---
Returns the CRC32 checksum of `x`, where 'x' is expected to be a string and (if possible) is treated as one if it is not.

## Syntax

```sql
CRC32( '<x>' )
```

## Examples

```sql
SELECT CRC32('databend');

┌───────────────────┐
│ crc32('databend') │
├───────────────────┤
│        1177678456 │
└───────────────────┘
```