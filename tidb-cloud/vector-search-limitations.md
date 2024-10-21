---
title: Vector Search Limitations
summary: Learn the limitations of the TiDB Vector Search.
---

# Vector Search Limitations

This document describes the known limitations of TiDB Vector Search. We are continuously working to enhance your experience by adding more features.

- TiDB Vector Search is only available for [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) clusters. It is not available for TiDB Cloud Dedicated or TiDB Self-Managed.

- Each [vector](/tidb-cloud/vector-search-data-types.md) supports up to 16,000 dimensions.

- Vector data supports only single-precision floating-point numbers (Float32).

- Only cosine distance and L2 distance are supported when you create a [vector search index](/tidb-cloud/vector-search-index.md).

## Feedback

We value your feedback and are always here to help:

- [Join our Discord](https://discord.gg/zcqexutz2R)
- [Visit our Support Portal](https://tidb.support.pingcap.com/)
