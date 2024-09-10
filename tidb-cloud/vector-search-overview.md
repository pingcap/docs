---
title: Vector Search (Beta) Overview
summary: Learn about Vector Search in TiDB Cloud. This feature provides an advanced search solution for performing semantic similarity searches across various data types, including documents, images, audio, and video.
---

# Vector Search (Beta) Overview

TiDB Vector Search (beta) provides an advanced search solution for performing semantic similarity searches across various data types, including documents, images, audio, and video. This feature enables developers to easily build scalable applications with generative artificial intelligence (AI) capabilities using familiar MySQL skills.

> **Note**
>
> TiDB Vector Search is currently in beta and only available for [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters.

## Concepts

Vector search is a search method that prioritizes the meaning of your data to deliver relevant results. This differs from traditional full-text search, which relies primarily on exact keyword matches and word frequency.

For example, a full-text search for "a swimming animal" only returns results with those exact keywords. In contrast, vector search can return results for other swimming animals, such as fish or ducks, even if the exact keywords are not present.

### Vector embedding

A vector embedding, also known as an embedding, is a sequence of numbers that represents real-world objects in a high-dimensional space. It captures the meaning and context of unstructured data, such as documents, images, audio, and videos.

Vector embeddings are essential in machine learning and serve as the foundation for semantic similarity searches.

TiDB introduces [Vector data types](/tidb-cloud/vector-search-data-types.md) designed to optimize the storage and retrieval of vector embeddings, enhancing their use in AI applications. You can store vector embeddings in TiDB and perform vector search queries to find the most relevant data using these data types.

### Embedding model

Embedding models are algorithms that transform data into [vector embeddings](#vector-embedding).

Selecting an appropriate embedding model is crucial for ensuring the accuracy and relevance of semantic search results. For unstructured text data, you can find top-performing text embedding models on the [Massive Text Embedding Benchmark (MTEB) Leaderboard](https://huggingface.co/spaces/mteb/leaderboard).

To learn how to generate vector embeddings for your specific data types, refer to the embedding provider integration tutorials or examples.

## How vector search works

After converting raw data into vector embeddings and storing them in TiDB, your application can execute vector search queries to find the data most semantically or contextually relevant to a user's query.

Vector Search in TiDB Cloud identifies the top-k nearest neighbor (KNN) vectors by using a [distance function](/tidb-cloud/vector-search-functions-and-operators.md) to calculate the distance between the given vector and vectors stored in the database. The vectors closest to the query represent the most similar data in meaning.

![The Schematic TiDB Vector Search](/media/vector-search/embedding-search.png)

As a relational database with integrated vector search capabilities, TiDB enables you to store data and their corresponding vector embeddings together in one database. You can store them in the same table using different columns, or separate them into different tables and combine them using `JOIN` queries when retrieving.

## Use cases

### Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation (RAG) is an architecture designed to optimize the output of Large Language Models (LLMs). By using vector search, RAG applications can store vector embeddings in the database and retrieve relevant documents as additional context when the LLM generates responses, thereby improving the quality and relevance of the answers.

### Semantic search

Semantic search is a search technology that returns results based on the meaning of a query, rather than simply matching keywords. It interprets the meaning across different languages and various types of data (such as text, images, and audio) using embeddings. Vector search algorithms then use these embeddings to find the most relevant data that satisfies the user's query.

### Recommendation engine

A recommendation engine is a system that proactively suggests content, products, or services that are relevant and personalized to users. It accomplishes this by creating embeddings that represent user behavior and preferences. These embeddings help the system identify similar items that other users have interacted with or shown interest in. This increases the likelihood that the recommendations will be both relevant and appealing to the user.

## See also

To get started with TiDB Vector Search, see the following documents:

- [Get started with vector search using Python](/tidb-cloud/vector-search-get-started-using-python.md)
- [Get started with vector search using SQL](/tidb-cloud/vector-search-get-started-using-sql.md)
