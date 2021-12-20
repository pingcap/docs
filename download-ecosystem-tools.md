---
title: Download TiDB Tools
summary: Download the most officially maintained versions of TiDB tools.
aliases: ['/docs/stable/download-ecosystem-tools/','/docs/v4.0/download-ecosystem-tools/','/docs/stable/reference/tools/download/','/docs/v4.0/reference/tools/download/']
---

# Download TiDB Tools

This document collects the available downloads for most officially maintained versions of TiDB tools.

## TiUP

You can install TiUP with a single command in both Darwin and Linux operating systems. For more information, see [Install TiUP](/tiup/tiup-overview.md#install-tiup).

## TiDB Operator

TiDB Operator runs in Kubernetes. After deploying the Kubernetes cluster, you can choose to deploy TiDB Operator either online or offline. For more information, see [Deploying TiDB Operator in Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-operator/).

## TiDB Binlog

If you want to download the latest version of [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md), directly download the TiDB package, because TiDB Binlog is included in the TiDB package.

| Package name | OS | Architecture | SHA256 checksum |
|:---|:---|:---|:---|
| `https://download.pingcap.org/tidb-{version}-linux-amd64.tar.gz` (TiDB Binlog) | Linux | amd64 | `https://download.pingcap.org/tidb-{version}-linux-amd64.sha256` |

> **Note:**
>
> `{version}` in the above download link indicates the version number of TiDB. For example, the download link for `v4.0.16` is `https://download.pingcap.org/tidb-v4.0.16-linux-amd64.tar.gz`.

## TiDB Lightning

Download [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) by using the download link in the following table:

| Package name | OS | Architecture |  SHA256 checksum |
|:---|:---|:---|:---|
| `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.tar.gz` | Linux | amd64 | `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.sha256` |

> **Note:**
>
> `{version}` in the above download link indicates the version number of TiDB Lightning. For example, the download link for `v4.0.16` is `https://download.pingcap.org/tidb-toolkit-v4.0.16-linux-amd64.tar.gz`.

## BR (backup and restore)

Download [BR](/br/backup-and-restore-tool.md) by using the download link in the following table:

| Package name | OS | Architecture | SHA256 checksum |
|:---|:---|:---|:---|
| `http://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.tar.gz` | Linux | amd64 | `http://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.sha256` |

> **Note:**
>
> `{version}` in the above download link indicates the version number of BR. For example, the download link for `v4.0.16` is `http://download.pingcap.org/tidb-toolkit-v4.0.16-linux-amd64.tar.gz`.

## TiDB DM (Data Migration)

Download [DM](https://docs.pingcap.com/tidb-data-migration/v1.0/overview) by using the download link in the following table:

| Package name | OS | Architecture | SHA256 checksum |
|:---|:---|:---|:---|
| `https://download.pingcap.org/dm-{version}-linux-amd64.tar.gz` | Linux | amd64 | `https://download.pingcap.org/dm-{version}-linux-amd64.sha256` |

> **Note:**
>
> `{version}` in the above download link indicates the version number of DM. For example, the download link for `v2.0.3` is `https://download.pingcap.org/dm-v2.0.3-linux-amd64.tar.gz`. You can check the published DM versions in the [DM Release](https://github.com/pingcap/dm/releases) page.

## Dumpling

Download [Dumpling](/dumpling-overview.md) from the links below:

| Installation package | Operating system | Architecture | SHA256 checksum |
|:---|:---|:---|:---|
| `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.tar.gz` | Linux | amd64 | `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.sha256` |

> **Note:**
>
> The `{version}` in the download link is the version number of Dumpling. For example, the link for downloading the `v4.0.16` version of Dumpling is `https://download.pingcap.org/tidb-toolkit-v4.0.16-linux-amd64.tar.gz`. You can view the currently released versions in [Dumpling Releases](https://github.com/pingcap/dumpling/releases).
>
> Dumpling supports arm64 linux. You can replace `amd64` in the download link with `arm64`, which means the `arm64` version of Dumpling.

## Syncer, Loader, and Mydumper

If you want to download the latest version of [Syncer](/syncer-overview.md), [Loader](/loader-overview.md), or [Mydumper](/mydumper-overview.md), directly download the tidb-enterprise-tools package, because all these tools are included in this package.

| Package name | OS | Architecture | SHA256 checksum |
|:---|:---|:---|:---|
| [tidb-enterprise-tools-nightly-linux-amd64.tar.gz](https://download.pingcap.org/tidb-enterprise-tools-nightly-linux-amd64.tar.gz) | Linux | amd64 | [tidb-enterprise-tools-nightly-linux-amd64.sha256](https://download.pingcap.org/tidb-enterprise-tools-nightly-linux-amd64.sha256) |

This enterprise tools package includes all the following tools:

- Syncer
- Loader
- Mydumper
- [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md)
