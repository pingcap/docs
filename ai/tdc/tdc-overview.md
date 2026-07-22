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

For a visual, interactive workflow, use the TiDB Cloud console instead. For TiDB Cloud Essential or legacy CLI operations that tdc does not yet provide, continue to use `ticloud` during the transition.

## tdc, ticloud, and the TiDB Cloud console

TiDB Cloud currently has two command-line interfaces. `tdc` is the new CLI and `ticloud` is the legacy CLI that is being gradually replaced.

| Interface | Use it for | Interaction model |
| --- | --- | --- |
| `tdc` (Preview) | New TiDB Cloud Starter automation and TiDB Cloud Filesystem workflows | Predictable commands, JSON output by default, and non-interactive operation except for `tdc configure` |
| `ticloud` (legacy) | TiDB Cloud Essential and operations not yet available in tdc, such as import, export, and audit-log commands | Traditional CLI workflows with interactive and non-interactive modes |
| TiDB Cloud console | Visual resource inspection, guided setup, and manual operations | Browser-based and interactive |

New Starter and Filesystem automation should use tdc. During the transition, keep `ticloud` for Essential and any command that has no tdc equivalent. The legacy `ticloud` CLI will be gradually retired as its supported workflows move to tdc.

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
- Read [Concepts and Architecture](/ai/tdc/concepts/tdc-concepts-and-architecture.md) to understand profiles, credentials, regions, SQL roles, and the Filesystem companion.

### Guides

Use guides to complete one focused task or manage one feature area:

- [Install, Configure, and Update tdc](/ai/tdc/guides/tdc-install-configure-update.md)
- [Manage Projects in TiDB Cloud Organizations with tdc](/ai/tdc/guides/tdc-organization.md)
- [Manage TiDB Cloud Starter Databases](/ai/tdc/guides/tdc-starter-database.md)
- [Manage TiDB Cloud Filesystem](/ai/tdc/guides/tdc-filesystem.md)
- [Use Git Workspaces on TiDB Cloud Filesystem](/ai/tdc/guides/tdc-filesystem-git.md)
- [Use Filesystem Journals](/ai/tdc/guides/tdc-filesystem-journal.md)
- [Use Filesystem Vault](/ai/tdc/guides/tdc-filesystem-vault.md)
- [Troubleshoot tdc](/ai/tdc/reference/tdc-troubleshooting.md)

### Examples

Use examples to follow a complete scenario that combines multiple commands and features:

For users and automation:

- [Run a Daily tdc Workflow](/ai/tdc/examples/tdc-daily-workflow-example.md)
- [Query SQL with Explicit Roles](/ai/tdc/examples/tdc-query-sql-with-roles-example.md)
- [Share a Filesystem Across Machines](/ai/tdc/examples/tdc-share-filesystem-across-machines-example.md)

For AI agents:

- [Use a Filesystem in an Agent Sandbox](/ai/tdc/examples/tdc-agent-sandbox-example.md)
- [Prepare a Git Workspace for Agents](/ai/tdc/examples/tdc-git-workspace-for-agents-example.md)
- [Record an Agent Workflow in a Journal](/ai/tdc/examples/tdc-journal-agent-workflow-example.md)
- [Delegate Secrets to an Agent](/ai/tdc/examples/tdc-vault-agent-secrets-example.md)

### Reference

- [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md)
- [tdc Configuration and Credentials](/ai/tdc/reference/tdc-configuration-and-credentials.md)
- [tdc Regions, Security, and Limitations](/ai/tdc/reference/tdc-regions-security-and-limitations.md)

To report a problem or suggest an improvement, create an issue in the [tdc GitHub repository](https://github.com/tidbcloud/tdc/issues).
