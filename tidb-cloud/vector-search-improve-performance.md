---
title: Improve Vector Search Performance
summary: Learn best practices to improve the performance of TiDB Vector Search.
---

# Improve Vector Search Performance

TiDB Vector Search allows you to perform ANN queries that search for results similar to an image, document and so on. To improve the query performance, review the following best practices.

## Add Vector Search Index for Vector Columns

[Vector Search Index](/tidb-cloud/vector-search-index.md) dramatically improves the performance of vector search queries, usually by 10x or more, with a trade-off of only a small decrease of recall rate.

## Reduce Vector Dimensions or Shorten Embeddings

The computational complexity of vector search indexing and queries increases significantly as the size of vectors grows, necessitating more floating point comparisons.

To optimize performance, consider reduce the vector dimensions whenever feasible. This usually needs to switch to another embedding model. Make sure to measure the impact of changing embedding models on the accuracy of your vector queries.

Certain embedding models like OpenAI `text-embedding-3-large` support [shortening embeddings](https://openai.com/index/new-embedding-models-and-api-updates/), which removes some numbers from the end of vector sequences without losing the embedding's concept-representing properties. This can also be used to reduce the vector dimensions.

## Exclude Vector Columns From the Results

Vector embedding data are usually large and only used during the search process. By excluding vector columns from the query results, you can greatly reduce the amount of data transferred between TiDB server and your SQL client, thus improving the query performance.

To exclude vector columns, explicitly list the columns you want to retrieve in the `SELECT` clause, instead of using `SELECT *`.

## Warm up Index

When an index is cold accessed, it takes time to load the whole index from S3, or load from disk (instead of from memory). Such processes usually result in high tail latency. Additionally, if there are no SQL queries on a cluster for a long time (e.g. hours), the compute resource is reclaimed and will result in cold access next time.

To avoid such tail latencies, warm up your index before actual workload by using similar vector search queries that will hit the vector index.
