---
title: Download TiDB Tools
summary: Download the most officially maintained versions of TiDB tools.
---

# TiDB ツールをダウンロード {#download-tidb-tools}

このドキュメントでは、 TiDB Toolkitをダウンロードする方法について説明します。

TiDB Toolkit には、データ エクスポート ツールDumpling、データ インポート ツールTiDB Lightning、バックアップおよび復元ツールBRなど、頻繁に使用される TiDB ツールが含まれています。

> **ヒント：**
>
> -   展開環境がインターネットにアクセスできる場合は、単一の[TiUPコマンド](/tiup/tiup-component-management.md)を使用して TiDB ツールを展開できるため、 TiDB Toolkit を個別にダウンロードする必要はありません。
> -   TiDB Toolkitをダウンロードする代わりに、Kubernetes に TiDB をデプロイして維持する必要がある場合は、 [TiDB Operatorオフライン インストール](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-operator#offline-installation)の手順に従ってください。

## 環境要件 {#environment-requirements}

-   オペレーティング システム: Linux
-   アーキテクチャ: amd64 または arm64

## ダウンロードリンク {#download-link}

次のリンクからTiDB Toolkitをダウンロードできます。

```
https://download.pingcap.org/tidb-community-toolkit-{version}-linux-{arch}.tar.gz
```

リンクの`{version}`は TiDB のバージョン番号を示し、 `{arch}`システムのアーキテクチャを示します。これは`amd64`または`arm64`です。たとえば、 `amd64`アーキテクチャの`v6.2.0`のダウンロード リンクは`https://download.pingcap.org/tidb-community-toolkit-v6.2.0-linux-amd64.tar.gz`です。

> **ノート：**
>
> [PD Control](/pd-control.md)ツール`pd-ctl`をダウンロードする必要がある場合は、 `https://download.pingcap.org/tidb-community-server-{version}-linux-{arch}.tar.gz`とは別に TiDB インストール パッケージをダウンロードします。

## TiDB Toolkitの説明 {#tidb-toolkit-description}

使用するツールに応じて、対応するオフライン パッケージを次のようにインストールできます。

| 道具                                                                  | オフライン パッケージ名                                                                                                                                                        |
| :------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [TiUP](/tiup/tiup-overview.md)                                      | `tiup-linux-{arch}.tar.gz` <br/>`tiup-{tiup-version}-linux-{arch}.tar.gz` <br/>`dm-{tiup-version}-linux-{arch}.tar.gz` <br/> `server-{version}-linux-{arch}.tar.gz` |
| [Dumpling](/dumpling-overview.md)                                   | `dumpling-{version}-linux-{arch}.tar.gz`                                                                                                                            |
| [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)        | `tidb-lightning-ctl` <br/>`tidb-lightning-{version}-linux-{arch}.tar.gz`                                                                                            |
| [TiDB データ移行 (DM)](/dm/dm-overview.md)                               | `dm-worker-{version}-linux-{arch}.tar.gz` <br/>`dm-master-{version}-linux-{arch}.tar.gz` <br/>`dmctl-{version}-linux-{arch}.tar.gz`                                 |
| [TiCDC](/ticdc/ticdc-overview.md)                                   | `cdc-{version}-linux-{arch}.tar.gz`                                                                                                                                 |
| [TiDBBinlog](/tidb-binlog/tidb-binlog-overview.md)                  | `pump-{version}-linux-{arch}.tar.gz` <br/>`drainer-{version}-linux-{arch}.tar.gz` <br/>`binlogctl` <br/>`reparo`                                                    |
| [バックアップと復元 (BR)](/br/backup-and-restore-overview.md)                | `br-{version}-linux-{arch}.tar.gz`                                                                                                                                  |
| [同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md) | `sync_diff_inspector`                                                                                                                                               |
| [ティスパーク](/tispark-overview.md)                                      | `tispark-{tispark-version}-any-any.tar.gz` <br/>`spark-{spark-version}-any-any.tar.gz`                                                                              |
| [PD 回復](/pd-recover.md)                                             | `pd-recover-{version}-linux-{arch}.tar`                                                                                                                             |

> **ノート：**
>
> `{version}`インストールするツールのバージョンによって異なります。 `{arch}`システムのアーキテクチャに依存し、 `amd64`または`arm64`の場合があります。
