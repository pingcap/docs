---
title: TiDB Installation Packages
summary: Learn about TiDB installation packages and the specific components included.
---

# TiDB インストール パッケージ {#tidb-installation-packages}

[TiUPのオフライン展開](/production-deployment-using-tiup.md#deploy-tiup-offline)の前に、 [公式ダウンロードページ](https://en.pingcap.com/download/)で TiDB のバイナリ パッケージをダウンロードする必要があります。

TiDB バイナリ パッケージは、amd64 および arm64 アーキテクチャで利用できます。どちらのアーキテクチャでも、TiDB は`TiDB-community-server`と`TiDB-community-toolkit` 2 つのバイナリ パッケージを提供します。

`TiDB-community-server`包の内容は以下の通りです。

| コンテンツ                                         | 変更履歴        |
| --------------------------------------------- | ----------- |
| tidb-{バージョン}-linux-{アーチ}.tar.gz               |             |
| tikv-{バージョン}-linux-{アーチ}.tar.gz               |             |
| tiflash-{バージョン}-linux-{アーチ}.tar.gz            |             |
| pd-{version}-linux-{arch}.tar.gz              |             |
| ctl-{バージョン}-linux-{アーチ}.tar.gz                |             |
| grafana-{version}-linux-{arch}.tar.gz         |             |
| alertmanager-{バージョン}-linux-{arch}.tar.gz      |             |
| blackbox_exporter-{バージョン}-linux-{arch}.tar.gz |             |
| prometheus-{バージョン}-linux-{arch}.tar.gz        |             |
| node_exporter-{バージョン}-linux-{arch}.tar.gz     |             |
| tiup-linux-{arch}.tar.gz                      |             |
| tiup-{バージョン}-linux-{アーチ}.tar.gz               |             |
| local_install.sh                              |             |
| cluster-{version}-linux-{arch}.tar.gz         |             |
| Insight-{バージョン}-linux-{arch}.tar.gz           |             |
| diag-{version}-linux-{arch}.tar.gz            | v6.0.0 の新機能 |
| influxdb-{バージョン}-linux-{arch}.tar.gz          |             |
| 遊び場-{バージョン}-linux-{アーチ}.tar.gz                |             |

> **ノート：**
>
> `{version}`インストールするコンポーネントまたはサーバーのバージョンによって異なります。 `{arch}`システムのアーキテクチャに依存し、 `amd64`または`arm64`の場合があります。

`TiDB-community-toolkit`包の内容は以下の通りです。

| コンテンツ                                         | 変更履歴        |
| --------------------------------------------- | ----------- |
| tikv-importer-{バージョン}-linux-{アーチ}.tar.gz      |             |
| pd-recover-{version}-linux-{arch}.tar.gz      |             |
| etcdctl                                       | v6.0.0 の新機能 |
| tiup-linux-{arch}.tar.gz                      |             |
| tiup-{バージョン}-linux-{アーチ}.tar.gz               |             |
| tidb-lightning-{version}-linux-{arch}.tar.gz  |             |
| tidb-lightning-ctl                            |             |
| dumpling-{バージョン}-linux-{arch}.tar.gz          |             |
| cdc-{バージョン}-linux-{arch}.tar.gz               |             |
| dm-{バージョン}-linux-{アーチ}.tar.gz                 |             |
| dm-worker-{バージョン}-linux-{arch}.tar.gz         |             |
| dm-master-{バージョン}-linux-{アーチ}.tar.gz          |             |
| dmctl-{バージョン}-linux-{アーチ}.tar.gz              |             |
| br-{バージョン}-linux-{アーチ}.tar.gz                 |             |
| spark-{バージョン}-any-any.tar.gz                  |             |
| tispark-{バージョン}-any-any.tar.gz                |             |
| package-{version}-linux-{arch}.tar.gz         |             |
| ベンチ-{バージョン}-linux-{アーチ}.tar.gz                |             |
| errdoc-{バージョン}-linux-{アーチ}.tar.gz             |             |
| dba-{バージョン}-linux-{アーチ}.tar.gz                |             |
| PCC-{バージョン}-linux-{アーキテクチャ}.tar.gz            |             |
| pump-{バージョン}-linux-{arch}.tar.gz              |             |
| drainer-{バージョン}-linux-{アーチ}.tar.gz            |             |
| binlogctl                                     | v6.0.0 の新機能 |
| sync_diff_inspector                           |             |
| レパロ                                           |             |
| アービタ                                          |             |
| マイダンパー                                        | v6.0.0 の新機能 |
| サーバー-{バージョン}-linux-{arch}.tar.gz              | v6.2.0 の新機能 |
| grafana-{version}-linux-{arch}.tar.gz         | v6.2.0 の新機能 |
| alertmanager-{バージョン}-linux-{arch}.tar.gz      | v6.2.0 の新機能 |
| prometheus-{バージョン}-linux-{arch}.tar.gz        | v6.2.0 の新機能 |
| blackbox_exporter-{バージョン}-linux-{arch}.tar.gz | v6.2.0 の新機能 |
| node_exporter-{バージョン}-linux-{arch}.tar.gz     | v6.2.0 の新機能 |

> **ノート：**
>
> `{version}`インストールするツールのバージョンによって異なります。 `{arch}`システムのアーキテクチャに依存し、 `amd64`または`arm64`の場合があります。

## こちらもご覧ください {#see-also}

[TiUP をオフラインでデプロイ](/production-deployment-using-tiup.md#deploy-tiup-offline)
