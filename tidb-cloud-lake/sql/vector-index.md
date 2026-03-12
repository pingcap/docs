---
title: Vector Index
---

Vector indexes in Databend enable efficient similarity search on high-dimensional vector data using the HNSW (Hierarchical Navigable Small World) algorithm. They support use cases like semantic search, recommendation systems, and AI applications.

:::tip Key Feature: Automatic Index Generation
Vector indexes are **automatically built as data is written**. When you insert or load data into a table with a Vector index, the index is generated automatically without manual intervention. You only need to run `REFRESH VECTOR INDEX` if you create an index on a table that already contains data.
:::

## Vector Index Management

| Command                                         | Description                                               |
|-------------------------------------------------|-----------------------------------------------------------|
| [CREATE VECTOR INDEX](create-vector-index.md)   | Creates a new Vector index for efficient similarity search |
| [REFRESH VECTOR INDEX](refresh-vector-index.md) | Builds index for data that existed before index creation  |
| [DROP VECTOR INDEX](drop-vector-index.md)       | Removes a Vector index                                    |
