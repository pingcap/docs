---
title: TiDB for AI
summary: Build modern AI applications with TiDB's integrated vector search, full-text search, and seamless Python SDK.
---

# TiDB for AI

TiDB is a distributed SQL database designed for modern AI applications, offering integrated vector search, full-text search, and hybrid search capabilities. This document provides an overview of the AI features and tools available for building AI-powered applications with TiDB.

## Quick Start

Get up and running quickly with TiDB's AI capabilities.

| Document | Description |
| --- | --- |
| [Get Started with Python](/ai/quickstart-via-python.md) | Build your first AI application with TiDB in minutes using Python. |
| [Get Started with SQL](/ai/quickstart-via-sql.md) | Quick start guide for vector search using SQL. |

## Concepts

Understand the foundational concepts behind AI-powered search in TiDB.

| Document | Description |
| --- | --- |
| [Vector Search](/ai/concepts/vector-search-overview.md) | Comprehensive overview of vector search, including concepts, how it works, and use cases. |

## Guides

Step-by-step guides for building AI applications with TiDB using the [`pytidb`](https://github.com/pingcap/pytidb) SDK or SQL.

| Document | Description |
| --- | --- |
| [Connect to TiDB](/ai/guides/connect.md) | Connect to TiDB Cloud or self-managed clusters using `pytidb`. |
| [Working with Tables](/ai/guides/tables.md) | Create, query, and manage tables with vector fields. |
| [Vector Search](/ai/guides/vector-search.md) | Perform semantic similarity searches using `pytidb`. |
| [Full-Text Search](/ai/guides/vector-search-full-text-search-python.md) | Keyword-based text search with BM25 ranking. |
| [Hybrid Search](/ai/guides/vector-search-hybrid-search.md) | Combine vector and full-text search for better results. |
| [Image Search](/ai/guides/image-search.md) | Search images using multimodal embeddings. |
| [Auto Embedding](/ai/guides/auto-embedding.md) | Automatically generate embeddings on data insertion. |
| [Filtering](/ai/guides/filtering.md) | Filter search results with metadata conditions. |

## Examples

Complete code examples and demos showcasing TiDB's AI capabilities.

| Document | Description |
| --- | --- |
| [Basic CRUD Operations](/ai/examples/basic-with-pytidb.md) | Fundamental table operations with `pytidb`. |
| [Vector Search](/ai/examples/vector-search-with-pytidb.md) | Semantic similarity search example. |
| [RAG Application](/ai/examples/rag-with-pytidb.md) | Build a Retrieval-Augmented Generation application. |
| [Image Search](/ai/examples/image-search-with-pytidb.md) | Multimodal image search with Jina AI embeddings. |
| [Conversational Memory](/ai/examples/memory-with-pytidb.md) | Persistent memory for AI agents and chatbots. |
| [Text-to-SQL](/ai/examples/text2sql-with-pytidb.md) | Convert natural language to SQL queries. |

## Integrations

Integrate TiDB with popular AI frameworks, embedding providers, and development tools.

| Document | Description |
| --- | --- |
| [Integration Overview](/ai/integrations/vector-search-integration-overview.md) | Overview of all available integrations. |
| [Embedding Providers](/ai/integrations/vector-search-auto-embedding-overview.md#available-text-embedding-models) | Unified interface for OpenAI, Cohere, Jina AI, and more. |
| [LangChain](/ai/integrations/vector-search-integrate-with-langchain.md) | Use TiDB as a vector store with LangChain. |
| [LlamaIndex](/ai/integrations/vector-search-integrate-with-llamaindex.md) | Use TiDB as a vector store with LlamaIndex. |
| [MCP Server](/ai/integrations/tidb-mcp-server.md) | Connect TiDB to Claude Code, Cursor, and other AI-powered IDEs. |

## Reference

Technical reference documentation for TiDB's AI and vector search features.

| Document | Description |
| --- | --- |
| [Vector Data Types](/ai/reference/vector-search-data-types.md) | Vector column types and usage. |
| [Functions and Operators](/ai/reference/vector-search-functions-and-operators.md) | Distance functions and vector operations. |
| [Vector Search Index](/ai/reference/vector-search-index.md) | Create and manage vector indexes for performance. |
| [Performance Tuning](/ai/reference/vector-search-improve-performance.md) | Optimize vector search performance. |
| [Limitations](/ai/reference/vector-search-limitations.md) | Current limitations and constraints. |
