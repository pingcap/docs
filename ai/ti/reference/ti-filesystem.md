---
title: TiDB Cloud Filesystem CLI Command Reference
summary: Reference every `ti fs` command for Filesystem resources, files, layers, packs, and mounts.
---

# TiDB Cloud Filesystem CLI Command Reference

Use `ti fs` to provision TiDB Cloud Filesystem resources and access their data from commands or local mounts.

In command syntax, square brackets (`[]`) enclose optional items. Parentheses group required choices, and a vertical bar (`|`) separates alternatives. For example, `(--ttl <duration> | --no-expiration)` means that you must specify exactly one of the two options.

## Resource and token commands

| Command | Description |
| --- | --- |
| [`create-file-system`](/ai/ti/reference/ti-fs-create-file-system.md) | Creates a Filesystem and its initial owner token. |
| [`list-file-systems`](/ai/ti/reference/ti-fs-list-file-systems.md) | Lists Filesystems in the effective region. |
| [`describe-file-system`](/ai/ti/reference/ti-fs-describe-file-system.md) | Describes one Filesystem by ID. |
| [`check-file-system`](/ai/ti/reference/ti-fs-check-file-system.md) | Checks Filesystem selection, routing, credentials, and data-plane access. |
| [`delete-file-system`](/ai/ti/reference/ti-fs-delete-file-system.md) | Permanently deletes a Filesystem. |
| [`import-file-system-token`](/ai/ti/reference/ti-fs-import-file-system-token.md) | Imports and selects an existing Filesystem token locally. |
| [`generate-file-system-token`](/ai/ti/reference/ti-fs-generate-file-system-token.md) | Generates an additional owner token. |
| [`generate-file-system-scoped-token`](/ai/ti/reference/ti-fs-generate-file-system-scoped-token.md) | Generates a token limited by path, operation, and lifetime. |
| [`list-file-system-tokens`](/ai/ti/reference/ti-fs-list-file-system-tokens.md) | Lists non-secret token metadata. |
| [`enable-file-system-token`](/ai/ti/reference/ti-fs-enable-file-system-token.md) | Re-enables a disabled token. |
| [`disable-file-system-token`](/ai/ti/reference/ti-fs-disable-file-system-token.md) | Temporarily disables a token. |
| [`delete-file-system-token`](/ai/ti/reference/ti-fs-delete-file-system-token.md) | Permanently revokes a token. |
| [`refresh-file-system-token`](/ai/ti/reference/ti-fs-refresh-file-system-token.md) | Rotates a token and returns its replacement once. |

### Token-management authorization

When an owner token authorizes token management, it can list tokens, create scoped tokens, and revoke either owner or scoped tokens. It can enable or disable scoped tokens only. TiDB Cloud API credentials can enable, disable, or revoke either token kind.

## AI provider configuration commands

These commands configure optional providers for extracting content from media files and generating embeddings. Ordinary Filesystem resource and file operations do not require AI provider configuration.

| Command | Description |
| --- | --- |
| [`describe-file-system-extract-configuration`](/ai/ti/reference/ti-fs-describe-file-system-extract-configuration.md) | Describes the media extraction provider configuration. |
| [`update-file-system-extract-configuration`](/ai/ti/reference/ti-fs-update-file-system-extract-configuration.md) | Updates the provider used to extract media content. |
| [`describe-file-system-embedding-configuration`](/ai/ti/reference/ti-fs-describe-file-system-embedding-configuration.md) | Describes the embedding provider configuration. |
| [`update-file-system-embedding-configuration`](/ai/ti/reference/ti-fs-update-file-system-embedding-configuration.md) | Updates the provider used to generate embeddings. |

## Data and namespace commands

| Command | Description |
| --- | --- |
| [`copy-file`](/ai/ti/reference/ti-fs-copy-file.md) | Copies files between local storage and a Filesystem, or within a Filesystem. |
| [`read-file`](/ai/ti/reference/ti-fs-read-file.md) | Reads a remote file or byte range. |
| [`list-files`](/ai/ti/reference/ti-fs-list-files.md) | Lists entries under a remote path. |
| [`describe-file`](/ai/ti/reference/ti-fs-describe-file.md) | Describes a remote file or directory. |
| [`move-file`](/ai/ti/reference/ti-fs-move-file.md) | Moves or renames a remote path. |
| [`delete-file`](/ai/ti/reference/ti-fs-delete-file.md) | Deletes a remote file or directory. |
| [`create-directory`](/ai/ti/reference/ti-fs-create-directory.md) | Creates a remote directory. |
| [`chmod-file`](/ai/ti/reference/ti-fs-chmod-file.md) | Changes POSIX-style mode metadata. |
| [`create-symlink`](/ai/ti/reference/ti-fs-create-symlink.md) | Creates a symbolic link. |
| [`create-hardlink`](/ai/ti/reference/ti-fs-create-hardlink.md) | Creates a hard link. |
| [`search-file-content`](/ai/ti/reference/ti-fs-search-file-content.md) | Searches extracted file content and descriptions. |
| [`find-files`](/ai/ti/reference/ti-fs-find-files.md) | Finds files by name, tag, date, size, or type. |

