---
title: Download TiDB Tools
summary: Download the most officially maintained versions of TiDB tools.
---

# TiDB ツールをダウンロード {#download-tidb-tools}

このドキュメントでは、 TiDB Toolkitのダウンロード方法について説明します。

TiDB Toolkit には、データ エクスポート ツールDumpling、データ インポート ツールTiDB Lightning、バックアップおよび復元ツールBRなど、頻繁に使用される TiDB ツールが含まれています。

> **ヒント：**
>
> -   デプロイメント環境にインターネット アクセスがある場合は、単一の[<a href="/tiup/tiup-component-management.md">TiUPコマンド</a>](/tiup/tiup-component-management.md)を使用して TiDB ツールをデプロイできるため、 TiDB Toolkitを個別にダウンロードする必要はありません。
> -   TiDB を Kubernetes にデプロイして維持する必要がある場合は、 TiDB Toolkitをダウンロードする代わりに、 [<a href="https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-operator#offline-installation">TiDB Operator のオフライン インストール</a>](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-operator#offline-installation)の手順に従ってください。

## 環境要件 {#environment-requirements}

-   オペレーティングシステム: Linux
-   アーキテクチャ: amd64 または arm64

## ダウンロードリンク {#download-link}

TiDB Toolkitは次のリンクからダウンロードできます。

```
https://download.pingcap.org/tidb-community-toolkit-{version}-linux-{arch}.tar.gz
```

リンク内の`{version}` TiDB のバージョン番号を示し、 `{arch}`システムのアーキテクチャ( `amd64`または`arm64`を示します。たとえば、 `amd64`アーキテクチャ内の`v6.2.0`のダウンロード リンクは`https://download.pingcap.org/tidb-community-toolkit-v6.2.0-linux-amd64.tar.gz`です。

> **ノート：**
>
> [<a href="/pd-control.md">PD Control</a>](/pd-control.md)ツール`pd-ctl`をダウンロードする必要がある場合は、 `https://download.pingcap.org/tidb-community-server-{version}-linux-{arch}.tar.gz`とは別に TiDB インストール パッケージをダウンロードします。

## TiDB Toolkitの説明 {#tidb-toolkit-description}

使用するツールに応じて、次のように対応するオフライン パッケージをインストールできます。

| 道具                                                                                                                                     | オフラインパッケージ名                                                                                                                                                         |
| :------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [<a href="/tiup/tiup-overview.md">TiUP</a>](/tiup/tiup-overview.md)                                                                    | `tiup-linux-{arch}.tar.gz` <br/>`tiup-{tiup-version}-linux-{arch}.tar.gz` <br/>`dm-{tiup-version}-linux-{arch}.tar.gz` <br/> `server-{version}-linux-{arch}.tar.gz` |
| [<a href="/dumpling-overview.md">Dumpling</a>](/dumpling-overview.md)                                                                  | `dumpling-{version}-linux-{arch}.tar.gz`                                                                                                                            |
| [<a href="/tidb-lightning/tidb-lightning-overview.md">TiDB Lightning</a>](/tidb-lightning/tidb-lightning-overview.md)                  | `tidb-lightning-ctl` <br/>`tidb-lightning-{version}-linux-{arch}.tar.gz`                                                                                            |
| [<a href="/dm/dm-overview.md">TiDB データ移行 (DM)</a>](/dm/dm-overview.md)                                                                 | `dm-worker-{version}-linux-{arch}.tar.gz` <br/>`dm-master-{version}-linux-{arch}.tar.gz` <br/>`dmctl-{version}-linux-{arch}.tar.gz`                                 |
| [<a href="/ticdc/ticdc-overview.md">TiCDC</a>](/ticdc/ticdc-overview.md)                                                               | `cdc-{version}-linux-{arch}.tar.gz`                                                                                                                                 |
| [<a href="/tidb-binlog/tidb-binlog-overview.md">TiDBBinlog</a>](/tidb-binlog/tidb-binlog-overview.md)                                  | `pump-{version}-linux-{arch}.tar.gz` <br/>`drainer-{version}-linux-{arch}.tar.gz` <br/>`binlogctl` <br/>`reparo`                                                    |
| [<a href="/br/backup-and-restore-overview.md">バックアップと復元 (BR)</a>](/br/backup-and-restore-overview.md)                                  | `br-{version}-linux-{arch}.tar.gz`                                                                                                                                  |
| [<a href="/sync-diff-inspector/sync-diff-inspector-overview.md">同期差分インスペクター</a>](/sync-diff-inspector/sync-diff-inspector-overview.md) | `sync_diff_inspector`                                                                                                                                               |
| [<a href="/tispark-overview.md">ティスパーク</a>](/tispark-overview.md)                                                                      | `tispark-{tispark-version}-any-any.tar.gz` <br/>`spark-{spark-version}-any-any.tar.gz`                                                                              |
| [<a href="/pd-recover.md">PD回復</a>](/pd-recover.md)                                                                                    | `pd-recover-{version}-linux-{arch}.tar`                                                                                                                             |

> **ノート：**
>
> `{version}`インストールしているツールのバージョンによって異なります。 `{arch}`システムのアーキテクチャに応じて`amd64`または`arm64`になります。
