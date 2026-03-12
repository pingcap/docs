---
title: YEARWEEK
---

Returns the year and week number in `YYYYWW` format, according to ISO week date. Week 1 is the week with the first Thursday of the year.

## Syntax

```sql
YEARWEEK(<date_or_timestamp>)
```

## Return Type

UInt32.

## Examples

```sql
SELECT
  YEARWEEK('2024-01-01') AS yw1,
  YEARWEEK('2024-12-31') AS yw2;   
```

```sql
┌─────────────────┐
│   yw1  │   yw2  │
├────────┼────────┤
│ 202401 │ 202501 │
└─────────────────┘
```