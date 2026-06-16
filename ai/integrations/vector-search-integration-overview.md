---
title: AI Integrations for TiDB
summary: An overview of AI integrations for TiDB, including Auto Embedding providers, AI frameworks, ORM libraries, cloud services, and MCP server support.
aliases: ['/tidb/stable/vector-search-integration-overview/','/tidb/dev/vector-search-integration-overview/','/tidbcloud/vector-search-integration-overview/']
---

# AI Integrations for TiDB

This document provides an overview of AI integrations for TiDB, including Auto Embedding providers, AI frameworks, Object Relational Mapping (ORM) libraries, cloud services, and MCP server support.

> **Note:**
>
> - The vector search feature is in beta. It might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.
> - The vector search feature is available on [TiDB Self-Managed](/overview.md), [{{{ .starter }}}](/tidb-cloud/select-cluster-tier.md#starter), [{{{ .essential }}}](/tidb-cloud/select-cluster-tier.md#essential), and [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated). For TiDB Self-Managed and TiDB Cloud Dedicated, the TiDB version must be v8.4.0 or later (v8.5.0 or later is recommended).

## Auto Embedding

The [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) feature lets you perform vector searches directly with plain text. TiDB automatically converts text into vectors behind the scenes, so you do not need to generate or manage embeddings yourself.

TiDB Vector Search supports storing vectors of up to 16383 dimensions, which accommodates most embedding models.

You can use either self-deployed open-source embedding models or third-party embedding APIs to generate vectors.

The following table lists the supported embedding providers. For details on how to configure each provider, see the corresponding guide.

| Provider          | Guide                                                                                |
|-------------------|--------------------------------------------------------------------------------------|
| OpenAI            | [OpenAI](/ai/integrations/vector-search-auto-embedding-openai.md)                    |
| OpenAI Compatible | [OpenAI Compatible](/ai/integrations/embedding-openai-compatible.md)                 |
| Jina AI           | [Jina AI](/ai/integrations/vector-search-auto-embedding-jina-ai.md)                  |
| Cohere            | [Cohere](/ai/integrations/vector-search-auto-embedding-cohere.md)                    |
| Google Gemini     | [Google Gemini](/ai/integrations/vector-search-auto-embedding-gemini.md)             |
| Hugging Face      | [Hugging Face](/ai/integrations/vector-search-auto-embedding-huggingface.md)         |
| NVIDIA NIM        | [NVIDIA NIM](/ai/integrations/vector-search-auto-embedding-nvidia-nim.md)            |
| Amazon Titan      | [Amazon Titan](/ai/integrations/vector-search-auto-embedding-amazon-titan.md)        |

## AI frameworks

TiDB provides official support for the following AI frameworks, enabling you to easily integrate AI applications developed with these frameworks into TiDB Vector Search.

| AI framework | Tutorial                                                                                          |
|---------------|---------------------------------------------------------------------------------------------------|
| LangChain     | [Integrate Vector Search with LangChain](/ai/integrations/vector-search-integrate-with-langchain.md)   |
| LlamaIndex    | [Integrate Vector Search with LlamaIndex](/ai/integrations/vector-search-integrate-with-llamaindex.md) |

You can also use TiDB for various tasks such as document storage and knowledge graph storage for AI applications.

## ORM libraries

You can integrate TiDB Vector Search with your ORM library to interact with the TiDB database.

The following table lists the supported ORM libraries and the corresponding integration tutorials:

| Language | ORM/Client         | How to install                    | Tutorial |
|----------|--------------------|-----------------------------------|----------|
| Python   | SQLAlchemy         | `pip install tidb-vector`         | [Integrate TiDB Vector Search with SQLAlchemy](/ai/integrations/vector-search-integrate-with-sqlalchemy.md)
| Python   | peewee             | `pip install tidb-vector`         | [Integrate TiDB Vector Search with peewee](/ai/integrations/vector-search-integrate-with-peewee.md) |
| Python   | Django             | `pip install django-tidb[vector]` | [Integrate TiDB Vector Search with Django](/ai/integrations/vector-search-integrate-with-django-orm.md) |

## Cloud services

You can use third-party cloud embedding services to generate vectors and store them in TiDB.

The following table lists the supported cloud services and the corresponding tutorials:

| Cloud service  | Tutorial                                                                                                                  |
|----------------|---------------------------------------------------------------------------------------------------------------------------|
| Jina AI        | [Integrate Vector Search with Jina AI Embeddings API](/ai/integrations/vector-search-integrate-with-jinaai-embedding.md)  |
| Amazon Bedrock | [Integrate TiDB Vector Search with Amazon Bedrock](/ai/integrations/vector-search-integrate-with-amazon-bedrock.md)       |

## MCP server

The [TiDB MCP Server](/ai/integrations/tidb-mcp-server.md) is an open-source tool that lets you interact with TiDB databases using natural language instructions through the Model Context Protocol (MCP).

The following table lists the supported MCP clients and the corresponding setup guides:

| MCP client     | Guide                                                                  |
|----------------|------------------------------------------------------------------------|
| Claude Code    | [Claude Code](/ai/integrations/tidb-mcp-claude-code.md)                |
| Claude Desktop | [Claude Desktop](/ai/integrations/tidb-mcp-claude-desktop.md)          |
| Cursor         | [Cursor](/ai/integrations/tidb-mcp-cursor.md)                          |
| VS Code        | [VS Code](/ai/integrations/tidb-mcp-vscode.md)                         |
| Windsurf       | [Windsurf](/ai/integrations/tidb-mcp-windsurf.md)                      |
