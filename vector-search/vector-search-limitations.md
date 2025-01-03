---
title: Vector Search Limitations
summary: Learn the limitations of the TiDB vector search.
---

# Vector Search Limitations

This document describes the known limitations of TiDB vector search.

<CustomContent platform="tidb">

> **Warning:**
>
> The vector search feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

</CustomContent>

> **Note:**
>
> The vector search feature is only available for TiDB Self-Managed clusters and [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) clusters.

## Vector data type limitations

- Each [vector](/vector-search-data-types.md) supports up to 16383 dimensions.
- Vector data types cannot store `NaN`, `Infinity`, or `-Infinity` values.
- Vector data types cannot store double-precision floating-point numbers. If you insert or store double-precision floating-point numbers in vector columns, TiDB converts them to single-precision floating-point numbers.
- Vector columns cannot be used as primary keys or as part of a primary key.
- Vector columns cannot be used as unique indexes or as part of a unique index.
- Vector columns cannot be used as partition keys or as part of a partition key.
- Currently, TiDB does not support modifying a vector column to other data types (such as `JSON` and `VARCHAR`).

## Vector index limitations

See [Vector search restrictions](/vector-search-index.md#restrictions).

## Compatibility with TiDB tools

<CustomContent platform="tidb">

- Make sure that you are using v8.4.0 or a later version of BR to back up and restore data. Restoring tables with vector data types to TiDB clusters earlier than v8.4.0 is not supported.
- TiDB Data Migration (DM) does not support migrating or replicating MySQL 9.0 vector data types to TiDB.
- When TiCDC replicates vector data to a downstream that does not support vector data types, it will change the vector data types to another type. For more information, see [Compatibility with vector data types](/ticdc/ticdc-compatibility.md#compatibility-with-vector-data-types).

</CustomContent>

<CustomContent platform="tidb-cloud">

- The Data Migration feature in the TiDB Cloud console does not support migrating or replicating MySQL 9.0 vector data types to TiDB Cloud.

</CustomContent>

## Feedback

We value your feedback and are always here to help:

<CustomContent platform="tidb">

- [Join our Discord](https://discord.gg/zcqexutz2R)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [Join our Discord](https://discord.gg/zcqexutz2R)
- [Visit our Support Portal](https://tidb.support.pingcap.com/)

</CustomContent>