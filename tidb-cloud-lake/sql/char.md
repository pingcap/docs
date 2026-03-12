---
id: string-char
title: CHAR
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.752"/>


Returns the character(s) for each integer passed. The function converts each integer to its corresponding Unicode character.

## Syntax

```sql
CHAR(N, ...)
CHR(N)
```

## Arguments

| Arguments | Description                                                    |
|-----------|----------------------------------------------------------------|
| N         | Integer value(s) representing Unicode code points (0 to 2^32-1) |

## Return Type

`STRING`

## Remarks

- Accepts any integer type (auto-casts to Int64).
- Returns empty string ('') and logs an error for invalid code points.
- `chr` is an alias for `char`.
- NULL inputs result in NULL output.

## Examples

```sql
-- Basic usage
SELECT CHAR(65, 66, 67);
┌───────┐
│ char  │
│ String│
├───────┤
│ ABC   │
└───────┘

-- Using the CHR alias
SELECT CHR(68);
┌───────┐
│ chr   │
│ String│
├───────┤
│ D     │
└───────┘

-- Creating a string from multiple code points
SELECT CHAR(77,121,83,81,76);
┌───────┐
│ char  │
│ String│
├───────┤
│ MySQL │
└───────┘

-- Auto-casting from different integer types
SELECT CHAR(CAST(65 AS UInt16));
┌───────┐
│ char  │
│ String│
├───────┤
│ A     │
└───────┘

-- NULL handling
SELECT CHAR(NULL);
┌───────┐
│ char  │
│ String│
├───────┤
│ NULL  │
└───────┘
```
