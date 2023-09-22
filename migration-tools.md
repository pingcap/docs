---
title: TiDB Migration Tools Overview
summary: Learn an overview of the TiDB migration tools.
---

# TiDB 移行ツールの概要 {#tidb-migration-tools-overview}

TiDB は、完全なデータ移行、増分データ移行、バックアップと復元、データ レプリケーションなど、さまざまなシナリオに対応する複数のデータ移行ツールを提供します。

このドキュメントでは、これらのツールのユーザー シナリオ、サポートされるアップストリームとダウンストリーム、利点、および制限事項を紹介します。ニーズに応じて適切なツールを選択できます。

<!--The following diagram shows the user scenario of each migration tool.

!TiDB Migration Tools media/migration-tools.png-->

## <a href="/dm/dm-overview.md">TiDB データ移行 (DM)</a> {#a-href-dm-dm-overview-md-tidb-data-migration-dm-a}

-   **ユーザーシナリオ**: MySQL 互換データベースから TiDB へのデータ移行
-   **アップストリーム**: MySQL、MariaDB、 Aurora
-   **ダウンストリーム**：TiDB
-   **利点**:
    -   完全なデータ移行と増分レプリケーションをサポートする便利な統合データ移行タスク管理ツール
    -   テーブルと操作のフィルタリングをサポート
    -   シャードのマージと移行をサポート
-   **制限事項**: データのインポート速度は、TiDB Lightning の[論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode.md)とほぼ同じですが、TiDB Lightning の[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)よりはかなり遅くなります。したがって、DM を使用して、サイズが 1 TiB 未満の完全なデータを移行することをお勧めします。

## <a href="/tidb-lightning/tidb-lightning-overview.md">TiDB Lightning</a> {#a-href-tidb-lightning-tidb-lightning-overview-md-tidb-lightning-a}

-   **ユーザーシナリオ**: TiDB への完全なデータのインポート
-   **上流 (インポートされたソース ファイル)** :
    -   Dumplingからエクスポートされたファイル
    -   Amazon Auroraまたは Apache Hive によってエクスポートされた Parquet ファイル
    -   CSVファイル
    -   ローカルディスクまたはAmazon S3からのデータ
-   **ダウンストリーム**：TiDB
-   **利点**:
    -   大量のデータの迅速なインポートと、TiDB クラスター内の特定のテーブルの迅速な初期化をサポートします。
    -   インポートの進行状況を保存するチェックポイントをサポートし、再起動後に中断したところからインポートを`tidb-lightning`できるようにします。
    -   データフィルタリングをサポート
-   **制限事項**:
    -   データのインポートに[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md)が使用される場合、インポート プロセス中、TiDB クラスターはサービスを提供できません。
    -   TiDB サービスに影響を与えたくない場合は、 TiDB Lightning [論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode-usage.md)に従ってデータ インポートを実行します。

## <a href="/dumpling-overview.md">Dumpling</a> {#a-href-dumpling-overview-md-dumpling-a}

-   **ユーザーシナリオ**: MySQL または TiDB からの完全なデータのエクスポート
-   **アップストリーム**: MySQL、TiDB
-   **ダウンストリーム (出力ファイル)** : SQL、CSV
-   **利点**:
    -   データを簡単にフィルタリングできるテーブル フィルタ機能をサポートします。
    -   Amazon S3 へのデータのエクスポートのサポート
-   **制限事項**:
    -   エクスポートされたデータを TiDB 以外のデータベースに復元する場合は、 Dumplingを使用することをお勧めします。
    -   エクスポートされたデータを別の TiDB クラスターに復元する場合は、バックアップと復元 (BR) を使用することをお勧めします。

## <a href="/ticdc/ticdc-overview.md">TiCDC</a> {#a-href-ticdc-ticdc-overview-md-ticdc-a}

-   **ユーザー シナリオ**: このツールは、TiKV 変更ログを取得することによって実装されます。クラスター データをアップストリーム TSO と一貫した状態に復元し、他のシステムがデータ変更をサブスクライブできるようにサポートします。
-   **上流**: TiDB
-   **ダウンストリーム**: TiDB、MySQL、Kafka、Confluent
-   **利点**: TiCDC オープン プロトコルを提供
-   **制限事項**: TiCDC は、少なくとも 1 つの有効なインデックスを持つテーブルのみを複製します。次のシナリオはサポートされていません。
    -   RawKV のみを使用する TiKV クラスター。
    -   DDL 操作`CREATE SEQUENCE`と`SEQUENCE` TiDB で機能します。

