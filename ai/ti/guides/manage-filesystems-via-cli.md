---
title: Manage TiDB Cloud Filesystem
summary: Learn how to create a file system and write and read a file with `ti fs`, then find guides for other file system tasks.
---

# Manage TiDB Cloud Filesystem

With TiDB Cloud CLI (`ti`), you can create and manage file system resources in TiDB Cloud Filesystem and work with their files from a terminal or automation workflow.

## Create and use a file system

Before you begin, [install and configure TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md) with API keys that can create a file system in your organization. Choose a supported file system region when you run `ti configure`.

Create a file system and wait until it is ready:

```shell
ti fs create-file-system --display-name my-workspace --wait
```

Copy the returned `file_system_id` and replace `<file-system-id>` in the following commands. The CLI stores the file system token locally. Treat the returned `fs_token` (file system token) as a secret; do not share the command output publicly.

```shell
echo "Hello from my workspace" | ti fs copy-file --file-system-id "<file-system-id>" --from-stdin --to-remote /hello.txt
ti fs read-file --file-system-id "<file-system-id>" --path /hello.txt
```

The read returns `Hello from my workspace`. For supported regions, detailed setup, and cleanup instructions, follow [Get Started with TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-quick-start.md).

## More file system tasks

After creating a file system, refer to the following guides for file system tasks:

| What you want to do | Guide |
| --- | --- |
| Access an existing file system from another machine, CI job, or agent environment | [Access an Existing File System](/tidb-cloud-filesystem/access-filesystem.md) |
| Upload, download, read, organize, inspect, or search files and directories | [Work with Files and Directories](/tidb-cloud-filesystem/work-with-filesystem-data.md) |
| Generate, import, scope, inspect, disable, refresh, or revoke access tokens | [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md) |
| Share files in a file system with another user, machine, CI job, or agent | [Share a File System](/tidb-cloud-filesystem/filesystem-sharing.md) |
| Access files in a file system through local file paths | [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md) |
| Isolate changes with layers and checkpoints | [Manage File System Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md) |
| Work with Git repositories on a mounted file system | [Manage Git Workspaces](/tidb-cloud-filesystem/manage-git-workspaces.md) |
| Record and verify ordered workflow events | [Use Journals in a File System](/tidb-cloud-filesystem/use-filesystem-journals.md) |
| Store, delegate, inject, audit, and revoke secrets | [Manage Vault Secrets for a File System](/tidb-cloud-filesystem/manage-filesystem-vault-secrets.md) |
| Configure AI providers for media extraction or semantic search | [Configure AI Providers for a File System](/tidb-cloud-filesystem/configure-filesystem-ai-providers.md) |

For syntax, flags, and output fields, see the [`ti fs` command reference](/ai/ti/reference/ti-filesystem.md).
