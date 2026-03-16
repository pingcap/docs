---
title: ARRAYS_ZIP
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.690"/>

Merges multiple arrays into a single array tuple.

## Syntax

```sql
ARRAYS_ZIP( <array1> [, ...] )
```

## Arguments

| Arguments  | Description       |
|------------|-------------------|
| `<arrayN>` | The input ARRAYs. |

:::note
- The length of each array must be the same.
:::

## Return Type

Array(Tuple).

## Examples

```sql
SELECT ARRAYS_ZIP([1, 2, 3], ['a', 'b', 'c']);
┌────────────────────────────────────────┐
│ arrays_zip([1, 2, 3], ['a', 'b', 'c']) │
├────────────────────────────────────────┤
│ [(1,'a'),(2,'b'),(3,'c')]              │
└────────────────────────────────────────┘
```
