---
title: Vector Search Limitations
summary: Learn the limitations of the TiDB Vector Search.
---

# Vector Search Limitations

This document describes the known limitations of TiDB Vector Search. We are continuously working to enhance your experience by adding more features.

<CustomContent platform="tidb">

- TiDB Vector Search is only available for the following clusters. It is not available for TiDB Dedicated clusters.

    - TiDB Self-Hosted clusters with TiDB versions of 8.4.0 or later
    - [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless) clusters

- Each [vector](/vector-search-data-types.md) supports up to 16,000 dimensions.

- Vector data supports only single-precision floating-point numbers (Float32).

</CustomContent>

<CustomContent platform="tidb-cloud">

- TiDB Vector Search is only available for the following clusters. It is not available for TiDB Dedicated clusters.

    - [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters
    - TiDB Self-Hosted clusters with TiDB versions of 8.4.0 or later

- Each [vector](/vector-search-data-types.md) supports up to 16,000 dimensions.

- Vector data supports only single-precision floating-point numbers (Float32).

- Only cosine distance and L2 distance are supported when you create a [vector search index](/tidb-cloud/vector-search-index.md).

</CustomContent>

## Feedback

We value your feedback and are always here to help:

- [Join our Discord](https://discord.gg/zcqexutz2R)
- [Visit our Support Portal](https://tidb.support.pingcap.com/)
