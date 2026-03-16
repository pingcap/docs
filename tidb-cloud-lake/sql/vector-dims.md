---
title: 'VECTOR_DIMS'
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.780"/>

Returns the dimensionality (number of elements) of a vector.

## Syntax

```sql
VECTOR_DIMS(vector)
```

## Arguments

- `vector`: Input vector (VECTOR Data Type)

## Returns

Returns a INT value representing the number of dimensions (elements) in the vector.

## Description

The `VECTOR_DIMS` function returns the dimensionality of a vector, which is the number of elements it contains. This function is useful for:

- Validating vector dimensions before performing operations
- Dynamic vector processing where dimension information is needed
- Debugging and data exploration with vector data
- Ensuring compatibility between vectors in calculations

:::info
This function performs vector computations within Databend and does not rely on external APIs.
:::

## Examples

```sql
SELECT 
    VECTOR_DIMS([1,2]::VECTOR(2)) AS dims_2d,
    VECTOR_DIMS([1,2,3]::VECTOR(3)) AS dims_3d,
    VECTOR_DIMS([1,2,3,4,5]::VECTOR(5)) AS dims_5d;
```

Result:
```
┌─────────┬─────────┬─────────┐
│ dims_2d │ dims_3d │ dims_5d │
├─────────┼─────────┼─────────┤
│       2 │       3 │       5 │
└─────────┴─────────┴─────────┘
```
