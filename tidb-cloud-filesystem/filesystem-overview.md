---
title: TiDB Cloud Filesystem Overview
summary: Learn what TiDB Cloud Filesystem is, when to use it, and how to access and share persistent files across applications, automation, and AI agents.
---

# TiDB Cloud Filesystem Overview

TiDB Cloud Filesystem is persistent, shared file storage that applications, automation, and AI agents can access across machines and sessions.

Use a Filesystem when files need to remain available after a local process or temporary environment ends, or when multiple environments need to work with the same files without repeatedly copying them between machines.

For example, you can use a Filesystem to:

- continue working with the same files from another machine or environment;
- share files or results with another user, application, CI job, or agent;
- mount shared files as a local directory for tools that expect local file paths; and
- isolate changes in layers before applying selected changes to shared files.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## How TiDB Cloud Filesystem works

Files in a TiDB Cloud Filesystem are stored independently of the machine or process that accesses them. When you move to another environment, you can access the same Filesystem instead of copying or recreating its files.

You use TiDB Cloud CLI (`ti`) to create and manage Filesystems and to work with their files. You do not need to provision or manage a separate database to use TiDB Cloud Filesystem.

You can work with Filesystem data in two main ways:

- **Use `ti fs` commands** to upload, download, read, organize, and search files directly without mounting the Filesystem.
- **Mount the Filesystem as a local directory** so applications and tools can work with its files through normal filesystem paths.

For more information, see [Work with Files and Directories](/tidb-cloud-filesystem/work-with-filesystem-data.md) and [Mount a TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-mount.md).

## Share files across environments

A Filesystem can be accessed from multiple machines or environments. Each environment can use its own credential instead of sharing the credentials of the user who created the Filesystem.

For example:

- a CI job can write build output to a Filesystem and another environment can read it later;
- an agent can continue working with files created during an earlier session; or
- a reviewer can receive read-only access to a specific directory.

TiDB Cloud Filesystem provides owner tokens and scoped tokens so you can control which files and operations each user or workload can access.

For more information, see [TiDB Cloud Filesystem Authorization](/tidb-cloud-filesystem/filesystem-authorization.md) and [Share a TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-sharing.md).

## Isolate and manage changes

When multiple tasks need to work from the same files without immediately changing the shared base, you can create Filesystem layers.

Each layer provides an isolated view where changes can be made independently. You can create checkpoints of a layer and later commit selected changes to the base Filesystem.

For more information, see [Layers and Checkpoints](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md).

## Get started

Choose the path that matches what you want to do:

- **Create a new Filesystem:** follow [Get Started with TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-quick-start.md).
- **Use a Filesystem that someone else has shared with you:** see [Access an Existing TiDB Cloud Filesystem](/tidb-cloud-filesystem/access-filesystem.md).
- **Check supported regions, platforms, and current limitations:** see [Regions and Limitations](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md).
