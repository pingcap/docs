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
| [Get Started with Vector Search via Python](/ai/quickstart-via-python.md) | Build your first AI application with TiDB in minutes using Python. |
| [Get Started with Vector Search via SQL](/ai/quickstart-via-sql.md) | Quick start guide for vector search using SQL. |
| [Get Started with TiDB Cloud CLI](/ai/ti/ti-quick-start.md) | Install and configure the TiDB Cloud CLI, then complete a first database or Filesystem operation. |

## Guides

Step-by-step guides for building AI applications with TiDB using the [`pytidb`](https://github.com/pingcap/pytidb) SDK or SQL.

### Connect to TiDB

| Document | Description |
| --- | --- |
| [Connect to TiDB via Python](/ai/guides/connect.md) | Connect to TiDB Cloud or TiDB Self-Managed using `pytidb`. |

### Search & retrieval

#### Vector search

| Document | Description |
| --- | --- |
| [Vector Search Overview](/ai/concepts/vector-search-overview.md) | Comprehensive overview of vector search, including concepts, how it works, and use cases. |
| [Vector Search Guide](/ai/guides/vector-search.md) | Perform semantic similarity searches using `pytidb`. |
| [Vector Search Example](/ai/examples/vector-search-with-pytidb.md) | Semantic similarity search example with `pytidb`. |

#### Full-text search

| Document | Description |
| --- | --- |
| [Full-Text Search via Python](/ai/guides/vector-search-full-text-search-python.md) | Keyword-based text search with BM25 ranking using `pytidb`. |
| [Full-Text Search via SQL](/ai/guides/vector-search-full-text-search-sql.md) | Keyword-based text search with BM25 ranking using SQL. |
| [Full-Text Search Example](/ai/examples/fulltext-search-with-pytidb.md) | Full-text search example with `pytidb`. |

#### Hybrid search

| Document | Description |
| --- | --- |
| [Hybrid Search Guide](/ai/guides/vector-search-hybrid-search.md) | Combine vector and full-text search for better results. |
| [Hybrid Search Example](/ai/examples/hybrid-search-with-pytidb.md) | Hybrid search example with `pytidb`. |

#### Auto embeddings

| Document | Description |
| --- | --- |
| [Auto Embedding Guide](/ai/guides/auto-embedding.md) | Automatically generate embeddings on data insertion. |
| [Auto Embedding Example](/ai/examples/auto-embedding-with-pytidb.md) | Auto embedding example with `pytidb`. |

#### Image search

| Document | Description |
| --- | --- |
| [Image Search Guide](/ai/guides/image-search.md) | Search images using multimodal embeddings. |
| [Image Search Example](/ai/examples/image-search-with-pytidb.md) | Multimodal image search example with Jina AI embeddings. |

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

### Build AI applications

| Document | Description |
| --- | --- |
| [RAG Example](/ai/examples/rag-with-pytidb.md) | Build a Retrieval-Augmented Generation application. |
| [Conversational Memory Example](/ai/examples/memory-with-pytidb.md) | Persistent memory for AI agents and chatbots. |
| [Text-to-SQL Example](/ai/examples/text2sql-with-pytidb.md) | Convert natural language to SQL queries. |

### TiDB Cloud CLI

| Document | Description |
| --- | --- |
| [TiDB Cloud CLI Overview](/ai/ti/ti-overview.md) | Learn when to use the TiDB Cloud CLI, how it differs from the `ticloud` CLI and TiDB Cloud console, and which Starter and Filesystem workflows it supports. |
| [Install, Configure, and Update TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md) | Install, configure profiles, and keep the CLI up to date. |
| [Manage TiDB Cloud Starter Instances](/ai/ti/guides/manage-starter-instances.md) | Create, list, branch, query, and delete Starter instances. |

#### Manage TiDB Cloud Filesystem

| Document | Description |
| --- | --- |
| [Manage Filesystem Resources](/ai/ti/guides/manage-filesystem-resources.md) | Create, list, check, and delete Filesystems. |
| [Configure Filesystem AI Providers](/ai/ti/guides/configure-filesystem-ai-providers.md) | Set up extract and embedding configurations for AI-powered pipelines. |
| [Manage Filesystem Tokens](/ai/ti/guides/manage-filesystem-tokens.md) | Generate, import, enable, disable, and refresh Filesystem tokens. |
| [Work with Filesystem Data](/ai/ti/guides/work-with-filesystem-data.md) | Copy, read, list, move, and delete files and directories. |
| [Manage Filesystem Layers and Checkpoints](/ai/ti/guides/manage-filesystem-layers.md) | Create, fork, diff, commit, and roll back layers. |
| [Mount a TiDB Cloud Filesystem](/ai/ti/guides/mount-filesystem.md) | Mount, drain, pack, and unpack Filesystems. |
| [Manage Git Workspaces](/ai/ti/guides/manage-git-workspaces.md) | Clone Git repositories and manage worktrees on Filesystems. |
| [Use Filesystem Journals](/ai/ti/guides/use-filesystem-journals.md) | Create journals, append and search entries, and verify hash chains. |
| [Manage Filesystem Vault Secrets](/ai/ti/guides/manage-filesystem-vault-secrets.md) | Store, grant, mount, and audit secrets in a Filesystem vault. |

#### Scenarios for users and automation

| Document | Description |
| --- | --- |
| [Daily Workflow](/ai/ti/reference/ti-daily-workflow-example.md) | Manage one TiDB Cloud Starter instance and Filesystem in a routine operator flow. |
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

#### Command reference

The command reference follows the `ti` command tree. Every command has a dedicated page with its syntax and examples.

| Document | Description |
| --- | --- |
| [TiDB Cloud CLI Command Reference](/ai/ti/reference/ti-cli-reference.md) | Command tree, global flags, output, queries, dry-run, help, errors, aliases, and links to command pages. |
| [`ti configure`](/ai/ti/reference/commands/ti/ti-configure.md) | Configure a local profile interactively or non-interactively. |
| [`ti update`](/ai/ti/reference/commands/ti/ti-update.md) | Check for and install release updates. |
| [`ti db` commands](/ai/ti/reference/ti-starter-database.md) | Commands for managing TiDB Cloud Starter instances. |
| [`ti fs` commands](/ai/ti/reference/ti-filesystem.md) | Commands for managing TiDB Cloud Filesystems. |
| [`ti fs-git` commands](/ai/ti/reference/ti-filesystem-git.md) | Commands for managing TiDB Cloud Filesystem Git workspaces. |
| [`ti fs-journal` commands](/ai/ti/reference/ti-filesystem-journal.md) | Commands for managing TiDB Cloud Filesystem journals. |
| [`ti fs-vault` commands](/ai/ti/reference/ti-filesystem-vault.md) | Commands for managing TiDB Cloud Filesystem vault secrets. |
| [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md) | Profiles, precedence, local state, credentials, mount locators, and logs. |
| [TiDB Cloud CLI Regions, Security, and Limitations](/ai/ti/reference/ti-regions-security-and-limitations.md) | Placement, authentication boundaries, platforms, durability, and preview constraints. |
| [Troubleshoot TiDB Cloud CLI](/ai/ti/reference/ti-troubleshooting.md) | Diagnose authentication, quota, SQL, companion, selection, and mount failures. |

## Integrations

Integrate TiDB with popular AI frameworks, embedding providers, and development tools.

| Document | Description |
| --- | --- |
| [Integration Overview](/ai/integrations/vector-search-integration-overview.md) | Overview of all available integrations. |

### Auto embedding

| Document | Description |
| --- | --- |
| [Auto Embedding Overview](/ai/integrations/vector-search-auto-embedding-overview.md) | Unified interface for embedding models in TiDB. |
| [OpenAI](/ai/integrations/vector-search-auto-embedding-openai.md) | Integrate OpenAI embedding models. |
| [OpenAI Compatible](/ai/integrations/embedding-openai-compatible.md) | Integrate OpenAI-compatible embedding providers. |
| [Jina AI](/ai/integrations/vector-search-auto-embedding-jina-ai.md) | Integrate Jina AI embedding models. |
| [Cohere](/ai/integrations/vector-search-auto-embedding-cohere.md) | Integrate Cohere embedding models. |
| [Google Gemini](/ai/integrations/vector-search-auto-embedding-gemini.md) | Integrate Google Gemini embedding models. |
| [Hugging Face](/ai/integrations/vector-search-auto-embedding-huggingface.md) | Integrate Hugging Face embedding models. |
| [NVIDIA NIM](/ai/integrations/vector-search-auto-embedding-nvidia-nim.md) | Integrate NVIDIA NIM embedding models. |
| [Amazon Titan](/ai/integrations/vector-search-auto-embedding-amazon-titan.md) | Integrate Amazon Titan embedding models. |

### AI frameworks

| Document | Description |
| --- | --- |
| [LlamaIndex](/ai/integrations/vector-search-integrate-with-llamaindex.md) | Use TiDB as a vector store with LlamaIndex. |

### ORM libraries

| Document | Description |
| --- | --- |
| [SQLAlchemy](/ai/integrations/vector-search-integrate-with-sqlalchemy.md) | Use TiDB vector search with SQLAlchemy ORM. |
| [Django ORM](/ai/integrations/vector-search-integrate-with-django-orm.md) | Use TiDB vector search with Django ORM. |
| [Peewee](/ai/integrations/vector-search-integrate-with-peewee.md) | Use TiDB vector search with Peewee ORM. |

### Cloud services

| Document | Description |
| --- | --- |
| [Jina AI Embedding](/ai/integrations/vector-search-integrate-with-jinaai-embedding.md) | Use Jina AI embedding API with TiDB. |
| [Amazon Bedrock](/ai/integrations/vector-search-integrate-with-amazon-bedrock.md) | Use Amazon Bedrock with TiDB. |

### MCP server

| Document | Description |
| --- | --- |
| [MCP Server Overview](/ai/integrations/tidb-mcp-server.md) | Connect TiDB to AI-powered IDEs using the TiDB MCP server. |
| [Claude Code](/ai/integrations/tidb-mcp-claude-code.md) | Set up TiDB MCP server with Claude Code. |
| [Claude Desktop](/ai/integrations/tidb-mcp-claude-desktop.md) | Set up TiDB MCP server with Claude Desktop. |
| [Cursor](/ai/integrations/tidb-mcp-cursor.md) | Set up TiDB MCP server with Cursor. |
| [VS Code](/ai/integrations/tidb-mcp-vscode.md) | Set up TiDB MCP server with VS Code. |
| [Windsurf](/ai/integrations/tidb-mcp-windsurf.md) | Set up TiDB MCP server with Windsurf. |

## Reference

Technical reference documentation for TiDB's AI and vector search features.

| Document | Description |
| --- | --- |
| [Vector Data Types](/ai/reference/vector-search-data-types.md) | Vector column types and usage. |
| [Vector Functions and Operators](/ai/reference/vector-search-functions-and-operators.md) | Distance functions and vector operations. |
| [Vector Search Index](/ai/reference/vector-search-index.md) | Create and manage vector indexes for performance. |
| [Vector Search Performance Tuning](/ai/reference/vector-search-improve-performance.md) | Optimize vector search performance. |
| [Vector Search Limitations](/ai/reference/vector-search-limitations.md) | Current limitations and constraints. |
