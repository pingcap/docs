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

- TiDB Cloud Starter instance and branch lifecycle operations;
- read-only, read-write, and admin SQL users, connection strings, and one-statement SQL execution;
- Filesystem provisioning, direct file operations, and FUSE or WebDAV mounts;
- Filesystem layers, packs, Git workspaces, journals, and vault operations;
- profiles, regional endpoint selection, local credentials, updates, structured output, and JMESPath queries.

The `ti` executable has a two-level command model:

```text
ti <service> <operation>
```

Examples include `ti db list-db-clusters --db-cluster-type starter`, `ti fs copy-file`, and `ti fs-journal verify-journal`. The top-level `ti configure` and `ti update` commands configure and maintain the CLI.

## TiDB Cloud Filesystem runtime

Drive9 is the data-plane runtime used by TiDB Cloud Filesystem. The TiDB Cloud CLI installs and manages this runtime as a bundled companion executable named `ti-drive9`. It is an implementation component of the TiDB Cloud Filesystem experience, not a separate product that you need to select or install.

The `ti` executable owns profile selection, TiDB Cloud credentials, region and Filesystem selection, output formatting, and CLI error behavior. The bundled runtime implements Filesystem data-plane semantics, FUSE and WebDAV mounts, layers, pack and unpack, Git workspace acceleration, journals, and vault operations. You do not need to configure or invoke `ti-drive9` separately for normal TiDB Cloud CLI workflows.

## Get started

If you have not used the TiDB Cloud CLI before, follow the [Quick Start](/ai/ti/ti-quick-start.md) to install `ti`, configure a profile, and run your first Starter or Filesystem command.

After the Quick Start, choose a path based on what you want to do:

- **Manage Starter databases** — [Manage TiDB Cloud Starter Instances](/ai/ti/guides/manage-starter-instances.md)
- **Work with Filesystem storage** — [Manage Filesystem Resources](/ai/ti/guides/manage-filesystem-resources.md)
- **See end-to-end workflows** — Browse the Scenarios for Users and Automation or Scenarios for AI Agents sections in the sidebar.
- **Look up a specific command** — [TiDB Cloud CLI Command Reference](/ai/ti/reference/ti-cli-reference.md)
- **Report a problem** — Create an issue in the [TiDB Cloud CLI GitHub repository](https://github.com/tidbcloud/ti-cli/issues).
