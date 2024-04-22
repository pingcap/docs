---
title: Download TiDB Tools
summary: TiDB Toolkitには、Dumpling、TiDB Lightning、BRなどのツールが含まれており、インターネットアクセスがある場合はTiUPコマンドを使用してデプロイできます。また、TiDB Operatorを使用する場合はオフラインインストール手順に従ってください。
---

# TiDB ツールをダウンロード {#download-tidb-tools}

このドキュメントでは、 TiDB Toolkitのダウンロード方法について説明します。

TiDB Toolkit には、データ エクスポート ツールDumpling、データ インポート ツールTiDB Lightning、バックアップおよび復元ツールBRなど、頻繁に使用される TiDB ツールが含まれています。

> **ヒント：**
>
> -   デプロイメント環境にインターネット アクセスがある場合は、単一の[TiUPコマンド](/tiup/tiup-component-management.md)を使用して TiDB ツールをデプロイできるため、 TiDB Toolkitを個別にダウンロードする必要はありません。
> -   TiDB を Kubernetes にデプロイして維持する必要がある場合は、 TiDB Toolkitをダウンロードする代わりに、 [TiDB Operator のオフライン インストール](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-operator#offline-installation)の手順に従ってください。

## 環境要件 {#environment-requirements}

-   オペレーティングシステム: Linux
-   アーキテクチャ: amd64 または arm64

## ダウンロードリンク {#download-link}

TiDB Toolkitは次のリンクからダウンロードできます。

    https://download.pingcap.org/tidb-community-toolkit-{version}-linux-{arch}.tar.gz

リンク内の`{version}` TiDB のバージョン番号を示し、 `{arch}`システムのアーキテクチャ( `amd64`または`arm64`を示します。たとえば、 `amd64`アーキテクチャ内の`v6.2.0`のダウンロード リンクは`https://download.pingcap.org/tidb-community-toolkit-v6.2.0-linux-amd64.tar.gz`です。

> **注記：**
>
> [PD Control](/pd-control.md)ツールをダウンロードする必要がある場合`pd-ctl` 、 `https://download.pingcap.org/tidb-community-server-{version}-linux-{arch}.tar.gz`とは別に TiDB インストール パッケージをダウンロードします。

## TiDB Toolkitの説明 {#tidb-toolkit-description}

使用するツールに応じて、次のように対応するオフライン パッケージをインストールできます。

| 道具                                                                  | オフラインパッケージ名                                                                                                                                                         |
| :------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [TiUP](/tiup/tiup-overview.md)                                      | `tiup-linux-{arch}.tar.gz` <br/>`tiup-{tiup-version}-linux-{arch}.tar.gz` <br/>`dm-{tiup-version}-linux-{arch}.tar.gz` <br/> `server-{version}-linux-{arch}.tar.gz` |
| [Dumpling](/dumpling-overview.md)                                   | `dumpling-{version}-linux-{arch}.tar.gz`                                                                                                                            |
| [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)        | `tidb-lightning-ctl` <br/>`tidb-lightning-{version}-linux-{arch}.tar.gz`                                                                                            |
| [TiDB データ移行 (DM)](/dm/dm-overview.md)                               | `dm-worker-{version}-linux-{arch}.tar.gz` <br/>`dm-master-{version}-linux-{arch}.tar.gz` <br/>`dmctl-{version}-linux-{arch}.tar.gz`                                 |
| [TiCDC](/ticdc/ticdc-overview.md)                                   | `cdc-{version}-linux-{arch}.tar.gz`                                                                                                                                 |
| [TiDBBinlog](/tidb-binlog/tidb-binlog-overview.md)                  | `pump-{version}-linux-{arch}.tar.gz` <br/>`drainer-{version}-linux-{arch}.tar.gz` <br/>`binlogctl` <br/>`reparo`                                                    |
| [バックアップと復元 (BR)](/br/backup-and-restore-overview.md)                | `br-{version}-linux-{arch}.tar.gz`                                                                                                                                  |
| [同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md) | `sync_diff_inspector`                                                                                                                                               |
| [PD回復](/pd-recover.md)                                              | `pd-recover-{version}-linux-{arch}.tar`                                                                                                                             |

> **注記：**
>
> `{version}`インストールしているツールのバージョンによって異なります。 `{arch}`システムのアーキテクチャに応じて`amd64`または`arm64`になります。
