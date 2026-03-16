---
title: TO_YYYYMMDDHH
---

Formats a given date or timestamp into a string representation in the format "YYYYMMDDHH" (Year, Month, Day, Hour).

## Syntax

```sql
TO_YYYYMMDDHH(<expr>)
```

## Arguments

| Arguments | Description                   |
|-----------|-------------------------------|
| `<expr>`  | date/datetime，date as default|

## Return Type

Returns an unsigned 64-bit integer (UInt64) in the format "YYYYMMDDHH".

## Examples

```sql
SELECT to_yyyymmddhh('2023-11-12 09:38:18.165575'), to_yyyymmddhh(to_date('2023-11-12 09:38:18.165575'));
┌─────────────────────────────────────────────┐─────────────────────────────────────────────────────┐
│ to_yyyymmddhh('2023-11-12 09:38:18.165575') │to_yyyymmddhh(to_date('2023-11-12 09:38:18.165575')  │
│                    UInt32                   │                    UInt32                           │
├─────────────────────────────────────────────┤─────────────────────────────────────────────────────┤
│                    2023111200               │                 2023111200                          │    
└─────────────────────────────────────────────┘─────────────────────────────────────────────────────┘

SELECT to_yyyymmddhh(to_timestamp('2023-11-12 09:38:18.165575'));

┌───────────────────────────────────────────────────────────┐
│ to_yyyymmddhh(to_timestamp('2023-11-12 09:38:18.165575')) │
│                    UInt32                                 │  
├───────────────────────────────────────────────────────────┤
│                    2023111209                             │     
└───────────────────────────────────────────────────────────┘

```
