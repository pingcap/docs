---
title: Vector Search Limitations
summary: Learn the limitations of the TiDB vector search.
---

# Vector Search Limitations

This document describes the known limitations of TiDB vector search.

> **Note:**
>
> - The vector search feature is in beta. It might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.
> - The vector search feature is available on [TiDB Self-Managed](/overview.md), [{{{ .starter }}}](/tidb-cloud/select-cluster-tier.md#starter)(/tidb-cloud/select-cluster-tier.md#starter), [{{{ .essential }}}](/tidb-cloud/select-cluster-tier.md#essential), and [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated). For TiDB Self-Managed and TiDB Cloud Dedicated, the TiDB version must be v8.4.0 or later (v8.5.0 or later is recommended).

## Vector data type limitations

- Each [vector](/ai/vector-search-data-types.md) supports up to 16383 dimensions.
- Vector data types cannot store `NaN`, `Infinity`, or `-Infinity` values.
- Vector data types cannot store double-precision floating-point numbers. If you insert or store double-precision floating-point numbers in vector columns, TiDB converts them to single-precision floating-point numbers.
- Vector columns cannot be used as primary keys or as part of a primary key.
- Vector columns cannot be used as unique indexes or as part of a unique index.
- Vector columns cannot be used as partition keys or as part of a partition key.
- Currently, TiDB does not support modifying a vector column to other data types (such as `JSON` and `VARCHAR`).

## Vector index limitations

See [Vector search restrictions](/ai/vector-search-index.md#restrictions).

## Compatibility with TiDB tools

When using vector search, note the following compatibility issues:

- TiDB Cloud features:
    - The Data Migration (DM) feature in the TiDB Cloud console does not support migrating or replicating MySQL vector data types to TiDB Cloud.
- TiDB Self-Managed tools:
    - Make sure that you are using v8.4.0 or a later version of BR to back up and restore data. Restoring tables with vector data types to TiDB clusters earlier than v8.4.0 is not supported.
    - TiDB Data Migration (DM) does not support migrating or replicating MySQL vector data types to TiDB.
    - When TiCDC replicates vector data to a downstream that does not support vector data types, it will change the vector data types to another type. For more information, see [Compatibility with vector data types](/ticdc/ticdc-compatibility.md#compatibility-with-vector-data-types).

## Feedback

We value your feedback and are always here to help:

- Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs).
- [Submit a support ticket for TiDB Cloud](https://tidb.support.pingcap.com/servicedesk/customer/portals)
- [Submit a support ticket for TiDB Self-Managed](/support.md)
