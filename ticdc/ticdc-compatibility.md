---
title: TiCDC Compatibility
summary: Learn about compatibility issues of TiCDC and how to handle them.
---

# TiCDC の互換性 {#ticdc-compatibility}

このセクションでは、TiCDC に関連する互換性の問題とその処理方法について説明します。

<!--
## component compatibility matrix

TODO

## feature compatibility matrix

TODO
-->

## CLI と構成ファイルの互換性 {#cli-and-configuration-file-compatibility}

-   TiCDC v4.0.0 では、 `ignore-txn-commit-ts`が削除され、 `ignore-txn-start-ts`が追加され、start_ts を使用してトランザクションをフィルタリングします。
-   TiCDC v4.0.2 では、 `db-dbs` / `db-tables` / `ignore-dbs` / `ignore-tables`が削除され、データベースとテーブルに新しいフィルター ルールを使用する`rules`が追加されました。詳細なフィルター構文については、 [テーブル フィルター](/table-filter.md)を参照してください。
-   TiCDC v6.2.0 から、TiCDC Open API を介して TiCDCサーバーと直接対話できるようになり`cdc cli`た。 `--server`パラメータを使用して、TiCDCサーバーのアドレスを指定できます。 `--pd`は非推奨です。
-   v6.4.0 以降、TiCDC Syncpoint 機能を使用できるのは、 `SYSTEM_VARIABLES_ADMIN`または`SUPER`特権を持つ changefeed のみです。

## 互換性の問題を処理する {#handle-compatibility-issues}

このセクションでは、TiCDC に関連する互換性の問題とその処理方法について説明します。

### TiCDC v5.0.0-rc <code>cdc cli</code>ツールを使用して v4.0.x クラスターを操作することによって引き起こされる非互換性の問題 {#incompatibility-issue-caused-by-using-the-ticdc-v5-0-0-rc-code-cdc-cli-code-tool-to-operate-a-v4-0-x-cluster}

TiCDC v5.0.0-rc の`cdc cli`ツールを使用して v4.0.x の TiCDC クラスターを操作すると、次の異常な状況が発生する場合があります。

-   TiCDC クラスターが v4.0.8 以前のバージョンである場合、v5.0.0-rc `cdc cli`ツールを使用してレプリケーション タスクを作成すると、クラスターの異常が発生し、レプリケーション タスクがスタックする可能性があります。

-   TiCDC クラスターが v4.0.9 以降のバージョンの場合、v5.0.0-rc `cdc cli`ツールを使用してレプリケーション タスクを作成すると、古い値と統合ソーター機能が予期せずデフォルトで有効になります。

ソリューション:

TiCDC クラスターのバージョンに対応する`cdc`実行可能ファイルを使用して、次の操作を実行します。

1.  v5.0.0-rc `cdc cli`ツールを使用して作成された変更フィードを削除します。たとえば、 `tiup cdc:v4.0.9 cli changefeed remove -c xxxx --pd=xxxxx --force`コマンドを実行します。
2.  レプリケーション タスクがスタックしている場合は、TiCDC クラスターを再起動します。たとえば、 `tiup cluster restart <cluster_name> -R cdc`コマンドを実行します。
3.  変更フィードを再作成します。たとえば、 `tiup cdc:v4.0.9 cli changefeed create --sink-uri=xxxx --pd=xxx`コマンドを実行します。

> **ノート：**
>
> この問題は、 `cdc cli`が v5.0.0-rc の場合にのみ発生します。他の v5.0.x バージョンの`cdc cli`ツールは、v4.0.x クラスターと互換性があります。

### <code>sort-dir</code>と<code>data-dir</code>の互換性に関する注意事項 {#compatibility-notes-for-code-sort-dir-code-and-code-data-dir-code}

`sort-dir`構成は、TiCDC ソーターの一時ファイル ディレクトリを指定するために使用されます。その機能は、バージョンによって異なる場合があります。次の表は、バージョン間の`sort-dir`の互換性の変更を示しています。

