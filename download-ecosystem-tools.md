---
title: Download TiDB Tools
summary: Download the most officially maintained versions of TiDB tools.
---

# TiDBツールをダウンロードする {#download-tidb-tools}

このドキュメントは、TiDBツールのほとんどの公式に保守されているバージョンで利用可能なダウンロードを収集します。

## TiUP {#tiup}

ダーウィンとLinuxの両方のオペレーティングシステムに1つのコマンドでTiUPをインストールできます。詳細については、 [TiUPをインストールします](/tiup/tiup-overview.md#install-tiup)を参照してください。

## TiDB Operator {#tidb-operator}

TiDB OperatorはKubernetesで実行されます。 Kubernetesクラスタをデプロイした後、 TiDB Operatorをオンラインまたはオフラインでデプロイすることを選択できます。詳細については、 [KubernetesでのTiDB Operatorのデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-operator/)を参照してください。

## TiDB Binlog {#tidb-binlog}

TiDB BinlogはTiDBパッケージに含まれているため、最新バージョンの[TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)をダウンロードする場合は、TiDBパッケージを直接ダウンロードしてください。

| パッケージ名                                                                         | OS    | 建築    | SHA256チェックサム                                                     |
| :----------------------------------------------------------------------------- | :---- | :---- | :--------------------------------------------------------------- |
| `https://download.pingcap.org/tidb-{version}-linux-amd64.tar.gz` （TiDB Binlog） | Linux | amd64 | `https://download.pingcap.org/tidb-{version}-linux-amd64.sha256` |

> **ノート：**
>
> 上記のダウンロードリンクの`{version}`は、TiDBのバージョン番号を示します。たとえば、 `v5.4.1`のダウンロードリンクは`https://download.pingcap.org/tidb-v5.4.1-linux-amd64.tar.gz`です。

## TiDB Lightning {#tidb-lightning}

次の表のダウンロードリンクを使用して[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)をダウンロードします。

| パッケージ名                                                                   | OS    | 建築    | SHA256チェックサム                                                             |
| :----------------------------------------------------------------------- | :---- | :---- | :----------------------------------------------------------------------- |
| `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.tar.gz` | Linux | amd64 | `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.sha256` |

> **ノート：**
>
> 上記のダウンロードリンクの`{version}`は、TiDBLightningのバージョン番号を示します。たとえば、 `v5.4.1`のダウンロードリンクは`https://download.pingcap.org/tidb-toolkit-v5.4.1-linux-amd64.tar.gz`です。

## BR（バックアップと復元） {#br-backup-and-restore}

次の表のダウンロードリンクを使用して[BR](/br/backup-and-restore-tool.md)をダウンロードします。

| パッケージ名                                                                  | OS    | 建築    | SHA256チェックサム                                                            |
| :---------------------------------------------------------------------- | :---- | :---- | :---------------------------------------------------------------------- |
| `http://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.tar.gz` | Linux | amd64 | `http://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.sha256` |

> **ノート：**
>
> 上記のダウンロードリンクの`{version}`は、BRのバージョン番号を示します。たとえば、 `v5.4.1`のダウンロードリンクは`https://download.pingcap.org/tidb-toolkit-v5.4.1-linux-amd64.tar.gz`です。

## TiDB DM（データ移行） {#tidb-dm-data-migration}

次の表のダウンロードリンクを使用して[DM](/dm/dm-overview.md)をダウンロードします。

| パッケージ名                                                         | OS    | 建築    | SHA256チェックサム                                                   |
| :------------------------------------------------------------- | :---- | :---- | :------------------------------------------------------------- |
| `https://download.pingcap.org/dm-{version}-linux-amd64.tar.gz` | Linux | amd64 | `https://download.pingcap.org/dm-{version}-linux-amd64.sha256` |

> **ノート：**
>
> 上記のダウンロードリンクの`{version}`は、DMのバージョン番号を示します。たとえば、 `v5.4.1`のダウンロードリンクは`https://download.pingcap.org/dm-v5.4.1-linux-amd64.tar.gz`です。公開されているDMのバージョンは[DMリリース](https://github.com/pingcap/dm/releases)ページで確認できます。

## Dumpling {#dumpling}

以下のリンクから[Dumpling](/dumpling-overview.md)をダウンロードしてください。

| インストールパッケージ                                                              | オペレーティング·システム | 建築    | SHA256チェックサム                                                             |
| :----------------------------------------------------------------------- | :------------ | :---- | :----------------------------------------------------------------------- |
| `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.tar.gz` | Linux         | amd64 | `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.sha256` |

> **ノート：**
>
> ダウンロードリンクの`{version}`は、 Dumplingのバージョン番号です。たとえば、 `v5.4.1`バージョンのDumplingをダウンロードするためのリンクは`https://download.pingcap.org/tidb-toolkit-v5.4.1-linux-amd64.tar.gz`です。現在リリースされているバージョンは[TiDBリリース](https://github.com/pingcap/tidb/releases)で表示できます。
>
> Dumplingはarm64linuxをサポートします。ダウンロードリンクの`amd64`を`arm64`に置き換えることができます。これは、 Dumplingの`arm64`バージョンを意味します。

## sync-diff-inspector {#sync-diff-inspector}

以下のリンクから[sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md)をダウンロードしてください。

| パッケージ名                                                                                                                            | OS    | 建築    | SHA256チェックサム                                                                                                                      |
| :-------------------------------------------------------------------------------------------------------------------------------- | :---- | :---- | :-------------------------------------------------------------------------------------------------------------------------------- |
| [tidb-enterprise-tools-nightly-linux-amd64.tar.gz](https://download.pingcap.org/tidb-enterprise-tools-nightly-linux-amd64.tar.gz) | Linux | amd64 | [tidb-enterprise-tools-nightly-linux-amd64.sha256](https://download.pingcap.org/tidb-enterprise-tools-nightly-linux-amd64.sha256) |

## TiCDC {#ticdc}

[TiCDC](/ticdc/ticdc-overview.md)をダウンロードするには、 [TiCDCをデプロイ](/ticdc/deploy-ticdc.md)を参照してください。
