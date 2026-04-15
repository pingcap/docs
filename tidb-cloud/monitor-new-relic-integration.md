---
title: Integrate TiDB Cloud with New Relic
summary: New Relicとの連携により、TiDBクラスタを監視する方法を学びましょう。
---

# TiDB CloudとNew Relicを統合する {#integrate-tidb-cloud-with-new-relic}

TiDB CloudはNew Relicとの連携をサポートしています。TiDB TiDB Cloudを設定して、TiDBクラスタのメトリクスを[ニューレリック](https://newrelic.com/)に送信することができます。その後、New Relicダッシュボードでこれらのメトリクスを直接確認できます。

## 新しいRelic統合バージョン {#new-relic-integration-version}

TiDB Cloudは、2023年4月11日よりプロジェクトレベルのNew Relic統合（ベータ版）をサポートしてきました。2025年7月31日より、TiDB CloudレベルのNew Relic統合（プレビュー版）を導入します。2025年9月30日より、クラスターレベルのNew Relic統合が一般提供（GA）となります。

-   **クラスタレベルのNew Relic統合**：2025年7月31日までに組織内で削除されていない従来のプロジェクトレベルのDatadogまたはNew Relic統合が残っていない場合、 TiDB Cloudは組織が最新の機能強化を体験できるように、クラスタレベルのNew Relic統合を提供します。
-   **従来のプロジェクトレベルの New Relic 統合 (ベータ版)** : 2025 年 7 月 31 日時点で組織内に少なくとも 1 つの従来のプロジェクトレベルの Datadog または New Relic 統合が削除されずに残っている場合、 TiDB Cloud は、現在のダッシュボードへの影響を回避するために、組織向けにプロジェクトレベルで既存および新規の統合の両方を保持します。従来のプロジェクトレベルの New Relic 統合は、2025 年 10 月 31 日に廃止されることに注意してください。組織がこれらの従来の統合をまだ使用している場合は、[DatadogとNew Relicの統合を移行する](/tidb-cloud/migrate-metrics-integrations.md)手順に従って、新しいクラスタレベルの統合に移行し、メトリクス関連サービスへの影響を最小限に抑えてください。

## 前提条件 {#prerequisites}

-   TiDB Cloud をNew Relic と統合するには、[ニューレリック](https://newrelic.com/)レリック アカウントと、 `Ingest - License`タイプの[New Relic APIキーを作成する](https://one.newrelic.com/admin-portal/api-keys/home?)必要があります。

    New Relicのアカウントをお持ちでない場合は、[ここ](https://newrelic.com/signup)ご登録ください。

-   TiDB Cloudのサードパーティ メトリクス統合を設定するには、 TiDB Cloudで`Organization Owner`または`Project Owner`アクセス権が必要です。統合ページを表示したり、提供されたリンクから設定済みのダッシュボードにアクセスしたりするには、TiDB TiDB Cloudのプロジェクト内の対象のTiDB Cloud Dedicatedクラスターにアクセスするための`Project Viewer`ロール以上が必要です。

## 制限 {#limitation}

-   New Relicとの連携機能は、現在[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターでのみ利用可能です。

-   クラスターの状態が**「作成中」** 、 **「復元中」** 、 **「一時停止中」** 、 **「再開中」**の場合は、New Relic の統合は利用できません。

-   New Relicとの連携が確立されたクラスターが削除されると、それに関連付けられた連携サービスも削除されます。

## 手順 {#steps}

### ステップ1. New Relic APIキーと連携する {#step-1-integrate-with-your-new-relic-api-key}

[新しいRelic統合バージョン](#new-relic-integration-version)に応じて、統合ページにアクセスする手順は異なります。

<SimpleTab>
<div label="Cluster-level New Relic integration">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Dedicatedクラスターの名前をクリックして、その概要ページに移動します。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[統合]**をクリックします。

3.  **統合**ページで、 **「New Relic との統合」**をクリックします。

4.  New RelicのAPIキーを入力し、New Relicのサイトを選択してください。

5.  **「統合テスト」**をクリックします。

    -   テストが成功すると、 **「確認」**ボタンが表示されます。
    -   テストが失敗した場合は、エラーメッセージが表示されます。メッセージに従ってトラブルシューティングを行い、統合を再試行してください。

6.  統合を完了するには、 **「確認」**をクリックしてください。

</div>
<div label="Legacy project-level New Relic integration (Beta)">

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、 **[プロジェクト ビュー]**タブをクリックします。

2.  プロジェクトビューで、対象のプロジェクトを見つけて、そのプロジェクトの<MDSvgIcon name="icon-project-settings" />をクリックします。

3.  左側のナビゲーションペインで、 **「プロジェクト設定」**の下にある**「統合」**をクリックします。

4.  **統合**ページで、 **[New Relic との統合 (ベータ版)]**をクリックします。

5.  New RelicのAPIキーを入力し、New Relicのサイトを選択してください。

6.  **「統合テスト」**をクリックします。

    -   テストが成功すると、 **「確認」**ボタンが表示されます。
    -   テストが失敗した場合は、エラーメッセージが表示されます。メッセージに従ってトラブルシューティングを行い、統合を再試行してください。

7.  統合を完了するには、 **「確認」**をクリックしてください。

</div>
</SimpleTab>

### ステップ2. New RelicにTiDB Cloudダッシュボードを追加する {#step-2-add-tidb-cloud-dashboard-in-new-relic}

[新しいRelic統合バージョン](#new-relic-integration-version)に応じて、手順は異なります。

<SimpleTab>
<div label="Cluster-level New Relic integration">

新しいTiDB Cloudダッシュボードは、保留中の[広報](https://github.com/newrelic/newrelic-quickstarts/pull/2681)New Relicによってマージされた後にNew Relicで利用可能になります。それまでは、以下の手順でダッシュボードをNew Relicに手動でインポートできます。

1.  新しいダッシュボード用のJSONファイルを準備します。

    1.  テンプレートの JSON ファイルを[ここ](https://github.com/pingcap/diag/blob/integration/integration/dashboards/newrelic-dashboard.json)ダウンロードします。

    2.  JSONファイルで、4行目に`"permissions": "PUBLIC_READ_WRITE"`以下のように追加します。

        ```json
        {
          "name": "TiDB Cloud Dynamic Tracker",
          "description": null,
          "permissions": "PUBLIC_READ_WRITE",
          ...
        }
        ```

    3.  JSON ファイル内のすべての`"accountIds": []`フィールドに New Relic アカウント ID を追加してください。

        例えば：

        ```json
        "accountIds": [
          1234567
        ],
        ```

        > **注記**：
        >
        > 統合エラーを回避するために、JSON ファイル内のすべての`"accountIds"`フィールドにアカウント ID が追加されていることを確認してください。

2.  [ニューレリック](https://one.newrelic.com/)にログインし、左側のナビゲーションバーの**「ダッシュボード」**をクリックし、右上隅の「ダッシュ**ボードのインポート」**をクリックします。

3.  表示されたダイアログで、準備した JSON ファイルの内容をすべてテキスト エリアに貼り付け、次に**[ダッシュボードをインポート] を**クリックします。

</div>
<div label="Legacy project-level New Relic integration (Beta)">

1.  [ニューレリック](https://one.newrelic.com/)にログインします。
2.  **「データの追加」**をクリックし、 `TiDB Cloud`を検索して、 **TiDB Cloud監視**ページに移動します。または、 [リンク](https://one.newrelic.com/marketplace?state=79bf274b-0c01-7960-c85c-3046ca96568e)クリックして直接ページにアクセスすることもできます。
3.  アカウントIDを選択し、New Relicでダッシュボードを作成してください。

</div>
</SimpleTab>

## 事前に構築されたダッシュボードをビュー {#view-the-pre-built-dashboard}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、 **「統合」**ページに移動します。

2.  **New Relic**セクションの**「ダッシュボード」**リンクをクリックすると、TiDBクラスターの事前構築済みダッシュボードが表示されます。

3.  [新しいRelic統合バージョン](#new-relic-integration-version)に応じて、次のいずれかを実行します。

    -   クラスタレベルでのNew Relic統合を行うには、 **TiDB Cloud Dynamic Tracker**をクリックして新しいダッシュボードを表示してください。
    -   従来のプロジェクトレベルのNew Relic統合（ベータ版）については、 **「TiDB Cloud Monitoring」**をクリックして従来のダッシュボードを表示してください。

## New Relicで利用可能なメトリクス {#metrics-available-to-new-relic}

New Relicは、TiDBクラスタに関して以下のメトリクスを追跡します。

| メトリック名                                     | メトリックタイプ | ラベル                                                                                                                                   | 説明                                                                                                                                                                                                                                                                                                                         |
| :----------------------------------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| tidb_cloud.db_database_time                | ゲージ      | sql_type: Select|Insert|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                | TiDBで実行されるすべてのSQLステートメントが1秒あたりに消費する合計時間。これには、すべてのプロセスのCPU時間と、アイドル状態ではない待機時間が含まれます。                                                                                                                                                                                                                                         |
| tidb_cloud.db_query_per_second             | ゲージ      | タイプ: 選択|挿入|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                             | すべての TiDB ノードで 1 秒あたりに実行される SQL ステートメントの数。これは`SELECT` 、 `INSERT` 、 `UPDATE` 、およびその他のタイプのステートメントに従ってカウントされます。                                                                                                                                                                                                               |
| tidb_cloud.db_average_query_duration       | ゲージ      | sql_type: Select|Insert|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                | クライアントのネットワーク要求がTiDBに送信されてから、TiDBが要求を実行した後、クライアントに要求が返されるまでの時間。                                                                                                                                                                                                                                                            |
| tidb_cloud.db_failed_queries               | ゲージ      | タイプ: 実行者:xxxx|パーサー:xxxx|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                | 各TiDBノードで1秒あたりに発生するSQL実行エラーに基づいた、エラーの種類（構文エラーや主キーの競合など）の統計情報。                                                                                                                                                                                                                                                              |
| tidb_cloud.db_total_connection             | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                                                     | TiDBサーバーにおける現在の接続数。                                                                                                                                                                                                                                                                                                        |
| tidb_cloud.db_active_connections           | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                                                     | アクティブな接続数。                                                                                                                                                                                                                                                                                                                 |
| tidb_cloud.db_disconnections               | ゲージ      | 結果：OK｜エラー｜不明<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                               | 接続が切断されたクライアントの数。                                                                                                                                                                                                                                                                                                          |
| tidb_cloud.db_command_per_second           | ゲージ      | タイプ: クエリ|ステートメント準備|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                     | TiDBが1秒間に処理するコマンド数。コマンド実行結果の成否に応じて分類されます。                                                                                                                                                                                                                                                                                  |
| tidb_cloud.db_queries_using_plan_cache_ops | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                                                     | [プランキャッシュ](/sql-prepared-plan-cache.md)を使用したクエリの 1 秒あたりの統計。実行プラン キャッシュは、プリペアドステートメントコマンドのみをサポートします。                                                                                                                                                                                                                        |
| tidb_cloud.db_transaction_per_second       | ゲージ      | txn_mode:悲観的|楽観的<br/><br/>タイプ: 中止|コミット|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb` | 1秒あたりに実行されるトランザクション数。                                                                                                                                                                                                                                                                                                      |
| tidb_cloud.node_storage_used_bytes         | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/><br/>コンポーネント: tikv|tiflash                          | TiKV またはTiFlashノードのディスク使用量（バイト単位）。このメトリックは主にstorageエンジンの論理データ サイズを表し、WAL ファイルと一時ファイルは除外されます。実際のディスク使用率を計算するには、代わりに`(capacity - available) / capacity`を使用してください。TiKV のstorage使用率が 80% を超えると、レイテンシーの急増が発生する可能性があり、使用率が高くなるとリクエストが失敗する可能性があります。すべてのTiFlashノードのstorage使用率が 80% に達すると、 TiFlashレプリカを追加する DDL ステートメントは無期限にハングします。 |
| tidb_cloud.node_storage_capacity_bytes     | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/><br/>コンポーネント: tikv|tiflash                          | TiKV/ TiFlashノードのディスク容量（バイト単位）。                                                                                                                                                                                                                                                                                            |
| tidb_cloud.node_cpu_seconds_total (ベータ版のみ) | カウント     | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/><br/>コンポーネント: tidb|tikv|tiflash                       | TiDB/TiKV/ TiFlashノードのCPU使用率。                                                                                                                                                                                                                                                                                              |
| tidb_cloud.node_cpu_capacity_cores         | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/><br/>コンポーネント: tidb|tikv|tiflash                       | TiDB/TiKV/ TiFlashノードのCPUコア数の制限。                                                                                                                                                                                                                                                                                           |
| tidb_cloud.node_memory_used_bytes          | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/><br/>コンポーネント: tidb|tikv|tiflash                       | TiDB/TiKV/ TiFlashノードで使用されているメモリ（バイト単位）。                                                                                                                                                                                                                                                                                   |
| tidb_cloud.node_memory_capacity_bytes      | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/><br/>コンポーネント: tidb|tikv|tiflash                       | TiDB/TiKV/ TiFlashノードのメモリ容量（バイト単位）。                                                                                                                                                                                                                                                                                        |

クラスターレベルのNew Relic統合では、以下の追加メトリクスも利用可能です。

| メトリック名                                                                  | メトリックタイプ | ラベル                                                                                                                                           | 説明                                                                                                                                                                   |
| :---------------------------------------------------------------------- | :------- | :-------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| tidb_cloud.node_storage_available_bytes                                 | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/><br/>コンポーネント: `tikv\|tiflash`<br/><br/>クラスター名: `<cluster name>`                                             | TiKVまたはTiFlashノードで使用可能なディスク容量（バイト単位）。                                                                                                                                |
| tidb_cloud.node_disk_read_latency                                       | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/><br/>コンポーネント: `tikv\|tiflash`<br/><br/>クラスター名: `<cluster name>`<br/><br/> `device` : `nvme.*\|dm.*`         | storageデバイスごとの読み取りレイテンシー（秒単位）。                                                                                                                                       |
| tidb_cloud.node_disk_write_latency                                      | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/><br/>コンポーネント: `tikv\|tiflash`<br/><br/>クラスター名: `<cluster name>`<br/><br/> `device` : `nvme.*\|dm.*`         | storageデバイスごとの書き込みレイテンシー（秒単位）。                                                                                                                                       |
| tidb_cloud.db_kv_request_duration                                       | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/><br/>コンポーネント: `tikv`<br/><br/>クラスター名: `<cluster name>`<br/><br/> `type` : `BatchGet\|Commit\|Prewrite\|...` | TiKVリクエストの種類別の所要時間（秒）。                                                                                                                                               |
| tidb_cloud.db_component_uptime                                          | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/><br/>コンポーネント: `tidb\|tikv\|tiflash`<br/><br/>クラスター名: `<cluster name>`                                       | TiDBコンポーネントの稼働時間（秒単位）。                                                                                                                                               |
| tidb_cloud.cdc_changefeed_latency (別名 cdc_changefeed_checkpoint_ts_lag) | ゲージ      | changefeed_id: `<changefeed-id>`<br/><br/>クラスター名: `<cluster name>`                                                                            | 変更フィード所有者のチェックポイントタイムスタンプの遅延（秒単位）。                                                                                                                                   |
| tidb_cloud.cdc_changefeed_resolved_ts_lag                               | ゲージ      | changefeed_id: `<changefeed-id>`<br/><br/>クラスター名: `<cluster name>`                                                                            | 変更フィード所有者の解決済みタイムスタンプ遅延（秒単位）。                                                                                                                                        |
| tidb_cloud.cdc_changefeed_status                                        | ゲージ      | changefeed_id: `<changefeed-id>`<br/><br/>クラスター名: `<cluster name>`                                                                            | 変更フィードのステータス:<br/><br/> `-1` : 不明<br/><br/>`0` : 通常<br/><br/>`1` : 警告<br/><br/>`2` : 失敗<br/><br/>`3` : 停止しました<br/><br/>`4` : 完了<br/><br/>`6` : 警告<br/><br/>`7` : その他 |
| tidb_cloud.resource_manager_resource_unit_read_request_unit             | ゲージ      | クラスター名: `<cluster name>`<br/><br/>リソースグループ: `<group-name>`                                                                                    | リソースマネージャによって消費された読み取りリクエストユニット（RU）。                                                                                                                                 |
| tidb_cloud.resource_manager_resource_unit_write_request_unit            | ゲージ      | クラスター名: `<cluster name>`<br/><br/>リソースグループ: `<group-name>`                                                                                    | リソースマネージャによって消費される書き込みリクエストユニット（RU）。                                                                                                                                 |
| tidb_cloud.dm_task_state                                                | ゲージ      | インスタンス: `instance`<br/><br/>タスク: `task`<br/><br/>クラスター名: `<cluster name>`                                                                     | データ移行のタスク状態:<br/><br/> `0` : 無効<br/><br/>`1` : 新規<br/><br/>`2` : 実行中<br/><br/>`3` : 一時停止<br/><br/>`4` : 停止しました<br/><br/>`5` : 完了<br/><br/>`15` : エラー                 |
| tidb_cloud.dm_syncer_replication_lag_bucket                             | ゲージ      | インスタンス: `instance`<br/><br/>クラスター名: `<cluster name>`                                                                                          | データ移行の遅延（バケット）を複製します。                                                                                                                                                |
| tidb_cloud.dm_syncer_replication_lag_gauge                              | ゲージ      | インスタンス: `instance`<br/><br/>タスク: `task`<br/><br/>クラスター名: `<cluster name>`                                                                     | データ移行の遅延（ゲージ）を複製します。                                                                                                                                                 |
| tidb_cloud.dm_relay_read_error_count                                    | ゲージ      | インスタンス: `instance`<br/><br/>クラスター名: `<cluster name>`                                                                                          | マスターからのbinlogの読み取りに失敗しました。                                                                                                                                           |
| tidb_cloud.node_memory_available_bytes                                  | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/><br/>コンポーネント: tidb|tikv|tiflash                               | TiDB/TiKV/ TiFlashノードで使用可能なメモリ（バイト単位）。                                                                                                                               |
| tidb_cloud.cdc_changefeed_replica_rows                                  | ゲージ      | changefeed_id: `<changefeed-id>`<br/><br/>クラスター名: `<cluster name>`                                                                            | TiCDCノードが1秒あたりにダウンストリームに書き込むイベントの数。                                                                                                                                  |
| tidb_cloud.node_cpu_seconds_total_rate                                  | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/><br/>コンポーネント: tidb|tikv|tiflash                               | TiDB/TiKV/ TiFlashノードのCPU使用率。                                                                                                                                        |
