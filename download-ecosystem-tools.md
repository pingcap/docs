---
title: Download
summary: Download the most officially maintained versions of TiDB enterprise tools.
aliases: ['/docs/dev/download-ecosystem-tools/','/docs/dev/reference/tools/download/']
---

# Download

This document collects the available downloads for most officially maintained versions of TiDB enterprise tools.

## TiDB Binlog

If you want to download the latest version of [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md), directly download the TiDB package, because TiDB Binlog is included in the TiDB package.

In addition, the Kafka version of TiDB Binlog is also provided.

| Package name | OS | Architecture | SHA256 checksum |
|:---|:---|:---|:---|
| `https://download.pingcap.org/tidb-{version}-linux-amd64.tar.gz` (TiDB Binlog) | Linux | amd64 | `https://download.pingcap.org/tidb-{version}-linux-amd64.sha256` |
| `https://download.pingcap.org/tidb-binlog-kafka-linux-amd64.tar.gz` (the Kafka version of TiDB Binlog) | Linux | amd64 | `https://download.pingcap.org/tidb-binlog-kafka-linux-amd64.sha256` |

> **Note:**
>
> `{version}` in the above download link indicates the version number of TiDB. For example, the download link for `v3.0.5` is `https://download.pingcap.org/tidb-v3.0.5-linux-amd64.tar.gz`.

## TiDB Lightning

Download [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) by using the download link in the following table:

| Package name | OS | Architecture |  SHA256 checksum |
|:---|:---|:---|:---|
| `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.tar.gz` | Linux | amd64 | `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.sha256` |

> **Note:**
>
> `{version}` in the above download link indicates the version number of TiDB Lightning. For example, the download link for `v3.0.5` is `https://download.pingcap.org/tidb-toolkit-v3.0.5-linux-amd64.tar.gz`.

## BR (backup and restore)

Download [BR](/br/backup-and-restore-tool.md) by using the download link in the following table:

| Package name | OS | Architecure | SHA256 checksum |
|:---|:---|:---|:---|
| `http://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.tar.gz` | Linux | amd64 | `http://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.sha256` |

> **Note:**
>
> `{version}` in the above download link indicates the version number of BR. For example, the download link for `v3.1.0-beta` is `http://download.pingcap.org/tidb-toolkit-v3.1.0-beta-linux-amd64.tar.gz`.

## TiDB DM (Data Migration)

Download [DM](https://docs.pingcap.com/tidb-data-migration/v1.0/overview) by using the download link in the following table:

| Package name | OS | Architecture | SHA256 checksum |
|:---|:---|:---|:---|
| `https://download.pingcap.org/dm-{version}-linux-amd64.tar.gz` | Linux | amd64 | `https://download.pingcap.org/dm-{version}-linux-amd64.sha256` |

> **Note:**
>
> `{version}` in the above download link indicates the version number of DM. For example, the download link for `v1.0.1` is `https://download.pingcap.org/dm-v1.0.1-linux-amd64.tar.gz`. You can check the published DM versions in the [DM Release](https://github.com/pingcap/dm/releases) page.

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
