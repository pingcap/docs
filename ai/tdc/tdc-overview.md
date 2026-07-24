---
title: TiDB Cloud CLI (tdc) Overview
summary: Learn when to use the Preview tdc command-line interface to manage TiDB Cloud Starter databases and persistent Filesystems for users, automation, and AI agents.
---

# TiDB Cloud CLI (tdc) Overview

tdc is the new TiDB Cloud command-line interface for managing TiDB Cloud Starter databases and TiDB Cloud Filesystem. It is designed for repeatable automation: commands are non-interactive except for configuration, structured output is JSON by default, and database and Filesystem credentials have separate security boundaries.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## When to use tdc

Use tdc when a workflow needs to manage TiDB Cloud from a terminal, script, CI job, or AI agent environment. Typical scenarios include:

- **Automate Starter database lifecycle operations.** Create a cluster or branch, wait until it is ready, inspect it as JSON, and delete only the resource identified by your workflow.
- **Separate SQL privileges by task.** Give an agent read-only access for inspection, read-write access for application work, or admin access for schema and privilege management without passing database passwords in every command.
- **Keep sandbox work after the sandbox disappears.** Provision a Filesystem on a trusted machine, then pass only its token, region, and name to an ephemeral environment.
- **Share one workspace across machines and interfaces.** Read and write the same remote namespace through direct data-plane commands or a FUSE or WebDAV mount.
- **Start large Git workspaces sooner.** Expose a repository file tree while clean Git data continues hydrating in the background.
- **Record and delegate agent work.** Store append-only workflow events in journals and grant temporary, scoped access to selected vault fields.

For a visual, interactive workflow, use the TiDB Cloud console instead. For TiDB Cloud Essential or CLI operations that tdc does not provide, use `ticloud`.

## tdc, ticloud, and the TiDB Cloud console

TiDB Cloud currently has two command-line interfaces with different product scopes. `tdc` is the new CLI for Starter and TiDB Cloud Filesystem. `ticloud` remains the CLI for Essential and also supports existing Starter workflows.

| Interface | Use it for | Interaction model |
| --- | --- | --- |
| `tdc` (Preview) | New TiDB Cloud Starter automation and TiDB Cloud Filesystem workflows | Predictable commands, JSON output by default, and non-interactive operation except for `tdc configure` |
| `ticloud` | TiDB Cloud Essential and operations not available in tdc, such as import, export, and audit-log commands | Traditional CLI workflows with interactive and non-interactive modes |
| TiDB Cloud console | Visual resource inspection, guided setup, and manual operations | Browser-based and interactive |

New Starter and Filesystem automation should use tdc. Use `ticloud` for Essential and any command that has no tdc equivalent. tdc replaces `ticloud` only for the Starter workflows that tdc supports; it does not replace `ticloud` for Essential.

## What tdc manages

tdc covers the following functional areas:

- Starter cluster and branch lifecycle operations;
- read-only, read-write, and admin SQL users, connection strings, and one-statement SQL execution;
- Filesystem provisioning, direct file operations, and FUSE or WebDAV mounts;
- Filesystem layers, packs, Git workspaces, journals, and vault operations;
- profiles, regional endpoint selection, local credentials, updates, structured output, and JMESPath queries.

tdc has a two-level command model:

```text
tdc <service> <operation>
```

Examples include `tdc db list-db-clusters`, `tdc fs copy-file`, and `tdc fs-journal verify-journal`. The top-level `tdc configure` and `tdc update` commands configure and maintain the CLI.

## tdc and Drive9

tdc installs a bundled [Drive9](https://github.com/mem9-ai/drive9) companion named `tdc-drive9`. tdc owns profile selection, TiDB Cloud credentials, region and Filesystem selection, output formatting, and tdc error behavior. The companion owns Filesystem data-plane semantics, FUSE and WebDAV mounts, layers, pack and unpack, Git workspace acceleration, journals, and vault operations.

You do not need to install, configure, or invoke Drive9 separately for normal tdc workflows.

## Find the right documentation

- Follow the [Quick Start](/ai/tdc/tdc-quick-start.md) to install tdc and complete your first Starter or Filesystem workflow.
- Use the command references for exact command trees, inputs, behavior, and examples:

- [Install, Configure, and Update tdc](/ai/tdc/reference/tdc-install-configure-update.md)
- [Manage Projects in TiDB Cloud Organizations with tdc](/ai/tdc/reference/tdc-organization.md)
- [tdc db Command Reference](/ai/tdc/reference/tdc-starter-database.md)
- [tdc fs Command Reference](/ai/tdc/reference/tdc-filesystem.md)
- [tdc fs-git Command Reference](/ai/tdc/reference/tdc-filesystem-git.md)
- [tdc fs-journal Command Reference](/ai/tdc/reference/tdc-filesystem-journal.md)
- [tdc fs-vault Command Reference](/ai/tdc/reference/tdc-filesystem-vault.md)
- [Troubleshoot tdc](/ai/tdc/reference/tdc-troubleshooting.md)

### Scenario references

Use scenarios to follow a complete workflow that combines multiple commands and features:

For users and automation:

- [Run a Daily tdc Workflow](/ai/tdc/reference/tdc-daily-workflow-example.md)
- [Query SQL with Explicit Roles](/ai/tdc/reference/tdc-query-sql-with-roles-example.md)
- [Share a Filesystem Across Machines](/ai/tdc/reference/tdc-share-filesystem-across-machines-example.md)
- [Hand Off CI Artifacts Between Jobs](/ai/tdc/reference/tdc-ci-artifact-handoff-example.md)

For AI agents:

- [Use a Filesystem in an Agent Sandbox](/ai/tdc/reference/tdc-agent-sandbox-example.md)
- [Persist Agent State Across Sandboxes](/ai/tdc/reference/tdc-persistent-agent-state-example.md)
- [Share a Read-Only Dataset Across Parallel Agents](/ai/tdc/reference/tdc-parallel-agent-dataset-example.md)
- [Prepare a Git Workspace for Agents](/ai/tdc/reference/tdc-git-workspace-for-agents-example.md)
- [Record an Agent Workflow in a Journal](/ai/tdc/reference/tdc-journal-agent-workflow-example.md)
- [Delegate Secrets to an Agent](/ai/tdc/reference/tdc-vault-agent-secrets-example.md)

### Reference

- [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md)
- [tdc Configuration and Credentials](/ai/tdc/reference/tdc-configuration-and-credentials.md)
- [tdc Regions, Security, and Limitations](/ai/tdc/reference/tdc-regions-security-and-limitations.md)

To report a problem or suggest an improvement, create an issue in the [tdc GitHub repository](https://github.com/tidbcloud/tdc/issues).
