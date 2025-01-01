---
title: TiDB Migration Tools Overview
summary: TiDB 移行ツールの概要を学びます。
---

# TiDB 移行ツールの概要 {#tidb-migration-tools-overview}

TiDB は、完全なデータ移行、増分データ移行、バックアップと復元、データ複製など、さまざまなシナリオに対応する複数のデータ移行ツールを提供します。

このドキュメントでは、これらのツールのユーザー シナリオ、サポートされているアップストリームとダウンストリーム、利点、制限について説明します。ニーズに応じて適切なツールを選択できます。

<!--The following diagram shows the user scenario of each migration tool.

!TiDB Migration Tools media/migration-tools.png-->

## <a href="/dm/dm-overview.md">TiDB データ移行 (DM)</a> {#a-href-dm-dm-overview-md-tidb-data-migration-dm-a}

-   **ユーザーシナリオ**: MySQL互換データベースからTiDBへのデータ移行
-   **アップストリーム**: MySQL、MariaDB、 Aurora
-   **下流**：TiDB
-   **利点**:
    -   完全なデータ移行と増分レプリケーションをサポートする、便利で統合されたデータ移行タスク管理ツール
    -   フィルタリングテーブルと操作をサポート
    -   シャードのマージと移行をサポート
-   **制限**: データのインポート速度は、TiDB Lightning [論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode.md)とほぼ同じですが、TiDB Lightning [物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)よりも大幅に遅くなります。そのため、1 TiB 未満のサイズの全データを移行するには、DM を使用することをお勧めします。

## <a href="/tidb-lightning/tidb-lightning-overview.md">TiDB Lightning</a> {#a-href-tidb-lightning-tidb-lightning-overview-md-tidb-lightning-a}

-   **ユーザーシナリオ**: TiDBへの完全なデータのインポート
-   **アップストリーム（インポートされたソースファイル）** :
    -   Dumplingからエクスポートされたファイル
    -   Amazon Aurora、Apache Hive、Snowflake によってエクスポートされた Parquet ファイル
    -   CSVファイル
    -   ローカルディスクまたは Amazon S3 からのデータ
-   **下流**：TiDB
-   **利点**:
    -   大量のデータを迅速にインポートし、TiDB クラスター内の特定のテーブルを迅速に初期化する機能をサポート
    -   インポートの進行状況を保存するチェックポイントをサポートし、再起動後に中断したところから`tidb-lightning`を続行します。
    -   データフィルタリングをサポート
-   **制限事項**:
    -   データのインポートに[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md)使用すると、インポート プロセス中に TiDB クラスターはサービスを提供できません。
    -   TiDB サービスに影響を与えたくない場合は、 TiDB Lightning [論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode-usage.md)に従ってデータのインポートを実行してください。

## <a href="/dumpling-overview.md">Dumpling</a> {#a-href-dumpling-overview-md-dumpling-a}

-   **ユーザーシナリオ**: MySQL または TiDB からの完全なデータエクスポート
-   **アップストリーム**: MySQL、TiDB
-   **下流（出力ファイル）** : SQL、CSV
-   **利点**:
    -   データのフィルタリングを容易にするテーブルフィルタ機能をサポート
    -   Amazon S3へのデータのエクスポートをサポート
-   **制限事項**:
    -   エクスポートしたデータを TiDB 以外のデータベースに復元する場合は、 Dumpling を使用することをお勧めします。
    -   エクスポートしたデータを別の TiDB クラスターに復元する場合は、バックアップと復元 (BR) を使用することをお勧めします。

## <a href="/ticdc/ticdc-overview.md">ティCDC</a> {#a-href-ticdc-ticdc-overview-md-ticdc-a}

-   **ユーザーシナリオ**: このツールは、TiKV 変更ログをプルすることによって実装されます。これにより、クラスター データを任意のアップストリーム TSO と一貫した状態に復元し、他のシステムがデータの変更をサブスクライブできるようにサポートできます。
-   **上流**: TiDB
-   **ダウンストリーム**: TiDB、MySQL、Kafka、MQ、Confluent、Amazon S3、GCS、Azure Blob Storage、NFS などのstorageサービス。
-   **利点**: TiCDCオープンプロトコルを提供する
-   **制限事項**: TiCDC は、少なくとも 1 つの有効なインデックスを持つテーブルのみをレプリケートします。次のシナリオはサポートされていません。
    -   RawKV のみを使用する TiKV クラスター。
    -   DDL 操作`CREATE SEQUENCE`と TiDB の`SEQUENCE`関数。

## <a href="/br/backup-and-restore-overview.md">バックアップと復元 (BR)</a> {#a-href-br-backup-and-restore-overview-md-backup-x26-restore-br-a}

