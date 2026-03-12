---
title: CEIL
---

Rounds the number up.

## Syntax

```sql
CEIL( <x> )
```

## Aliases

- [CEILING](ceiling.md)

## Examples

```sql
SELECT CEILING(-1.23), CEIL(-1.23);

┌────────────────────────────────────┐
│ ceiling((- 1.23)) │ ceil((- 1.23)) │
├───────────────────┼────────────────┤
│                -1 │             -1 │
└────────────────────────────────────┘
```