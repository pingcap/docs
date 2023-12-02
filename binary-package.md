---
title: TiDB Installation Packages
summary: Learn about TiDB installation packages and the specific components included.
---

# TiDB インストール パッケージ {#tidb-installation-packages}

[TiUP をオフラインで展開する](/production-deployment-using-tiup.md#deploy-tiup-offline)の前に、 [公式ダウンロードページ](https://en.pingcap.com/download/)で TiDB のバイナリ パッケージをダウンロードする必要があります。

TiDB バイナリ パッケージは、amd64 および arm64 アーキテクチャで利用できます。どちらのアーキテクチャでも、TiDB は 2 つのバイナリ パッケージ`TiDB-community-server`と`TiDB-community-toolkit`を提供します。

`TiDB-community-server`パッケージには以下の内容が含まれます。

| コンテンツ                                         | 変更履歴       |
| --------------------------------------------- | ---------- |
| tidb-{バージョン}-linux-{arch}.tar.gz              |            |
| tikv-{バージョン}-linux-{arch}.tar.gz              |            |
| tiflash-{バージョン}-linux-{arch}.tar.gz           |            |
| pd-{バージョン}-linux-{arch}.tar.gz                |            |
| ctl-{バージョン}-linux-{arch}.tar.gz               |            |
| grafana-{バージョン}-linux-{arch}.tar.gz           |            |
| alertmanager-{バージョン}-linux-{arch}.tar.gz      |            |
| blackbox_exporter-{バージョン}-linux-{arch}.tar.gz |            |
| prometheus-{バージョン}-linux-{arch}.tar.gz        |            |
| node_exporter-{バージョン}-linux-{arch}.tar.gz     |            |
| tiup-linux-{arch}.tar.gz                      |            |
| tiup-{バージョン}-linux-{arch}.tar.gz              |            |
| local_install.sh                              |            |
| クラスタ-{バージョン}-linux-{arch}.tar.gz              |            |
| Insight-{バージョン}-linux-{arch}.tar.gz           |            |
| diag-{バージョン}-linux-{arch}.tar.gz              | v6.0.0の新機能 |
| influxdb-{バージョン}-linux-{arch}.tar.gz          |            |
| playground-{バージョン}-linux-{arch}.tar.gz        |            |

> **注記：**
>
> `{version}`インストールするコンポーネントまたはサーバーのバージョンによって異なります。 `{arch}`システムのアーキテクチャに応じて`amd64`または`arm64`になります。

`TiDB-community-toolkit`パッケージには以下の内容が含まれます。

| コンテンツ                                         | 変更履歴       |
| --------------------------------------------- | ---------- |
| pd-recover-{バージョン}-linux-{arch}.tar.gz        |            |
| etcdctl                                       | v6.0.0の新機能 |
| tiup-linux-{arch}.tar.gz                      |            |
| tiup-{バージョン}-linux-{arch}.tar.gz              |            |
| tidb-lightning-{バージョン}-linux-{arch}.tar.gz    |            |
| tidb-ライトニング-ctl                               |            |
| dumpling-{バージョン}-linux-{arch}.tar.gz          |            |
| cdc-{バージョン}-linux-{arch}.tar.gz               |            |
| dm-{バージョン}-linux-{arch}.tar.gz                |            |
| dm-worker-{バージョン}-linux-{arch}.tar.gz         |            |
| dm-master-{バージョン}-linux-{arch}.tar.gz         |            |
| dmctl-{バージョン}-linux-{arch}.tar.gz             |            |
| br-{バージョン}-linux-{arch}.tar.gz                |            |
| パッケージ-{バージョン}-linux-{arch}.tar.gz             |            |
| ベンチ-{バージョン}-linux-{arch}.tar.gz               |            |
| errdoc-{バージョン}-linux-{arch}.tar.gz            |            |
| dba-{バージョン}-linux-{arch}.tar.gz               |            |
| PCC-{バージョン}-linux-{arch}.tar.gz               |            |
| ポンプ-{バージョン}-linux-{arch}.tar.gz               |            |
| drainer-{バージョン}-linux-{arch}.tar.gz           |            |
| binlogctl                                     | v6.0.0の新機能 |
| 同期差分インスペクター                                   |            |
| レパロ                                           |            |
| アービタ                                          |            |
| サーバー-{バージョン}-linux-{arch}.tar.gz              | v6.2.0の新機能 |
| grafana-{バージョン}-linux-{arch}.tar.gz           | v6.2.0の新機能 |
| alertmanager-{バージョン}-linux-{arch}.tar.gz      | v6.2.0の新機能 |
| prometheus-{バージョン}-linux-{arch}.tar.gz        | v6.2.0の新機能 |
| blackbox_exporter-{バージョン}-linux-{arch}.tar.gz | v6.2.0の新機能 |
| node_exporter-{バージョン}-linux-{arch}.tar.gz     | v6.2.0の新機能 |

> **注記：**
>
> `{version}`インストールしているツールのバージョンによって異なります。 `{arch}`システムのアーキテクチャに応じて`amd64`または`arm64`になります。

## こちらも参照 {#see-also}

[TiUP をオフラインでデプロイ](/production-deployment-using-tiup.md#deploy-tiup-offline)
