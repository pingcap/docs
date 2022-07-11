---
title: TiDB Migration Tools Overview
summary: Learn an overview of the TiDB migration tools.
---

# TiDB移行ツールの概要 {#tidb-migration-tools-overview}

TiDBは、完全なデータ移行、増分データ移行、バックアップと復元、データ複製など、さまざまなシナリオに対応する複数のデータ移行ツールを提供します。

このドキュメントでは、これらのツールのユーザーシナリオ、利点、および制限を紹介します。必要に応じて適切なツールを選択できます。

<!--The following diagram shows the user scenario of each migration tool.

!TiDB Migration Tools media/migration-tools.png-->

次の表は、ユーザーシナリオ、サポートされている移行ツールのアップストリームとダウンストリームを示しています。

| ツール名                                                                        | ユーザーシナリオ                                                                                         | アップストリーム（またはインポートされたソースファイル）                                                            | ダウンストリーム（または出力ファイル）                      | 利点                                                                                                                                                                    | 制限                                                                                                                                                                                        |
| :-------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------- | :--------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [TiDBデータ移行（DM）](/dm/dm-overview.md)                                         | MySQL互換データベースからTiDBへのデータ移行                                                                       | MySQL、MariaDB、 Aurora、MySQL                                                             | TiDB                                     | <li>完全なデータ移行と増分レプリケーションをサポートする便利で統合されたデータ移行タスク管理ツール</li><li>フィルタリングテーブルと操作をサポートする</li><li>シャードのマージと移行をサポートする</li>                                                     | データのインポート速度は、TiDB LightingのTiDBバックエンドとほぼ同じであり、TiDBLightingのローカルバックエンドよりもはるかに低速です。したがって、DMを使用して、1TiB未満のサイズの完全なデータを移行することをお勧めします。                                                           |
| [Dumpling](/dumpling-overview.md)                                           | MySQLまたはTiDBからの完全なデータエクスポート                                                                      | MySQL、TiDB                                                                              | SQL、CSV                                  | <li>データをより簡単にフィルタリングできるテーブルフィルター機能をサポートする</li><li>AmazonS3へのデータのエクスポートをサポート</li>                                                                                      | <li>エクスポートしたデータをTiDB以外のデータベースに復元する場合は、 Dumplingを使用することをお勧めします。</li><li>エクスポートされたデータを別のTiDBクラスタに復元する場合は、バックアップと復元（BR）を使用することをお勧めします。</li>                                                  |
| [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)                | TiDBへの完全なデータインポート                                                                                | <li>Dumplingからエクスポートされたファイル</li><li>CSVファイル</li><li>ローカルディスクまたはAmazonS3から読み取られたデータ</li> | TiDB                                     | <li>大量のデータの迅速なインポートとTiDBクラスタの特定のテーブルの迅速な初期化をサポート</li><li>インポートの進行状況を保存するチェックポイントをサポートし、 `tidb-lightning`が再起動後に中断したところからインポートを続行できるようにします</li><li>データフィルタリングをサポート</li> | <li>ローカルバックエンドがデータのインポートに使用されている場合、インポートプロセス中、TiDBクラスタはサービスを提供できません。</li><li> TiDBサービスに影響を与えたくない場合は、 TiDB Lightningバックエンドに従ってデータのインポートを実行します。</li>                                        |
| [バックアップと復元（BR）](/br/backup-and-restore-overview.md)                         | データをバックアップおよび復元することにより、大量のTiDBcusterデータを移行します。                                                   | TiDB                                                                                    | SST、backup.metaファイル、backup.lockファイル      | <li>別のTiDBクラスタへのデータの移行に適しています</li><li>災害復旧のための外部ストレージへのデータのバックアップをサポート</li>                                                                                           | <li>BRがTiCDCまたはDrainerのアップストリームクラスタにデータを復元する場合、復元されたデータをTiCDCまたはDrainerによってダウンストリームに複製することはできません。</li><li> BRは、同じ`new_collations_enabled_on_first_bootstrap`値を持つクラスター間の操作のみをサポートします。</li> |
| [TiCDC](/ticdc/ticdc-overview.md)                                           | このツールは、TiKV変更ログをプルすることによって実装されます。データをアップストリームTSOとの整合性のある状態に復元し、他のシステムがデータ変更をサブスクライブするのをサポートできます。 | TiDB                                                                                    | TiDB、MySQL、Apache Pulsar、Kafka、Confluent | TiCDCオープンプロトコルを提供する                                                                                                                                                   | TiCDCは、少なくとも1つの有効なインデックスを持つテーブルのみを複製します。次のシナリオはサポートされていません。<ul><li> RawKVのみを使用するTiKVクラスタ。</li><li> TiDBのDDL操作`CREATE SEQUENCE`および`SEQUENCE`関数。</li></ul>                                  |
| [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md)                         | 1つのTiDBクラスタを別のTiDBクラスタのセカンダリクラスタとして使用するなど、TiDBクラスター間の増分レプリケーション                                  | TiDB                                                                                    | TiDB、MySQL、Kafka、増分バックアップファイル            | リアルタイムのバックアップと復元をサポートします。災害復旧のために復元するTiDBクラスタデータをバックアップします                                                                                                            | 一部のTiDBバージョンと互換性がありません                                                                                                                                                                    |
| [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) | データベースに保存されているデータをMySQLプロトコルと比較する                                                                | TiDB、MySQL                                                                              | TiDB、MySQL                               | 少量のデータに一貫性がないシナリオでデータを修復するために使用できます                                                                                                                                   | <li>MySQLとTiDB間のデータ移行では、オンラインチェックはサポートされていません。</li><li> JSON、BIT、BINARY、BLOB、およびその他のタイプのデータはサポートされていません。</li>                                                                             |

## TiUPを使用してツールをインストールする {#install-tools-using-tiup}

TiDB v4.0以降、TiUPは、TiDBエコシステム内のさまざまなクラスタコンポーネントの管理を支援するパッケージマネージャーとして機能します。これで、1つのコマンドを使用して任意のクラスタコンポーネントを管理できます。

### 手順1.TiUPをインストールします {#step-1-install-tiup}

{{< copyable "" >}}

```shell
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

グローバル環境変数を再宣言します。

{{< copyable "" >}}

```shell
source ~/.bash_profile
```

### ステップ2.コンポーネントをインストールします {#step-2-install-components}

次のコマンドを使用して、使用可能なすべてのコンポーネントを表示できます。

{{< copyable "" >}}

```shell
tiup list
```

コマンド出力には、使用可能なすべてのコンポーネントが一覧表示されます。

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

インストールするコンポーネントを選択します。

{{< copyable "" >}}

```shell
tiup install dumpling tidb-lightning
```

> **ノート：**
>
> 特定のバージョンのコンポーネントをインストールするには、 `tiup install <component>[:version]`コマンドを使用します。

### 手順3.TiUPとそのコンポーネントを更新する（オプション） {#step-3-update-tiup-and-its-components-optional}

新しいバージョンのリリースログと互換性に関する注意事項を確認することをお勧めします。

{{< copyable "" >}}

```shell
tiup update --self && tiup update dm
```

## も参照してください {#see-also}

-   [TiUPをオフラインでデプロイ](/production-deployment-using-tiup.md#deploy-tiup-offline)
-   [ツールをバイナリでダウンロードしてインストールする](/download-ecosystem-tools.md)
