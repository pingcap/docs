---
title: TiDB Cloud Command Line Interface Overview
summary: Learn when to use the TiDB Cloud CLI to manage TiDB Cloud Starter databases and persistent Filesystems for users, automation, and AI agents.
---

# TiDB Cloud Command Line Interface Overview

The TiDB Cloud Command Line Interface—`ti`—is the new CLI for managing TiDB Cloud Starter databases and TiDB Cloud Filesystem. It is designed for repeatable automation: commands are non-interactive except for configuration, structured output is JSON by default, and database and Filesystem credentials have separate security boundaries.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## When to use TiDB Cloud CLI

Use the TiDB Cloud CLI when a workflow needs to manage TiDB Cloud from a terminal, script, CI job, or AI agent environment. Typical scenarios include:

- **Automate Starter database lifecycle operations.** Create a cluster or branch, wait until it is ready, inspect it as JSON, and delete only the resource identified by your workflow.
- **Separate SQL privileges by task.** Give an agent read-only access for inspection, read-write access for application work, or admin access for schema and privilege management without passing database passwords in every command.
- **Keep sandbox work after the sandbox disappears.** Provision a Filesystem on a trusted machine, then pass only its token, region, and name to an ephemeral environment.
- **Share one workspace across machines and interfaces.** Read and write the same remote namespace through direct data-plane commands or a FUSE or WebDAV mount.
- **Start large Git workspaces sooner.** Expose a repository file tree while clean Git data continues hydrating in the background.
- **Record and delegate agent work.** Store append-only workflow events in journals and grant temporary, scoped access to selected vault fields.

For a visual, interactive workflow, use the TiDB Cloud console instead. For TiDB Cloud Essential or CLI operations that the TiDB Cloud CLI does not provide, use `ticloud`.

## TiDB Cloud CLI, ticloud, and the TiDB Cloud console

TiDB Cloud currently has two command-line interfaces with different product scopes. `ti` is the new CLI for Starter and TiDB Cloud Filesystem. `ticloud` remains the CLI for Essential and also supports existing Starter workflows.

| Interface | Use it for | Interaction model |
| --- | --- | --- |
| `ti` (Preview) | New TiDB Cloud Starter automation and TiDB Cloud Filesystem workflows | Predictable commands, JSON output by default, and non-interactive operation except for `ti configure` |
| `ticloud` | TiDB Cloud Essential and operations not available in the TiDB Cloud CLI, such as import, export, and audit-log commands | Traditional CLI workflows with interactive and non-interactive modes |
| TiDB Cloud console | Visual resource inspection, guided setup, and manual operations | Browser-based and interactive |

New Starter and Filesystem automation should use the TiDB Cloud CLI. Use `ticloud` for Essential and any command that has no TiDB Cloud CLI equivalent. The TiDB Cloud CLI replaces `ticloud` only for the Starter workflows it supports; the TiDB Cloud CLI does not replace `ticloud` for Essential.

## What TiDB Cloud CLI manages

The TiDB Cloud CLI covers the following functional areas:

- Starter cluster and branch lifecycle operations;
- read-only, read-write, and admin SQL users, connection strings, and one-statement SQL execution;
- Filesystem provisioning, direct file operations, and FUSE or WebDAV mounts;
- Filesystem layers, packs, Git workspaces, journals, and vault operations;
- profiles, regional endpoint selection, local credentials, updates, structured output, and JMESPath queries.

The `ti` executable has a two-level command model:

```text
ti <service> <operation>
```

Examples include `ti db list-db-clusters --db-cluster-type starter`, `ti fs copy-file`, and `ti fs-journal verify-journal`. The top-level `ti configure` and `ti update` commands configure and maintain the CLI.

## TiDB Cloud CLI and Drive9

The TiDB Cloud CLI installs a bundled [Drive9](https://github.com/mem9-ai/drive9) companion named `ti-drive9`. The TiDB Cloud CLI owns profile selection, TiDB Cloud credentials, region and Filesystem selection, output formatting, and `ti` error behavior. The companion owns Filesystem data-plane semantics, FUSE and WebDAV mounts, layers, pack and unpack, Git workspace acceleration, journals, and vault operations.

You do not need to install, configure, or invoke Drive9 separately for normal TiDB Cloud CLI workflows.

## Find the right documentation

Follow the [Quick Start](/ai/ti/ti-quick-start.md) to install the TiDB Cloud CLI and complete your first Starter or Filesystem workflow. Use these guides for task-oriented instructions:

- [Install, Configure, and Update TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md)
- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
- [TiDB Cloud Filesystem Git CLI Command Reference](/ai/ti/reference/ti-filesystem-git.md)
- [TiDB Cloud Filesystem Journal CLI Command Reference](/ai/ti/reference/ti-filesystem-journal.md)
- [TiDB Cloud Filesystem Vault CLI Command Reference](/ai/ti/reference/ti-filesystem-vault.md)
- [Troubleshoot TiDB Cloud CLI](/ai/ti/reference/ti-troubleshooting.md)

### Scenario references

Use scenarios to follow a complete workflow that combines multiple commands and features:

For users and automation:

- [Run a Daily TiDB Cloud CLI Workflow](/ai/ti/reference/ti-daily-workflow-example.md)
- [Query SQL with Explicit Roles](/ai/ti/reference/ti-query-sql-with-roles-example.md)
- [Share a Filesystem Across Machines](/ai/ti/reference/ti-share-filesystem-across-machines-example.md)
- [Hand Off CI Artifacts Between Jobs](/ai/ti/reference/ti-ci-artifact-handoff-example.md)

For AI agents:

- [Use a Filesystem in an Agent Sandbox](/ai/ti/reference/ti-agent-sandbox-example.md)
- [Persist Agent State Across Sandboxes](/ai/ti/reference/ti-persistent-agent-state-example.md)
- [Share a Read-Only Dataset Across Parallel Agents](/ai/ti/reference/ti-parallel-agent-dataset-example.md)
- [Prepare a Git Workspace for Agents](/ai/ti/reference/ti-git-workspace-for-agents-example.md)
- [Record an Agent Workflow in a Journal](/ai/ti/reference/ti-journal-agent-workflow-example.md)
- [Delegate Secrets to an Agent](/ai/ti/reference/ti-vault-agent-secrets-example.md)

### Reference

- [TiDB Cloud CLI Command Reference](/ai/ti/reference/ti-cli-reference.md)
- [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md)
- [TiDB Cloud CLI Regions, Security, and Limitations](/ai/ti/reference/ti-regions-security-and-limitations.md)

To report a problem or suggest an improvement, create an issue in the [TiDB Cloud CLI GitHub repository](https://github.com/tidbcloud/ti-cli/issues).
