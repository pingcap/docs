---
title: Improve Vector Search Performance
summary: Learn best practices for improving the performance of TiDB Vector Search.
---

# Improve Vector Search Performance

TiDB Vector Search enables you to perform Approximate Nearest Neighbor (ANN) queries that search for results similar to an image, document, or other input. To improve the query performance, review the following best practices.

<CustomContent platform="tidb">

> **Warning:**
>
> The vector search feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

</CustomContent>

> **Note:**
>
> The vector search feature is only available for TiDB Self-Managed clusters and [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) clusters.

## Add vector search index for vector columns

The [vector search index](/vector-search/vector-search-index.md) dramatically improves the performance of vector search queries, usually by 10x or more, with a trade-off of only a small decrease of recall rate.

## Ensure vector indexes are fully built

After you insert a large volume of vector data, some of it might be in the Delta layer waiting for persistence. The vector index for such data will be built after the data is persisted. Until all vector data is indexed, vector search performance is suboptimal. To check the index build progress, see [View index build progress](/vector-search/vector-search-index.md#view-index-build-progress).

## Reduce vector dimensions or shorten embeddings

The computational complexity of vector search indexing and queries increases significantly as the dimension of vectors grows, requiring more floating-point comparisons.

To optimize performance, consider reducing vector dimensions whenever feasible. This usually needs switching to another embedding model. When switching models, you need to evaluate the impact of the model change on the accuracy of vector queries.

Certain embedding models like OpenAI `text-embedding-3-large` support [shortening embeddings](https://openai.com/index/new-embedding-models-and-api-updates/), which removes some numbers from the end of vector sequences without losing the embedding's concept-representing properties. You can also use such an embedding model to reduce the vector dimensions.

## Exclude vector columns from the results

Vector embedding data is usually large and only used during the search process. By excluding vector columns from query results, you can greatly reduce the data transferred between the TiDB server and your SQL client, thereby improving query performance.

To exclude vector columns, explicitly list the columns you want to retrieve in the `SELECT` clause, instead of using `SELECT *` to retrieve all columns.

## Warm up the index

When accessing an index that has never been used or has not been accessed for a long time (cold access), TiDB needs to load the entire index from cloud storage or disk (instead of from memory). This process takes time and often results in higher query latency. Additionally, if there are no SQL queries for an extended period (for example, several hours), computing resources are reclaimed, causing subsequent access to become cold access.

To avoid such query latency, warm up your index before actual workload by running similar vector search queries that hit the vector index.