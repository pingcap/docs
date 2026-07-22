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
    - [configure](/ai/tdc/reference/commands/tdc/tdc-configure.md)
    - [update](/ai/tdc/reference/commands/tdc/tdc-update.md)
    - organization
      - [list-projects](/ai/tdc/reference/commands/organization/tdc-organization-list-projects.md)
    - db
      - [create-db-cluster](/ai/tdc/reference/commands/db/tdc-db-create-db-cluster.md)
      - [list-db-clusters](/ai/tdc/reference/commands/db/tdc-db-list-db-clusters.md)
      - [describe-db-cluster](/ai/tdc/reference/commands/db/tdc-db-describe-db-cluster.md)
      - [update-db-cluster](/ai/tdc/reference/commands/db/tdc-db-update-db-cluster.md)
      - [delete-db-cluster](/ai/tdc/reference/commands/db/tdc-db-delete-db-cluster.md)
      - [create-db-cluster-branch](/ai/tdc/reference/commands/db/tdc-db-create-db-cluster-branch.md)
      - [list-db-cluster-branches](/ai/tdc/reference/commands/db/tdc-db-list-db-cluster-branches.md)
      - [describe-db-cluster-branch](/ai/tdc/reference/commands/db/tdc-db-describe-db-cluster-branch.md)
      - [delete-db-cluster-branch](/ai/tdc/reference/commands/db/tdc-db-delete-db-cluster-branch.md)
      - [create-db-sql-users](/ai/tdc/reference/commands/db/tdc-db-create-db-sql-users.md)
      - [format-db-connection-string](/ai/tdc/reference/commands/db/tdc-db-format-db-connection-string.md)
      - [execute-sql-statement](/ai/tdc/reference/commands/db/tdc-db-execute-sql-statement.md)
    - fs
      - [create-file-system](/ai/tdc/reference/commands/fs/tdc-fs-create-file-system.md)
      - [list-file-systems](/ai/tdc/reference/commands/fs/tdc-fs-list-file-systems.md)
      - [describe-file-system](/ai/tdc/reference/commands/fs/tdc-fs-describe-file-system.md)
      - [set-default-file-system](/ai/tdc/reference/commands/fs/tdc-fs-set-default-file-system.md)
      - [unset-default-file-system](/ai/tdc/reference/commands/fs/tdc-fs-unset-default-file-system.md)
      - [check-file-system](/ai/tdc/reference/commands/fs/tdc-fs-check-file-system.md)
      - [delete-file-system](/ai/tdc/reference/commands/fs/tdc-fs-delete-file-system.md)
      - [copy-file](/ai/tdc/reference/commands/fs/tdc-fs-copy-file.md)
      - [read-file](/ai/tdc/reference/commands/fs/tdc-fs-read-file.md)
      - [list-files](/ai/tdc/reference/commands/fs/tdc-fs-list-files.md)
      - [describe-file](/ai/tdc/reference/commands/fs/tdc-fs-describe-file.md)
      - [move-file](/ai/tdc/reference/commands/fs/tdc-fs-move-file.md)
      - [delete-file](/ai/tdc/reference/commands/fs/tdc-fs-delete-file.md)
      - [create-directory](/ai/tdc/reference/commands/fs/tdc-fs-create-directory.md)
      - [chmod-file](/ai/tdc/reference/commands/fs/tdc-fs-chmod-file.md)
      - [create-symlink](/ai/tdc/reference/commands/fs/tdc-fs-create-symlink.md)
      - [create-hardlink](/ai/tdc/reference/commands/fs/tdc-fs-create-hardlink.md)
      - [search-file-content](/ai/tdc/reference/commands/fs/tdc-fs-search-file-content.md)
      - [find-files](/ai/tdc/reference/commands/fs/tdc-fs-find-files.md)
      - [create-layer](/ai/tdc/reference/commands/fs/tdc-fs-create-layer.md)
      - [list-layers](/ai/tdc/reference/commands/fs/tdc-fs-list-layers.md)
      - [describe-layer](/ai/tdc/reference/commands/fs/tdc-fs-describe-layer.md)
      - [diff-layer](/ai/tdc/reference/commands/fs/tdc-fs-diff-layer.md)
      - [create-layer-checkpoint](/ai/tdc/reference/commands/fs/tdc-fs-create-layer-checkpoint.md)
      - [rollback-layer](/ai/tdc/reference/commands/fs/tdc-fs-rollback-layer.md)
      - [commit-layer](/ai/tdc/reference/commands/fs/tdc-fs-commit-layer.md)
      - [pack-file-system](/ai/tdc/reference/commands/fs/tdc-fs-pack-file-system.md)
      - [unpack-file-system](/ai/tdc/reference/commands/fs/tdc-fs-unpack-file-system.md)
      - [mount-file-system](/ai/tdc/reference/commands/fs/tdc-fs-mount-file-system.md)
      - [drain-file-system](/ai/tdc/reference/commands/fs/tdc-fs-drain-file-system.md)
      - [unmount-file-system](/ai/tdc/reference/commands/fs/tdc-fs-unmount-file-system.md)
    - fs-git
      - [clone-git-workspace](/ai/tdc/reference/commands/fs-git/tdc-fs-git-clone-git-workspace.md)
      - [hydrate-git-workspace](/ai/tdc/reference/commands/fs-git/tdc-fs-git-hydrate-git-workspace.md)
      - [add-git-worktree](/ai/tdc/reference/commands/fs-git/tdc-fs-git-add-git-worktree.md)
      - [remove-git-worktree](/ai/tdc/reference/commands/fs-git/tdc-fs-git-remove-git-worktree.md)
    - fs-journal
      - [create-journal](/ai/tdc/reference/commands/fs-journal/tdc-fs-journal-create-journal.md)
      - [append-journal-entries](/ai/tdc/reference/commands/fs-journal/tdc-fs-journal-append-journal-entries.md)
      - [read-journal-entries](/ai/tdc/reference/commands/fs-journal/tdc-fs-journal-read-journal-entries.md)
      - [search-journal-entries](/ai/tdc/reference/commands/fs-journal/tdc-fs-journal-search-journal-entries.md)
      - [verify-journal](/ai/tdc/reference/commands/fs-journal/tdc-fs-journal-verify-journal.md)
    - fs-vault
      - [create-secret](/ai/tdc/reference/commands/fs-vault/tdc-fs-vault-create-secret.md)
      - [replace-secret](/ai/tdc/reference/commands/fs-vault/tdc-fs-vault-replace-secret.md)
      - [read-secret](/ai/tdc/reference/commands/fs-vault/tdc-fs-vault-read-secret.md)
      - [list-secrets](/ai/tdc/reference/commands/fs-vault/tdc-fs-vault-list-secrets.md)
      - [delete-secret](/ai/tdc/reference/commands/fs-vault/tdc-fs-vault-delete-secret.md)
      - [create-grant](/ai/tdc/reference/commands/fs-vault/tdc-fs-vault-create-grant.md)
      - [delete-grant](/ai/tdc/reference/commands/fs-vault/tdc-fs-vault-delete-grant.md)
      - [list-audit-events](/ai/tdc/reference/commands/fs-vault/tdc-fs-vault-list-audit-events.md)
      - [run-with-secret](/ai/tdc/reference/commands/fs-vault/tdc-fs-vault-run-with-secret.md)
      - [mount-vault](/ai/tdc/reference/commands/fs-vault/tdc-fs-vault-mount-vault.md)
      - [unmount-vault](/ai/tdc/reference/commands/fs-vault/tdc-fs-vault-unmount-vault.md)
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
