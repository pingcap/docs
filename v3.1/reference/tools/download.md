---
title: Download
summary: Download the most officially maintained versions of TiDB enterprise tools.
category: reference
---

# Download

This document collects the available downloads for most officially maintained versions of TiDB enterprise tools.

## TiDB Binlog

If you want to download the latest version of [TiDB Binlog](/v3.1/reference/tidb-binlog/overview.md), directly download the TiDB package, because TiDB Binlog is included in the TiDB package.

In addition, the Kafka version of TiDB Binlog is also provided.

| Package name | OS | Architecture | SHA256 checksum |
|:---|:---|:---|:---|
| `http://download.pingcap.org/tidb-{version}-linux-amd64.tar.gz` (TiDB Binlog) | Linux | amd64 | `http://download.pingcap.org/tidb-{version}-linux-amd64.sha256` |
| `http://download.pingcap.org/tidb-binlog-kafka-linux-amd64.tar.gz` (the Kafka version of TiDB Binlog) | Linux | amd64 | `http://download.pingcap.org/tidb-binlog-kafka-linux-amd64.sha256` |

> **Note:**
>
> `{version}` in the above download link indicates the version number of TiDB. For example, the download link for `v3.0.5` is `http://download.pingcap.org/tidb-v3.0.5-linux-amd64.tar.gz`. You can also download the latest unpublished version by replacing `{version}` with `latest`.

## TiDB Lightning

Download [TiDB Lightning](/v3.1/reference/tools/tidb-lightning/overview.md) by using the download link in the following table:

| Package name | OS | Architecture |  SHA256 checksum |
|:---|:---|:---|:---|
| `http://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.tar.gz` | Linux | amd64 | `http://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.sha256` |

> **Note:**
>
> `{version}` in the above download link indicates the version number of TiDB Lightning. For example, the download link for `v3.0.5` is `http://download.pingcap.org/tidb-toolkit-v3.0.5-linux-amd64.tar.gz`. You can also download the latest unpublished version by replacing `{version}` with `latest`.

## TiDB DM (Data Migration)

Download [DM](/v3.1/reference/tools/data-migration/overview.md) by using the download link in the following table:

| Package name | OS | Architecture | SHA256 checksum |
|:---|:---|:---|:---|
| `http://download.pingcap.org/dm-{version}-linux-amd64.tar.gz` | Linux | amd64 | `http://download.pingcap.org/dm-{version}-linux-amd64.sha256` |

> **Note:**
>
> `{version}` in the above download link indicates the version number of DM. For example, the download link for `v1.0.1` is `http://download.pingcap.org/dm-v1.0.1-linux-amd64.tar.gz`. You can check the published DM versions in the [DM Release](https://github.com/pingcap/dm/releases) page. You can also download the latest unpublished version by replacing `{version}` with `latest`.

## Syncer, Loader, and Mydumper

If you want to download the latest version of [Syncer](/v3.1/reference/tools/syncer.md), [Loader](/v3.1/reference/tools/loader.md), or [Mydumper](/v3.1/reference/tools/mydumper.md), directly download the tidb-enterprise-tools package, because all these tools are included in this package.

| Package name | OS | Architecture | SHA256 checksum |
|:---|:---|:---|:---|
| [tidb-enterprise-tools-latest-linux-amd64.tar.gz](http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz) | Linux | amd64 | [tidb-enterprise-tools-latest-linux-amd64.sha256](http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.sha256) |

This enterprise tools package includes all the following tools:

- Syncer
- Loader
- Mydumper
- ddl_checker
- [sync-diff-inspector](/v3.1/reference/tools/sync-diff-inspector/overview.md)
