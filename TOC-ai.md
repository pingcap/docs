<!-- markdownlint-disable MD007 -->
<!-- markdownlint-disable MD041 -->

# Table of Contents

## QUICK START

- [Get Started with Vector Search via Python](/ai/quickstart-via-python.md)
- [Get Started with Vector Search via SQL](/ai/quickstart-via-sql.md)
- [Get Started with TiDB Cloud CLI](/ai/ti/ti-quick-start.md)

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
- [Vector Functions and Operators](/ai/reference/vector-search-functions-and-operators.md)
- [Vector Search Index](/ai/reference/vector-search-index.md)
- [Vector Search Performance Tuning](/ai/reference/vector-search-improve-performance.md)
- [Vector Search Limitations](/ai/reference/vector-search-limitations.md)
- TiDB Cloud CLI
  - [TiDB Cloud Command Line Interface Overview](/ai/ti/ti-overview.md)
  - Guides
    - [Install, Configure, and Update TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md)
    - [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
    - [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
    - [TiDB Cloud Filesystem Git CLI Command Reference](/ai/ti/reference/ti-filesystem-git.md)
    - [TiDB Cloud Filesystem Journal CLI Command Reference](/ai/ti/reference/ti-filesystem-journal.md)
    - [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/ti/reference/ti-filesystem-vault.md)
  - Command Reference
    - [TiDB Cloud CLI Command Reference](/ai/ti/reference/ti-cli-reference.md)
    - [configure](/ai/ti/reference/commands/ti/ti-configure.md)
    - [update](/ai/ti/reference/commands/ti/ti-update.md)
    - db
      - [create-db-cluster](/ai/ti/reference/commands/db/ti-db-create-db-cluster.md)
      - [list-db-clusters](/ai/ti/reference/commands/db/ti-db-list-db-clusters.md)
      - [describe-db-cluster](/ai/ti/reference/commands/db/ti-db-describe-db-cluster.md)
      - [update-db-cluster](/ai/ti/reference/commands/db/ti-db-update-db-cluster.md)
      - [delete-db-cluster](/ai/ti/reference/commands/db/ti-db-delete-db-cluster.md)
      - [create-db-cluster-branch](/ai/ti/reference/commands/db/ti-db-create-db-cluster-branch.md)
      - [list-db-cluster-branches](/ai/ti/reference/commands/db/ti-db-list-db-cluster-branches.md)
      - [describe-db-cluster-branch](/ai/ti/reference/commands/db/ti-db-describe-db-cluster-branch.md)
      - [delete-db-cluster-branch](/ai/ti/reference/commands/db/ti-db-delete-db-cluster-branch.md)
      - [create-db-sql-users](/ai/ti/reference/commands/db/ti-db-create-db-sql-users.md)
      - [format-db-connection-string](/ai/ti/reference/commands/db/ti-db-format-db-connection-string.md)
      - [execute-sql-statement](/ai/ti/reference/commands/db/ti-db-execute-sql-statement.md)
    - fs
      - [create-file-system](/ai/ti/reference/commands/fs/ti-fs-create-file-system.md)
      - [import-file-system-token](/ai/ti/reference/commands/fs/ti-fs-import-file-system-token.md)
      - [generate-file-system-token](/ai/ti/reference/commands/fs/ti-fs-generate-file-system-token.md)
      - [generate-file-system-scoped-token](/ai/ti/reference/commands/fs/ti-fs-generate-file-system-scoped-token.md)
      - [list-file-system-tokens](/ai/ti/reference/commands/fs/ti-fs-list-file-system-tokens.md)
      - [enable-file-system-token](/ai/ti/reference/commands/fs/ti-fs-enable-file-system-token.md)
      - [disable-file-system-token](/ai/ti/reference/commands/fs/ti-fs-disable-file-system-token.md)
      - [delete-file-system-token](/ai/ti/reference/commands/fs/ti-fs-delete-file-system-token.md)
      - [refresh-file-system-token](/ai/ti/reference/commands/fs/ti-fs-refresh-file-system-token.md)
      - [list-file-systems](/ai/ti/reference/commands/fs/ti-fs-list-file-systems.md)
      - [describe-file-system](/ai/ti/reference/commands/fs/ti-fs-describe-file-system.md)
      - [check-file-system](/ai/ti/reference/commands/fs/ti-fs-check-file-system.md)
      - [delete-file-system](/ai/ti/reference/commands/fs/ti-fs-delete-file-system.md)
      - [copy-file](/ai/ti/reference/commands/fs/ti-fs-copy-file.md)
      - [read-file](/ai/ti/reference/commands/fs/ti-fs-read-file.md)
      - [list-files](/ai/ti/reference/commands/fs/ti-fs-list-files.md)
      - [describe-file](/ai/ti/reference/commands/fs/ti-fs-describe-file.md)
      - [move-file](/ai/ti/reference/commands/fs/ti-fs-move-file.md)
      - [delete-file](/ai/ti/reference/commands/fs/ti-fs-delete-file.md)
      - [create-directory](/ai/ti/reference/commands/fs/ti-fs-create-directory.md)
      - [chmod-file](/ai/ti/reference/commands/fs/ti-fs-chmod-file.md)
      - [create-symlink](/ai/ti/reference/commands/fs/ti-fs-create-symlink.md)
      - [create-hardlink](/ai/ti/reference/commands/fs/ti-fs-create-hardlink.md)
      - [search-file-content](/ai/ti/reference/commands/fs/ti-fs-search-file-content.md)
      - [find-files](/ai/ti/reference/commands/fs/ti-fs-find-files.md)
      - [create-layer](/ai/ti/reference/commands/fs/ti-fs-create-layer.md)
      - [list-layers](/ai/ti/reference/commands/fs/ti-fs-list-layers.md)
      - [fork-layer](/ai/ti/reference/commands/fs/ti-fs-fork-layer.md)
      - [list-layer-chain](/ai/ti/reference/commands/fs/ti-fs-list-layer-chain.md)
      - [describe-layer](/ai/ti/reference/commands/fs/ti-fs-describe-layer.md)
      - [diff-layer](/ai/ti/reference/commands/fs/ti-fs-diff-layer.md)
      - [create-layer-checkpoint](/ai/ti/reference/commands/fs/ti-fs-create-layer-checkpoint.md)
      - [delete-layer](/ai/ti/reference/commands/fs/ti-fs-delete-layer.md)
      - [rollback-layer](/ai/ti/reference/commands/fs/ti-fs-rollback-layer.md)
      - [commit-layer](/ai/ti/reference/commands/fs/ti-fs-commit-layer.md)
      - [pack-file-system](/ai/ti/reference/commands/fs/ti-fs-pack-file-system.md)
      - [unpack-file-system](/ai/ti/reference/commands/fs/ti-fs-unpack-file-system.md)
      - [mount-file-system](/ai/ti/reference/commands/fs/ti-fs-mount-file-system.md)
      - [drain-file-system](/ai/ti/reference/commands/fs/ti-fs-drain-file-system.md)
      - [unmount-file-system](/ai/ti/reference/commands/fs/ti-fs-unmount-file-system.md)
    - fs-git
      - [clone-git-workspace](/ai/ti/reference/commands/fs-git/ti-fs-git-clone-git-workspace.md)
      - [hydrate-git-workspace](/ai/ti/reference/commands/fs-git/ti-fs-git-hydrate-git-workspace.md)
      - [add-git-worktree](/ai/ti/reference/commands/fs-git/ti-fs-git-add-git-worktree.md)
      - [remove-git-worktree](/ai/ti/reference/commands/fs-git/ti-fs-git-remove-git-worktree.md)
    - fs-journal
      - [create-journal](/ai/ti/reference/commands/fs-journal/ti-fs-journal-create-journal.md)
      - [append-journal-entries](/ai/ti/reference/commands/fs-journal/ti-fs-journal-append-journal-entries.md)
      - [read-journal-entries](/ai/ti/reference/commands/fs-journal/ti-fs-journal-read-journal-entries.md)
      - [search-journal-entries](/ai/ti/reference/commands/fs-journal/ti-fs-journal-search-journal-entries.md)
      - [verify-journal](/ai/ti/reference/commands/fs-journal/ti-fs-journal-verify-journal.md)
    - fs-vault
      - [create-secret](/ai/ti/reference/commands/fs-vault/ti-fs-vault-create-secret.md)
      - [replace-secret](/ai/ti/reference/commands/fs-vault/ti-fs-vault-replace-secret.md)
      - [read-secret](/ai/ti/reference/commands/fs-vault/ti-fs-vault-read-secret.md)
      - [list-secrets](/ai/ti/reference/commands/fs-vault/ti-fs-vault-list-secrets.md)
      - [delete-secret](/ai/ti/reference/commands/fs-vault/ti-fs-vault-delete-secret.md)
      - [create-grant](/ai/ti/reference/commands/fs-vault/ti-fs-vault-create-grant.md)
      - [delete-grant](/ai/ti/reference/commands/fs-vault/ti-fs-vault-delete-grant.md)
      - [list-audit-events](/ai/ti/reference/commands/fs-vault/ti-fs-vault-list-audit-events.md)
      - [run-with-secret](/ai/ti/reference/commands/fs-vault/ti-fs-vault-run-with-secret.md)
      - [mount-vault](/ai/ti/reference/commands/fs-vault/ti-fs-vault-mount-vault.md)
      - [unmount-vault](/ai/ti/reference/commands/fs-vault/ti-fs-vault-unmount-vault.md)
  - Scenarios for Users and Automation
    - [Run a Daily TiDB Cloud CLI Workflow](/ai/ti/reference/ti-daily-workflow-example.md)
    - [Query TiDB Cloud Starter with Explicit SQL Roles](/ai/ti/reference/ti-query-sql-with-roles-example.md)
    - [Share a TiDB Cloud Filesystem Across Machines](/ai/ti/reference/ti-share-filesystem-across-machines-example.md)
    - [Hand Off CI Artifacts Between Isolated Jobs with TiDB Cloud Filesystem](/ai/ti/reference/ti-ci-artifact-handoff-example.md)
  - Scenarios for AI Agents
    - [Use TiDB Cloud Filesystem in an Agent Sandbox](/ai/ti/reference/ti-agent-sandbox-example.md)
    - [Persist Agent State Across Disposable Sandboxes with TiDB Cloud Filesystem](/ai/ti/reference/ti-persistent-agent-state-example.md)
    - [Share a Read-Only Dataset Across Parallel Agents with TiDB Cloud Filesystem](/ai/ti/reference/ti-parallel-agent-dataset-example.md)
    - [Prepare a Git Workspace for Agents on TiDB Cloud Filesystem](/ai/ti/reference/ti-git-workspace-for-agents-example.md)
    - [Record an Agent Workflow in a TiDB Cloud Filesystem Journal](/ai/ti/reference/ti-journal-agent-workflow-example.md)
    - [Delegate TiDB Cloud Filesystem Vault Secrets to an Agent](/ai/ti/reference/ti-vault-agent-secrets-example.md)
  - [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md)
  - [TiDB Cloud CLI Regions, Security, and Limitations](/ai/ti/reference/ti-regions-security-and-limitations.md)
  - [Troubleshoot TiDB Cloud CLI](/ai/ti/reference/ti-troubleshooting.md)
