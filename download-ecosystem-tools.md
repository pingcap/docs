---
title: Download TiDB Tools
summary: TiDBツールの公式メンテナンス版をダウンロードしてください。
---

# TiDBツールをダウンロード {#download-tidb-tools}

このドキュメントでは、TiDB Toolkitのダウンロード方法について説明します。

TiDB Toolkitには、 Dumpling （データエクスポート）、 TiDB Lightning （データインポート）、 BR （バックアップと復元）、sync-diff-inspector（データ整合性チェック）など、頻繁に使用されるツールが含まれています。

> **ヒント：**
>
> -   TiDB v8.5.6以降では、sync-diff-inspectorを含むほとんどのツールがTiUPから直接利用できます。デプロイ環境にインターネット接続があれば、 [TiUPコマンド](/tiup/tiup-component-management.md)1つ使用してツールをデプロイできます。 TiDB Toolkitを別途ダウンロードする必要はありません。
> -   TiDB を Kubernetes 上にデプロイして保守する必要がある場合は、 TiDB Toolkit をダウンロードする代わりに、 [TiDB Operatorのオフラインインストール](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-operator#offline-installation)の手順に従ってください。

## 環境要件 {#environment-requirements}

-   オペレーティングシステム: Linux
-   アーキテクチャ：amd64またはarm64

## ダウンロードリンク {#download-link}

TiDB Toolkitは以下のリンクからダウンロードできます。

    https://download.pingcap.com/tidb-community-toolkit-{version}-linux-{arch}.tar.gz

リンク内の`{version}`は TiDB のバージョン番号を示し、 `{arch}`システムのアーキテクチャを示し、 `amd64`または`arm64`のいずれかになります。たとえば、 `v8.5.4`アーキテクチャの`amd64`のダウンロードリンクは`https://download.pingcap.com/tidb-community-toolkit-v8.5.4-linux-amd64.tar.gz`です。

> **注記：**
>
> [PD Control](/pd-control.md)ツール`pd-ctl`をダウンロードする必要がある場合は、TiDB インストール パッケージを`https://download.pingcap.com/tidb-community-server-{version}-linux-{arch}.tar.gz`から別途ダウンロードしてください。

## TiDB Toolkitの説明 {#tidb-toolkit-description}

使用したいツールに応じて、対応するオフラインパッケージを以下のようにインストールできます。

| 道具                                                                | オフラインパッケージ名                                                                                                                                                         |
| :---------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [TiUP](/tiup/tiup-overview.md)                                    | `tiup-linux-{arch}.tar.gz` <br/>`tiup-{tiup-version}-linux-{arch}.tar.gz` <br/>`dm-{tiup-version}-linux-{arch}.tar.gz` <br/> `server-{version}-linux-{arch}.tar.gz` |
| [Dumpling](/dumpling-overview.md)                                 | `dumpling-{version}-linux-{arch}.tar.gz`                                                                                                                            |
| [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)      | `tidb-lightning-ctl` <br/>`tidb-lightning-{version}-linux-{arch}.tar.gz`                                                                                            |
| [TiDBデータ移行（DM）](/dm/dm-overview.md)                               | `dm-worker-{version}-linux-{arch}.tar.gz` <br/>`dm-master-{version}-linux-{arch}.tar.gz` <br/>`dmctl-{version}-linux-{arch}.tar.gz`                                 |
| [TiCDC](/ticdc/ticdc-overview.md)                                 | `cdc-{version}-linux-{arch}.tar.gz`                                                                                                                                 |
| [バックアップと復元 (BR)](/br/backup-and-restore-overview.md)              | `br-{version}-linux-{arch}.tar.gz`                                                                                                                                  |
| [同期差分検査ツール](/sync-diff-inspector/sync-diff-inspector-overview.md) | TiDB v8.5.6以降の場合： `tiflow-{version}-linux-{arch}.tar.gz`<br/> v8.5.6より前のバージョンの場合： `sync_diff_inspector`                                                             |
| [PD回復](/pd-recover.md)                                            | `pd-recover-{version}-linux-{arch}.tar`                                                                                                                             |

> **注記：**
>
> `{version}`インストールするツールのバージョンによって異なります。 `{arch}` 、システムのアーキテクチャによって異なります。アーキテクチャは`amd64`または`arm64`のいずれかです。
