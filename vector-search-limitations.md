---
title: Vector Search Limitations
summary: Learn the limitations of the TiDB Vector Search.
---

# Vector Search Limitations

This document describes the known limitations of TiDB Vector Search.

<CustomContent platform="tidb">

> **Warning:**
>
> The vector search feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

</CustomContent>

> **Note:**
>
> The vector search feature is only available for TiDB Self-Managed clusters and [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) clusters.

- Each [vector](/vector-search-data-types.md) supports up to 16383 dimensions.
- You cannot store `NaN`, `Infinity`, or `-Infinity` values in the vector data type.
- Only cosine distance and L2 distance (Euclidean distance) are supported when you create a [vector search index](/vector-search-index.md).
- Vector data types cannot store double-precision floating-point numbers （this is planned to be supported in a future release). If you insert or store double-precision floating-point numbers in Vector columns, they are converted to single-precision floating-point numbers.

## Feedback

We value your feedback and are always here to help:

<CustomContent platform="tidb">

- [Join our Discord](https://discord.gg/zcqexutz2R)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [Join our Discord](https://discord.gg/zcqexutz2R)
- [Visit our Support Portal](https://tidb.support.pingcap.com/)

</CustomContent>