| バージョン                                                       | `sort-engine`機能                                                     | ノート                                                                                                                                                                                                                                                                                                                                                                                          | おすすめ                                                             |
| :---------------------------------------------------------- | :------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------- |
| v4.0.11 またはそれ以前の v4.0 バージョン、v5.0.0-rc                       | これは changefeed 設定項目で、 `file`ソーターと`unified`ソーターの一時ファイル ディレクトリを指定します。 | これらのバージョンでは、 `file`ソーターと`unified`のソーターは**実験的機能**であり、本番環境には推奨され<strong>ません</strong>。<br/><br/>複数のチェンジフィードが`unified`ソーターを`sort-engine`として使用する場合、実際の一時ファイル ディレクトリはいずれかのチェンジフィードの`sort-dir`構成である可能性があり、各 TiCDC ノードに使用されるディレクトリは異なる可能性があります。                                                                                                                                                      | 本番環境で`unified`ソーターを使用することはお勧めしません。                               |
| v4.0.12、v4.0.13、v5.0.0、および v5.0.1                           | changefeed または`cdc server`の設定項目です。                                  | デフォルトでは、changefeed の`sort-dir`構成は有効にならず、 `cdc server`の`sort-dir`構成はデフォルトで`/tmp/cdc_sort`になります。本番環境では`cdc server`のみを構成することをお勧めします。<br/><br/> TiUPを使用して TiCDC をデプロイする場合は、最新のTiUPバージョンを使用し、TiCDCサーバー構成で`sorter.sort-dir`を設定することをお勧めします。<br/><br/> v4.0.13、v5.0.0、および v5.0.1 では、 `unified`ソーターがデフォルトで有効になっています。クラスターをこれらのバージョンにアップグレードする場合は、TiCDCサーバー構成で`sorter.sort-dir`が正しく構成されていることを確認してください。 | `cdc server`コマンドライン パラメータ (またはTiUP) を使用して`sort-dir`を構成する必要があります。 |
| v4.0.14 以降の v4.0 バージョン、v5.0.3 以降の v5.0 バージョン、以降の TiDB バージョン | `sort-dir`は非推奨です。 `data-dir`を設定することをお勧めします。                         | TiUPの最新バージョンを使用して`data-dir`を構成できます。これらの TiDB バージョンでは、デフォルトで`unified`ソーターが有効になっています。クラスターをアップグレードするときは、 `data-dir`正しく構成されていることを確認してください。それ以外の場合、一時ファイル ディレクトリとしてデフォルトで`/tmp/cdc_data`が使用されます。<br/><br/>ディレクトリが配置されているデバイスのstorage容量が不足している場合、ハードディスク容量が不足する問題が発生する可能性があります。この状況では、changefeed の以前の`sort-dir`構成は無効になります。                                                                        | `cdc server`コマンドライン パラメータ (またはTiUP) を使用して`data-dir`を構成する必要があります。 |
| v6.0.0 以降のバージョン                                             | `data-dir`は、TiCDC によって生成された一時ファイルを保存するために使用されます。                    | v6.0.0 以降、TiCDC はデフォルトでソートエンジンとして`db sorter`を使用します。 `data-dir`は、このエンジンのディスク ディレクトリです。                                                                                                                                                                                                                                                                                                        | `cdc server`コマンドライン パラメータ (またはTiUP) を使用して`data-dir`を構成する必要があります。 |

### 一時テーブルとの互換性 {#compatibility-with-temporary-tables}

v5.3.0 以降、TiCDC は[グローバル一時テーブル](/temporary-tables.md#global-temporary-tables)をサポートしています。 v5.3.0 より前のバージョンの TiCDC を使用してグローバル一時テーブルをダウンストリームに複製すると、テーブル定義エラーが発生します。

アップストリーム クラスターにグローバル一時テーブルが含まれている場合、ダウンストリーム TiDB クラスターは v5.3.0 以降のバージョンであると予想されます。そうしないと、レプリケーション プロセス中にエラーが発生します。
