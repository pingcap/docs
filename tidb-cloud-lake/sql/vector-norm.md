---
title: 'VECTOR_NORM'
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.780"/>

Calculates the L2 norm (Euclidean norm) of a vector, which represents the length or magnitude of the vector.

## Syntax

```sql
VECTOR_NORM(vector)
```

## Arguments

- `vector`: Input vector (VECTOR Data Type)

## Returns

Returns a FLOAT value representing the L2 norm (magnitude) of the vector.

## Description

The `VECTOR_NORM` function calculates the L2 norm (also known as Euclidean norm) of a vector, which represents its length or magnitude in Euclidean space. The function:

1. Squares each element of the vector
2. Sums all the squared values
3. Returns the square root of the sum

The mathematical formula implemented is:

```
vector_norm(v) = √(Σ(vᵢ²))
```

Where vᵢ are the elements of the input vector.

The vector norm is fundamental in:
- Normalizing vectors to unit length
- Measuring vector magnitude in machine learning
- Computing distances and similarities
- Feature scaling and preprocessing
- Physics calculations involving magnitude

:::info
This function performs vector computations within Databend and does not rely on external APIs.
:::

## Examples

```sql
-- Calculate vector magnitude (length)
SELECT 
    VECTOR_NORM([3,4]::VECTOR(2)) AS norm_2d,
    VECTOR_NORM([1,2,3]::VECTOR(3)) AS norm_3d,
    VECTOR_NORM([0,0,0]::VECTOR(3)) AS zero_vector;
```

Result:
```
┌─────────┬───────────┬─────────────┐
│ norm_2d │  norm_3d  │ zero_vector │
├─────────┼───────────┼─────────────┤
│     5.0 │ 3.7416575 │         0.0 │
└─────────┴───────────┴─────────────┘
```
