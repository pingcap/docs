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

### TiDB Cloud CLI (Preview)

| Document | Description |
| --- | --- |
| [TiDB Cloud Command Line Interface Overview](/ai/ti/ti-overview.md) | Learn when to use the TiDB Cloud CLI, how it differs from the `ticloud` CLI and TiDB Cloud console, and which Starter and Filesystem workflows it supports. |
| [Get Started with TiDB Cloud CLI](/ai/ti/ti-quick-start.md) | Install and configure the TiDB Cloud CLI, then complete a first database or Filesystem operation. |

## Concepts

Understand the foundational concepts behind AI-powered search in TiDB.

| Document | Description |
| --- | --- |
| [Vector Search](/ai/concepts/vector-search-overview.md) | Comprehensive overview of vector search, including concepts, how it works, and use cases. |

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

### TiDB Cloud CLI (Preview)

The command reference follows the two-level `ti` command tree. Every command has a dedicated page with its syntax and examples. Expand **Command Reference** in the documentation navigation to browse commands by family.

#### Command reference

| Document | Description |
| --- | --- |
| [TiDB Cloud Command Line Interface Overview](/ai/ti/ti-overview.md) | Decide when to use the TiDB Cloud CLI and understand its scope relative to `ticloud` and the TiDB Cloud console. |
| [TiDB Cloud CLI Command Reference](/ai/ti/reference/ti-cli-reference.md) | Command tree, global flags, output, queries, dry-run, help, errors, aliases, and links to command pages. |
| [`ti configure`](/ai/ti/reference/commands/ti/ti-configure.md) | Configure a local profile interactively or non-interactively. |
| [`ti update`](/ai/ti/reference/commands/ti/ti-update.md) | Check for and install release updates. |
| [`ti db create-db-cluster`](/ai/ti/reference/commands/db/ti-db-create-db-cluster.md) | Start with the database command reference. |
| [`ti fs create-file-system`](/ai/ti/reference/commands/fs/ti-fs-create-file-system.md) | Start with the Filesystem command reference. |
| [`ti fs import-file-system-token`](/ai/ti/reference/commands/fs/ti-fs-import-file-system-token.md) | Restore local access from an existing FS token. |
| [`ti fs-git clone-git-workspace`](/ai/ti/reference/commands/fs-git/ti-fs-git-clone-git-workspace.md) | Start with the Filesystem Git command reference. |
| [`ti fs-journal create-journal`](/ai/ti/reference/commands/fs-journal/ti-fs-journal-create-journal.md) | Start with the Filesystem journal command reference. |
| [`ti fs-vault create-secret`](/ai/ti/reference/commands/fs-vault/ti-fs-vault-create-secret.md) | Start with the Filesystem Vault command reference. |
| [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md) | Profiles, precedence, local state, credentials, mount locators, and logs. |
| [TiDB Cloud CLI Regions, Security, and Limitations](/ai/ti/reference/ti-regions-security-and-limitations.md) | Placement, authentication boundaries, platforms, durability, and preview constraints. |
| [Troubleshoot TiDB Cloud CLI](/ai/ti/reference/ti-troubleshooting.md) | Diagnose authentication, quota, SQL, companion, selection, and mount failures. |

#### Scenarios for users and automation

| Document | Description |
| --- | --- |
| [Daily Workflow](/ai/ti/reference/ti-daily-workflow-example.md) | Manage one Starter cluster and Filesystem in a routine operator flow. |
| [Query SQL with Roles](/ai/ti/reference/ti-query-sql-with-roles-example.md) | Use explicit read-only, read-write, and admin SQL roles. |
| [Share a Filesystem Across Machines](/ai/ti/reference/ti-share-filesystem-across-machines-example.md) | Transfer an owner token securely and verify cross-machine visibility. |
| [Hand Off CI Artifacts Between Jobs](/ai/ti/reference/ti-ci-artifact-handoff-example.md) | Persist build output across isolated jobs without copying a complete TiDB Cloud CLI profile. |

#### Scenarios for AI agents

| Document | Description |
| --- | --- |
| [Agent Sandbox](/ai/ti/reference/ti-agent-sandbox-example.md) | Give a clean sandbox Filesystem access without TiDB Cloud API keys. |
| [Persistent Agent State](/ai/ti/reference/ti-persistent-agent-state-example.md) | Preserve plans, checkpoints, and results across disposable sandboxes. |
| [Parallel Agent Dataset](/ai/ti/reference/ti-parallel-agent-dataset-example.md) | Give multiple agents read-only access to one shared unstructured dataset. |
| [Git Workspace for Agents](/ai/ti/reference/ti-git-workspace-for-agents-example.md) | Prepare a mounted Git workspace and isolated linked worktree. |
| [Journal an Agent Workflow](/ai/ti/reference/ti-journal-agent-workflow-example.md) | Record structured events and verify their hash chain. |
| [Delegate Vault Secrets](/ai/ti/reference/ti-vault-agent-secrets-example.md) | Grant an agent temporary access to one secret field. |
