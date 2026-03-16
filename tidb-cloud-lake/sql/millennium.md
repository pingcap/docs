---
title: MILLENNIUM
---

Returns the millennium of a given date or timestamp. The 1st millennium spans years 0001–1000, the 2nd spans 1001–2000, the 3rd spans 2001–3000, and so on.

## Syntax

```sql
MILLENNIUM(<date_or_timestamp>)
```

## Return Type

UInt8 — the millennium number starting from 1.

## Examples

```sql
SELECT
  MILLENNIUM('1992-02-15')       AS millennium_1992,
  MILLENNIUM('2025-04-16 12:34:56')    AS millennium_2025;
```

```sql
┌───────────────────────────────────┐
│ millennium_1992 │ millennium_2025 │
├─────────────────┼─────────────────┤
│               2 │               3 │
└───────────────────────────────────┘
```