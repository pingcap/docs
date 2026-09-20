---
title: Manage TiDB Cloud Filesystem
summary: Learn how to create a TiDB Cloud Filesystem and write and read a file with `ti fs`, then find guides for other Filesystem tasks.
---

# Manage TiDB Cloud Filesystem

With TiDB Cloud CLI (`ti`), you can create and manage TiDB Cloud Filesystems and work with their files from a terminal or automation workflow.

## Create and use a Filesystem

Before you begin, [install and configure TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md) with API keys that can create a Filesystem in your organization. Choose a supported Filesystem region when you run `ti configure`.

Create a Filesystem and wait until it is ready:

```shell
ti fs create-file-system --display-name my-workspace --wait
```

Copy the returned `file_system_id` and replace `<file-system-id>` in the following commands. The CLI stores the Filesystem token locally. Treat the returned `fs_token` (Filesystem token) as a secret; do not share the command output publicly.

```shell
echo "Hello from my workspace" | ti fs copy-file --file-system-id "<file-system-id>" --from-stdin --to-remote /hello.txt
ti fs read-file --file-system-id "<file-system-id>" --path /hello.txt
```

The read returns `Hello from my workspace`. For supported regions, detailed setup, and cleanup instructions, follow [Get Started with TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-quick-start.md).

## More Filesystem tasks

For common tasks, see the following guides in the **TiDB Cloud Filesystem** documentation:

| What you want to do | Guide |
| --- | --- |
| Create, inspect, or delete a Filesystem | [Manage TiDB Cloud Filesystems](/tidb-cloud-filesystem/manage-filesystem-resources.md) |
| Manage access tokens | [Manage Filesystem Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md) |
| Copy, read, and organize files | [Work with Files and Directories](/tidb-cloud-filesystem/work-with-filesystem-data.md) |
| Access files through a local mount | [Mount a Filesystem](/tidb-cloud-filesystem/filesystem-mount.md) |
| Isolate changes with layers and checkpoints | [Manage Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md) |

For syntax, flags, and output fields, see the [`ti fs` command reference](/ai/ti/reference/ti-filesystem.md).
