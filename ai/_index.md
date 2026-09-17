---
title: TiDB for AI
summary: Build AI applications and agent workflows with TiDB using SQL, integrated search, TiDB Cloud Starter, and persistent shared Filesystems.
---

# TiDB for AI

TiDB provides data and workspace capabilities for building AI applications and running AI agent workflows.

- For application development, you can use SQL or [Python SDK for TiDB AI (`pytidb`)](https://github.com/pingcap/pytidb) with structured data, vector search, full-text search, hybrid search, and AI-powered retrieval.
- For AI agents and automation, you can use [TiDB Cloud CLI (`ti`)](https://github.com/tidbcloud/ti-cli) to manage TiDB Cloud Starter instances and SQL workflows, and use [TiDB Cloud Filesystems](/tidb-cloud-filesystem/_index.md) as persistent, shared storage across local machines, CI jobs, and ephemeral agent sandboxes. Filesystems also support mounted workspaces, Git workflows, journals, and delegated secrets.

## Get started

Choose a path based on what you want to build:

| Goal | Start here |
| --- | --- |
| Build an AI application with vector search | [Get Started with Vector Search via Python](/ai/quickstart-via-python.md) or [Get Started with Vector Search via SQL](/ai/quickstart-via-sql.md) |
| Build agent and automation workflows with TiDB Cloud | [Get Started with TiDB Cloud CLI](/ai/ti/ti-quick-start.md) |

## Build AI applications with TiDB

Use the [`pytidb`](https://github.com/pingcap/pytidb) SDK or SQL to connect to TiDB, search and retrieve data, and build AI-powered applications.

### Connect to TiDB

| Document | Description |
| --- | --- |
| [Connect to TiDB via Python](/ai/guides/connect.md) | Connect to TiDB Cloud or TiDB Self-Managed using `pytidb`. |

### Search & retrieval

#### Vector search

| Document | Description |
| --- | --- |
| [Vector Search Overview](/ai/guides/vector-search-overview.md) | Comprehensive overview of vector search, including concepts, how it works, and use cases. |
| [Vector Search Guide](/ai/guides/vector-search.md) | Perform semantic similarity searches using `pytidb`. |
| [Vector Search Example](/ai/guides/vector-search-with-pytidb.md) | Semantic similarity search example with `pytidb`. |

#### Full-text search

| Document | Description |
| --- | --- |
| [Full-Text Search via Python](/ai/guides/vector-search-full-text-search-python.md) | Keyword-based text search with BM25 ranking using `pytidb`. |
| [Full-Text Search via SQL](/ai/guides/vector-search-full-text-search-sql.md) | Keyword-based text search with BM25 ranking using SQL. |
| [Full-Text Search Example](/ai/guides/fulltext-search-with-pytidb.md) | Full-text search example with `pytidb`. |

#### Hybrid search

| Document | Description |
| --- | --- |
| [Hybrid Search Guide](/ai/guides/vector-search-hybrid-search.md) | Combine vector and full-text search for better results. |
| [Hybrid Search Example](/ai/guides/hybrid-search-with-pytidb.md) | Hybrid search example with `pytidb`. |

#### Auto embeddings

| Document | Description |
| --- | --- |
| [Auto Embedding Guide](/ai/guides/auto-embedding.md) | Automatically generate embeddings on data insertion. |
| [Auto Embedding Example](/ai/guides/auto-embedding-with-pytidb.md) | Auto embedding example with `pytidb`. |

#### Image search

| Document | Description |
| --- | --- |
| [Image Search Guide](/ai/guides/image-search.md) | Search images using multimodal embeddings. |
| [Image Search Example](/ai/guides/image-search-with-pytidb.md) | Multimodal image search example with Jina AI embeddings. |

#### Reranking

| Document | Description |
| --- | --- |
| [Reranking](/ai/guides/reranking.md) | Rerank search results for improved relevance. |

### Work with data

| Document | Description |
| --- | --- |
| [Working with Tables](/ai/guides/tables.md) | Create, query, and manage tables with vector fields. |
| [Filtering](/ai/guides/filtering.md) | Filter search results with metadata conditions. |
| [Join Queries](/ai/guides/join-queries.md) | Perform join queries across tables. |
| [Raw SQL Queries](/ai/guides/raw-queries.md) | Execute raw SQL queries directly. |
| [Transactions](/ai/guides/transactions.md) | Use transactions for data consistency. |

### Application examples

| Document | Description |
| --- | --- |
| [RAG Example](/ai/guides/rag-with-pytidb.md) | Build a Retrieval-Augmented Generation application. |
| [Conversational Memory Example](/ai/guides/memory-with-pytidb.md) | Persistent memory for AI agents and chatbots. |
| [Text-to-SQL Example](/ai/guides/text2sql-with-pytidb.md) | Convert natural language to SQL queries. |

## Build agent and automation workflows with TiDB Cloud CLI

The TiDB Cloud CLI (`ti`) lets users, scripts, CI jobs, and AI agents manage TiDB Cloud from a terminal. Use it to automate TiDB Cloud Starter and SQL operations or to keep files and workspaces available independently of the machines and sandboxes that use them.

| What you want to do | Start here |
| --- | --- |
| Understand what `ti` manages and when to use it | [TiDB Cloud CLI Overview](/ai/ti/ti-overview.md) |
| Install and configure `ti`, then complete a first workflow | [Get Started with TiDB Cloud CLI](/ai/ti/ti-quick-start.md) |
| Automate TiDB Cloud Starter instance, branch, and SQL operations | [Manage TiDB Cloud Starter Instances](/ai/ti/guides/manage-starter-instances.md) |
| Persist and share files across machines, CI jobs, and sandboxes | [Use TiDB Cloud Filesystem with TiDB Cloud CLI](/ai/ti/guides/manage-filesystems-via-cli.md) |
| Use mounted workspaces, Git workspaces, journals, or delegated secrets | [Mount a Filesystem](/tidb-cloud-filesystem/filesystem-mount.md), [Manage Git Workspaces](/tidb-cloud-filesystem/manage-git-workspaces.md), [Use Filesystem Journals](/tidb-cloud-filesystem/use-filesystem-journals.md), and [Manage Filesystem Vault Secrets](/tidb-cloud-filesystem/manage-filesystem-vault-secrets.md) |
| Follow an end-to-end automation or agent example | [Run a Daily TiDB Cloud CLI Workflow](/ai/ti/guides/ti-daily-workflow-example.md) or [Use TiDB Cloud Filesystem in an Agent Sandbox](/ai/ti/guides/ti-agent-sandbox-example.md) |
| Look up commands, global options, output behavior, and errors | [TiDB Cloud CLI Command Reference](/ai/ti/reference/ti-cli-reference.md) |

## Integrations

Connect TiDB to embedding providers, AI frameworks, application libraries, cloud services, and AI development tools.

| Integration area | Start here |
| --- | --- |
| All integrations | [AI Integrations for TiDB](/ai/integrations/vector-search-integration-overview.md) |
| Auto Embedding providers | [Auto Embedding Overview](/ai/integrations/vector-search-auto-embedding-overview.md) |
| AI frameworks | [LlamaIndex](/ai/integrations/vector-search-integrate-with-llamaindex.md) |
| ORM libraries | [SQLAlchemy](/ai/integrations/vector-search-integrate-with-sqlalchemy.md), [Django ORM](/ai/integrations/vector-search-integrate-with-django-orm.md), and [Peewee](/ai/integrations/vector-search-integrate-with-peewee.md) |
| Cloud embedding services | [Jina AI Embedding](/ai/integrations/vector-search-integrate-with-jinaai-embedding.md) and [Amazon Bedrock](/ai/integrations/vector-search-integrate-with-amazon-bedrock.md) |
| MCP clients and AI development tools | [TiDB MCP Server](/ai/integrations/tidb-mcp-server.md) |

## Reference

Technical reference documentation for TiDB's AI and vector search features.

| Document | Description |
| --- | --- |
| [Vector Data Types](/ai/reference/vector-search-data-types.md) | Vector column types and usage. |
| [Vector Functions and Operators](/ai/reference/vector-search-functions-and-operators.md) | Distance functions and vector operations. |
| [Vector Search Index](/ai/reference/vector-search-index.md) | Create and manage vector indexes for performance. |
| [Vector Search Performance Tuning](/ai/reference/vector-search-improve-performance.md) | Optimize vector search performance. |
| [Vector Search Limitations](/ai/reference/vector-search-limitations.md) | Current limitations and constraints. |
