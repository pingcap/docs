---
title: TiDB Cloud File System Overview
summary: TiDB Cloud File System is a distributed file system for AI agents, built on TiDB Cloud's elastic storage. It provides transparent scaling, multi-agent collaboration, git-aware workspaces, semantic search, configurable consistency, and optional local caching.
---

# TiDB Cloud File System Overview

TiDB Cloud File System is a distributed file system designed for AI agent workloads. Built on TiDB Cloud's elastic storage layer, it provides transparent scaling, shared access across multiple agents, git-aware workspaces, semantic search, and configurable consistency — all without manual infrastructure management.

> **Warning:**
>
> TiDB Cloud File System is currently in **preview**. Feature availability and service limits might change as we continue to improve the product.

## Key features

| Feature | Description |
|---------|-------------|
| **Transparent Scaling** | Storage and throughput scale automatically as your workload grows. No capacity planning or manual provisioning is needed. |
| **Multi-Agent Collaboration** | Multiple agents can read and write to the same file system concurrently. TiDB Cloud handles distributed locking, conflict resolution, and atomic operations transparently. |
| **Git-Aware Workspace** | The file system understands commit, branch, and checkout semantics. Agents can snapshot workspace state, run parallel experiments on branches, and merge outputs seamlessly. |
| **Local Overlay with Auto Pack/Unpack** | An optional local caching layer stores frequently accessed files on the agent's local disk. The system automatically packs directories into efficient storage bundles and unpacks them on demand. |
| **Semantic Search** | Powered by TiDB Cloud's vector search, the file system indexes file contents as embeddings. You can search millions of files using natural language queries instead of filenames and grep. |
| **Optional Layered File System** | Stack multiple file system layers — each with its own storage backend, caching policy, and access semantics — into a unified mount point. Common layers include agent outputs (ephemeral), shared datasets (read-only), tool configurations (versioned), and base system (read-only). |
| **Configurable Consistency** | Choose the right consistency level for your workload: writeback (async commit queue for maximum throughput), close-sync (read-after-close visibility), or write-sync (read-after-write guarantees). |

## Use cases

- **Multi-agent coding workflows**: Multiple AI agents collaborate on a shared codebase, with git-aware snapshots and branching supporting parallel experimentation.
- **Long-running agent sessions**: Agents persist workspace state across sessions with configurable consistency for safe concurrent access.
- **Data pipeline agents**: Agents read datasets from a shared layer, write processed results to an output layer, and use semantic search to locate relevant files.
- **Agent evaluation and benchmarking**: Each agent run produces results in its own branch, making diff and comparison straightforward.

## Architecture overview

TiDB Cloud File System uses a layered architecture:

- **Storage layer**: Backed by TiDB Cloud's elastic storage, providing transparent scaling and high durability.
- **Consistency layer**: Configurable writeback, close-sync, or write-sync modes to match workload requirements.
- **Caching layer**: Optional local overlay that reduces latency for frequently accessed files.
- **Layering system**: Multiple logical layers can be stacked to separate data by lifecycle, access pattern, or access control.
- **Indexing layer**: Content embeddings enable semantic search across the file system.

## Consistency modes

| Mode | Behavior | Best for |
|------|----------|----------|
| **Writeback** | Writes go to local cache first. An async commit queue flushes changes to remote storage. | Bulk writes, log aggregation, throughput-sensitive workloads |
| **Close-sync** | Changes sync to remote storage when the file is closed. Other agents see the latest version after close. | Agent workspaces where files are written then read by other agents |
| **Write-sync** | Every write is confirmed on remote storage before returning. Provides read-after-write guarantees. | Critical shared state, coordination files, metadata |

## Get started

1. [**Quick Start**](/tidb-cloud-filesystem/fs-quick-start.md): Set up your first TiDB Cloud File System and connect an agent.
2. **Explore pricing**: Review the pricing model and estimate costs for your workload.
3. **Learn about consistency**: Choose the right consistency mode for your use case.

## Pricing

TiDB Cloud File System pricing is based on stored data volume and data transfer. <!-- TODO: update with final pricing when available -->

For the latest pricing details, see [Pricing & Billing](/tidb-cloud-filesystem/pricing-billing.md).

## Limitations

<!-- TODO: add limitations when product scope is finalized -->

- TiDB Cloud File System is in preview. Do not use for production workloads.
- Availability might be limited to specific cloud regions.

## See also

- [TiDB Cloud File System Quick Start](/tidb-cloud-filesystem/fs-quick-start.md)
- [TiDB Cloud Documentation](https://docs.pingcap.com/tidbcloud)
