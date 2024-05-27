---
title: TiCDC Compatibility
summary: TiCDC の互換性の問題とその対処方法について学習します。
---

# TiCDC 互換性 {#ticdc-compatibility}

このセクションでは、TiCDC に関連する互換性の問題とその処理方法について説明します。

<!--
## component compatibility matrix

TODO

## feature compatibility matrix

TODO
-->

## CLIと設定ファイルの互換性 {#cli-and-configuration-file-compatibility}

-   TiCDC v4.0.0 では、 `ignore-txn-commit-ts`が削除され、start_ts を使用してトランザクションをフィルター処理する`ignore-txn-start-ts`が追加されました。
-   TiCDC v4.0.2 では、 `db-dbs` / `db-tables` / `ignore-dbs` / `ignore-tables`が削除され、データベースとテーブルに新しいフィルター ルールを使用する`rules`が追加されました。詳細なフィルター構文については、 [テーブルフィルター](/table-filter.md)を参照してください。
-   TiCDC v6.2.0 以降では、 `cdc cli` `--server` Open API を介して TiCDCサーバーと直接対話できます。3 パラメータを使用して TiCDCサーバーのアドレスを指定できます。5 `--pd`非推奨です。
-   v6.4.0 以降では、権限`SYSTEM_VARIABLES_ADMIN`または`SUPER`を持つ changefeed のみが TiCDC Syncpoint 機能を使用できます。

## 互換性の問題に対処する {#handle-compatibility-issues}

このセクションでは、TiCDC に関連する互換性の問題とその処理方法について説明します。

### TiCDC v5.0.0-rc <code>cdc cli</code>ツールを使用して v4.0.x クラスターを操作することによって発生する非互換性の問題 {#incompatibility-issue-caused-by-using-the-ticdc-v5-0-0-rc-code-cdc-cli-code-tool-to-operate-a-v4-0-x-cluster}

TiCDC v5.0.0-rc の`cdc cli`ツールを使用して v4.0.x TiCDC クラスターを操作すると、次の異常な状況が発生する可能性があります。

-   TiCDC クラスターが v4.0.8 以前のバージョンの場合、v5.0.0-rc `cdc cli`ツールを使用してレプリケーション タスクを作成すると、クラスターの異常が発生し、レプリケーション タスクが停止する可能性があります。

-   TiCDC クラスターが v4.0.9 以降のバージョンの場合、v5.0.0-rc `cdc cli`ツールを使用してレプリケーション タスクを作成すると、古い値と統合ソート機能が予期せずデフォルトで有効になります。

解決策:

TiCDC クラスター バージョンに対応する`cdc`実行可能ファイルを使用して、次の操作を実行します。

1.  v5.0.0-rc `cdc cli`ツールを使用して作成された changefeed を削除します。たとえば、 `tiup cdc:v4.0.9 cli changefeed remove -c xxxx --pd=xxxxx --force`コマンドを実行します。
2.  レプリケーション タスクが停止している場合は、TiCDC クラスターを再起動します。たとえば、 `tiup cluster restart <cluster_name> -R cdc`コマンドを実行します。
3.  変更フィードを再作成します。たとえば、 `tiup cdc:v4.0.9 cli changefeed create --sink-uri=xxxx --pd=xxx`コマンドを実行します。

> **注記：**
>
> この問題は、 `cdc cli` v5.0.0-rc の場合にのみ発生します。3 他の v5.0.x バージョンの`cdc cli`は、v4.0.x クラスターと互換性があります。

### <code>sort-dir</code>と<code>data-dir</code>の互換性に関する注意事項 {#compatibility-notes-for-code-sort-dir-code-and-code-data-dir-code}

`sort-dir`構成は、TiCDC ソーターの一時ファイル ディレクトリを指定するために使用されます。その機能はバージョンによって異なる場合があります。次の表は、バージョン間での`sort-dir`の互換性の変更を示しています。

