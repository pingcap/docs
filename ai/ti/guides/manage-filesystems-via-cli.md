---
title: Manage TiDB Cloud Filesystems via CLI
summary: Learn how to create a TiDB Cloud Filesystem with the CLI, write and read a file, and find detailed guides for more Filesystem tasks.
---

# Manage TiDB Cloud Filesystems via CLI

Use the TiDB Cloud CLI (`ti`) to create a Filesystem and work with its files from a terminal or automation workflow.

## Prerequisites

- [Install and configure TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md) with API keys that can create a Filesystem in your organization.
- Choose a supported Filesystem region when you run `ti configure`. For region choices and installation details, see the [Filesystem Quick Start](/tidb-cloud-filesystem/filesystem-quick-start.md).

## Create and use a Filesystem

Create a Filesystem and wait until it is ready:

```shell
ti fs create-file-system --display-name my-workspace --wait
```

Save the returned `file_system_id` for the next commands. The CLI stores this Filesystem's token locally. Treat the returned `fs_token` as a secret; do not put it in a public issue or log.

Replace `<file-system-id>` with the returned ID, write a file, and read it back:

```shell
echo "Hello from my workspace" | ti fs copy-file --file-system-id "<file-system-id>" --from-stdin --to-remote /hello.txt
ti fs read-file --file-system-id "<file-system-id>" --path /hello.txt
```

The read returns `Hello from my workspace`. The file remains available after you close the terminal. For a guided first run and cleanup instructions, see the [Filesystem Quick Start](/tidb-cloud-filesystem/filesystem-quick-start.md).

## More Filesystem operations

For more Filesystem operations, see the following guides in the TiDB Cloud Filesystem documentation:

- Manage a Filesystem

    - [Create, inspect, check, and delete Filesystem resources](/tidb-cloud-filesystem/manage-filesystem-resources.md)
    - [Manage Filesystem tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md)
    - [Configure Filesystem AI providers](/tidb-cloud-filesystem/configure-filesystem-ai-providers.md)

- Work with Filesystem data

    - [Copy, read, organize, and search files](/tidb-cloud-filesystem/work-with-filesystem-data.md)
    - [Manage layers and checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md)
    - [Mount a Filesystem with the CLI](/tidb-cloud-filesystem/mount-filesystem.md)

- Use advanced Filesystem features

    - [Manage Git workspaces](/tidb-cloud-filesystem/manage-git-workspaces.md)
    - [Use Filesystem journals](/tidb-cloud-filesystem/use-filesystem-journals.md)
    - [Manage Filesystem Vault secrets](/tidb-cloud-filesystem/manage-filesystem-vault-secrets.md)

For details about commands, command flags, and output fields, see [`ti fs` command reference](/ai/ti/reference/ti-filesystem.md).