---
title: TiDB Smooth Upgrade
summary: このドキュメントでは、DDL 操作を手動でキャンセルせずに TiDB クラスターのアップグレードをサポートする、TiDB のスムーズ アップグレード機能について説明します。
---

# TiDB スムーズアップグレード {#tidb-smooth-upgrade}

このドキュメントでは、DDL 操作を手動でキャンセルせずに TiDB クラスターのアップグレードをサポートする、TiDB のスムーズ アップグレード機能について説明します。

Starting from v7.1.0, when you upgrade TiDB to a later version, TiDB supports smooth upgrade. This feature removes the limitations during the upgrade process and provides a more user-friendly upgrade experience. Note that you need to ensure that there are no user-initiated DDL operations during the upgrade process.

## サポートされているバージョン {#supported-versions}

機能がスイッチによって制御される必要があるかどうかに応じて、スムーズ アップグレードを使用する方法は 2 つあります。

-   この機能はデフォルトで有効になっており、スイッチによる制御は不要です。現在、この方法をサポートしているバージョンはv7.1.0、v7.1.1、v7.2.0、v7.3.0です。具体的には、以下のバージョンがサポートされています。
    -   Upgrade from v7.1.0 to v7.1.1, v7.2.0, or v7.3.0
    -   Upgrade from v7.1.1 to v7.2.0 or v7.3.0
    -   Upgrade from v7.2.0 to v7.3.0

