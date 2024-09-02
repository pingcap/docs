---
title: Improve Vector Search Performance
summary: Learn best practices for improving the performance of TiDB Vector Search.
---

# Improve Vector Search Performance

TiDB Vector Search allows you to perform ANN queries that search for results similar to an image, document and so on. To improve the query performance, review the following best practices.

## Add vector search index for vector columns

The [vector search index](/tidb-cloud/vector-search-index.md) dramatically improves the performance of vector search queries, usually by 10x or more, with a trade-off of only a small decrease of recall rate.

## Ensure vector indexes are fully built

Vector indexes are built asynchronously. Until all vector data is indexed, vector search performance is suboptimal. To check the index build progress, see [View index build progress](/tidb-cloud/vector-search-index.md#view-index-build-progress).

## Reduce vector dimensions or shorten embeddings

The computational complexity of vector search indexing and queries increases significantly as the size of vectors grows, necessitating more floating point comparisons.

To optimize performance, consider reducing the vector dimensions whenever feasible. This usually needs switching to another embedding model. Make sure to measure the impact of changing embedding models on the accuracy of your vector queries.

Certain embedding models like OpenAI `text-embedding-3-large` support [shortening embeddings](https://openai.com/index/new-embedding-models-and-api-updates/), which removes some numbers from the end of vector sequences without losing the embedding's concept-representing properties. You can also use such an embedding model to reduce the vector dimensions.

## Exclude vector columns from the results

Vector embedding data are usually large and only used during the search process. By excluding vector columns from the query results, you can greatly reduce the amount of data transferred between the TiDB server and your SQL client, thereby improving query performance.

To exclude vector columns, explicitly list the columns you want to retrieve in the `SELECT` clause, instead of using `SELECT *`.

## Warm up the index

When an index is cold accessed, it takes time to load the whole index from S3, or load from disk (instead of from memory). Such processes usually result in high tail latency. Additionally, if no SQL queries exist on a cluster for a long time (e.g. hours), the compute resource is reclaimed and will result in cold access next time.

To avoid such tail latencies, warm up your index before actual workload by using similar vector search queries that hit the vector index.
