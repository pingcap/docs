---
title: TiCDC Compatibility
summary: TiCDCの互換性に関する問題とその対処方法について学びましょう。
---

# TiCDCとの互換性 {#ticdc-compatibility}

このセクションでは、TiCDCに関連する互換性の問題と、それらの対処方法について説明します。

## TiCDCの新アーキテクチャとTiDBクラスター間の互換性 {#compatibility-between-ticdc-new-architecture-and-tidb-clusters}

TiCDCの新しいアーキテクチャは、TiDBクラスターv7.5.0以降をサポートしています。 [互換性](/ticdc/ticdc-architecture.md#compatibility)に関する特別な注意事項については、を参照してください。 。

## TiDB Lightningとの互換性 {#compatibility-with-tidb-lightning}

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) [論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode.md)と[物理輸入モード](/tidb-lightning/tidb-lightning-physical-import-mode.md)モードという 2 つのデータ インポート モードを提供します。このセクションでは、これらのモードと TiCDC の互換性、およびクラスター内でTiDB Lightningと TiCDC を一緒に使用する手順について説明します。

論理インポートモードでは、 TiDB Lightning はSQL ステートメントを実行してデータをインポートします。このモードは TiCDC と互換性があります。TiDB Lightning の論理インポートモードを TiCDC でデータレプリケーションに使用するには、次の手順を実行します。