| バージョン                                                         | `sort-engine`機能                                                       | 注記                                                                                                                                                                                                                                                                                                                                                                                     | おすすめ                                                           |
| :------------------------------------------------------------ | :-------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------- |
| v4.0.11 またはそれ以前の v4.0 バージョン、v5.0.0-rc                         | これは、changefeed 構成項目であり、 `file`ソーターと`unified`ソーターの一時ファイル ディレクトリを指定します。 | これらのバージョンでは、 `file`ソーターと`unified`ソーターは**実験的機能**であり、本番環境には推奨され**ません**。<br/><br/>複数の changefeed が`unified`ソーターを`sort-engine`として使用する場合、実際の一時ファイル ディレクトリはいずれかの changefeed の`sort-dir`構成になる可能性があり、各 TiCDC ノードに使用されるディレクトリは異なる場合があります。                                                                                                                                                       | 本番環境で`unified`ソーターを使用することは推奨されません。                             |
| v4.0.12、v4.0.13、v5.0.0、および v5.0.1                             | これは changefeed または`cdc server`の構成項目です。                                | デフォルトでは、 changefeed の`sort-dir`構成は有効にならず、 `cdc server`の`sort-dir`構成はデフォルトで`/tmp/cdc_sort`になります。本番環境では`cdc server`のみを構成することをお勧めします。<br/><br/> TiUPを使用して TiCDC を展開する場合は、最新のTiUPバージョンを使用し、TiCDCサーバー構成で`sorter.sort-dir`を設定することをお勧めします。<br/><br/> `unified`ソーターは、v4.0.13、v5.0.0、v5.0.1 ではデフォルトで有効になっています。クラスターをこれらのバージョンにアップグレードする場合は、TiCDCサーバー構成で`sorter.sort-dir`が正しく構成されていることを確認してください。 | `cdc server`コマンドラインパラメータ (またはTiUP) を使用して`sort-dir`構成する必要があります。 |
| v4.0.14 以降の v4.0 バージョン、v5.0.3 以降の v5.0 バージョン、それ以降の TiDB バージョン | `sort-dir`は非推奨です。 `data-dir`を設定することをお勧めします。                           | 最新バージョンのTiUPを使用して`data-dir`設定できます。これらの TiDB バージョンでは、 `unified`ソーターがデフォルトで有効になっています。クラスターをアップグレードするときに、 `data-dir`が正しく設定されていることを確認してください。そうでない場合、一時ファイル ディレクトリとしてデフォルトで`/tmp/cdc_data`使用されます。<br/><br/>ディレクトリが配置されているデバイスのstorage容量が不足している場合、ハードディスク容量不足の問題が発生する可能性があります。この場合、changefeed の以前の`sort-dir`構成は無効になります。                                                                      | `cdc server`コマンドラインパラメータ (またはTiUP) を使用して`data-dir`構成する必要があります。 |
| v6.0.0以降のバージョン                                                | `data-dir` 、TiCDC によって生成された一時ファイルを保存するために使用されます。                      | v6.0.0 以降、TiCDC はデフォルトでソート エンジンとして`db sorter`使用します。3 `data-dir`このエンジンのディスク ディレクトリです。                                                                                                                                                                                                                                                                                                   | `cdc server`コマンドラインパラメータ (またはTiUP) を使用して`data-dir`構成する必要があります。 |

### 一時テーブルとの互換性 {#compatibility-with-temporary-tables}

v5.3.0 以降、TiCDC は[グローバル一時テーブル](/temporary-tables.md#global-temporary-tables)サポートします。v5.3.0 より前のバージョンの TiCDC を使用してグローバル一時テーブルをダウンストリームに複製すると、テーブル定義エラーが発生します。

アップストリーム クラスターにグローバル一時テーブルが含まれている場合、ダウンストリーム TiDB クラスターは v5.3.0 以降のバージョンである必要があります。それ以外の場合、レプリケーション プロセス中にエラーが発生します。
