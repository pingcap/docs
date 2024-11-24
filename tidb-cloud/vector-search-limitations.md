---
title: Vector Search Limitations
summary: Learn the limitations of the TiDB Vector Search.
---

# Vector Search Limitations

This document describes the known limitations of TiDB Vector Search.

> **Note**
>
> TiDB Vector Search is only available for TiDB (>= v8.4) and [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless). It is not available for [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated).

## Vector data type limitations

- Each [vector](/tidb-cloud/vector-search-data-types.md) supports up to 16383 dimensions.
- Vector data types cannot store `NaN`, `Infinity`, or `-Infinity` values.
- Vector data types cannot store double-precision floating-point numbers. If you insert or store double-precision floating-point numbers in vector columns, TiDB converts them to single-precision floating-point numbers.
- Vector columns cannot be used in primary keys, unique indexes or partition keys. To accelerate the vector search performance, use [Vector Search Index](/tidb-cloud/vector-search-index.md).
- Multiple vector columns in a table is allowed. However, there is [a limit of total number of columns in a table](/tidb-limitations.md#limitations-on-a-single-table).
- Currently TiDB does not support dropping a vector column with a vector index. To drop such column, drop the vector index first, then drop the vector column.
- Currently TiDB does not support modifying a vector column to other data types such as `JSON` and `VARCHAR`.

## Vector index limitations

- Vector index is used for vector search. It cannot accelerate other queries like range queries or equality queries. Thus, it is not possible to create a vector index on a non-vector column, or on multiple vector columns.
- Multiple vector indexes in a table is allowed. However, there is [a limit of total number of indexes in a table](/tidb-limitations.md#limitations-on-a-single-table).
- Multiple vector indexes on the same column is allowed only if they use different distance functions.
- Currently only `VEC_COSINE_DISTANCE()` and `VEC_L2_DISTANCE()` are supported as the distance functions for vector indexes.
- Currently TiDB does not support dropping a vector column with a vector index. To drop such column, drop the vector index first, then drop the vector column.
- Currently TiDB does not support setting vector index as [invisible](/sql-statements/sql-statement-alter-index.md).

## Compatibility with TiDB tools

- The Data Migration feature in the TiDB Cloud console does not support migrating or replicating MySQL 9.0 vector data types to TiDB Cloud.

## Feedback

We value your feedback and are always here to help:

- [Join our Discord](https://discord.gg/zcqexutz2R)
- [Visit our Support Portal](https://tidb.support.pingcap.com/)