1.  チェンジフィードを作成します。詳細については、 [レプリケーションタスクを作成する](/ticdc/ticdc-manage-changefeed.md#create-a-replication-task)参照してください。
2.  TiDB Lightningを起動し、論理インポート モードを使用してデータをインポートします。詳細については、 [論理インポートモードを使用する](/tidb-lightning/tidb-lightning-logical-import-mode-usage.md)参照してください。

物理インポートモードでは、 TiDB Lightning はSST ファイルを TiKV に挿入することでデータをインポートします。TiCDC はこのモードと互換性がなく、物理インポートモードでインポートされたデータの複製をサポートしていません。TiDB Lightning の物理インポートモードと TiCDC の両方を使用する必要がある場合は、ダウンストリームシステムに基づいて、以下のいずれかのソリューションを選択してください。

-   ダウンストリームがTiDBクラスターである場合は、以下の手順を実行してください。

    1.  データの一貫性を確保するため、 TiDB Lightningを使用してデータをアップストリームとダウンストリームの両方のTiDBクラスターにインポートしてください。
    2.  変更フィードを作成して、SQL を通じて書き込まれた後続の増分データをレプリケートします。詳細については、 [レプリケーションタスクを作成する](/ticdc/ticdc-manage-changefeed.md#create-a-replication-task)参照してください。

-   ダウンストリームがTiDBクラスターでない場合は、以下の手順を実行してください。

    1.  TiDB Lightningの入力ファイルをインポートするには、ダウンストリームシステムが提供するオフラインインポートツールを使用してください。
    2.  変更フィードを作成して、SQL を通じて書き込まれた後続の増分データをレプリケートします。詳細については、 [レプリケーションタスクを作成する](/ticdc/ticdc-manage-changefeed.md#create-a-replication-task)参照してください。

## TiFlashとの互換性 {#compatibility-with-tiflash}

現在、TiCDC を使用してテーブルを下流の TiDB クラスターにレプリケートする場合、テーブルのTiFlashレプリカを作成することはサポートされていません。つまり、TiCDC は、次のようなTiFlash関連の DDL ステートメントのレプリケートをサポートしていません。

-   `ALTER TABLE table_name SET TIFLASH REPLICA count;`
-   `ALTER DATABASE db_name SET TIFLASH REPLICA count;`

## 以前のバージョンからのアップグレードに関する互換性に関する注意事項 {#compatibility-notes-for-upgrading-from-earlier-versions}

TiCDCは、上流の変更データおよび関連インターフェースを提供するために、TiDB、TiKV、およびPDに依存しています。TiDBおよび関連コンポーネントは進化を続けており、これらのデータ形式やインターフェースも変更される可能性があります。例えば、TiDBの並列DDLや高速テーブル作成などの機能は、関連するロジックやデータ処理ワークフローを変更する可能性があり、TiCDCはそれに応じた対応が必要となります。そのため、従来**のTiCDCアーキテクチャでは、バージョンをまたいだTiDB/TiKV/PD混在環境における公式な前方互換性または後方互換性は保証されません**。TiCDCの新しいアーキテクチャでは、v7.5.0以降のTiDBクラスターとの**後方互換性**が提供されます。

### TiCDCクラシックアーキテクチャのアップグレードに関する推奨事項 {#upgrade-recommendations-for-the-ticdc-classic-architecture}

TiCDC をクラシックアーキテクチャから新しいアーキテクチャにアップグレードする前に、すべての変更フィードを一時停止します。詳細については、 [TiCDC新アーキテクチャアップグレードガイド](/ticdc/ticdc-architecture.md#upgrade-guide)を参照してください。

アップグレードが、両方ともクラシックアーキテクチャを使用する TiCDC デプロイメント間で行われる場合、マイナーバージョン間のローリングアップグレードがサポートされます。ただし、メジャーバージョン間のアップグレード (たとえば、v8.5.0 -&gt; v8.5.3 はマイナーバージョンアップグレード、v8.1.x -&gt; v8.5.x はメジャーバージョンアップグレード) の場合、 **TiDB クラスターのローリングアップグレード中にチェンジフィードを実行し続けることは推奨されません**。メジャーバージョンアップグレードの場合は、次の手順を順番に実行してください。

1.  すべての変更フィードを一時停止します。
2.  TiDBクラスターに対してローリングアップグレードを実行します。
3.  アップグレード完了後、すべての変更フィードを再開してください。

例えば、クラスターをv8.5.4からv8.5.5にアップグレードする場合、 TiUPを使用してクラスターを管理している場合は、以下のコマンドを参照してください。以下の例では`linux-amd64`を使用しています。他のプラットフォームの場合は、環境に合わせてパッケージ名のプラットフォーム情報を置き換えてください。

```sh
# 1. Pause all changefeeds. Run this command once for each changefeed.
tiup cdc:v8.5.4 cli changefeed pause \
  --server=http://<ticdc-host>:8300 \
  --changefeed-id=<changefeed-id>

# 2. Perform a rolling upgrade on the TiDB cluster.
tiup cluster upgrade <cluster-name> v8.5.5

# 3. Resume all changefeeds after the upgrade is complete.
#    Run this command once for each changefeed.
tiup cdc:v8.5.5 cli changefeed resume \
  --server=http://<ticdc-host>:8300 \
  --changefeed-id=<changefeed-id>
```

### TiCDC新アーキテクチャ向けアップグレード推奨事項 {#upgrade-recommendations-for-the-ticdc-new-architecture}

TiCDCの新しいアーキテクチャは、 TiDBのローリングアップグレード中に変更フィードの実行を継続できますが、そのためには、アップグレード前にTiCDCが既に新しいアーキテクチャを使用している場合に限ります。

TiCDC クラシック アーキテクチャと新しいアーキテクチャの間でアップグレードまたは切り替える必要がある場合は、 [アップグレードガイド](/ticdc/ticdc-architecture.md#upgrade-guide)参照してください。

## CLIと設定ファイルの互換性 {#cli-and-configuration-file-compatibility}

-   TiCDC v4.0.0では、 `ignore-txn-commit-ts`が削除され、 `ignore-txn-start-ts`が追加されました。これは`start_ts`を使用してトランザクションをフィルタリングします。
-   TiCDC v4.0.2 では、 `db-dbs` / `db-tables` / `ignore-dbs` / `ignore-tables`が削除され、 `rules`が追加されました。これは、データベースとテーブルに新しいフィルタルールを使用します。フィルタ構文の詳細については、[テーブルフィルター](/table-filter.md)参照してください。
-   TiCDC v6.2.0 以降、 `cdc cli`は TiCDC Open API を介して TiCDCサーバーと直接やり取りし、PD へのアクセスは不要です。 `--pd`サブコマンドの`cdc cli`パラメータは非推奨となり、TiCDCサーバーアドレスを指定するために`--server`パラメータが追加されました。 `--server` `--pd` } を使用してください。
-   バージョン6.4.0以降、 `SYSTEM_VARIABLES_ADMIN`または`SUPER`の権限を持つチェンジフィードのみがTiCDC Syncpoint機能を使用できます。

## 互換性の問題に対処する {#handle-compatibility-issues}

このセクションでは、TiCDCに関連する互換性の問題と、それらの対処方法について説明します。

### TiCDC v5.0.0-rc <code>cdc cli</code>ツールを使用してv4.0.xクラスターを操作すると、互換性の問題が発生します。 {#incompatibility-issue-caused-by-using-the-ticdc-v5-0-0-rc-code-cdc-cli-code-tool-to-operate-a-v4-0-x-cluster}

TiCDC v5.0.0-rc の`cdc cli`ツールを使用して v4.0.x TiCDC クラスターを操作する場合、次のような異常な状況が発生する可能性があります。

-   TiCDC クラスターが v4.0.8 以前のバージョンである場合、v5.0.0-rc `cdc cli`ツールを使用してレプリケーション タスクを作成すると、クラスターの異常が発生し、レプリケーション タスクが停止する可能性があります。

-   TiCDC クラスターが v4.0.9 以降のバージョンである場合、v5.0.0-rc `cdc cli`ツールを使用してレプリケーション タスクを作成すると、古い値と統合ソーター機能がデフォルトで予期せず有効になります。

解決策：

TiCDCクラスターのバージョンに対応する`cdc`実行可能ファイルを使用して、以下の操作を実行します。

1.  v5.0.0-rc `cdc cli`ツールを使用して作成された変更フィードを削除します。たとえば、 `tiup cdc:v4.0.9 cli changefeed remove -c xxxx --pd=xxxxx --force`コマンドを実行します。
2.  レプリケーションタスクが停止している場合は、TiCDCクラスターを再起動してください。たとえば、 `tiup cluster restart <cluster_name> -R cdc`コマンドを実行します。
3.  変更フィードを再作成します。たとえば、 `tiup cdc:v4.0.9 cli changefeed create --sink-uri=xxxx --pd=xxx`コマンドを実行します。

> **注記：**
>
> この問題は、 `cdc cli`が v5.0.0-rc の場合にのみ発生します。他の v5.0.x バージョンの`cdc cli`ツールは、v4.0.x クラスターと互換性があります。

### <code>sort-dir</code>と<code>data-dir</code>の互換性に関する注意事項 {#compatibility-notes-for-code-sort-dir-code-and-code-data-dir-code}

`sort-dir`設定は、TiCDC ソーターの一時ファイルディレクトリを指定するために使用されます。その機能はバージョンによって異なる場合があります。次の表は`sort-dir`バージョン間の互換性の変更点を示しています。

| バージョン                                                 | `sort-engine`機能                                                  | 注記                                                                                                                                                                                                                                                                                                                                                                              | おすすめ                                                            |
| :---------------------------------------------------- | :--------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :-------------------------------------------------------------- |
| v4.0.11 またはそれ以前の v4.0 バージョン、v5.0.0-rc                 | これはチェンジフィード構成項目であり、 `file`ソーターと`unified`ソーターの一時ファイルディレクトリを指定します。 | これらのバージョンでは、 `file`ソーターと`unified`ソーターは**実験的機能**であり、本番環境での使用は推奨され**ません**。<br/><br/>複数のチェンジフィードが`unified`ソーターを`sort-engine`として使用する場合、実際の一時ファイルディレクトリは、いずれかのチェンジフィードの`sort-dir`構成になる可能性があり、各TiCDCノードで使用されるディレクトリは異なる可能性があります。                                                                                                                                                      | `unified`ソーターを本番環境で使用することは推奨されません。                              |
| v4.0.12、v4.0.13、v5.0.0、および v5.0.1                     | これは、changefeed または`cdc server`の構成項目です。                           | デフォルトでは、変更フィードの`sort-dir`設定は有効にならず、 `sort-dir`の`cdc server`設定は`/tmp/cdc_sort`にデフォルト設定されます。本番環境では`cdc server`のみを設定することをお勧めします。<br/><br/> TiUPを使用してTiCDCをデプロイする場合は、最新のTiUPバージョンを使用し、TiCDCサーバー構成で`sorter.sort-dir`を設定することをお勧めします。<br/><br/> `unified`ソーターは、v4.0.13、v5.0.0、v5.0.1 でデフォルトで有効になっています。クラスターをこれらのバージョンにアップグレードする場合は、TiCDCサーバー構成で`sorter.sort-dir`正しく構成されていることを確認してください。 | `sort-dir` `cdc server`コマンドラインパラメータ (またはTiUP) を使用して設定する必要があります。 |
| v4.0.14以降、v4.0バージョン、v5.0.3以降、v5.0バージョン、それ以降のTiDBバージョン | `sort-dir`は非推奨です。 `data-dir`を設定することをお勧めします。                      | 最新バージョンのTiUPを使用して`data-dir`を構成できます。これらの TiDB バージョンでは、 `unified`ソーターがデフォルトで有効になっています。クラスターをアップグレードする際は、 `data-dir`正しく構成されていることを確認してください。そうでない場合、 `/tmp/cdc_data`デフォルトで一時ファイル ディレクトリとして使用されます。<br/><br/>ディレクトリが配置されているデバイスのストレージ容量が不足している場合、ハードディスクの空き容量不足の問題が発生する可能性があります。この場合、changefeed の以前の`sort-dir`設定は無効になります。                                                            | `data-dir` `cdc server`コマンドラインパラメータ (またはTiUP) を使用して設定する必要があります。 |
| v6.0.0以降のバージョン                                        | `data-dir` TiCDC によって生成された一時ファイルを保存するために使用されます。                  | バージョン6.0.0以降、TiCDCはデフォルトで`db sorter`ソートエンジンとして使用します。 `data-dir`はこのエンジンのディスクディレクトリです。                                                                                                                                                                                                                                                                                            | `data-dir` `cdc server`コマンドラインパラメータ (またはTiUP) を使用して設定する必要があります。 |

### 一時テーブルとの互換性 {#compatibility-with-temporary-tables}

TiCDC は v5.3.0 以降、 [グローバル一時テーブル](/temporary-tables.md#global-temporary-tables)をサポートしています。 v5.3.0 より前のバージョンの TiCDC を使用してグローバル一時テーブルをダウンストリームにレプリケートすると、テーブル定義エラーが発生します。

アップストリームクラスターにグローバル一時テーブルが含まれている場合、ダウンストリームのTiDBクラスターはv5.3.0以降のバージョンである必要があります。そうでない場合、レプリケーション処理中にエラーが発生します。

### ベクトルデータ型との互換性 {#compatibility-with-vector-data-types}

v8.4.0 以降、TiCDC は、自動 [ベクトルデータ型](/ai/reference/vector-search-data-types.md)ストリームへのテーブルの複製をサポートします (実験的)。

ダウンストリームがKafkaまたはストレージサービス（Amazon S3、GCS、Azure Blob Storage、NFSなど）の場合、TiCDCはダウンストリームに書き込む前にベクトルデータ型を文字列型に変換します。

ダウンストリームがベクトルデータ型をサポートしないMySQL互換データベースである場合、TiCDCはベクトル型を含むDDLイベントをダウンストリームに書き込むことができません。この場合、 `has-vector-type=true`に`sink-url`パラメータを追加してください。これにより、TiCDCは書き込み前にベクトルデータ型を`LONGTEXT`型に変換できます。
