---
title: 'INNER_PRODUCT'
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.780"/>

Calculates the inner product (dot product) of two vectors, which measures the similarity and projection between vectors.

## Syntax

```sql
INNER_PRODUCT(vector1, vector2)
```

## Arguments

- `vector1`: First vector (VECTOR Data Type)
- `vector2`: Second vector (VECTOR Data Type)

## Returns

Returns a FLOAT value representing the inner product of the two vectors.

## Description

The inner product (also known as dot product) calculates the sum of the products of corresponding elements in two vectors. The function:

1. Verifies that both input vectors have the same length
2. Multiplies corresponding elements from each vector
3. Sums all the products to produce a single scalar value

The mathematical formula implemented is:

```
inner_product(v1, v2) = Σ(v1ᵢ * v2ᵢ)
```

Where v1ᵢ and v2ᵢ are the elements of the input vectors.

The inner product is fundamental in:
- Measuring vector similarity (higher values indicate more similar directions)
- Computing projections of one vector onto another
- Machine learning algorithms (neural networks, SVM, etc.)
- Physics calculations involving work and energy

:::info
This function performs vector computations within Databend and does not rely on external APIs.
:::

## Examples

### Basic Usage

```sql
SELECT INNER_PRODUCT([1,2,3]::VECTOR(3), [4,5,6]::VECTOR(3)) AS inner_product;
```

Result:
```
┌───────────────┐
│ inner_product │
├───────────────┤
│          32.0 │
└───────────────┘
```

### Working with Table Data

Create a table with vector data:

```sql
CREATE TABLE vector_examples (
    id INT,
    vector_a VECTOR(3),
    vector_b VECTOR(3)
);

INSERT INTO vector_examples VALUES
    (1, [1.0, 2.0, 3.0], [4.0, 5.0, 6.0]),
    (2, [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]),
    (3, [2.0, 3.0, 1.0], [1.0, 2.0, 3.0]);
```

Calculate inner products:

```sql
SELECT 
    id,
    vector_a,
    vector_b,
    INNER_PRODUCT(vector_a, vector_b) AS inner_product
FROM vector_examples;
```

Result:
```
┌────┬───────────────┬───────────────┬───────────────┐
│ id │   vector_a    │   vector_b    │ inner_product │
├────┼───────────────┼───────────────┼───────────────┤
│  1 │ [1.0,2.0,3.0] │ [4.0,5.0,6.0] │          32.0 │
│  2 │ [1.0,0.0,0.0] │ [0.0,1.0,0.0] │           0.0 │
│  3 │ [2.0,3.0,1.0] │ [1.0,2.0,3.0] │          11.0 │
└────┴───────────────┴───────────────┴───────────────┘
```

### Vector Similarity Analysis

```sql
-- Calculate inner products to measure vector similarity
SELECT 
    INNER_PRODUCT([1,0,0]::VECTOR(3), [1,0,0]::VECTOR(3)) AS same_direction,
    INNER_PRODUCT([1,0,0]::VECTOR(3), [0,1,0]::VECTOR(3)) AS orthogonal,
    INNER_PRODUCT([1,0,0]::VECTOR(3), [-1,0,0]::VECTOR(3)) AS opposite;
```

Result:
```
┌────────────────┬─────────────┬──────────┐
│ same_direction │ orthogonal  │ opposite │
├────────────────┼─────────────┼──────────┤
│           1.0  │         0.0 │     -1.0 │
└────────────────┴─────────────┴──────────┘
```
