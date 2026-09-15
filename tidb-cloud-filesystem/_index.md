---
title: TiDB Cloud Filesystem
summary: Learn how TiDB Cloud Filesystem keeps agent files available across sessions, shares workspaces, and isolates changes with layers.
---

# TiDB Cloud Filesystem

TiDB Cloud Filesystem is persistent, shared file storage for applications and AI agents. Keep a workspace in the cloud, access it from different machines, and retain its files after a sandbox or process ends.

Use the TiDB Cloud Command Line Interface (`ti`) to create a Filesystem, upload and download files, or mount a remote directory for tools that work with local paths. You do not need to provision or manage a separate database to get started.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Keep work beyond one session

An agent might collect source documents in one sandbox, generate a report in another, and hand the result to a person on a laptop. Files stored only on the sandbox's local disk disappear when that environment is removed. Repeatedly exporting and importing archives also creates separate copies that can drift apart.

With a Filesystem, these participants use the same remote files. A new environment needs an access token and the Filesystem's region code, not the creator's TiDB Cloud API keys or local configuration directory.

- **Continue a task in another environment.** Mount the existing workspace instead of recreating its input files.
- **Share results with a reviewer.** Give the reviewer a read-only scoped token for a report directory.
- **Compare parallel approaches.** Fork layers for independent drafts, create checkpoints, and commit a selected result to the shared base.

## Work with files through the CLI or a mount

The CLI provides two ways to use the same remote Filesystem:

- **Direct file commands:** upload, download, list, read, and search files with `ti fs`. These commands do not require FUSE or a mount.
- **Local mounts:** expose remote files at a local directory so existing tools can use commands such as `cat`, `cp`, and `ls`. Linux uses FUSE. macOS uses WebDAV by default and can use macFUSE for layer and checkpoint mounts.

For example, after selecting a Filesystem and supplying its token:

```bash
# Read a remote file without mounting it.
ti fs read-file --path /workspace/report.md
```

Or mount the workspace on macOS or Linux:

```bash
# Give local tools a directory backed by the remote workspace.
mkdir -p "$HOME/workspace"
ti fs mount-file-system --remote-path /workspace --mount-path "$HOME/workspace"
cat "$HOME/workspace/report.md"
```

## Control sharing and changes

- [Authorization](/tidb-cloud-filesystem/filesystem-authorization.md) distinguishes resource-management credentials from owner and scoped Filesystem tokens.
- [Sharing Filesystems](/tidb-cloud-filesystem/filesystem-sharing.md) explains how participants access one remote workspace without sharing account credentials.
- [Branches and Checkpoints](/tidb-cloud-filesystem/filesystem-branches-checkpoints.md) explains layers, saved history points, and publishing changes to the base Filesystem.

## Before you begin

Choose how to access the Filesystem:

- **Create and manage a Filesystem:** obtain a TiDB Cloud API public key and private key from the [API Keys page](https://tidbcloud.com/org-settings/api-keys), then run `ti configure`. Follow the [Quick Start](/tidb-cloud-filesystem/filesystem-quick-start.md) to create a Filesystem and write your first file.
- **Use an existing Filesystem:** if someone has supplied an FS token, set `TI_FS_TOKEN` and `TI_REGION_CODE`. You do not need TiDB Cloud API keys or `ti configure` to access files within the token's permissions. Follow [Mounting Locally](/tidb-cloud-filesystem/filesystem-mount.md#use-a-token-without-configuring-a-profile).

See [Authorization](/tidb-cloud-filesystem/filesystem-authorization.md) for the differences between API keys, owner tokens, and scoped tokens. An FS token does not grant permission to create or delete a Filesystem through the CLI.

Choose a supported Filesystem region: `aws-us-east-1`, `aws-ap-southeast-1`, `aws-us-west-2`, or `alicloud-ap-southeast-1`. Keep compute close to that region when possible to reduce network latency.

Mount support depends on the operating system and its permissions. Windows supports direct file commands but not native mounting through `ti`. WebDAV does not support layer or checkpoint mounts. Buffered writes must reach the service before you remove an environment; a successful local write alone is not a durability guarantee.

These guides focus on file storage and access. TiDB Cloud Filesystem does not provision an agent's compute environment. A layer is not a security sandbox, and checkpoints do not snapshot the entire live base Filesystem.

## What's next

- [Create a Filesystem and write your first file](/tidb-cloud-filesystem/filesystem-quick-start.md).
- [Mount an existing Filesystem locally](/tidb-cloud-filesystem/filesystem-mount.md).
- [Try the interactive agent sandbox lab](https://labs.tidb.io/labs/demo_901).