-   **ユーザーシナリオ**: データのバックアップと復元によって大量の TiDB クラスターデータを移行する
-   **上流**: TiDB
-   **下流（出力ファイル）** : SST、backup.meta ファイル、backup.lock ファイル
-   **利点**:
    -   別のTiDBクラスタへのデータ移行に適しています
    -   災害復旧のための外部storageへのデータバックアップをサポート
-   **制限事項**:
    -   BR がTiCDC またはDrainerの上流クラスターにデータを復元する場合、復元されたデータは TiCDC またはDrainerによって下流に複製できません。
    -   BR は、 `mysql.tidb`テーブルで同じ`new_collation_enabled`値を持つクラスター間の操作のみをサポートします。

## <a href="/sync-diff-inspector/sync-diff-inspector-overview.md">同期差分インスペクター</a> {#a-href-sync-diff-inspector-sync-diff-inspector-overview-md-sync-diff-inspector-a}

-   **ユーザーシナリオ**: MySQLプロトコルを使用してデータベースに保存されたデータを比較する
-   **アップストリーム**: TiDB、MySQL
-   **ダウンストリーム**: TiDB、MySQL
-   **利点**: 少量のデータが不整合なシナリオでデータを修復するために使用できます。
-   **制限事項**:
    -   MySQL と TiDB 間のデータ移行ではオンライン チェックはサポートされていません。
    -   JSON、BIT、BINARY、BLOB などのタイプのデータはサポートされていません。

## TiUPを使用してツールをインストールする {#install-tools-using-tiup}

TiDB v4.0 以降、 TiUP は、 TiDB エコシステム内のさまざまなクラスター コンポーネントの管理に役立つパッケージ マネージャーとして機能します。これで、1 つのコマンドを使用して任意のクラスターコンポーネントを管理できます。

### ステップ1. TiUPをインストールする {#step-1-install-tiup}

```shell
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

グローバル環境変数を再宣言します。

```shell
source ~/.bash_profile
```

### ステップ2. コンポーネントをインストールする {#step-2-install-components}

利用可能なコンポーネントを確認するには、次のコマンドを使用できます。

```shell
tiup list
```

このコマンドは利用可能なコンポーネントを出力します。

```bash
Available components:
Name            Owner      Description
----            -----      -----------
PCC             community  A tool used to capture plan changes among different versions of TiDB
bench           pingcap    Benchmark database with different workloads
br              pingcap    TiDB/TiKV cluster backup restore tool.
cdc             pingcap    CDC is a change data capture tool for TiDB
chaosd          community  An easy-to-use Chaos Engineering tool used to inject failures to a physical node
client          pingcap    Client to connect playground
cloud           pingcap    CLI tool to manage TiDB Cloud
cluster         pingcap    Deploy a TiDB cluster for production
ctl             pingcap    TiDB controller suite
dm              pingcap    Data Migration Platform manager
dmctl           pingcap    dmctl component of Data Migration Platform.
errdoc          pingcap    Document about TiDB errors
pd-recover      pingcap    PD Recover is a disaster recovery tool of PD, used to recover the PD cluster which cannot start or provide services normally.
playground      pingcap    Bootstrap a local TiDB cluster for fun
tidb            pingcap    TiDB is an open source distributed HTAP database compatible with the MySQL protocol.
tidb-dashboard  pingcap    TiDB Dashboard is a Web UI for monitoring, diagnosing, and managing the TiDB cluster
tidb-lightning  pingcap    TiDB Lightning is a tool used for fast full import of large amounts of data into a TiDB cluster
tikv-br         pingcap    TiKV cluster backup restore tool
tikv-cdc        pingcap    TiKV-CDC is a change data capture tool for TiKV
tiproxy         pingcap    TiProxy is a database proxy that is based on TiDB.
tiup            pingcap    TiUP is a command-line component management tool that can help to download and install TiDB platform components to the local system
```

必要なコンポーネントを 1 つ以上インストールします。例:

```shell
tiup install dm
```

```shell
tiup install dm tidb-lightning
```

> **注記：**
>
> 特定のバージョンのコンポーネントをインストールするには、 `tiup install <component>[:version]`コマンドを使用します。

### ステップ3. TiUPとそのコンポーネントを更新する（オプション） {#step-3-update-tiup-and-its-components-optional}

新しいバージョンのリリース ログと互換性に関する注意事項を確認することをお勧めします。

```shell
tiup update --self && tiup update dm
```

## 参照 {#see-also}

-   [TiUPをオフラインでデプロイ](/production-deployment-using-tiup.md#deploy-tiup-offline)
-   [バイナリでツールをダウンロードしてインストールする](/download-ecosystem-tools.md)
