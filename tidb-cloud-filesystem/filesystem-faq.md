---
title: TiDB Cloud Filesystem FAQ
summary: Find answers about TiDB Cloud Filesystem usage, shared writes, regions, mounts, SDKs, search, checkpoints, preview policies, and pricing.
---

# TiDB Cloud Filesystem FAQ

TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## What is TiDB Cloud Filesystem?

TiDB Cloud Filesystem provides persistent, shared file storage for applications, automation, and AI agents. Files remain available independently of the machine or process that creates them, so another session, sandbox, agent, or reviewer can continue using the same workspace.

You can access files through TiDB Cloud CLI (`ti`) commands or mount the file system as a local directory. You do not need to provision or manage a TiDB database. For more information, see [TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-intro.md).

## Do I need TiDB Cloud Filesystem if my sandbox already provides persistence?

If your workflow stays within one sandbox platform, that platform's snapshots, pause and resume features, or persistent volumes might be sufficient. Consider TiDB Cloud Filesystem when you need to access the same working directory from another platform, machine, agent, reviewer, or CI job.

For examples, see [Automation and AI Agent Workflows](/tidb-cloud-filesystem/use-filesystem-for-automation-and-ai-agents.md).

## Are file changes immediately available to other environments?

Not necessarily. A mount can buffer changes locally before uploading them to the remote file system. FUSE mounts do this by default, so a local write does not mean that another environment can already read the updated file.

For a FUSE mount, stop applications from writing, close open files, and then use [`ti fs drain-file-system --mount-path <local-mount-path>`](/ai/ti/reference/ti-fs-drain-file-system.md) to upload pending writes while keeping the mount running. Normal FUSE unmount also uploads pending writes. WebDAV does not support this command; stop applications from writing, close open files, and unmount instead.

Before deleting the machine or its local cache, use `ti fs read-file` to verify that required changes reached the remote file system. If drain or unmount fails, keep the machine and its local data available for recovery. For details, see [Finish safely](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely).

## Which regions support TiDB Cloud Filesystem?

See [Supported regions](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md#supported-regions) for the current list. File system availability differs from TiDB Cloud Starter availability.

When creating a file system through the CLI, select a supported region with `ti configure`, or override the configured default for the command with `--region`. For the creation workflow, see [Get Started with TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-quick-start.md).

## Can I mount a file system on my laptop?

Yes, on macOS or Linux. For evaluation, it is recommended to use a cloud virtual machine (VM) in the same region as the file system. If you only need to read a remote file, use `ti fs read-file` without mounting.

Native mounting is not supported on Windows. For platform requirements and alternatives, see [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md).

## Does TiDB Cloud Filesystem support POSIX?

Yes. When mounted, TiDB Cloud Filesystem provides POSIX-compatible access: applications and agents can read and write files through normal local paths, shell commands, and file system APIs.

Mount capabilities differ by platform and driver. For example, layer and checkpoint mounts require FUSE. See [Mount platform support](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md#mount-platform-support).

## Are SDKs available for TiDB Cloud Filesystem?

Yes. You can use the Drive9 client SDKs for TypeScript, Go, Python, Rust, Kotlin, and Swift. Drive9 is the workspace engine used by TiDB Cloud Filesystem.

Use a file system token as the SDK API key, and set the server URL to the TiDB Cloud Filesystem endpoint for your file system's region. The default `https://api.drive9.ai` endpoint does not accept TiDB Cloud Filesystem tokens. An SDK release might include operations that the hosted service does not yet support, so check the SDK documentation before using it.

For endpoint mappings and integration guides, see [TiDB Cloud Filesystem SDKs](/tidb-cloud-filesystem/filesystem-sdks.md).

## Can I use semantic or vector search over my files?

Yes. Semantic search finds content by meaning using embeddings, which represent text as numerical vectors. To search images, audio, or video, configure media extraction to produce searchable text or descriptions.

Semantic search requires embeddings. Check the file system's embedding configuration before setting up a provider: some file systems use service-managed embeddings and do not allow a custom provider. Media extraction and custom embedding providers are optional and can be configured separately.

The `ti fs search-file-content` command accepts a text query for full-text and, when embeddings are available, semantic search. Its `--pattern` value is not a regular expression or glob. To find paths by name, type, tag, size, or modification time, use `ti fs find-files`.

For setup, see [Configure AI Providers for a File System](/tidb-cloud-filesystem/configure-filesystem-ai-providers.md). For search examples, see [Work with Files and Directories](/tidb-cloud-filesystem/work-with-filesystem-data.md).

## Does the public preview support checkpoints and rollback?

Yes. A layer lets you change files without changing the shared base file system until you commit the layer. Use `ti fs create-layer-checkpoint` to save a point in the layer's history. Use `ti fs rollback-layer` to discard its uncommitted changes.

Rollback does not restore an earlier checkpoint. To continue working from a checkpoint, fork it into a new writable layer. A checkpoint preserves layer history, but does not freeze the entire base file system or replace a backup. Complex layer histories have additional limitations during public preview; see [Boundaries and limitations](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md#boundaries-and-limitations).

For concepts and limitations, see [Layers and Checkpoints](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md). For commands, see [Manage File System Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md).

## Is a service-level agreement (SLA) available during public preview?

No. Keep a backup of evaluation data outside TiDB Cloud Filesystem and report unexpected behavior.

## What happens to my workspace after public preview ends?

The policy for retaining or deleting workspaces after public preview has not been finalized. Keep a backup of important data outside TiDB Cloud Filesystem.

## How much does TiDB Cloud Filesystem cost?

TiDB Cloud Filesystem uses pay-as-you-go pricing for reads, writes, storage, and internet egress. Each organization receives a $5.00 monthly free-tier allowance shared across all file systems, billing items, and regions. This allowance reduces usage charges; it is not a maximum monthly bill.

Public preview prices might change at general availability. For current regional rates, free-tier details, and limits without a credit card, see [TiDB Cloud Filesystem Pricing Details](https://www.pingcap.com/tidb-cloud-filesystem-pricing-details/).
