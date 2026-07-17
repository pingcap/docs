---
title: TiDB for AI
summary: Build modern AI applications with TiDB's integrated vector search, full-text search, and seamless Python SDK.
---

# TiDB for AI

TiDB is a distributed SQL database designed for modern AI applications, offering integrated vector search, full-text search, and hybrid search capabilities. This document provides an overview of the AI features and tools available for building AI-powered applications with TiDB.

## Quick start

Get up and running quickly with TiDB's AI capabilities.

| Document | Description |
| --- | --- |
| [Get Started with Python](/ai/quickstart-via-python.md) | Build your first AI application with TiDB in minutes using Python. |
| [Get Started with SQL](/ai/quickstart-via-sql.md) | Quick start guide for vector search using SQL. |

### TiDB Cloud CLI (tdc) (Preview)

| Document | Description |
| --- | --- |
| [tdc Overview](/ai/tdc/tdc-overview.md) | Understand what tdc manages and how it uses its bundled Filesystem companion. |
| [Get Started with tdc](/ai/tdc/tdc-quick-start.md) | Install and configure tdc, then complete a first database or Filesystem operation. |

## Concepts

Understand the foundational concepts behind AI-powered search in TiDB.

| Document | Description |
| --- | --- |
| [Vector Search](/ai/concepts/vector-search-overview.md) | Comprehensive overview of vector search, including concepts, how it works, and use cases. |
| [tdc Concepts and Architecture (Preview)](/ai/tdc/concepts/tdc-concepts-and-architecture.md) | Understand profiles, regions, credentials, SQL roles, Filesystems, and the Drive9 companion boundary. |

## Guides

Step-by-step guides for building AI applications with TiDB using the [`pytidb`](https://github.com/pingcap/pytidb) SDK or SQL.

| Document | Description |
| --- | --- |
| [Connect to TiDB](/ai/guides/connect.md) | Connect to TiDB Cloud or TiDB Self-Managed using `pytidb`. |
| [Working with Tables](/ai/guides/tables.md) | Create, query, and manage tables with vector fields. |
| [Vector Search](/ai/guides/vector-search.md) | Perform semantic similarity searches using `pytidb`. |
| [Full-Text Search](/ai/guides/vector-search-full-text-search-python.md) | Keyword-based text search with BM25 ranking. |
| [Hybrid Search](/ai/guides/vector-search-hybrid-search.md) | Combine vector and full-text search for better results. |
| [Image Search](/ai/guides/image-search.md) | Search images using multimodal embeddings. |
| [Auto Embedding](/ai/guides/auto-embedding.md) | Automatically generate embeddings on data insertion. |
| [Filtering](/ai/guides/filtering.md) | Filter search results with metadata conditions. |

### TiDB Cloud CLI (tdc) (Preview)

| Document | Description |
| --- | --- |
| [Install, Configure, and Update tdc](/ai/tdc/guides/tdc-install-configure-update.md) | Install release binaries, configure profiles, update, and uninstall tdc. |
| [Organization](/ai/tdc/guides/tdc-organization.md) | List projects and understand virtual-project selection. |
| [Starter Database](/ai/tdc/guides/tdc-starter-database.md) | Manage clusters, branches, SQL users, connection strings, and SQL execution. |
| [Filesystem](/ai/tdc/guides/tdc-filesystem.md) | Manage resources, data, layers, packs, and FUSE or WebDAV mounts. |
| [Filesystem Git](/ai/tdc/guides/tdc-filesystem-git.md) | Clone, hydrate, and manage linked Git worktrees. |
| [Filesystem Journal](/ai/tdc/guides/tdc-filesystem-journal.md) | Record, search, and verify append-only workflow events. |
| [Filesystem Vault](/ai/tdc/guides/tdc-filesystem-vault.md) | Store secrets, delegate access, audit, inject, and mount a read-only vault. |

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

### TiDB Cloud CLI (tdc) (Preview)

| Document | Description |
| --- | --- |
| [Agent Sandbox](/ai/tdc/examples/tdc-agent-sandbox-example.md) | Give a clean sandbox Filesystem access without TiDB Cloud API keys. |
| [Daily Workflow](/ai/tdc/examples/tdc-daily-workflow-example.md) | Manage one Starter cluster and Filesystem in a routine operator flow. |
| [Query SQL with Roles](/ai/tdc/examples/tdc-query-sql-with-roles-example.md) | Use explicit read-only, read-write, and admin SQL roles. |
| [Share a Filesystem Across Machines](/ai/tdc/examples/tdc-share-filesystem-across-machines-example.md) | Transfer an owner token securely and verify cross-machine visibility. |
| [Git Workspace for Agents](/ai/tdc/examples/tdc-git-workspace-for-agents-example.md) | Prepare a mounted Git workspace and isolated linked worktree. |
| [Journal an Agent Workflow](/ai/tdc/examples/tdc-journal-agent-workflow-example.md) | Record structured events and verify their hash chain. |
| [Delegate Vault Secrets](/ai/tdc/examples/tdc-vault-agent-secrets-example.md) | Grant an agent temporary access to one secret field. |

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

### TiDB Cloud CLI (tdc) (Preview)

| Document | Description |
| --- | --- |
| [CLI Reference](/ai/tdc/reference/tdc-cli-reference.md) | Global flags, output, queries, dry-run, help, errors, and aliases. |
| [Configuration and Credentials](/ai/tdc/reference/tdc-configuration-and-credentials.md) | Profiles, precedence, local state, credentials, mount locators, and logs. |
| [Regions, Security, and Limitations](/ai/tdc/reference/tdc-regions-security-and-limitations.md) | Placement, authentication boundaries, platforms, durability, and Preview constraints. |
| [Troubleshooting](/ai/tdc/reference/tdc-troubleshooting.md) | Diagnose authentication, quota, SQL, companion, selection, and mount failures. |
