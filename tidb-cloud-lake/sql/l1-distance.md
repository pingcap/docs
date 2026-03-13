---
title: 'L1_DISTANCE'
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.777"/>

Calculates the Manhattan (L1) distance between two vectors, measuring the sum of absolute differences between corresponding elements.

## Syntax

```sql
L1_DISTANCE(vector1, vector2)
```

## Arguments

- `vector1`: First vector (VECTOR Data Type)
- `vector2`: Second vector (VECTOR Data Type)

## Returns

Returns a FLOAT value representing the Manhattan (L1) distance between the two vectors. The value is always non-negative:
- 0: Identical vectors
- Larger values: Vectors that are farther apart

## Description

The L1 distance, also known as Manhattan distance or taxicab distance, calculates the sum of absolute differences between corresponding elements of two vectors. It's useful for feature comparison and sparse data analysis.

Formula: `L1_DISTANCE(a, b) = |a1 - b1| + |a2 - b2| + ... + |an - bn|`

## Examples

### Basic Usage

```sql
-- Calculate L1 distance between two vectors
SELECT L1_DISTANCE([1.0, 2.0, 3.0]::vector(3), [4.0, 5.0, 6.0]::vector(3)) AS distance;
```

Result:
```
╭──────────╮
│ distance │
├──────────┤
│        9 │
╰──────────╯
```

Create a table with vector data:

```sql
CREATE OR REPLACE TABLE vectors (
    id INT,
    vec VECTOR(3)
);

INSERT INTO vectors VALUES
    (1, [1.0000, 2.0000, 3.0000]),
    (2, [1.0000, 2.2000, 3.0000]),
    (3, [4.0000, 5.0000, 6.0000]);
```

Find the vector closest to [1, 2, 3] using L1 distance:

```sql
SELECT
    id,
    vec,
    L1_DISTANCE(vec, [1.0000, 2.0000, 3.0000]::VECTOR(3)) AS distance
FROM
    vectors
ORDER BY
    distance ASC;
```

```
╭─────────────────────────────╮
│ id │    vec    │  distance  │
├────┼───────────┼────────────┤
│  1 │ [1,2,3]   │          0 │
│  2 │ [1,2.2,3] │ 0.20000005 │
│  3 │ [4,5,6]   │          9 │
╰─────────────────────────────╯
```

