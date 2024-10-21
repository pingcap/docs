---
title: Vector Search Integration Overview
summary: An overview of TiDB vector search integration, including supported AI frameworks and embedding models.
---

# Vector Search Integration Overview

This document provides an overview of TiDB vector search integration, including supported AI frameworks and embedding models.

<CustomContent platform="tidb">

> **Warning:**
>
> The vector search feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

</CustomContent>

> **Note:**
>
> The vector search feature is only available for TiDB Self-Managed clusters and [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) clusters.

## AI frameworks

TiDB provides official support for the following AI frameworks, enabling you to easily integrate AI applications developed based on these frameworks with TiDB Vector Search.

| AI frameworks | Tutorial                                                                                          |
|---------------|---------------------------------------------------------------------------------------------------|
| Langchain     | [Integrate Vector Search with LangChain](/vector-search-integrate-with-langchain.md)   |
| LlamaIndex    | [Integrate Vector Search with LlamaIndex](/vector-search-integrate-with-llamaindex.md) |

Moreover, you can also use TiDB for various purposes, such as document storage and knowledge graph storage for AI applications.

## Embedding models and services

TiDB Vector Search supports storing vectors of up to 16383 dimensions, which accommodates most embedding models.

You can either use self-deployed open-source embedding models or third-party embedding APIs provided by third-party embedding providers to generate vectors.

The following table lists some mainstream embedding service providers and the corresponding integration tutorials.

| Embedding service providers | Tutorial                                                                                                            |
|-----------------------------|---------------------------------------------------------------------------------------------------------------------|
| Jina AI                     | [Integrate Vector Search with Jina AI Embeddings API](/vector-search-integrate-with-jinaai-embedding.md) |