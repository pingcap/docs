---
title: Download TiDB Tools
summary: TiDB ツールの最も公式にメンテナンスされたバージョンをダウンロードします。
---

# TiDBツールをダウンロード {#download-tidb-tools}

このドキュメントでは、 TiDB Toolkitをダウンロードする方法について説明します。

TiDB Toolkit には、データ エクスポート ツールDumpling、データ インポート ツールTiDB Lightning、バックアップおよび復元ツールBRなど、頻繁に使用される TiDB ツールが含まれています。

> **ヒント：**
>
> -   デプロイメント環境にインターネット アクセスがある場合は、単一の[TiUPコマンド](/tiup/tiup-component-management.md)を使用して TiDB ツールをデプロイメントできるため、 TiDB Toolkitを個別にダウンロードする必要はありません。
> -   Kubernetes 上で TiDB をデプロイして保守する必要がある場合は、 TiDB Toolkit をダウンロードする代わりに、 [TiDB Operatorのオフラインインストール](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-operator#offline-installation)の手順に従います。

## 環境要件 {#environment-requirements}

-   オペレーティングシステム: Linux
-   アーキテクチャ: amd64 または arm64

## ダウンロードリンク {#download-link}

TiDB Toolkit は次のリンクからダウンロードできます。

    https://download.pingcap.com/tidb-community-toolkit-{version}-linux-{arch}.tar.gz

リンク内の`{version}` TiDBのバージョン番号を示し、 `{arch}`システムのアーキテクチャ（ `amd64`または`arm64`を示します。例えば、 `amd64`アーキテクチャの`v8.5.4`のダウンロードリンクは`https://download.pingcap.com/tidb-community-toolkit-v8.5.4-linux-amd64.tar.gz`です。

> **注記：**
>
> [PD Control](/pd-control.md)ツール`pd-ctl`をダウンロードする必要がある場合は、 `https://download.pingcap.com/tidb-community-server-{version}-linux-{arch}.tar.gz`から TiDB インストール パッケージを別途ダウンロードします。

## TiDB Toolkitの説明 {#tidb-toolkit-description}

使用するツールに応じて、次のように対応するオフライン パッケージをインストールできます。

| 道具                                                                  | オフラインパッケージ名                                                                                                                                                         |
| :------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [TiUP](/tiup/tiup-overview.md)                                      | `tiup-linux-{arch}.tar.gz` <br/>`tiup-{tiup-version}-linux-{arch}.tar.gz` <br/>`dm-{tiup-version}-linux-{arch}.tar.gz` <br/> `server-{version}-linux-{arch}.tar.gz` |
| [Dumpling](/dumpling-overview.md)                                   | `dumpling-{version}-linux-{arch}.tar.gz`                                                                                                                            |
| [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)        | `tidb-lightning-ctl` <br/>`tidb-lightning-{version}-linux-{arch}.tar.gz`                                                                                            |
| [TiDB データ移行 (DM)](/dm/dm-overview.md)                               | `dm-worker-{version}-linux-{arch}.tar.gz` <br/>`dm-master-{version}-linux-{arch}.tar.gz` <br/>`dmctl-{version}-linux-{arch}.tar.gz`                                 |
| [TiCDC](/ticdc/ticdc-overview.md)                                   | `cdc-{version}-linux-{arch}.tar.gz`                                                                                                                                 |
| [バックアップと復元 (BR)](/br/backup-and-restore-overview.md)                | `br-{version}-linux-{arch}.tar.gz`                                                                                                                                  |
| [同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md) | `sync_diff_inspector`                                                                                                                                               |
| [PD回復](/pd-recover.md)                                              | `pd-recover-{version}-linux-{arch}.tar`                                                                                                                             |

> **注記：**
>
> `{version}`はインストールするツールのバージョンによって異なります。2 `{arch}`システムのアーキテクチャによって異なり、 `amd64`または`arm64`になります。
