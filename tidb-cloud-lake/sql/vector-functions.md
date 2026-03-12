---
title: 'Vector Functions'
description: 'Vector functions in Databend for vector operations and analysis'
---

This section provides reference information for vector functions in Databend. These functions enable comprehensive vector operations including distance calculations, similarity measurements, and vector analysis for machine learning applications, vector search, and AI-powered analytics.

## Distance Functions

| Function | Description | Example |
|----------|-------------|--------|
| [COSINE_DISTANCE](./00-vector-cosine-distance.md) | Calculates Cosine distance between vectors (range: 0-1) | `COSINE_DISTANCE([1,2,3]::VECTOR(3), [4,5,6]::VECTOR(3))` |
| [L1_DISTANCE](./02-vector-l1-distance.md) | Calculates Manhattan (L1) distance between vectors | `L1_DISTANCE([1,2,3]::VECTOR(3), [4,5,6]::VECTOR(3))` |
| [L2_DISTANCE](./01-vector-l2-distance.md) | Calculates Euclidean (straight-line) distance | `L2_DISTANCE([1,2,3]::VECTOR(3), [4,5,6]::VECTOR(3))` |
| [INNER_PRODUCT](./03-inner-product.md) | Calculates the inner product (dot product) of two vectors | `INNER_PRODUCT([1,2,3]::VECTOR(3), [4,5,6]::VECTOR(3))` |

## Vector Analysis Functions

| Function | Description | Example |
|----------|-------------|--------|
| [VECTOR_NORM](./05-vector-norm.md) | Calculates the L2 norm (magnitude) of a vector | `VECTOR_NORM([1,2,3]::VECTOR(3))` |
| [VECTOR_DIMS](./04-vector-dims.md) | Returns the dimensionality of a vector | `VECTOR_DIMS([1,2,3]::VECTOR(3))` |

## Distance Functions Comparison

| Function | Description | Range | Best For | Use Cases |
|----------|-------------|-------|----------|-----------|
| [COSINE_DISTANCE](./00-vector-cosine-distance.md) | Cosine distance between vectors | [0, 1] | When direction matters more than magnitude | • Document similarity<br/>• Semantic search<br/>• Recommendation systems<br/>• Text analysis |
| [L1_DISTANCE](./02-vector-l1-distance.md) | Manhattan (L1) distance between vectors | [0, ∞) | Robust to outliers | • Feature comparison<br/>• Outlier detection<br/>• Grid-based pathfinding<br/>• Clustering algorithms |
| [L2_DISTANCE](./01-vector-l2-distance.md) | Euclidean (straight-line) distance | [0, ∞) | When magnitude and absolute differences are important | • Image similarity<br/>• Geographical data<br/>• Anomaly detection<br/>• Feature-based clustering |
| [INNER_PRODUCT](./03-inner-product.md) | Dot product of two vectors | (-∞, ∞) | When both magnitude and direction are important | • Neural networks<br/>• Machine learning<br/>• Physics calculations<br/>• Vector projections |

## Vector Analysis Functions Comparison

| Function | Description | Range | Best For | Use Cases |
|----------|-------------|-------|----------|-----------|
| [VECTOR_NORM](./05-vector-norm.md) | L2 norm (magnitude) of a vector | [0, ∞) | Vector normalization and magnitude | • Vector normalization<br/>• Feature scaling<br/>• Magnitude calculations<br/>• Physics applications |
| [VECTOR_DIMS](./04-vector-dims.md) | Number of vector dimensions | [1, 4096] | Vector validation and processing | • Data validation<br/>• Dynamic processing<br/>• Debugging<br/>• Compatibility checks |
