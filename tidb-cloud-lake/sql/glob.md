---
title: GLOB
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.714"/>

Performs case-sensitive pattern matching using wildcard characters:  

- `?` matches any single character.
- `*` matches zero or more characters.

## Syntax

```sql
GLOB(<string>, <pattern>)
```

## Return Type

Returns BOOLEAN: `true` if the input string matches the pattern, `false` otherwise.

## Examples

```sql
SELECT
    GLOB('abc', 'a?c'),
    GLOB('abc', 'a*d'),
    GLOB('abc', 'abc'),
    GLOB('abc', 'abcd'),
    GLOB('abcdef', 'a?c*'),
    GLOB('hello', 'h*l');;

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ glob('abc', 'a?c') │ glob('abc', 'a*d') │ glob('abc', 'abc') │ glob('abc', 'abcd') │ glob('abcdef', 'a?c*') │ glob('hello', 'h*l') │
├────────────────────┼────────────────────┼────────────────────┼─────────────────────┼────────────────────────┼──────────────────────┤
│ true               │ false              │ true               │ false               │ true                   │ false                │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```