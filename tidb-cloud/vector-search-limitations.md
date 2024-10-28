---
title: Vector Search Limitations
summary: Learn the limitations of the TiDB vector search.
---

# Vector Search Limitations

This document describes the known limitations of TiDB vector search.

> **Note**
>
> TiDB Vector Search is only available for [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) clusters. It is not available for TiDB Cloud Dedicated.

## Vector data type limitations

- Each [vector](/tidb-cloud/vector-search-data-types.md) supports up to 16383 dimensions.
- Vector data types cannot store `NaN`, `Infinity`, or `-Infinity` values.
- Vector data types cannot store double-precision floating-point numbers. If you insert or store double-precision floating-point numbers in vector columns, TiDB converts them to single-precision floating-point numbers.
- Vector columns cannot be used as primary keys or as part of a primary key.
- Vector columns cannot be used as unique indexes or as part of a unique index.
- Vector columns cannot be used as partition keys or as part of a partition key.
- Currently, TiDB does not support modifying a vector column to other data types (such as `JSON` and `VARCHAR`).

## Vector index limitations

See [Vector search restrictions](/tidb-cloud/vector-search-index.md#restrictions).

## Compatibility with TiDB tools

- The Data Migration feature in the TiDB Cloud console does not support migrating or replicating MySQL 9.0 vector data types to TiDB Cloud.

## Feedback

We value your feedback and are always here to help:

- [Join our Discord](https://discord.gg/zcqexutz2R)
- [Visit our Support Portal](https://tidb.support.pingcap.com/)