## Layer and portability commands

| Command | Description |
| --- | --- |
| [`create-layer`](/ai/ti/reference/ti-fs-create-layer.md) | Creates an isolated writable layer. |
| [`list-layers`](/ai/ti/reference/ti-fs-list-layers.md) | Lists layers in a Filesystem. |
| [`fork-layer`](/ai/ti/reference/ti-fs-fork-layer.md) | Forks a child layer from a parent tip or checkpoint. |
| [`list-layer-chain`](/ai/ti/reference/ti-fs-list-layer-chain.md) | Lists the pinned ancestry of a layer. |
| [`describe-layer`](/ai/ti/reference/ti-fs-describe-layer.md) | Describes a layer by ID. |
| [`diff-layer`](/ai/ti/reference/ti-fs-diff-layer.md) | Lists changes recorded in a layer. |
| [`create-layer-checkpoint`](/ai/ti/reference/ti-fs-create-layer-checkpoint.md) | Creates a durable checkpoint in a layer. |
| [`delete-layer`](/ai/ti/reference/ti-fs-delete-layer.md) | Logically abandons a layer. |
| [`rollback-layer`](/ai/ti/reference/ti-fs-rollback-layer.md) | Rolls a layer back without committing its changes. |
| [`commit-layer`](/ai/ti/reference/ti-fs-commit-layer.md) | Applies a layer's changes to the base Filesystem. |
| [`pack-file-system`](/ai/ti/reference/ti-fs-pack-file-system.md) | Archives selected local overlay state to the Filesystem. |
| [`unpack-file-system`](/ai/ti/reference/ti-fs-unpack-file-system.md) | Restores local overlay state from an archive. |

### Layer references

A layer reference can be a layer ID, a unique layer name, or a tag reference in the form `tag:<key>=<value>`, for example `tag:run=123`. Because names and tag references can be ambiguous, use layer IDs in automation.

### Mount profiles and local overlays

A local overlay stores files that a mount profile keeps on the local machine instead of in the remote namespace. Mount profiles define which paths use that overlay:

| Mount profile | Behavior |
| --- | --- |
| `coding-agent` | Keeps version-control metadata, dependency directories, caches, build output, and common temporary paths in the local overlay. It does not select automatic pack paths. |
| `portable` | Uses the same local-path rules as `coding-agent` and packs or unpacks the complete overlay by default, so you can move it between machines or sandbox sessions. |
| `none` | Disables local-overlay path routing and automatic pack or unpack behavior. |

## Mount commands

| Command | Description |
| --- | --- |
| [`mount-file-system`](/ai/ti/reference/ti-fs-mount-file-system.md) | Mounts a Filesystem at a local path. |
| [`drain-file-system`](/ai/ti/reference/ti-fs-drain-file-system.md) | Flushes pending writes from a live FUSE mount. |
| [`unmount-file-system`](/ai/ti/reference/ti-fs-unmount-file-system.md) | Flushes and unmounts a Filesystem. |

## Command aliases

The following `ti fs` commands have Unix-style aliases. For example, `ti fs cp` is equivalent to `ti fs copy-file`. Commands not listed in the table, including `pack-file-system` and `unpack-file-system`, do not have aliases.

| Alias | Canonical command |
| --- | --- |
| `cp` | `copy-file` |
| `cat` | `read-file` |
| `ls` | `list-files` |
| `stat` | `describe-file` |
| `mv` | `move-file` |
| `rm` | `delete-file` |
| `mkdir` | `create-directory` |
| `chmod` | `chmod-file` |
| `symlink` | `create-symlink` |
| `hardlink` | `create-hardlink` |
| `grep` | `search-file-content` |
| `find` | `find-files` |
| `mount` | `mount-file-system` |
| `drain` | `drain-file-system` |
| `umount` | `unmount-file-system` |

Aliases use the same options, authentication, output, query, and error behavior as canonical commands.

## See also

- [Manage TiDB Cloud Filesystems](/tidb-cloud-filesystem/manage-filesystem-resources.md)
- [Configure TiDB Cloud Filesystem AI Providers](/tidb-cloud-filesystem/configure-filesystem-ai-providers.md)
- [Manage TiDB Cloud Filesystem Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md)
- [Work with Files and Directories](/tidb-cloud-filesystem/work-with-filesystem-data.md)
- [Manage Filesystem Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md)
- [Mount a TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-mount.md)
- [Manage Git Workspaces on TiDB Cloud Filesystem](/tidb-cloud-filesystem/manage-git-workspaces.md)
- [Use TiDB Cloud Filesystem Journals](/tidb-cloud-filesystem/use-filesystem-journals.md)
- [Manage TiDB Cloud Filesystem Vault Secrets](/tidb-cloud-filesystem/manage-filesystem-vault-secrets.md)
