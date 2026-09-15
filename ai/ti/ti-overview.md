---
title: TiDB Cloud CLI (`ti`) Overview
summary: Learn when to use the TiDB Cloud CLI (`ti`) to manage TiDB Cloud Starter instances and TiDB Cloud Filesystems.
---

# TiDB Cloud CLI (`ti`) Overview

The [TiDB Cloud CLI (`ti`)](https://github.com/tidbcloud/ti-cli) is a CLI for managing TiDB Cloud Starter instances and TiDB Cloud Filesystems. It is designed for both interactive use and automation, with structured JSON output by default.

With `ti`, you can manage TiDB Cloud Starter instances and use TiDB Cloud Filesystems for persistent storage, shared workspaces, and AI agent workflows.

> **Note:**
>
> - TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface might change without prior notice.
> - For differences between TiDB Cloud CLI (`ti`) and TiDB Cloud CLI (`ticloud`), see [Differences between `ti` and `ticloud`](#differences-between-ti-and-ticloud).

## When to use TiDB Cloud CLI (`ti`)

Use the TiDB Cloud CLI (`ti`) when you want to manage TiDB Cloud from a terminal, script, CI job, or AI agent environment.

| Typical use case | What you can do |
| --- | --- |
| Automate TiDB Cloud Starter lifecycle operations | Create and manage TiDB Cloud Starter instances and branches, wait until they are ready, inspect results as JSON, run SQL statements, and delete resources by ID. |
| Separate SQL privileges by task | Use CLI-managed read-only, read-write, or admin identities for each task without handling database passwords in every command. |
| Persist and share files across environments | Keep files available across local machines, CI jobs, sandboxes, and other ephemeral environments, and access the same remote namespace through direct file commands or supported FUSE and WebDAV mounts. |
| Use Filesystems in ephemeral environments | Provision a Filesystem on a trusted machine, then give a sandbox its Filesystem token and region code without copying a CLI profile or providing TiDB Cloud API keys. |
| Start large Git workspaces sooner | Expose a repository file tree while clean Git data continues hydrating in the background. |
| Record and delegate agent work | Store append-only, hash-chained workflow events in journals and grant temporary, scoped access to selected vault fields. |

For visual, guided workflows, use the [TiDB Cloud console](https://tidbcloud.com/). For TiDB Cloud Essential or operations that `ti` does not support, use [`ticloud`](#differences-between-ti-and-ticloud).

## What TiDB Cloud CLI manages

The TiDB Cloud CLI covers the following functional areas:

- **TiDB Cloud Starter**
    - Instance and branch lifecycle operations
    - SQL users and connection information
    - SQL statement execution
- **TiDB Cloud Filesystem**
    - Filesystem lifecycle and file operations
    - FUSE and WebDAV mounts
    - Layers, packs, and Git workspaces
    - Journals and vaults
- **CLI configuration**
    - Profiles, regions, and local credentials
    - CLI updates
    - Output formatting and JMESPath queries

Most resource commands follow a two-level command model:

```text
ti <command-group> <operation>
```

For example, `ti db list-db-clusters --db-cluster-type starter`, `ti fs copy-file`, and `ti fs-journal verify-journal`.

You can also use the top-level `ti configure` and `ti update` commands to configure and maintain the CLI.

## Differences between `ti` and `ticloud`

Currently, TiDB Cloud provides two CLIs with different scopes: TiDB Cloud CLI (`ti`) and [TiDB Cloud CLI (`ticloud`)](/tidb-cloud/cli-reference.md).

| Interface | Best for | Key characteristics |
| --- | --- | --- |
| `ti` | TiDB Cloud Filesystems and supported TiDB Cloud Starter workflows | JSON output by default; commands support non-interactive workflows, and `ti configure` can also prompt interactively |
| `ticloud` | TiDB Cloud Essential and operations not available in `ti`, such as import, export, and audit-log commands | Supports both interactive and non-interactive modes |

`ti` does not replace `ticloud`.

- For automation of new TiDB Cloud Starter instances, it is recommended that you use `ti` when it supports the operations you need.
- For management of TiDB Cloud Filesystems, you can only use `ti`.
- If you have existing `ticloud` workflows of TiDB Cloud Starter or Essential instances, they still work.
- For TiDB Cloud Essential or for operations that are not available in `ti`, use [TiDB Cloud CLI (`ticloud`)](/tidb-cloud/cli-reference.md).

## Next steps

If you are new to the TiDB Cloud CLI, start with the [Quick Start](/ai/ti/ti-quick-start.md) to install `ti`, configure a profile, and complete a basic Starter or Filesystem workflow.

Then continue based on what you want to do:

- [Manage TiDB Cloud Starter Instances](/ai/ti/guides/manage-starter-instances.md)
- [Manage TiDB Cloud Filesystems](/ai/ti/guides/manage-filesystem-resources.md)
- **See end-to-end workflows**: Start with [Run a Daily TiDB Cloud CLI Workflow](/ai/ti/reference/ti-daily-workflow-example.md) or [Use TiDB Cloud Filesystem in an Agent Sandbox](/ai/ti/reference/ti-agent-sandbox-example.md)
- **Look up a specific command**: Check the [TiDB Cloud CLI Command Reference](/ai/ti/reference/ti-cli-reference.md)
- **Report a problem**: Create an issue in the [TiDB Cloud CLI GitHub repository](https://github.com/tidbcloud/ti-cli/issues).
