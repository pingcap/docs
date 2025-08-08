---
title: TiDB Installation Packages
summary: TiDB インストール パッケージと、含まれる特定のコンポーネントについて説明します。
---

# TiDB インストール パッケージ {#tidb-installation-packages}

[TiUPをオフラインで展開する](/production-deployment-using-tiup.md#deploy-tiup-offline)前に、 [TiUPオフラインコンポーネントパッケージを準備する](/production-deployment-using-tiup.md#prepare-the-tiup-offline-component-package)で説明されているように TiDB のバイナリ パッケージをダウンロードする必要があります。

TiDBバイナリパッケージは、amd64およびarm64アーキテクチャで利用可能です。どちらのアーキテクチャでも、TiDBは`TiDB-community-server`と`TiDB-community-toolkit` 2つのバイナリパッケージを提供します。

`TiDB-community-server`パッケージには以下の内容物が入っています。

| コンテンツ                                            | 変更履歴           |
| ------------------------------------------------ | -------------- |
| tidb-{バージョン}-linux-{arch}.tar.gz                 |                |
| tikv-{バージョン}-linux-{アーキテクチャ}.tar.gz              |                |
| tiflash-{バージョン}-linux-{アーキテクチャ}.tar.gz           |                |
| pd-{バージョン}-linux-{アーキテクチャ}.tar.gz                |                |
| ctl-{バージョン}-linux-{アーキテクチャ}.tar.gz               |                |
| grafana-{バージョン}-linux-{アーキテクチャ}.tar.gz           |                |
| アラートマネージャー-{バージョン}-linux-{アーキテクチャ}.tar.gz        |                |
| blackbox_exporter-{バージョン}-linux-{アーキテクチャ}.tar.gz |                |
| prometheus-{バージョン}-linux-{アーキテクチャ}.tar.gz        |                |
| node_exporter-{バージョン}-linux-{アーキテクチャ}.tar.gz     |                |
| tiup-linux-{arch}.tar.gz                         |                |
| tiup-{バージョン}-linux-{アーキテクチャ}.tar.gz              |                |
| ローカルインストール.sh                                    |                |
| cluster-{バージョン}-linux-{アーキテクチャ}.tar.gz           |                |
| insight-{バージョン}-linux-{アーキテクチャ}.tar.gz           |                |
| diag-{バージョン}-linux-{アーキテクチャ}.tar.gz              | バージョン6.0.0の新機能 |
| influxdb-{バージョン}-linux-{アーキテクチャ}.tar.gz          |                |
| プレイグラウンド-{バージョン}-linux-{アーキテクチャ}.tar.gz          |                |
| tiproxy-{バージョン}-linux-{アーキテクチャ}.tar.gz           | バージョン7.6.0の新機能 |

> **注記：**
>
> `{version}` 、インストールするコンポーネントまたはサーバーのバージョンによって異なります。 `{arch}` 、システムのアーキテクチャによって異なり、 `amd64`または`arm64`になります。

`TiDB-community-toolkit`パッケージには以下の内容物が入っています。

| コンテンツ                                            | 変更履歴           |
| ------------------------------------------------ | -------------- |
| pd-recover-{バージョン}-linux-{アーキテクチャ}.tar.gz        |                |
| etcdctl                                          | バージョン6.0.0の新機能 |
| tiup-linux-{arch}.tar.gz                         |                |
| tiup-{バージョン}-linux-{アーキテクチャ}.tar.gz              |                |
| tidb-lightning-{バージョン}-linux-{アーキテクチャ}.tar.gz    |                |
| tidb-lightning-ctl                               |                |
| dumpling-{バージョン}-linux-{アーキテクチャ}.tar.gz          |                |
| cdc-{バージョン}-linux-{アーキテクチャ}.tar.gz               |                |
| dm-{バージョン}-linux-{アーキテクチャ}.tar.gz                |                |
| dm-worker-{バージョン}-linux-{アーキテクチャ}.tar.gz         |                |
| dm-master-{バージョン}-linux-{アーキテクチャ}.tar.gz         |                |
| dmctl-{バージョン}-linux-{アーキテクチャ}.tar.gz             |                |
| br-{バージョン}-linux-{アーキテクチャ}.tar.gz                |                |
| パッケージ-{バージョン}-linux-{アーキテクチャ}.tar.gz             |                |
| bench-{バージョン}-linux-{アーキテクチャ}.tar.gz             |                |
| errdoc-{バージョン}-linux-{アーキテクチャ}.tar.gz            |                |
| dba-{バージョン}-linux-{アーキテクチャ}.tar.gz               |                |
| PCC-{バージョン}-linux-{アーキテクチャ}.tar.gz               |                |
| 同期差分インスペクター                                      |                |
| レパロ                                              |                |
| サーバー-{バージョン}-linux-{アーキテクチャ}.tar.gz              | バージョン6.2.0の新機能 |
| grafana-{バージョン}-linux-{アーキテクチャ}.tar.gz           | バージョン6.2.0の新機能 |
| アラートマネージャー-{バージョン}-linux-{アーキテクチャ}.tar.gz        | バージョン6.2.0の新機能 |
| prometheus-{バージョン}-linux-{アーキテクチャ}.tar.gz        | バージョン6.2.0の新機能 |
| blackbox_exporter-{バージョン}-linux-{アーキテクチャ}.tar.gz | バージョン6.2.0の新機能 |
| node_exporter-{バージョン}-linux-{アーキテクチャ}.tar.gz     | バージョン6.2.0の新機能 |

> **注記：**
>
> `{version}`インストールするツールのバージョンによって異なります。2 `{arch}`システムのアーキテクチャによって異なり、 `amd64`または`arm64`になります。

## 参照 {#see-also}

[TiUPをオフラインでデプロイ](/production-deployment-using-tiup.md#deploy-tiup-offline)
