---
title: Download TiDB Tools
summary: Download the most officially maintained versions of TiDB tools.
aliases: ['/docs/dev/download-ecosystem-tools/','/docs/dev/reference/tools/download/']
---

# Download TiDB Tools

This document describes how to download the TiDB Toolkit.

TiDB Toolkit contains frequently used TiDB tools, such as data export tool Dumpling, data import tool TiDB Lightning, backup and restore tool BR, and data consistency checker sync-diff-inspector.

> **Tip:**
>
> - For TiDB v9.0.0 and later versions, most tools, including sync-diff-inspector, are directly available through TiUP. If your deployment environment has internet access, you can deploy a TiDB tool using a single [TiUP command](/tiup/tiup-component-management.md), so there is no need to download the TiDB Toolkit separately.
> - If you need to deploy and maintain TiDB on Kubernetes, instead of downloading the TiDB Toolkit, follow the steps in [TiDB Operator offline installation](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-operator#offline-installation).

## Environment requirements

- Operating system: Linux
- Architecture: amd64 or arm64

## Download link

You can download TiDB Toolkit from the following link:

```
https://download.pingcap.com/tidb-community-toolkit-{version}-linux-{arch}.tar.gz
```

`{version}` in the link indicates the version number of TiDB and `{arch}` indicates the architecture of the system, which can be `amd64` or `arm64`. For example, the download link for `v8.5.0` in the `amd64` architecture is `https://download.pingcap.com/tidb-community-toolkit-v8.5.0-linux-amd64.tar.gz`.

> **Note:**
>
> If you need to download the [PD Control](/pd-control.md) tool `pd-ctl`, download the TiDB installation package separately from `https://download.pingcap.com/tidb-community-server-{version}-linux-{arch}.tar.gz`.

## TiDB Toolkit description

Depending on which tools you want to use, you can install the corresponding offline packages as follows:

| Tool | Offline package name |
|:------|:----------|
| [TiUP](/tiup/tiup-overview.md)  | `tiup-linux-{arch}.tar.gz` <br/>`tiup-{tiup-version}-linux-{arch}.tar.gz` <br/>`dm-{tiup-version}-linux-{arch}.tar.gz` <br/> `server-{version}-linux-{arch}.tar.gz` |
| [Dumpling](/dumpling-overview.md)  | `dumpling-{version}-linux-{arch}.tar.gz`  |
| [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)  | `tidb-lightning-ctl` <br/>`tidb-lightning-{version}-linux-{arch}.tar.gz`  |
| [TiDB Data Migration (DM)](/dm/dm-overview.md)  | `dm-worker-{version}-linux-{arch}.tar.gz` <br/>`dm-master-{version}-linux-{arch}.tar.gz` <br/>`dmctl-{version}-linux-{arch}.tar.gz`  |
| [TiCDC](/ticdc/ticdc-overview.md)  | `cdc-{version}-linux-{arch}.tar.gz`  |
| [Backup & Restore (BR)](/br/backup-and-restore-overview.md)  | `br-{version}-linux-{arch}.tar.gz`  |
| [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md)  | For TiDB v9.0.0 and later versions: `tiflow-{version}-linux-{arch}.tar.gz` <br/>For TiDB versions before v9.0.0: `sync_diff_inspector`  |
| [PD Recover](/pd-recover.md)  | `pd-recover-{version}-linux-{arch}.tar` |

> **Note:**
>
> `{version}` depends on the version of the tool you are installing. `{arch}` depends on the architecture of the system, which can be `amd64` or `arm64`.
