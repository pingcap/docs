---
title: TiDB Migration Tools Overview
summary: Learn an overview of the TiDB migration tools.
---

# TiDB 移行ツールの概要 {#tidb-migration-tools-overview}

TiDB は、完全なデータ移行、増分データ移行、バックアップと復元、データ複製など、さまざまなシナリオに対応する複数のデータ移行ツールを提供します。

このドキュメントでは、これらのツールのユーザー シナリオ、利点、および制限事項について説明します。必要に応じて適切なツールを選択できます。

<!--The following diagram shows the user scenario of each migration tool.

!TiDB Migration Tools media/migration-tools.png-->

次の表は、ユーザー シナリオ、サポートされている移行ツールのアップストリームとダウンストリームを示しています。

| ツール名                                                                | ユーザーシナリオ                                                                                              | アップストリーム (またはインポートされたソース ファイル)                                                              | 下流 (または出力ファイル)                        | 利点                                                                                                                                                                       | 制限                                                                                                                                                                                             |
| :------------------------------------------------------------------ | :---------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------ | :------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [TiDB データ移行 (DM)](/dm/dm-overview.md)                               | MySQL 互換データベースから TiDB へのデータ移行                                                                         | MySQL、MariaDB、 Aurora、MySQL                                                                 | TiDB                                  | <li>完全なデータ移行と増分レプリケーションをサポートする、便利で統合されたデータ移行タスク管理ツール</li><li>テーブルと操作のフィルタリングをサポート</li><li>シャードのマージと移行をサポート</li>                                                          | データのインポート速度は、TiDB Lighting の TiDB バックエンドとほぼ同じですが、TiDB Lighting の Local バックエンドよりもはるかに低速です。そのため、DM を使用して、サイズが 1 TiB 未満の完全なデータを移行することをお勧めします。                                                     |
| [Dumpling](/dumpling-overview.md)                                   | MySQL または TiDB からの完全なデータ エクスポート                                                                       | MySQL、TiDB                                                                                  | SQL、CSV                               | <li>データのフィルタリングを容易にするテーブル フィルター機能のサポート</li><li>Amazon S3 へのデータのエクスポートをサポート</li>                                                                                          | <li>エクスポートしたデータを TiDB 以外のデータベースに復元する場合は、 Dumplingを使用することをお勧めします。</li><li>エクスポートしたデータを別の TiDBクラスタに復元する場合は、バックアップと復元 (BR) を使用することをお勧めします。</li>                                                   |
| [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)        | TiDB への完全なデータのインポート                                                                                   | <li>Dumplingからエクスポートされたファイル</li><li>CSV ファイル</li><li>ローカル ディスクまたは Amazon S3 から読み取ったデータ</li> | TiDB                                  | <li>大量のデータを迅速にインポートし、TiDBクラスタの特定のテーブルを迅速に初期化するサポート</li><li>インポートの進行状況を保存するチェックポイントをサポートし、 `tidb-lightning`が再起動後に中断したところからインポートを続行できるようにします。</li><li>データフィルタリングをサポート</li> | <li>データのインポートに Local-backend が使用されている場合、インポート プロセス中に TiDBクラスタはサービスを提供できません。</li><li> TiDB サービスに影響を与えたくない場合は、 TiDB Lightning TiDB-backend に従ってデータ インポートを実行します。</li>                             |
| [バックアップと復元 (BR)](/br/backup-and-restore-overview.md)                | データのバックアップと復元により、大量の TiDB 顧客データを移行します。                                                                | TiDB                                                                                        | SST、backup.meta ファイル、backup.lock ファイル | <li>別の TiDBクラスタへのデータの移行に適しています</li><li>ディザスタ リカバリ用の外部ストレージへのデータのバックアップをサポート</li>                                                                                         | <li>BR が TiCDC またはDrainerのアップストリームクラスタにデータを復元する場合、復元されたデータは TiCDC またはDrainerによってダウンストリームにレプリケートできません。</li><li> BR は、同じ`new_collations_enabled_on_first_bootstrap`値を持つクラスター間の操作のみをサポートします。</li> |
| [TiCDC](/ticdc/ticdc-overview.md)                                   | このツールは、TiKV 変更ログをプルすることによって実装されます。アップストリームの TSO と整合性のある状態にデータを復元し、他のシステムがデータの変更をサブスクライブできるようにサポートします。 | TiDB                                                                                        | TiDB、MySQL、アパッチ パルサー、カフカ、コンフルエント      | TiCDC Open Protocol を提供                                                                                                                                                  | TiCDC は、少なくとも 1 つの有効なインデックスを持つテーブルのみをレプリケートします。次のシナリオはサポートされていません。<ul><li> RawKV のみを使用する TiKVクラスタ。</li><li> DDL 操作`CREATE SEQUENCE`と TiDB の`SEQUENCE`関数。</li></ul>                             |
| [Binlog](/tidb-binlog/tidb-binlog-overview.md)                      | 1 つの TiDBクラスタを別の TiDBクラスタのセカンダリクラスタとして使用するなど、TiDB クラスター間の増分レプリケーション                                   | TiDB                                                                                        | TiDB、MySQL、Kafka、増分バックアップ ファイル        | リアルタイムのバックアップと復元をサポートします。ディザスタ リカバリ用に復元する TiDBクラスタデータをバックアップする                                                                                                           | 一部の TiDB バージョンと互換性がない                                                                                                                                                                          |
| [同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md) | データベースに格納されたデータを MySQL プロトコルと比較する                                                                     | TiDB、MySQL                                                                                  | TiDB、MySQL                            | 少量のデータが矛盾しているシナリオでデータを修復するために使用できます                                                                                                                                      | <li>MySQL と TiDB 間のデータ移行では、オンライン チェックはサポートされていません。</li><li> JSON、BIT、BINARY、BLOB およびその他のタイプのデータはサポートされていません。</li>                                                                              |

## TiUP を使用してツールをインストールする {#install-tools-using-tiup}

TiDB v4.0 以降、TiUP は、TiDB エコシステム内のさまざまなクラスタコンポーネントを管理するのに役立つパッケージ マネージャーとして機能します。単一のコマンドを使用して、任意のクラスタコンポーネントを管理できるようになりました。

### ステップ 1. TiUP をインストールする {#step-1-install-tiup}

{{< copyable "" >}}

```shell
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

グローバル環境変数を再宣言します。

{{< copyable "" >}}

```shell
source ~/.bash_profile
```

### ステップ 2. コンポーネントをインストールする {#step-2-install-components}

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

### ステップ 3. TiUP とそのコンポーネントを更新する (オプション) {#step-3-update-tiup-and-its-components-optional}

新しいバージョンのリリース ログと互換性に関する注意事項を参照することをお勧めします。

{{< copyable "" >}}

```shell
tiup update --self && tiup update dm
```

## こちらもご覧ください {#see-also}

-   [TiUP をオフラインでデプロイ](/production-deployment-using-tiup.md#deploy-tiup-offline)
-   [ツールをバイナリでダウンロードしてインストールする](/download-ecosystem-tools.md)
