---
title: TRIM
summary: Removes spaces, specific characters, or substrings from the start, end, or both sides of a string.
---

# TRIM

Removes spaces, specific characters, or substrings from the start, end, or both sides of a string.

See also: [TRIM_BOTH](/tidb-cloud-lake/sql/trim-both.md)

## Syntax

```sql
-- Remove all occurrences of the specified trim string from the beginning, end, or both sides of the string
TRIM({ BOTH | LEADING | TRAILING } <trim_string> FROM <string>)

-- Remove all leading and trailing occurrences of any character present in the specified trim string
TRIM(<string>, <trim_string>)

-- Trim spaces from both sides
TRIM(<string>)
```

## Examples

This example removes all occurrences of the specified characters from both the beginning and end of the string 'xxxdatalakexxx':

```sql
SELECT TRIM(BOTH 'xxx' FROM 'xxxdatalakexxx'), TRIM(BOTH 'xx' FROM 'xxxdatalakexxx'), TRIM(BOTH 'x' FROM 'xxxdatalakexxx');

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ TRIM(BOTH 'xxx' FROM 'xxxdatalakexxx') │ TRIM(BOTH 'xx' FROM 'xxxdatalakexxx') │ TRIM(BOTH 'x' FROM 'xxxdatalakexxx') │
├────────────────────────────────────────┼───────────────────────────────────────┼──────────────────────────────────────┤
│ datalake                               │ xdatalakex                            │ datalake                             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

This example removes all occurrences of the specified characters from the beginning of the input string 'xxxdatalake':

```sql
SELECT TRIM(LEADING 'xxx' FROM 'xxxdatalake'), TRIM(LEADING 'xx' FROM 'xxxdatalake'), TRIM(LEADING 'x' FROM 'xxxdatalake');

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ TRIM(LEADING 'xxx' FROM 'xxxdatalake') │ TRIM(LEADING 'xx' FROM 'xxxdatalake') │ TRIM(LEADING 'x' FROM 'xxxdatalake') │
├────────────────────────────────────────┼───────────────────────────────────────┼──────────────────────────────────────┤
│ datalake                               │ xdatalake                             │ datalake                             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

This example removes all occurrences of the specified characters from the end of the input string 'datalakexxx':

```sql
SELECT TRIM(TRAILING 'xxx' FROM 'datalakexxx' ), TRIM(TRAILING 'xx' FROM 'datalakexxx' ), TRIM(TRAILING 'x' FROM 'datalakexxx' );

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ TRIM(TRAILING 'xxx' FROM 'datalakexxx') │ TRIM(TRAILING 'xx' FROM 'datalakexxx') │ TRIM(TRAILING 'x' FROM 'datalakexxx') │
├─────────────────────────────────────────┼────────────────────────────────────────┼───────────────────────────────────────┤
│ datalake                                │ datalakex                              │ datalake                              │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

This example treats each character in the trim string individually and removes any matching characters from both the beginning and the end of the input string:

```sql
SELECT TRIM('xxxdatalakexxx', 'xyz'), TRIM('xxxdatalakexxx', 'xy'), TRIM('xxxdatalakexxx', 'x');

┌────────────────────────────────────────────────────────────────────────────────────────────┐
│ trim('xxxdatalakexxx', 'xyz') │ trim('xxxdatalakexxx', 'xy') │ trim('xxxdatalakexxx', 'x') │
├───────────────────────────────┼──────────────────────────────┼─────────────────────────────┤
│ datalake                      │ datalake                     │ datalake                    │
└────────────────────────────────────────────────────────────────────────────────────────────┘
```

This example removes the leading and/or trailing spaces:

```sql
SELECT TRIM('   datalake   '), TRIM('   datalake'), TRIM('datalake   ');

┌────────────────────────────────────────────────────────────────────┐
│ TRIM('   datalake   ') │ TRIM('   datalake') │ TRIM('datalake   ') │
├────────────────────────┼─────────────────────┼─────────────────────┤
│ datalake               │ datalake            │ datalake            │
└────────────────────────────────────────────────────────────────────┘
```
