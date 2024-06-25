---
title: Vector Search Limitations
summary: Learn the limitations of the TiDB Vector Search.
---

# Vector Search Limitations

This page lists out some known limitations that you may encounter when using TiDB Vector Search. We are continuously working to bring in more features to enhance your experience.

- TiDB Vector Search is only available for TiDB Cloud Serverless. It is not available for TiDB Dedicated and TiDB On-Premise.

- Each [vector](/tidb-cloud/vector-search-data-types.md) supports up to 16000 dimensions.

- Vector data only supports single-precision floating-point numbers (Float32).

- Only cosine distance and L2 distance are supported when creating a [vector search index](/tidb-cloud/vector-search-index.md).

## Feedback

We value your feedback and always here to help:

- Discord: https://discord.gg/zcqexutz2R
- Support Portal: https://tidb.support.pingcap.com/
