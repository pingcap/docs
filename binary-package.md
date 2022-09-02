---
title: TiDB Installation Packages
summary: Learn about TiDB installation packages and the specific components included.
---

# TiDB インストール パッケージ {#tidb-installation-packages}

[TiUP のオフライン展開](/production-deployment-using-tiup.md#deploy-tiup-offline)の前に、 [公式ダウンロードページ](https://en.pingcap.com/download/)で TiDB のバイナリ パッケージをダウンロードする必要があります。

TiDB は`TiDB-community-server`と`TiDB-community-toolkit`の 2 つのバイナリ パッケージを提供します。

`TiDB-community-server`包の内容は以下の通りです。

| コンテンツ                                        | 変更履歴        |
| -------------------------------------------- | ----------- |
| tidb-{バージョン}-linux-amd64.tar.gz              |             |
| tikv-{バージョン}-linux-amd64.tar.gz              |             |
| tiflash-{バージョン}-linux-amd64.tar.gz           |             |
| pd-{バージョン}-linux-amd64.tar.gz                |             |
| ctl-{バージョン}-linux-amd64.tar.gz               |             |
| grafana-{バージョン}-linux-amd64.tar.gz           |             |
| alertmanager-{バージョン}-linux-amd64.tar.gz      |             |
| blackbox_exporter-{バージョン}-linux-amd64.tar.gz |             |
| プロメテウス-{バージョン}-linux-amd64.tar.gz            |             |
| node_exporter-{バージョン}-linux-amd64.tar.gz     |             |
| tiup-linux-amd64.tar.gz                      |             |
| tiup-{バージョン}-linux-amd64.tar.gz              |             |
| local_install.sh                             |             |
| クラスター-{バージョン}-linux-amd64.tar.gz             |             |
| インサイト-{バージョン}-linux-amd64.tar.gz             |             |
| diag-{バージョン}-linux-amd64.tar.gz              | v6.0.0 の新機能 |
| influxdb-{バージョン}-linux-amd64.tar.gz          |             |
| 遊び場-{バージョン}-linux-amd64.tar.gz               |             |

`TiDB-community-toolkit`包の内容は以下の通りです。

| コンテンツ                                        | 変更履歴        |
| -------------------------------------------- | ----------- |
| tikv-importer-{バージョン}-linux-amd64.tar.gz     |             |
| pd-recover-{バージョン}-linux-amd64.tar.gz        |             |
| etcdctl                                      | v6.0.0 の新機能 |
| tiup-linux-amd64.tar.gz                      |             |
| tiup-{バージョン}-linux-amd64.tar.gz              |             |
| tidb-lightning-{バージョン}-linux-amd64.tar.gz    |             |
| tidb-lightning-ctl                           |             |
| dumpling-{バージョン}-linux-amd64.tar.gz          |             |
| cdc-{バージョン}-linux-amd64.tar.gz               |             |
| dm-{バージョン}-linux-amd64.tar.gz                |             |
| dm-worker-{バージョン}-linux-amd64.tar.gz         |             |
| dm-master-{バージョン}-linux-amd64.tar.gz         |             |
| dmctl-{バージョン}-linux-amd64.tar.gz             |             |
| br-{バージョン}-linux-amd64.tar.gz                |             |
| spark-{バージョン}-any-any.tar.gz                 |             |
| tispark-{バージョン}-any-any.tar.gz               |             |
| パッケージ-{バージョン}-linux-amd64.tar.gz             |             |
| ベンチ-{バージョン}-linux-amd64.tar.gz               |             |
| errdoc-{バージョン}-linux-amd64.tar.gz            |             |
| dba-{バージョン}-linux-amd64.tar.gz               |             |
| PCC-{バージョン}-linux-amd64.tar.gz               |             |
| ポンプ-{バージョン}-linux-amd64.tar.gz               |             |
| ドレーン -{バージョン}-linux- drainer                 |             |
| binlogctl                                    | v6.0.0 の新機能 |
| sync_diff_inspector                          |             |
| レパロ                                          |             |
| アービタ                                         |             |
| マイダンパー                                       | v6.0.0 の新機能 |
| サーバー-{バージョン}-linux-amd64.tar.gz              | v6.2.0 の新機能 |
| grafana-{バージョン}-linux-amd64.tar.gz           | v6.2.0 の新機能 |
| alertmanager-{バージョン}-linux-amd64.tar.gz      | v6.2.0 の新機能 |
| プロメテウス-{バージョン}-linux-amd64.tar.gz            | v6.2.0 の新機能 |
| blackbox_exporter-{バージョン}-linux-amd64.tar.gz | v6.2.0 の新機能 |
| node_exporter-{バージョン}-linux-amd64.tar.gz     | v6.2.0 の新機能 |

## こちらもご覧ください {#see-also}

[TiUP をオフラインでデプロイ](/production-deployment-using-tiup.md#deploy-tiup-offline)
