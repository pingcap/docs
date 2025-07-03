---
title: Vector Search Overview
summary: Learn about Vector Search in TiDB. This feature provides an advanced search solution for performing semantic similarity searches across various data types, including documents, images, audio, and video.
---

# Vector Search Overview

Vector search offers a powerful solution for semantic similarity searches across diverse data types, such as documents, images, audio, and video. It allows developers to leverage their MySQL expertise to build scalable applications enriched with generative AI capabilities, simplifying the integration of advanced search functionality.

<CustomContent platform="tidb">

> **Warning:**
>
> The vector search feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Warning:**
>
> The vector search feature is in beta. It might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

</CustomContent>

> **Note:**
>
> The vector search feature is only available for TiDB Self-Managed clusters and [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) clusters.

## Concepts

Vector search is a search method that prioritizes the meaning of your data to deliver relevant results.

Unlike traditional full-text search, which relies on exact keyword matching and word frequency, vector search converts various data types (such as text, images, or audio) into high-dimensional vectors and queries based on the similarity between these vectors. This search method captures the semantic meaning and contextual information of the data, leading to a more precise understanding of user intent.

Even when the search terms do not exactly match the content in the database, vector search can still provide results that align with the user's intent by analyzing the semantics of the data.

For example, a full-text search for "a swimming animal" only returns results containing these exact keywords. In contrast, vector search can return results for other swimming animals, such as fish or ducks, even if these results do not contain the exact keywords.

### Vector embedding

A vector embedding, also known as an embedding, is a sequence of numbers that represents real-world objects in a high-dimensional space. It captures the meaning and context of unstructured data, such as documents, images, audio, and videos.

Vector embeddings are essential in machine learning and serve as the foundation for semantic similarity searches.

TiDB introduces [Vector data types](/vector-search/vector-search-data-types.md) and [Vector search index](/vector-search/vector-search-index.md) designed to optimize the storage and retrieval of vector embeddings, enhancing their use in AI applications. You can store vector embeddings in TiDB and perform vector search queries to find the most relevant data using these data types.

### Embedding model

Embedding models are algorithms that transform data into [vector embeddings](#vector-embedding).

Choosing an appropriate embedding model is crucial for ensuring the accuracy and relevance of semantic search results. For unstructured text data, you can find top-performing text embedding models on the [Massive Text Embedding Benchmark (MTEB) Leaderboard](https://huggingface.co/spaces/mteb/leaderboard).

To learn how to generate vector embeddings for your specific data types, refer to integration tutorials or examples of embedding models.

## How vector search works

After converting raw data into vector embeddings and storing them in TiDB, your application can execute vector search queries to find the data most semantically or contextually relevant to a user's query.

TiDB vector search identifies the top-k nearest neighbor (KNN) vectors by using a [distance function](/vector-search/vector-search-functions-and-operators.md) to calculate the distance between the given vector and vectors stored in the database. The vectors closest to the given vector in the query represent the most similar data in meaning.

![The Schematic TiDB Vector Search](/media/vector-search/embedding-search.png)

As a relational database with integrated vector search capabilities, TiDB enables you to store data and their corresponding vector representations (that is, vector embeddings) together in one database. You can choose any of the following ways for storage:

- Store data and their corresponding vector representations in different columns of the same table.
- Store data and their corresponding vector representation in different tables. In this way, you need to use `JOIN` queries to combine the tables when retrieving data.

## Use cases

### Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation (RAG) is an architecture designed to optimize the output of Large Language Models (LLMs). By using vector search, RAG applications can store vector embeddings in the database and retrieve relevant documents as additional context when the LLM generates responses, thereby improving the quality and relevance of the answers.

### Semantic search

Semantic search is a search technology that returns results based on the meaning of a query, rather than simply matching keywords. It interprets the meaning across different languages and various types of data (such as text, images, and audio) using embeddings. Vector search algorithms then use these embeddings to find the most relevant data that satisfies the user's query.

### Recommendation engine

A recommendation engine is a system that proactively suggests content, products, or services that are relevant and personalized to users. It accomplishes this by creating embeddings that represent user behavior and preferences. These embeddings help the system identify similar items that other users have interacted with or shown interest in. This increases the likelihood that the recommendations will be both relevant and appealing to the user.

## See also

To get started with TiDB Vector Search, see the following documents:

- [Get started with vector search using Python](/vector-search/vector-search-get-started-using-python.md)
- [Get started with vector search using SQL](/vector-search/vector-search-get-started-using-sql.md)
