---
title: Download TiDB Tools
summary: Download the most officially maintained versions of TiDB tools.
---

# TiDBツールをダウンロードする {#download-tidb-tools}

このドキュメントでは、TiDBツールキットをダウンロードする方法について説明します。

TiDB Toolkitには、データエクスポートツールDumpling、データインポートツールTiDB Lightning、バックアップと復元ツールBRなどの頻繁に使用されるTiDBツールが含まれています。

> **ヒント：**
>
> -   展開環境にインターネットアクセスがある場合は、単一の[TiUPコマンド](/tiup/tiup-component-management.md)を使用してTiDBツールを展開できるため、TiDBツールキットを個別にダウンロードする必要はありません。
> -   TiDB Toolkitをダウンロードする代わりに、KubernetesにTiDBをデプロイして維持する必要がある場合は、 [TiDB Operatorのオフラインインストール](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-operator#offline-installation)の手順に従ってください。

## 環境要件 {#environment-requirements}

-   オペレーティングシステム：Linux
-   アーキテクチャ：amd64

## ダウンロードリンク {#download-link}

TiDB Toolkitは、次のリンクからダウンロードできます。

```
https://download.pingcap.org/tidb-community-toolkit-{version}-linux-amd64.tar.gz
```

リンクの`{version}`は、TiDBのバージョン番号を示します。たとえば、 `v6.1.0`のダウンロードリンクは`https://download.pingcap.org/tidb-community-toolkit-v6.1.0-linux-amd64.tar.gz`です。

## TiDBツールキットの説明 {#tidb-toolkit-description}

使用するツールに応じて、対応するオフラインパッケージを次のようにインストールできます。

| 道具                                                                          | オフラインパッケージ名                                                                                                                      |
| :-------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| [TiUP](/tiup/tiup-overview.md)                                              | `tiup-linux-amd64.tar.gz` <br/>`tiup-{tiup-version}-linux-amd64.tar.gz` <br/>`dm-{tiup-version}-linux-amd64.tar.gz`              |
| [Dumpling](/dumpling-overview.md)                                           | `dumpling-{version}-linux-amd64.tar.gz`                                                                                          |
| [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)                | `tidb-lightning-ctl` <br/>`tidb-lightning-{version}-linux-amd64.tar.gz`                                                          |
| [TiDBデータ移行（DM）](/dm/dm-overview.md)                                         | `dm-worker-{version}-linux-amd64.tar.gz` <br/>`dm-master-{version}-linux-amd64.tar.gz` <br/>`dmctl-{version}-linux-amd64.tar.gz` |
| [TiCDC](/ticdc/ticdc-overview.md)                                           | `cdc-{version}-linux-amd64.tar.gz`                                                                                               |
| [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)                         | `pump-{version}-linux-amd64.tar.gz` <br/>`drainer-{version}-linux-amd64.tar.gz` <br/>`binlogctl` <br/>`reparo`                   |
| [バックアップと復元（BR）](/br/backup-and-restore-tool.md)                             | `br-{version}-linux-amd64.tar.gz`                                                                                                |
| [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) | `sync_diff_inspector`                                                                                                            |
| [TiSpark](/tispark-overview.md)                                             | `tispark-{tispark-version}-any-any.tar.gz` <br/>`spark-{spark-version}-any-any.tar.gz`                                           |
| [PD制御](/pd-control.md)                                                      | `pd-recover-{version}-linux-amd64.tar`                                                                                           |
| [PD回復](/pd-recover.md)                                                      | `etcdctl`                                                                                                                        |
