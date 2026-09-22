---
title: TiDB Cloud Filesystem
summary: Learn what TiDB Cloud Filesystem is, when to use it, and how to access and share persistent files across applications, automation, and AI agents.
---

# TiDB Cloud Filesystem

TiDB Cloud Filesystem is a persistent, shared cloud file system for applications, automation, and AI agents. Files remain available independently of the machine or process that creates them, so you can reuse the same workspace across sessions and environments.

Use TiDB Cloud Filesystem when files need to remain available after a process or sandbox ends, when your workflow spans multiple machines or temporary environments, or when multiple users or workloads need controlled access to the same files.

For example, you can use a Filesystem for the following tasks:

- Access and modify the same files from different machines or environments.
- Share files and results with users, applications, CI jobs, or AI agents.
- Mount the Filesystem as a local directory for tools that require local file paths.
- Isolate file changes in layers before applying them to shared files.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## How TiDB Cloud Filesystem works

TiDB Cloud Filesystem persists in TiDB Cloud independently of the machines and processes that access it. Different authorized environments can therefore access the same files without copying them between machines.

To create and manage Filesystems and access their files, you can use [TiDB Cloud CLI (`ti`)](/ai/ti/ti-overview.md). You do not need to provision or manage a TiDB database to use TiDB Cloud Filesystem.

You can access and work with Filesystem data in two ways:

- **Use `ti fs` commands**: upload, download, read, organize, and search files directly from the command line without mounting the Filesystem.
- **Mount the Filesystem as a local directory**: let applications and tools access Filesystem data through normal local file paths.

For more information, see [Work with Files and Directories](/tidb-cloud-filesystem/work-with-filesystem-data.md) and [Mount TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-mount.md).

## Share files across environments

Multiple machines or environments can access a Filesystem simultaneously. Each environment can use its own Filesystem token, so credentials do not need to be shared across environments.

For example:

- A CI job can write build output to a Filesystem and another environment can read it later.
- An AI agent can continue working on files created during an earlier session.
- A reviewer can receive read-only access to a specific directory.

TiDB Cloud Filesystem provides owner tokens and scoped tokens so you can control which files and operations each user or workload can access.

For more information, see [TiDB Cloud Filesystem Authorization](/tidb-cloud-filesystem/filesystem-authorization.md) and [Share a TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-sharing.md).

## Isolate and manage changes

To let multiple tasks work from the same files without modifying the shared base, you can create Filesystem layers.

Each layer provides an isolated view where changes can be made independently. You can create checkpoints for a layer and later commit selected changes to the base Filesystem.

For more information, see [Layers and Checkpoints](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md).

## Get started

Choose the path that matches what you want to do:

- **Create a new Filesystem:** follow [Get Started with TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-quick-start.md).
- **Use a Filesystem that someone else has shared with you:** see [Access an Existing TiDB Cloud Filesystem](/tidb-cloud-filesystem/access-filesystem.md).
- **Check supported regions, platforms, and current limitations:** see [Regions and Limitations](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md).