## <a href="/br/backup-and-restore-overview.md">バックアップと復元 (BR)</a> {#a-href-br-backup-and-restore-overview-md-backup-x26-restore-br-a}

-   **ユーザー シナリオ**: データのバックアップと復元による大量の TiDB クラスター データの移行
-   **上流**: TiDB
-   **ダウンストリーム (出力ファイル)** : SST、backup.meta ファイル、backup.lock ファイル
-   **利点**:
    -   別の TiDB クラスターへのデータの移行に適しています
    -   災害復旧のために外部storageへのデータのバックアップをサポート
-   **制限事項**:
    -   BR がTiCDC またはDrainerの上流クラスターにデータを復元する場合、復元されたデータは TiCDC またはDrainerによって下流に複製できません。
    -   BR は、同じ値`new_collations_enabled_on_first_bootstrap`を持つクラスター間の操作のみをサポートします。

## <a href="/sync-diff-inspector/sync-diff-inspector-overview.md">同期差分インスペクター</a> {#a-href-sync-diff-inspector-sync-diff-inspector-overview-md-sync-diff-inspector-a}

-   **ユーザーシナリオ**: MySQL プロトコルを使用してデータベースに保存されたデータを比較する
-   **アップストリーム**: TiDB、MySQL
-   **ダウンストリーム**: TiDB、MySQL
-   **利点**: 少量のデータに不整合があるシナリオでデータを修復するために使用できます。
-   **制限事項**:
    -   オンライン チェックは、MySQL と TiDB 間のデータ移行ではサポートされていません。
    -   JSON、BIT、BINARY、BLOB、およびその他のタイプのデータはサポートされていません。

## TiUPを使用してツールをインストールする {#install-tools-using-tiup}

TiDB v4.0 以降、 TiUP は、TiDB エコシステム内のさまざまなクラスター コンポーネントの管理を支援するパッケージ マネージャーとして機能します。単一のコマンドを使用して任意のクラスターコンポーネントを管理できるようになりました。

### ステップ 1. TiUPをインストールする {#step-1-install-tiup}

```shell
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

グローバル環境変数を再宣言します。

```shell
source ~/.bash_profile
```

### ステップ 2. コンポーネントをインストールする {#step-2-install-components}

次のコマンドを使用すると、使用可能なすべてのコンポーネントを表示できます。

```shell
tiup list
```

コマンド出力には、使用可能なすべてのコンポーネントがリストされます。

```bash
Available components:
Name            Owner    Description
----            -----    -----------
bench           pingcap  Benchmark database with different workloads
br              pingcap  TiDB/TiKV cluster backup restore tool
cdc             pingcap  CDC is a change data capture tool for TiDB
client          pingcap  Client to connect playground
cluster         pingcap  Deploy a TiDB cluster for production
ctl             pingcap  TiDB controller suite
dm              pingcap  Data Migration Platform manager
dmctl           pingcap  dmctl component of Data Migration Platform
errdoc          pingcap  Document about TiDB errors
pd-recover      pingcap  PD Recover is a disaster recovery tool of PD, used to recover the PD cluster which cannot start or provide services normally
playground      pingcap  Bootstrap a local TiDB cluster for fun
tidb            pingcap  TiDB is an open source distributed HTAP database compatible with the MySQL protocol
tidb-lightning  pingcap  TiDB Lightning is a tool used for fast full import of large amounts of data into a TiDB cluster
tiup            pingcap  TiUP is a command-line component management tool that can help to download and install TiDB platform components to the local system
```

インストールするコンポーネントを選択します:

```shell
tiup install dumpling tidb-lightning
```

> **注記：**
>
> 特定のバージョンのコンポーネントをインストールするには、 `tiup install <component>[:version]`コマンドを使用します。

### ステップ 3. TiUPとそのコンポーネントを更新する (オプション) {#step-3-update-tiup-and-its-components-optional}

新しいバージョンのリリース ログと互換性に関するメモを参照することをお勧めします。

```shell
tiup update --self && tiup update dm
```

## こちらも参照 {#see-also}

-   [TiUP をオフラインでデプロイ](/production-deployment-using-tiup.md#deploy-tiup-offline)
-   [ツールをバイナリでダウンロードしてインストールする](/download-ecosystem-tools.md)
