---
title: Vector Search
summary: Introduce the vector search feature in TiDB for developers, including concepts, tutorials, integrations, and reference documentation.
---

# Vector Search

[Vector search](/ai/concepts/vector-search-overview.md) enables semantic similarity searches across diverse data types such as documents, images, audio, and video. By leveraging your MySQL expertise, you can build scalable AI applications with advanced search functionality.

## Get started

To get started with TiDB vector search, refer to the following tutorials:

- [Get Started via Python](/ai/quickstart-via-python.md)
- [Get Started via SQL](/ai/quickstart-via-sql.md)

## Auto Embedding

The Auto Embedding feature lets you perform vector searches directly with plain text, without providing your own vectors. With this feature, you can insert text data directly and perform semantic searches using text queries, while TiDB automatically converts the text into vectors behind the scenes.

Currently, TiDB supports various embedding models, such as Amazon Titan, Cohere, Jina AI, OpenAI, Gemini, Hugging Face, and NVIDIA NIM. You can choose the one that best fits your needs. For more information, see [Auto Embedding Overview](/ai/integrations/vector-search-auto-embedding-overview.md).

## Integrations

To accelerate your development, you can integrate TiDB vector search with popular AI frameworks (such as LlamaIndex and LangChain), embedding services (such as Jina AI), and ORM libraries (such as SQLAlchemy, Peewee, and Django ORM). You can choose the one that best fits your needs.

For more information, see [Vector Search Integration Overview](/ai/integrations/vector-search-integration-overview.md).

## Text search

Unlike vector search, which focuses on semantic similarity, full-text search lets you retrieve documents for exact keywords.

To improve the retrieval quality in RAG scenarios, you can combine vector search with full-text search.

| Scenario | Documentation |
|---------------|-------------|
| Perform keyword-based search using SQL. | [Full-Text Search with SQL](/ai/guides/vector-search-full-text-search-sql.md) |
| Implement full-text search in Python applications. | [Full-Text Search with Python](/ai/guides/vector-search-full-text-search-python.md) |
| Combine vector and full-text search for better results. | [Hybrid Search](/ai/guides/vector-search-hybrid-search.md) |

## Improve performance

To optimize the performance of your vector search queries, you can follow a series of best practices, such as adding vector indexes, monitoring index build progress, reducing dimensions, excluding vector columns, and warming up indexes.

For more information about these best practices, see [Improve Vector Search Performance](/ai/reference/vector-search-improve-performance.md).

## Limitations

Before implementing vector search, be aware of the following limitations:

- Maximum 16383 dimensions per vector
- Vector columns cannot be primary keys, unique indexes, or partition keys
- No direct casting between vector and other data types (use string as intermediate)

For a complete list, see [Vector Search Limitations](/ai/reference/vector-search-limitations.md).

## Reference

- [Vector Data Types](/ai/reference/vector-search-data-types.md)
- [Vector Functions and Operators](/ai/reference/vector-search-functions-and-operators.md)
- [Vector Index](/ai/reference/vector-search-index.md)
