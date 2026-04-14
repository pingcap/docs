---
title: Integrate TiDB Cloud with Datadog
summary: Datadogとの連携により、TiDBクラスタを監視する方法を学びましょう。
---

# TiDB CloudとDatadogを統合する {#integrate-tidb-cloud-with-datadog}

TiDB CloudはDatadogとの連携をサポートしています。TiDB Cloudを設定することで、TiDBクラスタに関するメトリクスを[データドッグ](https://www.datadoghq.com/)に送信できます。その後、これらのメトリクスをDatadogダッシュボードで直接確認できます。

## Datadog統合バージョン {#datadog-integration-version}

TiDB Cloudは、2022年3月4日よりプロジェクトレベルのDatadog統合（ベータ版）をサポートしてきました。2025年7月31日より、TiDB CloudレベルのDatadog統合（プレビュー版）を導入します。2025年9月30日より、クラスターレベルのDatadog統合が一般提供（GA）となります。

-   **クラスタレベルのDatadog統合**：2025年7月31日までに組織内に削除されていない従来のプロジェクトレベルのDatadogまたはNew Relic統合が残っていない場合、 TiDB Cloudは組織が最新の機能強化を体験できるように、クラスタレベルのDatadog統合を提供します。
-   **従来のプロジェクトレベルの Datadog 統合 (ベータ版)** : 2025 年 7 月 31 日時点で組織内に少なくとも 1 つの従来のプロジェクトレベルの Datadog または New Relic 統合が削除されずに残っている場合、 TiDB Cloudは、現在のダッシュボードへの影響を回避するために、組織向けにプロジェクトレベルで既存および新規の統合の両方を保持します。従来のプロジェクトレベルの Datadog 統合は、2025 年 10 月 31 日に廃止されることに注意してください。組織がこれらの従来の統合をまだ使用している場合は、[DatadogとNew Relicの統合を移行する](/tidb-cloud/migrate-metrics-integrations.md)手順に従って、新しいクラスタレベルの統合に移行し、メトリクス関連サービスへの影響を最小限に抑えてください。

## 前提条件 {#prerequisites}

-   TiDB CloudをDatadogと連携させるには、Datadogアカウントと[Datadog APIキー](https://app.datadoghq.com/organization-settings/api-keys)必要です。Datadogアカウントを初めて作成すると、DatadogからAPIキーが発行されます。

    Datadogアカウントをお持ちでない場合は、 [https://app.datadoghq.com/signup](https://app.datadoghq.com/signup)でサインアップしてください。

-   TiDB Cloudのサードパーティ メトリクス統合を設定するには、 TiDB Cloudで`Organization Owner`または`Project Owner`アクセス権が必要です。統合ページを表示したり、提供されたリンクから設定済みのダッシュボードにアクセスしたりするには、TiDB Cloudのプロジェクト内の対象のTiDB Cloud Dedicatedクラスターにアクセスするための`Project Viewer`ロール以上が必要です。

## 制限 {#limitation}

-   Datadogとの連携機能は、現在[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターでのみ利用可能です。

-   クラスターの状態が**「作成中」** 、 **「復元中」** 、 **「一時停止中」** 、 **「再開中」**の場合は、Datadog の統合は利用できません。

-   Datadogとの統合が設定されているクラスターが削除されると、それに関連付けられている統合サービスも削除されます。

## 手順 {#steps}

### ステップ1. Datadog APIキーと連携する {#step-1-integrate-with-your-datadog-api-key}

[Datadog統合バージョン](#datadog-integration-version)に応じて、統合ページにアクセスする手順は異なります。

<SimpleTab>
<div label="Cluster-level Datadog integration">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Dedicatedクラスターの名前をクリックして、その概要ページに移動します。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[統合]**をクリックします。

3.  **統合**ページで、 **「Datadogへの統合」**をクリックします。

4.  Datadog APIキーを入力し、Datadogサイトを選択してください。

5.  **「統合テスト」**をクリックします。

    -   テストが成功すると、 **「確認」**ボタンが表示されます。
    -   テストが失敗した場合は、エラーメッセージが表示されます。メッセージに従ってトラブルシューティングを行い、統合を再試行してください。

6.  統合を完了するには、 **「確認」**をクリックしてください。

</div>
<div label="Datadog integration (Beta)">

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、 **[プロジェクト ビュー]**タブをクリックします。

2.  プロジェクトビューで、対象のプロジェクトを見つけて、そのプロジェクトの<MDSvgIcon name="icon-project-settings" />をクリックします。

3.  左側のナビゲーションペインで、 **「プロジェクト設定」**の下にある**「統合」**をクリックします。

4.  **統合**ページで、 **[Datadogとの統合（ベータ版）]**をクリックします。

5.  Datadog APIキーを入力し、Datadogサイトを選択してください。

6.  **「統合テスト」**をクリックします。

    -   テストが成功すると、 **「確認」**ボタンが表示されます。
    -   テストが失敗した場合は、エラーメッセージが表示されます。メッセージに従ってトラブルシューティングを行い、統合を再試行してください。

7.  統合を完了するには、 **「確認」**をクリックしてください。

</div>
</SimpleTab>

### ステップ2. DatadogにTiDB Cloud統合をインストールする {#step-2-install-tidb-cloud-integration-in-datadog}

> **注記：**
>
> Datadog にTiDB Cloud統合をすでにインストールしている場合は、このセクションの次の手順をスキップできます。 [**TiDB Cloudダイナミックトラッカー**](https://app.datadoghq.com/dash/integration/32021/tidb-cloud-dynamic-tracker)または[**TiDB Cloudクラスタの概要**](https://app.datadoghq.com/dash/integration/30586/tidbcloud-cluster-overview)ダッシュボードは、Datadog [**ダッシュボード一覧**](https://app.datadoghq.com/dashboard/lists)で自動的に利用可能になります。

1.  [データドッグ](https://app.datadoghq.com)にログインします。
2.  Datadog の[**TiDB Cloud統合**ページ](https://app.datadoghq.com/account/settings#integrations/tidb-cloud)に移動します。
3.  **「コンフィグレーション」**タブで、 **「統合のインストール」を**クリックします。

    -   クラスターレベルの Datadog 統合の場合、 [**TiDB Cloudダイナミックトラッカー**](https://app.datadoghq.com/dash/integration/32021/tidb-cloud-dynamic-tracker)ダッシュボードが[**ダッシュボード一覧**](https://app.datadoghq.com/dashboard/lists)に表示されます。
    -   従来のプロジェクト レベルの Datadog 統合 (ベータ版) の場合、 [**TiDB Cloudクラスタの概要**](https://app.datadoghq.com/dash/integration/30586/tidbcloud-cluster-overview)ボード[**ダッシュボード一覧**](https://app.datadoghq.com/dashboard/lists)に表示されます。

## 事前に構築されたダッシュボードをビュー {#view-the-pre-built-dashboard}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、 **「統合」**ページに移動します。
2.  **Datadog**セクションの**「ダッシュボード」**リンクをクリックしてください。

    -   クラスタレベルのDatadog統合の場合、**ダッシュボード**リンクをクリックすると、拡張バージョンで導入された最新のメトリクスを含む新しいダッシュボードが開きます。
    -   従来のプロジェクトレベルのDatadog統合（ベータ版）の場合、**ダッシュボード**リンクをクリックすると従来のダッシュボードが開きますが、そこにはクラスタレベルのDatadog統合で導入された最新のメトリクスは含まれていません。

## Datadogで利用可能な指標 {#metrics-available-to-datadog}

Datadogは、TiDBクラスタに関して以下のメトリクスを追跡します。

| メトリック名                                     | メトリックタイプ | ラベル                                                                                                               | 説明                                                                                                                                                                                                                                                                                                                         |
| :----------------------------------------- | :------- | :---------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| tidb_cloud.db_database_time                | ゲージ      | sql_type: Select|Insert|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`           | TiDBで実行されているすべてのSQLステートメントが1秒あたりに消費する合計時間。これには、すべてのプロセスのCPU時間と、アイドル状態ではない待機時間が含まれます。                                                                                                                                                                                                                                       |
| tidb_cloud.db_query_per_second             | ゲージ      | タイプ: 選択|挿入|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                        | すべての TiDB ノードで 1 秒あたりに実行される SQL ステートメントの数。ステートメントの種類 ( `SELECT` 、 `INSERT` 、または`UPDATE` ) ごとにカウントされます。                                                                                                                                                                                                                     |
| tidb_cloud.db_average_query_duration       | ゲージ      | sql_type: Select|Insert|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`           | クライアントのネットワーク要求がTiDBに送信されてから、TiDBが要求を実行した後、クライアントに要求が返されるまでの時間。                                                                                                                                                                                                                                                            |
| tidb_cloud.db_failed_queries               | ゲージ      | タイプ: 実行者:xxxx|パーサー:xxxx|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`           | 各TiDBノードで1秒あたりに発生するSQL実行エラーに基づいた、エラーの種類（構文エラーや主キーの競合など）の統計情報。                                                                                                                                                                                                                                                              |
| tidb_cloud.db_total_connection             | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                                           | TiDBサーバーにおける現在の接続数。                                                                                                                                                                                                                                                                                                        |
| tidb_cloud.db_active_connections           | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                                           | アクティブな接続数。                                                                                                                                                                                                                                                                                                                 |
| tidb_cloud.db_disconnections               | ゲージ      | 結果：OK｜エラー｜不明<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                          | 接続が切断されたクライアントの数。                                                                                                                                                                                                                                                                                                          |
| tidb_cloud.db_command_per_second           | ゲージ      | タイプ: クエリ|ステートメント準備|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                | TiDBが1秒間に処理するコマンド数。コマンド実行結果の成否に応じて分類されます。                                                                                                                                                                                                                                                                                  |
| tidb_cloud.db_queries_using_plan_cache_ops | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                                           | [プランキャッシュ](/sql-prepared-plan-cache.md)を使用したクエリの 1 秒あたりの統計。実行プラン キャッシュは、プリペアドステートメントコマンドのみをサポートします。                                                                                                                                                                                                                        |
| tidb_cloud.db_transaction_per_second       | ゲージ      | txn_mode:悲観的|楽観的<br/>タイプ: 中止|コミット|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb` | 1秒あたりに実行されるトランザクション数。                                                                                                                                                                                                                                                                                                      |
| tidb_cloud.node_storage_used_bytes         | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/>コンポーネント: tikv|tiflash                | TiKV またはTiFlashノードのディスク使用量（バイト単位）。このメトリックは主にstorageエンジンの論理データ サイズを表し、WAL ファイルと一時ファイルは除外されます。実際のディスク使用率を計算するには、代わりに`(capacity - available) / capacity`を使用してください。TiKV のstorage使用率が 80% を超えると、レイテンシーの急増が発生する可能性があり、使用率が高くなるとリクエストが失敗する可能性があります。すべてのTiFlashノードのstorage使用率が 80% に達すると、 TiFlashレプリカを追加する DDL ステートメントは無期限にハングします。 |
| tidb_cloud.node_storage_capacity_bytes     | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/>コンポーネント: tikv|tiflash                | TiKV/ TiFlashノードのディスク容量（バイト単位）。                                                                                                                                                                                                                                                                                            |
| tidb_cloud.node_cpu_seconds_total          | カウント     | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードのCPU使用率。                                                                                                                                                                                                                                                                                              |
| tidb_cloud.node_cpu_capacity_cores         | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードのCPUコア数の制限。                                                                                                                                                                                                                                                                                           |
| tidb_cloud.node_memory_used_bytes          | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードで使用されているメモリ（バイト単位）。                                                                                                                                                                                                                                                                                   |
| tidb_cloud.node_memory_capacity_bytes      | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードのメモリ容量（バイト単位）。                                                                                                                                                                                                                                                                                        |

クラスタレベルのDatadog統合では、以下の追加メトリクスも利用可能です。

| メトリック名                                                                  | メトリックタイプ | ラベル                                                                                                                            | 説明                                                                                                                           |
| :---------------------------------------------------------------------- | :------- | :----------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| tidb_cloud.node_storage_available_bytes                                 | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv\|tiflash`<br/>クラスター名: `<cluster name>`                                        | TiKV/ TiFlashノードで使用可能なディスク容量（バイト単位）。                                                                                         |
| tidb_cloud.node_disk_read_latency                                       | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv\|tiflash`<br/>クラスター名: `<cluster name>`<br/> `device` : `nvme.*\|dm.*`         | storageデバイスごとの読み取りレイテンシー（秒）。                                                                                                 |
| tidb_cloud.node_disk_write_latency                                      | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv\|tiflash`<br/>クラスター名: `<cluster name>`<br/> `device` : `nvme.*\|dm.*`         | storageデバイスごとの書き込みレイテンシー（秒）。                                                                                                 |
| tidb_cloud.db_kv_request_duration                                       | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv`<br/>クラスター名: `<cluster name>`<br/> `type` : `BatchGet\|Commit\|Prewrite\|...` | TiKVリクエストの種類別の所要時間（秒）。                                                                                                       |
| tidb_cloud.db_component_uptime                                          | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tidb\|tikv\|tiflash`<br/>クラスター名: `<cluster name>`                                  | TiDBコンポーネントの稼働時間（秒単位）。                                                                                                       |
| tidb_cloud.cdc_changefeed_latency (別名 cdc_changefeed_checkpoint_ts_lag) | ゲージ      | changefeed_id: `<changefeed-id>`<br/>クラスター名: `<cluster name>`                                                                  | 変更フィード所有者のチェックポイントタイムスタンプの遅延（秒単位）。                                                                                           |
| tidb_cloud.cdc_changefeed_resolved_ts_lag                               | ゲージ      | changefeed_id: `<changefeed-id>`<br/>クラスター名: `<cluster name>`                                                                  | 変更フィード所有者の解決済みタイムスタンプ遅延（秒単位）。                                                                                                |
| tidb_cloud.cdc_changefeed_status                                        | ゲージ      | changefeed_id: `<changefeed-id>`<br/>クラスター名: `<cluster name>`                                                                  | 変更フィードのステータス:<br/> `-1` : 不明<br/>`0` : 通常<br/>`1` : 警告<br/>`2` : 失敗<br/>`3` : 停止しました<br/>`4` : 完了<br/>`6` : 警告<br/>`7` : その他 |
| tidb_cloud.resource_manager_resource_unit_read_request_unit             | ゲージ      | クラスター名: `<cluster name>`<br/>リソースグループ: `<group-name>`                                                                          | リソースマネージャによって消費された読み取りリクエストユニット（RU）。                                                                                         |
| tidb_cloud.resource_manager_resource_unit_write_request_unit            | ゲージ      | クラスター名: `<cluster name>`<br/>リソースグループ: `<group-name>`                                                                          | リソースマネージャによって消費される書き込みリクエストユニット（RU）。                                                                                         |
| tidb_cloud.dm_task_state                                                | ゲージ      | インスタンス: `instance`<br/>タスク: `task`<br/>クラスター名: `<cluster name>`                                                                | データ移行のタスク状態:<br/> 0: 無効<br/>1: 新着<br/>2：ランニング<br/>3：一時停止<br/>4：停止<br/>5：完了<br/>15: エラー                                       |
| tidb_cloud.dm_syncer_replication_lag_bucket                             | ゲージ      | インスタンス: `instance`<br/>クラスター名: `<cluster name>`                                                                                | データ移行の遅延（バケット）を複製します。                                                                                                        |
| tidb_cloud.dm_syncer_replication_lag_gauge                              | ゲージ      | インスタンス: `instance`<br/>タスク: `task`<br/>クラスター名: `<cluster name>`                                                                | データ移行の遅延（ゲージ）を複製します。                                                                                                         |
| tidb_cloud.dm_relay_read_error_count                                    | ゲージ      | インスタンス: `instance`<br/>クラスター名: `<cluster name>`                                                                                | マスターからのbinlogの読み取りに失敗しました。                                                                                                   |
| tidb_cloud.node_memory_available_bytes                                  | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash                          | TiDB/TiKV/ TiFlashノードで使用可能なメモリ（バイト単位）。                                                                                       |
| tidb_cloud.cdc_changefeed_replica_rows                                  | ゲージ      | changefeed_id: `<changefeed-id>`<br/>クラスター名: `<cluster name>`                                                                  | TiCDCノードが1秒あたりにダウンストリームに書き込むイベントの数。                                                                                          |
