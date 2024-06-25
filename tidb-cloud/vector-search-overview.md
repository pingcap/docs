---
title: Vector Search (Beta) Overview
summary: Learn about the vector search feature in TiDB Cloud. This feature provides an advanced search solution for performing semantic similarity searches across various data types, including documents, images, audio, and video.
---

# Vector Search (Beta) Overview

The vector search (beta) feature in TiDB Cloud provides an advanced search solution for performing semantic similarity searches across various data types, including documents, images, audio, and video. This feature enables developers to easily build scalable applications with generative artificial intelligence (AI) capabilities using familiar MySQL skills.

> **Note**
>
> The vector search feature is currently in beta and only available for [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters.

## Concepts

Vector search is a search method that prioritizes the meaning of your data to deliver relevant results. This differs from traditional full-text search, which relies primarily on exact keyword matches and word frequency.

For example, a full-text search for "a swimming animal" only returns results with those exact keywords. In contrast, vector search can return results for other swimming animals, such as fish or ducks, even if the exact keywords are not present.

### Vector embedding

A vector embedding, also known as an embedding, is an array of numbers that represents real-world objects in a high-dimensional space. It captures the meaning and context of unstructured data, such as documents, images, audio, and videos.

Vector embeddings are essential in machine learning and serve as the foundation for semantic similarity searches.

To store vector embeddings, TiDB introduces a new `VECTOR` data type. For more information, see [Vector Data Type](/tidb-cloud/vector-search-data-types.md).

### Embedding model

Embedding models are algorithms that transform data into [vector embeddings](#vector-embedding).

Selecting an appropriate embedding model is crucial for ensuring the accuracy and relevance of semantic search results. For unstructured text data, you can find top-performing text embedding models on the [Massive Text Embedding Benchmark (MTEB) Leaderboard](https://huggingface.co/spaces/mteb/leaderboard).

To learn how to generate vector embeddings for your specific data types, refer to the embedding provider integration tutorials or examples.

## How vector search works

After converting raw data into vector embeddings and storing them in TiDB, your application can execute vector search queries to find the data most semantically or contextually relevant to a user's query.

The vector search feature in TiDB Cloud identifies the top-k nearest neighbor (KNN) vectors by using a [distance function](/tidb-cloud/vector-search-functions-and-operators.md) to calculate the distance between a given vectorized query and the data vectors in the embedding space. The vectors closest to the query represent the most similar data in meaning.

![The Schematic TiDB Vector Search](/media/vector-search/embedding-search.png)

As a relational database with integrated vector search capabilities, TiDB enables you to store data and their corresponding vector embeddings together in one database. You can store them in the same table using different columns, or separate them into different tables and combine them using `JOIN` queries when retrieving.

## Use cases

### Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation (RAG) is an architecture designed to optimize the output of Large Language Models (LLMs). By using vector search, RAG applications can store vector embeddings in the database and retrieve relevant documents as additional context when the LLM generates responses, thereby improving the quality and relevance of the answers.

## See also

To get started with the vector search feature, see the following documents:

- [Get started with vector search via SQL](/tidb-cloud/vector-search-get-started-via-sql.md)
- [Get started with vector search via Python client](/tidb-cloud/vector-search-get-started-via-python-client.md)
