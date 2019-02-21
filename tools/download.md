---
title: Download
summary: Download the most officially maintained versions of TiDB enterprise tools.
category: resources
---

# Download

This document collects the available downloads for most officially maintained versions of TiDB enterprise tools.

## TiDB-Binlog and Lightning

If you want to download the latest version of [TiDB-Binlog](../tools/tidb-binlog-cluster.md) or [Lightning](../tools/lightning/overview-architecture.md), directly download the TiDB package, because both TiDB-Binlog and Lightning are included in the TiDB package.

In addition, the Kafka version of TiDB-Binlog is also provided.

| Package name | OS | Architecture | SHA256 checksum |
|:---|:---|:---|:---|
| [tidb-latest-linux-amd64.tar.gz](http://download.pingcap.org/tidb-latest-linux-amd64.tar.gz) (TiDB-Binlog, Lightning) | Linux | amd64 |[tidb-latest-linux-amd64.sha256](http://download.pingcap.org/tidb-latest-linux-amd64.sha256)|
| [tidb-binlog-kafka-linux-amd64.tar.gz](http://download.pingcap.org/tidb-binlog-kafka-linux-amd64.tar.gz) (the Kafka version of TiDB-Binlog) | Linux | amd64 |[tidb-binlog-kafka-linux-amd64.sha256](http://download.pingcap.org/tidb-binlog-kafka-linux-amd64.sha256)|

## DM (Data Migration)

If you want to download the latest version of [DM](../tools/dm/overview.md), click the download link in the following table. You can also check the [DM Release](https://github.com/pingcap/dm/releases) page.

| Package name | OS | Architecture |  SHA256 checksum |
|:---|:---|:---|:---|
| [dm-latest-linux-amd64.tar.gz](http://download.pingcap.org/dm-latest-linux-amd64.tar.gz) | Linux | amd64 | [dm-latest-linux-amd64.sha256](http://download.pingcap.org/dm-latest-linux-amd64.sha256) |

## Syncer, Loader, and mydumper

If you want to download the latest version of [Syncer](../tools/syncer.md), [Loader](../tools/loader.md), or [mydumper](../tools/mydumper.md), directly download the tidb-enterprise-tools package, because all these tools are included in this package.

| Package name | OS | Architecture | SHA256 checksum |
|:---|:---|:---|:---|
| [tidb-enterprise-tools-latest-linux-amd64.tar.gz](http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz) | Linux | amd64 | [tidb-enterprise-tools-latest-linux-amd64.sha256](http://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.sha256) |

This enterprise tools package includes all the following tools:

- Syncer
- Loader
- mydumper
- [binlogctl](../tools/tidb-binlog-cluster.md#binlogctl-guide)
- ddl_checker
- [sync_diff_inspector](../tools/sync-diff-inspector.md)