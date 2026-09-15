---
title: TiDB Cloud CLI (`ti`) Overview
summary: Learn when to use the TiDB Cloud CLI (`ti`) to manage TiDB Cloud Starter instances and TiDB Cloud Filesystems.
---

# TiDB Cloud CLI (`ti`) Overview

[TiDB Cloud CLI (`ti`)](https://github.com/tidbcloud/ti-cli) is a CLI for managing [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) instances and [TiDB Cloud Filesystems](/tidb-cloud/tidb-cloud-glossary.md#tidb-cloud-filesystem). It is designed for both interactive use and automation, with structured JSON output by default.

> **Note:**
>
> - TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface might change without prior notice.
> - TiDB Cloud currently provides two CLIs with different scopes: [`ti`](https://github.com/tidbcloud/ti-cli) and [`ticloud`](https://github.com/tidbcloud/tidbcloud-cli). To learn when to use `ti` or `ticloud`, see [Differences between `ti` and `ticloud`](#differences-between-ti-and-ticloud) and [When to use TiDB Cloud CLI (`ti`)](#when-to-use-tidb-cloud-cli-ti).

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

TiDB Cloud currently provides two CLIs with different scopes: `ti` and [`ticloud`](/tidb-cloud/cli-reference.md).

`ti` is designed for automation with TiDB Cloud Starter and for managing TiDB Cloud Filesystems, while `ticloud` continues to support TiDB Cloud Essential and additional TiDB Cloud operations that are not available in `ti`.

| CLI | Best for | Key characteristics |
| --- | --- | --- |
| `ti` | Supported TiDB Cloud Starter automation workflows and TiDB Cloud Filesystems | Designed for automation; outputs JSON by default; commands support non-interactive workflows, while `ti configure` can also prompt interactively |
| `ticloud` | TiDB Cloud Essential, existing TiDB Cloud Starter workflows, and operations not available in `ti` (such as data import, data export, and audit log operations) | Supports additional TiDB Cloud operations that are not available in `ti`, and both interactive and non-interactive modes |

`ti` does not replace `ticloud`. Choose the CLI based on the resource and operation you need:

- For new automation workflows with TiDB Cloud Starter, use `ti` when it supports the operations you need.
- For managing TiDB Cloud Filesystems, use `ti`.
- If you have existing `ticloud` workflows for TiDB Cloud Starter or TiDB Cloud Essential, you can continue to use them.
- For TiDB Cloud Essential or operations not available in `ti` (such as data import, data export, and audit log operations), use [`ticloud`](/tidb-cloud/cli-reference.md).

## Next steps

If you are new to the TiDB Cloud CLI, start with the [Quick Start](/ai/ti/ti-quick-start.md) to install `ti`, configure a profile, and complete a basic TiDB Cloud Starter or Filesystem workflow.

Then continue based on what you want to do:

- [Manage TiDB Cloud Starter Instances](/ai/ti/guides/manage-starter-instances.md)
- [Manage TiDB Cloud Filesystems](/ai/ti/guides/manage-filesystem-resources.md)
- **Follow end-to-end workflows**: Start with [Run a Daily TiDB Cloud CLI Workflow](/ai/ti/guides/ti-daily-workflow-example.md) or [Use TiDB Cloud Filesystem in an Agent Sandbox](/ai/ti/guides/ti-agent-sandbox-example.md)
- **Look up a specific command**: Check the [TiDB Cloud CLI Command Reference](/ai/ti/reference/ti-cli-reference.md)
- **See what’s new in TiDB Cloud CLI**: Check the [TiDB Cloud CLI (`ti`) Release Notes](https://github.com/tidbcloud/ti-cli/releases)
- **Report a problem**: Create an issue in the [TiDB Cloud CLI GitHub repository](https://github.com/tidbcloud/ti-cli/issues).
