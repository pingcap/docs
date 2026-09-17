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

## Choose how to work with files

The CLI provides two ways to use the same remote Filesystem:

- **Direct file commands:** [Copy, read, organize, and search files](/tidb-cloud-filesystem/work-with-filesystem-data.md) with `ti fs`, without setting up a mount.
- **Local mounts:** [Expose remote files at a local directory](/tidb-cloud-filesystem/filesystem-mount.md) so existing tools can use filesystem paths. Mount support depends on your operating system.

## Control access and changes

- [Authorization](/tidb-cloud-filesystem/filesystem-authorization.md) explains when to use API keys, owner tokens, or scoped tokens.
- [Share a TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-sharing.md) shows how to give another machine access without sharing account credentials.
- [Layers and Checkpoints](/tidb-cloud-filesystem/filesystem-branches-checkpoints.md) explains how to isolate drafts and publish selected changes.

## Get started

If you need to create a Filesystem, follow [Get Started with TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-quick-start.md). You will need TiDB Cloud API keys with permission to create one.

If someone has given you access to an existing Filesystem, [use its FS token and region without configuring a profile](/tidb-cloud-filesystem/filesystem-mount.md#use-a-token-without-configuring-a-profile). You do not need the creator's API keys to access files within your token's permissions.

For supported regions, platform requirements, and current constraints, see [Regions and Limitations](/ai/ti/reference/ti-regions-security-and-limitations.md).

## What's next

- [Create a Filesystem and write your first file](/tidb-cloud-filesystem/filesystem-quick-start.md).
- [Share a Filesystem across machines](/tidb-cloud-filesystem/filesystem-sharing.md).
- [Explore automation and AI agent workflows](/tidb-cloud-filesystem/use-filesystem-for-automation-and-ai-agents.md).
- [Try the interactive agent sandbox lab](https://labs.tidb.io/labs/demo_901).
