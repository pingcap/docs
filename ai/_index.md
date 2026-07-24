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
| [tdc Overview](/ai/tdc/tdc-overview.md) | Learn when to use tdc, how it differs from the legacy ticloud CLI and TiDB Cloud console, and which Starter and Filesystem workflows it supports. |
| [Get Started with tdc](/ai/tdc/tdc-quick-start.md) | Install and configure tdc, then complete a first database or Filesystem operation. |

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

The command reference follows the two-level tdc command tree. Every command has a dedicated page with its syntax and examples. Expand **Command Reference** in the documentation navigation to browse commands by family.

#### Command reference

| Document | Description |
| --- | --- |
| [tdc Overview](/ai/tdc/tdc-overview.md) | Decide when to use tdc and understand its scope relative to ticloud and the TiDB Cloud console. |
| [CLI Syntax and Global Behavior](/ai/tdc/reference/tdc-cli-reference.md) | Command tree, global flags, output, queries, dry-run, help, errors, aliases, and links to command pages. |
| [`tdc configure`](/ai/tdc/reference/commands/tdc/tdc-configure.md) | Configure a local profile interactively or non-interactively. |
| [`tdc update`](/ai/tdc/reference/commands/tdc/tdc-update.md) | Check for and install release updates. |
| [`tdc organization list-projects`](/ai/tdc/reference/commands/organization/tdc-organization-list-projects.md) | List accessible TiDB Cloud projects. |
| [`tdc db create-db-cluster`](/ai/tdc/reference/commands/db/tdc-db-create-db-cluster.md) | Start with the database command reference. |
| [`tdc fs create-file-system`](/ai/tdc/reference/commands/fs/tdc-fs-create-file-system.md) | Start with the Filesystem command reference. |
| [`tdc fs-git clone-git-workspace`](/ai/tdc/reference/commands/fs-git/tdc-fs-git-clone-git-workspace.md) | Start with the Filesystem Git command reference. |
| [`tdc fs-journal create-journal`](/ai/tdc/reference/commands/fs-journal/tdc-fs-journal-create-journal.md) | Start with the Filesystem journal command reference. |
| [`tdc fs-vault create-secret`](/ai/tdc/reference/commands/fs-vault/tdc-fs-vault-create-secret.md) | Start with the Filesystem Vault command reference. |
| [Configuration and Credentials](/ai/tdc/reference/tdc-configuration-and-credentials.md) | Profiles, precedence, local state, credentials, mount locators, and logs. |
| [Regions, Security, and Limitations](/ai/tdc/reference/tdc-regions-security-and-limitations.md) | Placement, authentication boundaries, platforms, durability, and Preview constraints. |
| [Troubleshooting](/ai/tdc/reference/tdc-troubleshooting.md) | Diagnose authentication, quota, SQL, companion, selection, and mount failures. |

#### Scenarios for users and automation

| Document | Description |
| --- | --- |
| [Daily Workflow](/ai/tdc/reference/tdc-daily-workflow-example.md) | Manage one Starter cluster and Filesystem in a routine operator flow. |
| [Query SQL with Roles](/ai/tdc/reference/tdc-query-sql-with-roles-example.md) | Use explicit read-only, read-write, and admin SQL roles. |
| [Share a Filesystem Across Machines](/ai/tdc/reference/tdc-share-filesystem-across-machines-example.md) | Transfer an owner token securely and verify cross-machine visibility. |
| [Hand Off CI Artifacts Between Jobs](/ai/tdc/reference/tdc-ci-artifact-handoff-example.md) | Persist build output across isolated jobs without copying a complete tdc profile. |

#### Scenarios for AI agents

| Document | Description |
| --- | --- |
| [Agent Sandbox](/ai/tdc/reference/tdc-agent-sandbox-example.md) | Give a clean sandbox Filesystem access without TiDB Cloud API keys. |
| [Persistent Agent State](/ai/tdc/reference/tdc-persistent-agent-state-example.md) | Preserve plans, checkpoints, and results across disposable sandboxes. |
| [Parallel Agent Dataset](/ai/tdc/reference/tdc-parallel-agent-dataset-example.md) | Give multiple agents read-only access to one shared unstructured dataset. |
| [Git Workspace for Agents](/ai/tdc/reference/tdc-git-workspace-for-agents-example.md) | Prepare a mounted Git workspace and isolated linked worktree. |
| [Journal an Agent Workflow](/ai/tdc/reference/tdc-journal-agent-workflow-example.md) | Record structured events and verify their hash chain. |
| [Delegate Vault Secrets](/ai/tdc/reference/tdc-vault-agent-secrets-example.md) | Grant an agent temporary access to one secret field. |
