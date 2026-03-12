---
title: TRIM
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.694"/>

Removes spaces, specific characters, or substrings from the start, end, or both sides of a string.

See also: [TRIM_BOTH](trim-both.md)

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

This example removes all occurrences of the specified characters from both the beginning and end of the string 'xxxdatabendxxx':

```sql
SELECT TRIM(BOTH 'xxx' FROM 'xxxdatabendxxx'), TRIM(BOTH 'xx' FROM 'xxxdatabendxxx'), TRIM(BOTH 'x' FROM 'xxxdatabendxxx');

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ TRIM(BOTH 'xxx' FROM 'xxxdatabendxxx') │ TRIM(BOTH 'xx' FROM 'xxxdatabendxxx') │ TRIM(BOTH 'x' FROM 'xxxdatabendxxx') │
├────────────────────────────────────────┼───────────────────────────────────────┼──────────────────────────────────────┤
│ databend                               │ xdatabendx                            │ databend                             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

This example removes all occurrences of the specified characters from the beginning of the input string 'xxxdatabend':

```sql
SELECT TRIM(LEADING 'xxx' FROM 'xxxdatabend'), TRIM(LEADING 'xx' FROM 'xxxdatabend'), TRIM(LEADING 'x' FROM 'xxxdatabend');

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ TRIM(LEADING 'xxx' FROM 'xxxdatabend') │ TRIM(LEADING 'xx' FROM 'xxxdatabend') │ TRIM(LEADING 'x' FROM 'xxxdatabend') │
├────────────────────────────────────────┼───────────────────────────────────────┼──────────────────────────────────────┤
│ databend                               │ xdatabend                             │ databend                             │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

This example removes all occurrences of the specified characters from the end of the input string 'databendxxx':

```sql
SELECT TRIM(TRAILING 'xxx' FROM 'databendxxx' ), TRIM(TRAILING 'xx' FROM 'databendxxx' ), TRIM(TRAILING 'x' FROM 'databendxxx' );

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ TRIM(TRAILING 'xxx' FROM 'databendxxx') │ TRIM(TRAILING 'xx' FROM 'databendxxx') │ TRIM(TRAILING 'x' FROM 'databendxxx') │
├─────────────────────────────────────────┼────────────────────────────────────────┼───────────────────────────────────────┤
│ databend                                │ databendx                              │ databend                              │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

This example treats each character in the trim string individually and removes any matching characters from both the beginning and the end of the input string:

```sql
SELECT TRIM('xxxdatabendxxx', 'xyz'), TRIM('xxxdatabendxxx', 'xy'), TRIM('xxxdatabendxxx', 'x');

┌────────────────────────────────────────────────────────────────────────────────────────────┐
│ trim('xxxdatabendxxx', 'xyz') │ trim('xxxdatabendxxx', 'xy') │ trim('xxxdatabendxxx', 'x') │
├───────────────────────────────┼──────────────────────────────┼─────────────────────────────┤
│ databend                      │ databend                     │ databend                    │
└────────────────────────────────────────────────────────────────────────────────────────────┘
```

This example removes the leading and/or trailing spaces:

```sql
SELECT TRIM('   databend   '), TRIM('   databend'), TRIM('databend   ');

┌────────────────────────────────────────────────────────────────────┐
│ TRIM('   databend   ') │ TRIM('   databend') │ TRIM('databend   ') │
├────────────────────────┼─────────────────────┼─────────────────────┤
│ databend               │ databend            │ databend            │
└────────────────────────────────────────────────────────────────────┘
```