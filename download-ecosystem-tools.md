---
title: Download TiDB Tools
summary: Download the most officially maintained versions of TiDB tools.
---

# TiDB ツールをダウンロード {#download-tidb-tools}

この文書は、TiDB ツールの公式に維持されているほとんどのバージョンで利用可能なダウンロードをまとめたものです。

## TiUP {#tiup}

Darwin と Linux の両方のオペレーティング システムで、1 つのコマンドで TiUP をインストールできます。詳細については、 [TiUPをインストールする](/tiup/tiup-overview.md#install-tiup)を参照してください。

## TiDB Operator {#tidb-operator}

TiDB Operatorは Kubernetes で実行されます。 Kubernetes クラスターをデプロイした後、 TiDB Operatorをオンラインまたはオフラインでデプロイすることを選択できます。詳細については、 [TiDB Operatorを Kubernetes にデプロイする](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-operator/)を参照してください。

## Binlog {#tidb-binlog}

[Binlog](/tidb-binlog/tidb-binlog-overview.md)の最新バージョンをダウンロードする場合は、TiDB パッケージに TiDB Binlogが含まれているため、TiDB パッケージを直接ダウンロードしてください。

| パッケージ名                                                                           | OS    | アーキテクチャ | SHA256 チェックサム                                                    |
| :------------------------------------------------------------------------------- | :---- | :------ | :--------------------------------------------------------------- |
| `https://download.pingcap.org/tidb-{version}-linux-amd64.tar.gz` ( Binlogバイナリログ) | Linux | amd64   | `https://download.pingcap.org/tidb-{version}-linux-amd64.sha256` |

> **ノート：**
>
> 上記のダウンロード リンクの`{version}`は、TiDB のバージョン番号を示します。たとえば、 `v5.4.3`のダウンロード リンクは`https://download.pingcap.org/tidb-v5.4.3-linux-amd64.tar.gz`です。

## TiDB Lightning {#tidb-lightning}

次の表のダウンロード リンクを使用して[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)をダウンロードします。

| パッケージ名                                                                   | OS    | アーキテクチャ | SHA256 チェックサム                                                            |
| :----------------------------------------------------------------------- | :---- | :------ | :----------------------------------------------------------------------- |
| `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.tar.gz` | Linux | amd64   | `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.sha256` |

> **ノート：**
>
> 上記のダウンロード リンクの`{version}`は、 TiDB Lightningのバージョン番号を示します。たとえば、 `v5.4.3`のダウンロード リンクは`https://download.pingcap.org/tidb-toolkit-v5.4.3-linux-amd64.tar.gz`です。

## BR (バックアップと復元) {#br-backup-and-restore}

次の表のダウンロード リンクを使用して[ブラジル](/br/backup-and-restore-tool.md)をダウンロードします。

| パッケージ名                                                                  | OS    | アーキテクチャ | SHA256 チェックサム                                                           |
| :---------------------------------------------------------------------- | :---- | :------ | :---------------------------------------------------------------------- |
| `http://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.tar.gz` | Linux | amd64   | `http://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.sha256` |

> **ノート：**
>
> 上記のダウンロード リンクの`{version}`は、BR のバージョン番号を示します。たとえば、 `v5.4.3`のダウンロード リンクは`https://download.pingcap.org/tidb-toolkit-v5.4.3-linux-amd64.tar.gz`です。

## TiDB DM (データ移行) {#tidb-dm-data-migration}

次の表のダウンロード リンクを使用して[DM](/dm/dm-overview.md)をダウンロードします。

| パッケージ名                                                         | OS    | アーキテクチャ | SHA256 チェックサム                                                  |
| :------------------------------------------------------------- | :---- | :------ | :------------------------------------------------------------- |
| `https://download.pingcap.org/dm-{version}-linux-amd64.tar.gz` | Linux | amd64   | `https://download.pingcap.org/dm-{version}-linux-amd64.sha256` |

> **ノート：**
>
> 上記のダウンロード リンクの`{version}`は、DM のバージョン番号を示します。たとえば、 `v5.4.3`のダウンロード リンクは`https://download.pingcap.org/dm-v5.4.3-linux-amd64.tar.gz`です。公開されたDMのバージョンは[DMリリース](https://github.com/pingcap/dm/releases)ページで確認できます。

## Dumpling {#dumpling}

以下のリンクから[Dumpling](/dumpling-overview.md)をダウンロードします。

| インストールパッケージ                                                              | オペレーティング·システム | アーキテクチャ | SHA256 チェックサム                                                            |
| :----------------------------------------------------------------------- | :------------ | :------ | :----------------------------------------------------------------------- |
| `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.tar.gz` | Linux         | amd64   | `https://download.pingcap.org/tidb-toolkit-{version}-linux-amd64.sha256` |

> **ノート：**
>
> ダウンロード リンクの`{version}`はDumplingのバージョン番号です。たとえば、 `v5.4.3`バージョンのDumplingをダウンロードするためのリンクは`https://download.pingcap.org/tidb-toolkit-v5.4.3-linux-amd64.tar.gz`です。 [TiDB リリース](https://github.com/pingcap/tidb/releases)で現在リリースされているバージョンを表示できます。
>
> Dumplingは arm64 Linux をサポートしています。ダウンロード リンクの`amd64`を`arm64`に置き換えることができます。これは、 Dumplingの`arm64`バージョンを意味します。

## 同期差分インスペクター {#sync-diff-inspector}

以下のリンクから[同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md)をダウンロードします。

| パッケージ名                                                                                                                            | OS    | アーキテクチャ | SHA256 チェックサム                                                                                                                     |
| :-------------------------------------------------------------------------------------------------------------------------------- | :---- | :------ | :-------------------------------------------------------------------------------------------------------------------------------- |
| [tidb-enterprise-tools-nightly-linux-amd64.tar.gz](https://download.pingcap.org/tidb-enterprise-tools-nightly-linux-amd64.tar.gz) | Linux | amd64   | [tidb-enterprise-tools-nightly-linux-amd64.sha256](https://download.pingcap.org/tidb-enterprise-tools-nightly-linux-amd64.sha256) |

## TiCDC {#ticdc}

[TiCDC](/ticdc/ticdc-overview.md)をダウンロードするには、 [TiCDC をデプロイ](/ticdc/deploy-ticdc.md)を参照してください。
