<!-- markdownlint-disable MD007 -->
<!-- markdownlint-disable MD041 -->

# Table of Contents

## QUICK START

- [Get Started with Vector Search via Python](/ai/quickstart-via-python.md)
- [Get Started with Vector Search via SQL](/ai/quickstart-via-sql.md)
- [Get Started with TiDB Cloud CLI (tdc)](/ai/tdc/tdc-quick-start.md)

## CONCEPTS

- [Vector Search](/ai/concepts/vector-search-overview.md)

## GUIDES

- [Connect to TiDB](/ai/guides/connect.md)
- [Working with Tables](/ai/guides/tables.md)
- Search Features
  - [Vector Search](/ai/guides/vector-search.md)
  - Full-Text Search
    - [Full-Text Search via Python](/ai/guides/vector-search-full-text-search-python.md)
    - [Full-Text Search via SQL](/ai/guides/vector-search-full-text-search-sql.md)
  - [Hybrid Search](/ai/guides/vector-search-hybrid-search.md)
  - [Image Search](/ai/guides/image-search.md)
- Advanced Search Features
  - [Auto Embedding](/ai/guides/auto-embedding.md)
  - [Filtering](/ai/guides/filtering.md)
  - [Reranking](/ai/guides/reranking.md)
  - [Join Queries](/ai/guides/join-queries.md)
  - [Raw SQL Queries](/ai/guides/raw-queries.md)
  - [Transactions](/ai/guides/transactions.md)

## EXAMPLES

- [Basic CRUD Operations](/ai/examples/basic-with-pytidb.md)
- [Auto Embedding](/ai/examples/auto-embedding-with-pytidb.md)
- Search & Retrieval
  - [Vector Search](/ai/examples/vector-search-with-pytidb.md)
  - [Full-Text Search](/ai/examples/fulltext-search-with-pytidb.md)
  - [Hybrid Search](/ai/examples/hybrid-search-with-pytidb.md)
  - [Image Search](/ai/examples/image-search-with-pytidb.md)
- AI Applications
  - [RAG Application](/ai/examples/rag-with-pytidb.md)
  - [Conversational Memory](/ai/examples/memory-with-pytidb.md)
  - [Text-to-SQL](/ai/examples/text2sql-with-pytidb.md)

## INTEGRATIONS

- [Integration Overview](/ai/integrations/vector-search-integration-overview.md)
- Auto Embedding
  - [Overview](/ai/integrations/vector-search-auto-embedding-overview.md)
  - [OpenAI](/ai/integrations/vector-search-auto-embedding-openai.md)
  - [OpenAI Compatible](/ai/integrations/embedding-openai-compatible.md)
  - [Jina AI](/ai/integrations/vector-search-auto-embedding-jina-ai.md)
  - [Cohere](/ai/integrations/vector-search-auto-embedding-cohere.md)
  - [Google Gemini](/ai/integrations/vector-search-auto-embedding-gemini.md)
  - [Hugging Face](/ai/integrations/vector-search-auto-embedding-huggingface.md)
  - [NVIDIA NIM](/ai/integrations/vector-search-auto-embedding-nvidia-nim.md)
  - [Amazon Titan](/ai/integrations/vector-search-auto-embedding-amazon-titan.md)
- AI Frameworks
  - [LangChain](/ai/integrations/vector-search-integrate-with-langchain.md)
  - [LlamaIndex](/ai/integrations/vector-search-integrate-with-llamaindex.md)
- ORM Libraries
  - [SQLAlchemy](/ai/integrations/vector-search-integrate-with-sqlalchemy.md)
  - [Django ORM](/ai/integrations/vector-search-integrate-with-django-orm.md)
  - [Peewee](/ai/integrations/vector-search-integrate-with-peewee.md)
- Cloud Services
  - [Jina AI Embedding](/ai/integrations/vector-search-integrate-with-jinaai-embedding.md)
  - [Amazon Bedrock](/ai/integrations/vector-search-integrate-with-amazon-bedrock.md)
- MCP Server
  - [Overview](/ai/integrations/tidb-mcp-server.md)
  - [Claude Code](/ai/integrations/tidb-mcp-claude-code.md)
  - [Claude Desktop](/ai/integrations/tidb-mcp-claude-desktop.md)
  - [Cursor](/ai/integrations/tidb-mcp-cursor.md)
  - [VS Code](/ai/integrations/tidb-mcp-vscode.md)
  - [Windsurf](/ai/integrations/tidb-mcp-windsurf.md)

## REFERENCE

- [Vector Data Types](/ai/reference/vector-search-data-types.md)
- [Functions and Operators](/ai/reference/vector-search-functions-and-operators.md)
- [Vector Search Index](/ai/reference/vector-search-index.md)
- [Performance Tuning](/ai/reference/vector-search-improve-performance.md)
- [Limitations](/ai/reference/vector-search-limitations.md)
- [Changelogs](/ai/reference/vector-search-changelogs.md)
- TiDB Cloud CLI (tdc)
  - [Overview](/ai/tdc/tdc-overview.md)
  - Command Reference
    - [CLI Syntax and Global Behavior](/ai/tdc/reference/tdc-cli-reference.md)
    - [Install, Configure, and Update](/ai/tdc/reference/tdc-install-configure-update.md)
    - [Organization and Projects](/ai/tdc/reference/tdc-organization.md)
    - [Starter Databases and SQL](/ai/tdc/reference/tdc-starter-database.md)
    - [Filesystem](/ai/tdc/reference/tdc-filesystem.md)
    - [Filesystem Git Workspaces](/ai/tdc/reference/tdc-filesystem-git.md)
    - [Filesystem Journals](/ai/tdc/reference/tdc-filesystem-journal.md)
    - [Filesystem Vault](/ai/tdc/reference/tdc-filesystem-vault.md)
  - Scenarios for Users and Automation
    - [Automate Daily Database Operations](/ai/tdc/reference/tdc-daily-workflow-example.md)
    - [Run SQL Queries with Role-Based Access](/ai/tdc/reference/tdc-query-sql-with-roles-example.md)
    - [Share a Filesystem Across Machines](/ai/tdc/reference/tdc-share-filesystem-across-machines-example.md)
    - [Hand Off CI Artifacts Between Jobs](/ai/tdc/reference/tdc-ci-artifact-handoff-example.md)
  - Scenarios for AI Agents
    - [Set Up an Agent Sandbox Environment](/ai/tdc/reference/tdc-agent-sandbox-example.md)
    - [Persist Agent State Across Sandboxes](/ai/tdc/reference/tdc-persistent-agent-state-example.md)
    - [Share a Read-Only Dataset Across Parallel Agents](/ai/tdc/reference/tdc-parallel-agent-dataset-example.md)
    - [Set Up a Git Workspace for AI Agents](/ai/tdc/reference/tdc-git-workspace-for-agents-example.md)
    - [Record Agent Workflows in a Journal](/ai/tdc/reference/tdc-journal-agent-workflow-example.md)
    - [Delegate Secrets Securely to Agents](/ai/tdc/reference/tdc-vault-agent-secrets-example.md)
  - [Configuration and Credentials](/ai/tdc/reference/tdc-configuration-and-credentials.md)
  - [Regions, Security, and Limitations](/ai/tdc/reference/tdc-regions-security-and-limitations.md)
  - [Troubleshooting](/ai/tdc/reference/tdc-troubleshooting.md)