-   この機能はデフォルトで無効になっていますが、 `/upgrade/start`リクエストを送信することで有効にできます。詳細は[TiDB HTTP API](https://github.com/pingcap/tidb/blob/release-8.5/docs/tidb_http_api.md)参照してください。サポートされているバージョンは次のとおりです。
    -   Upgrade from v7.1.2 and later v7.1 versions (that is, v7.1.x, where x >= 2) to v7.4.0 and later versions
    -   Upgrade from v7.4.0 to later versions

特定のバージョンでサポートされているアップグレード方法については、次の表を参照してください。

| オリジナル版                           | Upgraded version         | アップグレード方法                                                                                                                                            | 注記                                                                                                  |
| -------------------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| &lt; バージョン7.1.0                  | 任意のバージョン                 | スムーズなアップグレードはサポートされません。                                                                                                                              |                                                                                                     |
| v7.1.0                           | v7.1.1、v7.2.0、または v7.3.0 | スムーズなアップグレードが自動的にサポートされます。追加の操作は必要ありません。                                                                                                             | Experimentalな機能です。問題[＃44760](https://github.com/pingcap/tidb/pull/44760)発生する可能性があります。               |
| バージョン7.1.1                       | v7.2.0 または v7.3.0        | スムーズなアップグレードが自動的にサポートされます。追加の操作は必要ありません。                                                                                                             | Experimental機能です。                                                                                   |
| バージョン7.2.0                       | バージョン7.3.0               | スムーズなアップグレードが自動的にサポートされます。追加の操作は必要ありません。                                                                                                             | Experimental機能です。                                                                                   |
| [v7.1.2、v7.2.0)                  | [v7.1.2、v7.2.0)          | `/upgrade/start` HTTPリクエストを送信することでスムーズなアップグレードが可能になります。方法は[TiUPを使用する](#use-tiup-to-upgrade)と[その他のアップグレード方法](#other-upgrade-methods) 2つあります。          | When smooth upgrade is not enabled, ensure that no DDL operations are performed during the upgrade. |
| [v7.1.2、v7.2.0) または &gt;= v7.4.0 | = v7.4.0                 | `/upgrade/start` HTTPリクエストを送信することでスムーズなアップグレードが可能になります。方法は[TiUPを使用する](#use-tiup-to-upgrade)と[Other upgrade methods](#other-upgrade-methods) 2つがあります。 | スムーズ アップグレードが有効になっていない場合は、アップグレード中に DDL 操作が実行されないようにしてください。                                         |
| v7.1.0、v7.1.1、v7.2.0、および v7.3.0  | = v7.4.0                 | スムーズなアップグレードはサポートされません。                                                                                                                              |                                                                                                     |

## Feature introduction {#feature-introduction}

Before the smooth upgrade feature is introduced, there are the following limitations on DDL operations during the upgrade process:

-   アップグレード プロセス中に DDL 操作を実行すると、TiDB で未定義の動作が発生する可能性があります。
-   DDL 操作中に TiDB をアップグレードすると、TiDB で未定義の動作が発生する可能性があります。

These limitations can be summarized as that you need to ensure that there are no user-initiated DDL operations during the upgrade process. After the smooth upgrade feature is introduced, TiDB is no longer subject to this limitation during the upgrade process.

詳細については、 [TiUPを使用して TiDB をアップグレードする](/upgrade-tidb-using-tiup.md#upgrade-tidb-using-tiup)の**警告の**内容を参照してください。

### アップグレード手順 {#upgrade-steps}

#### TiUPを使用してアップグレードする {#use-tiup-to-upgrade}

v1.14.0以降、 TiUPはこの機能を自動的にサポートします。つまり、 `tiup cluster upgrade`コマンドを使用してTiDBクラスタを直接アップグレードできます。3 `tiup cluster patch`は現在サポートされていないことに注意してください。

#### TiDB Operatorを使用してアップグレードする {#use-tidb-operator-to-upgrade}

現在、この機能はサポートされていません。できるだけ早くサポートされる予定です。

#### その他のアップグレード方法 {#other-upgrade-methods}

You can take the following steps to upgrade TiDB manually or by using a script:

1.  クラスター内の任意の TiDB ノードに HTTP アップグレード開始要求を送信します`curl -X POST http://{TiDBIP}:10080/upgrade/start` .
    -   The TiDB cluster enters the **Upgrading** state.
    -   The DDL operations to be performed are paused.

2.  Replace the TiDB binary and perform a rolling upgrade. This process is the same as the original upgrade process.
    -   システム DDL 操作はアップグレード プロセス中に実行されます。

3.  クラスター内のすべての TiDB ノードが正常にアップグレードされたら、任意の TiDB ノードに HTTP アップグレード完了要求を送信します`curl -X POST http://{TiDBIP}:10080/upgrade/finish` .
    -   ユーザーの一時停止された DDL 操作が再開されます。

## Limitations {#limitations}

スムーズ アップグレード機能を使用する場合は、次の制限に注意してください。

> **注記：**
>
> The limitations in this section apply not only to scenarios using the smooth upgrade feature, but also to [upgrading TiDB using TiUP](/upgrade-tidb-using-tiup.md#upgrade-tidb-using-tiup).

### ユーザー操作の制限 {#limitations-on-user-operations}

-   アップグレードする前に、次の制限を考慮してください。

    -   クラスタ内にキャンセル中のDDLジョブがある場合、つまり実行中のDDLジョブがユーザーによってキャンセルされている場合、キャンセル中のジョブは一時停止できないため、TiDBはジョブのキャンセルを再試行します。再試行が失敗した場合はエラーが報告され、アップグレードは終了します。
    -   現在ご使用の TiDB バージョンが v8.1.0 より前で、TiDB Distributed eXecution Framework (DXF) が有効になっている場合は、 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710)を`OFF`に設定して無効にしてください。実行中の分散タスク`ADD INDEX`と`IMPORT INTO`すべて完了していることを確認してください。または、これらのタスクをキャンセルし、アップグレードが完了するまで待ってから再開することもできます。そうしないと、アップグレード中の`ADD INDEX`操作によってデータインデックスの不整合が発生する可能性があります。現在ご使用の TiDB バージョンが v8.1.0 以降の場合は、DXF を無効にする必要はなく、この制限は無視してかまいません。

-   TiUPを使用して TiDB をアップグレードするシナリオでは、 TiUPアップグレードにはタイムアウト期間があるため、アップグレード前にクラスターのキューで待機している DDL ジョブが多数 (300 を超える) ある場合、アップグレードが失敗する可能性があります。

-   アップグレード中は、次の操作は許可されません。

    -   システム テーブル ( `mysql.*` 、 `information_schema.*` 、 `performance_schema.*` 、および`metrics_schema.*` ) に対して DDL 操作を実行します。
    -   DDL ジョブを手動でキャンセルします: `ADMIN CANCEL DDL JOBS job_id [, job_id] ...;` .
    -   データをインポートします。

### ツールの制限 {#limitations-on-tools}

-   アップグレード中は、次のツールの使用はサポートされません。

    -   BR: BRは一時停止中のDDLジョブをTiDBに複製する可能性があります。一時停止中のDDLジョブは自動的に再開できないため、後でDDLジョブが停止する可能性があります。

    -   DM および TiCDC: アップグレード プロセス中に DM または TiCDC を使用して SQL ステートメントを TiDB にインポートする場合、SQL ステートメントの 1 つに DDL 操作が含まれていると、インポート操作がブロックされ、未定義のエラーが発生する可能性があります。

### プラグインの制限 {#limitation-on-plugins}

TiDBにインストールされているプラグインにはDDL操作が含まれている可能性があります。ただし、アップグレード中にプラグイン内のDDL操作がシステムテーブル以外のテーブルに対して実行されると、アップグレードが失敗する可能性があります。
