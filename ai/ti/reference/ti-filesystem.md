---
title: TiDB Cloud Filesystem CLI Command Reference
summary: Reference every `ti fs` command for Filesystem resources, files, layers, packs, and mounts.
---

# TiDB Cloud Filesystem CLI Command Reference

Use `ti fs` to provision TiDB Cloud Filesystem resources and access their data from commands or local mounts.

## Resource and token commands

- [`create-file-system`](/ai/ti/reference/commands/fs/ti-fs-create-file-system.md)
- [`list-file-systems`](/ai/ti/reference/commands/fs/ti-fs-list-file-systems.md)
- [`describe-file-system`](/ai/ti/reference/commands/fs/ti-fs-describe-file-system.md)
- [`check-file-system`](/ai/ti/reference/commands/fs/ti-fs-check-file-system.md)
- [`delete-file-system`](/ai/ti/reference/commands/fs/ti-fs-delete-file-system.md)
- [`import-file-system-token`](/ai/ti/reference/commands/fs/ti-fs-import-file-system-token.md)
- [`generate-file-system-token`](/ai/ti/reference/commands/fs/ti-fs-generate-file-system-token.md)
- [`generate-file-system-scoped-token`](/ai/ti/reference/commands/fs/ti-fs-generate-file-system-scoped-token.md)
- [`list-file-system-tokens`](/ai/ti/reference/commands/fs/ti-fs-list-file-system-tokens.md)
- [`enable-file-system-token`](/ai/ti/reference/commands/fs/ti-fs-enable-file-system-token.md)
- [`disable-file-system-token`](/ai/ti/reference/commands/fs/ti-fs-disable-file-system-token.md)
- [`delete-file-system-token`](/ai/ti/reference/commands/fs/ti-fs-delete-file-system-token.md)
- [`refresh-file-system-token`](/ai/ti/reference/commands/fs/ti-fs-refresh-file-system-token.md)

## AI provider configuration commands

- [`describe-file-system-extract-configuration`](/ai/ti/reference/commands/fs/ti-fs-describe-file-system-extract-configuration.md)
- [`update-file-system-extract-configuration`](/ai/ti/reference/commands/fs/ti-fs-update-file-system-extract-configuration.md)
- [`describe-file-system-embedding-configuration`](/ai/ti/reference/commands/fs/ti-fs-describe-file-system-embedding-configuration.md)
- [`update-file-system-embedding-configuration`](/ai/ti/reference/commands/fs/ti-fs-update-file-system-embedding-configuration.md)

## Data and namespace commands

- [`copy-file`](/ai/ti/reference/commands/fs/ti-fs-copy-file.md)
- [`read-file`](/ai/ti/reference/commands/fs/ti-fs-read-file.md)
- [`list-files`](/ai/ti/reference/commands/fs/ti-fs-list-files.md)
- [`describe-file`](/ai/ti/reference/commands/fs/ti-fs-describe-file.md)
- [`move-file`](/ai/ti/reference/commands/fs/ti-fs-move-file.md)
- [`delete-file`](/ai/ti/reference/commands/fs/ti-fs-delete-file.md)
- [`create-directory`](/ai/ti/reference/commands/fs/ti-fs-create-directory.md)
- [`chmod-file`](/ai/ti/reference/commands/fs/ti-fs-chmod-file.md)
- [`create-symlink`](/ai/ti/reference/commands/fs/ti-fs-create-symlink.md)
- [`create-hardlink`](/ai/ti/reference/commands/fs/ti-fs-create-hardlink.md)
- [`search-file-content`](/ai/ti/reference/commands/fs/ti-fs-search-file-content.md)
- [`find-files`](/ai/ti/reference/commands/fs/ti-fs-find-files.md)

## Layer and portability commands

- [`create-layer`](/ai/ti/reference/commands/fs/ti-fs-create-layer.md)
- [`list-layers`](/ai/ti/reference/commands/fs/ti-fs-list-layers.md)
- [`fork-layer`](/ai/ti/reference/commands/fs/ti-fs-fork-layer.md)
- [`list-layer-chain`](/ai/ti/reference/commands/fs/ti-fs-list-layer-chain.md)
- [`describe-layer`](/ai/ti/reference/commands/fs/ti-fs-describe-layer.md)
- [`diff-layer`](/ai/ti/reference/commands/fs/ti-fs-diff-layer.md)
- [`create-layer-checkpoint`](/ai/ti/reference/commands/fs/ti-fs-create-layer-checkpoint.md)
- [`delete-layer`](/ai/ti/reference/commands/fs/ti-fs-delete-layer.md)
- [`rollback-layer`](/ai/ti/reference/commands/fs/ti-fs-rollback-layer.md)
- [`commit-layer`](/ai/ti/reference/commands/fs/ti-fs-commit-layer.md)
- [`pack-file-system`](/ai/ti/reference/commands/fs/ti-fs-pack-file-system.md)
- [`unpack-file-system`](/ai/ti/reference/commands/fs/ti-fs-unpack-file-system.md)

## Mount commands

- [`mount-file-system`](/ai/ti/reference/commands/fs/ti-fs-mount-file-system.md)
- [`drain-file-system`](/ai/ti/reference/commands/fs/ti-fs-drain-file-system.md)
- [`unmount-file-system`](/ai/ti/reference/commands/fs/ti-fs-unmount-file-system.md)

## See also

- [Manage TiDB Cloud Filesystem Resources](/ai/ti/guides/manage-filesystem-resources.md)
- [Configure TiDB Cloud Filesystem AI Providers](/ai/ti/guides/configure-filesystem-ai-providers.md)
- [Manage TiDB Cloud Filesystem Tokens](/ai/ti/guides/manage-filesystem-tokens.md)
- [Work with TiDB Cloud Filesystem Data](/ai/ti/guides/work-with-filesystem-data.md)
- [Manage Filesystem Layers and Checkpoints](/ai/ti/guides/manage-filesystem-layers.md)
- [Mount a TiDB Cloud Filesystem](/ai/ti/guides/mount-filesystem.md)
- [Manage Git Workspaces on TiDB Cloud Filesystem](/ai/ti/guides/manage-git-workspaces.md)
- [Use TiDB Cloud Filesystem Journals](/ai/ti/guides/use-filesystem-journals.md)
- [Manage TiDB Cloud Filesystem Vault Secrets](/ai/ti/guides/manage-filesystem-vault-secrets.md)
