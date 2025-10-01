---
title: Integrate TiDB Cloud with Datadog
summary: Datadog 統合を使用して TiDB クラスターを監視する方法を学習します。
---

# TiDB CloudとDatadogの統合 {#integrate-tidb-cloud-with-datadog}

TiDB CloudはDatadogとの連携をサポートしています。TiDB TiDB Cloudを設定して、TiDBクラスターのメトリクスを[データドッグ](https://www.datadoghq.com/)に送信することができます。その後、これらのメトリクスをDatadogダッシュボードで直接確認できるようになります。

## Datadog統合バージョン {#datadog-integration-version}

TiDB Cloudは、2022年3月4日よりプロジェクトレベルのDatadog統合（ベータ版）をサポートしています。2025年7月31日より、 TiDB CloudはクラスターレベルのDatadog統合（プレビュー版）を導入します。2025年9月30日より、クラスターレベルのDatadog統合が一般提供（GA）されます。

-   **クラスター レベルの Datadog 統合**: 2025 年 7 月 31 日までに組織内に削除されていないレガシー プロジェクト レベルの Datadog または New Relic 統合がない場合、 TiDB Cloud は、組織が最新の機能強化を体験できるように、クラスター レベルの Datadog 統合を提供します。
-   **レガシープロジェクトレベルの Datadog 統合（ベータ版）** ：2025年7月31日までに組織内でレガシープロジェクトレベルの Datadog または New Relic 統合が少なくとも1つ削除されていない場合、 TiDB Cloud は既存の統合と新規の統合の両方をプロジェクトレベルで保持し、現在のダッシュボードへの影響を回避します。レガシープロジェクトレベルの Datadog 統合は、2025年10月31日に廃止されることにご注意ください。組織でこれらのレガシー統合をまだ使用している場合は、手順[DatadogとNew Relicの統合の移行](/tidb-cloud/migrate-metrics-integrations.md)に従って新しいクラスターレベルの統合に移行し、メトリクス関連サービスへの影響を最小限に抑えてください。

## 前提条件 {#prerequisites}

-   TiDB Cloudを Datadog と統合するには、Datadog アカウントと[Datadog APIキー](https://app.datadoghq.com/organization-settings/api-keys)必要です。Datadog アカウントを初めて作成すると、Datadog から API キーが付与されます。

    Datadog アカウントをお持ちでない場合は、 [https://app.datadoghq.com/signup](https://app.datadoghq.com/signup)でサインアップしてください。

-   TiDB Cloudのサードパーティメトリクス統合を設定するには、 TiDB Cloudの`Organization Owner`または`Project Owner`アクセス権が必要です。統合ページを表示したり、提供されたリンクを介して設定済みのダッシュボードにアクセスしたりするには、 TiDB Cloudのプロジェクト内のターゲットクラスターにアクセスするための`Project Viewer`以上のロールが必要です。

## 制限 {#limitation}

-   [TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)または[TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential)クラスターでは Datadog 統合を使用できません。

-   クラスターのステータスが**CREATING** 、 **RESTORING** 、 **PAUSED** 、または**RESUMING**の場合、Datadog 統合は使用できません。

-   Datadog 統合を備えたクラスターが削除されると、それに関連付けられている統合サービスも削除されます。

## 手順 {#steps}

### ステップ1. Datadog APIキーとの統合 {#step-1-integrate-with-your-datadog-api-key}

[Datadog統合バージョン](#datadog-integration-version)に応じて、統合ページにアクセスする手順は異なります。

<SimpleTab>
<div label="Cluster-level Datadog integration">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  左側のナビゲーション ペインで、 **[設定]** &gt; **[統合]**をクリックします。

3.  **「統合」**ページで、 **「Datadog への統合」を**クリックします。

4.  Datadog API キーを入力し、Datadog サイトを選択します。

5.  **[統合のテスト]**をクリックします。

    -   テストが成功すると、 **「確認」**ボタンが表示されます。
    -   テストに失敗した場合は、エラーメッセージが表示されます。メッセージに従ってトラブルシューティングを行い、統合を再試行してください。

6.  **「確認」**をクリックして統合を完了します。

</div>
<div label="Datadog integration (Beta)">

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボ ボックスを使用してターゲット プロジェクトに切り替えます。

2.  左側のナビゲーション ペインで、 **[プロジェクト設定]** &gt; **[統合]**をクリックします。

3.  **[統合]**ページで、 **[Datadog への統合 (ベータ版)]**をクリックします。

4.  Datadog API キーを入力し、Datadog サイトを選択します。

5.  **[統合のテスト]**をクリックします。

    -   テストが成功すると、 **「確認」**ボタンが表示されます。
    -   テストに失敗した場合は、エラーメッセージが表示されます。メッセージに従ってトラブルシューティングを行い、統合を再試行してください。

6.  **「確認」**をクリックして統合を完了します。

</div>
</SimpleTab>

### ステップ2. DatadogにTiDB Cloud Integrationをインストールする {#step-2-install-tidb-cloud-integration-in-datadog}

> **注記：**
>
> DatadogにTiDB Cloud統合を既にインストールしている場合は、このセクションの以下の手順をスキップできます。ダッシュボード[**TiDB Cloudダイナミック トラッカー**](https://app.datadoghq.com/dash/integration/32021/tidb-cloud-dynamic-tracker)または[**TiDB Cloudクラスタの概要**](https://app.datadoghq.com/dash/integration/30586/tidbcloud-cluster-overview) 、Datadog [**ダッシュボードリスト**](https://app.datadoghq.com/dashboard/lists)で自動的に利用可能になります。

1.  [データドッグ](https://app.datadoghq.com)にログインします。
2.  Datadog の[**TiDB Cloud統合**ページ](https://app.datadoghq.com/account/settings#integrations/tidb-cloud)へ進みます。
3.  **[コンフィグレーション]**タブで、 **[統合のインストール]を**クリックします。

    -   クラスターレベルの Datadog 統合の場合、 [**TiDB Cloudダイナミック トラッカー**](https://app.datadoghq.com/dash/integration/32021/tidb-cloud-dynamic-tracker)ダッシュボードが[**ダッシュボードリスト**](https://app.datadoghq.com/dashboard/lists)に表示されます。
    -   従来のプロジェクト レベルの Datadog 統合 (ベータ版) の場合、 [**TiDB Cloudクラスタの概要**](https://app.datadoghq.com/dash/integration/30586/tidbcloud-cluster-overview)ダッシュボードが[**ダッシュボードリスト**](https://app.datadoghq.com/dashboard/lists)に表示されます。

## あらかじめ構築されたダッシュボードをビュー {#view-the-pre-built-dashboard}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、 **「統合」**ページに移動します。
2.  **Datadog**セクションの**ダッシュボード**リンクをクリックします。

    -   クラスターレベルの Datadog 統合の場合、**ダッシュボード**リンクをクリックすると、拡張バージョンで導入された最新のメトリックを含む新しいダッシュボードが開きます。
    -   従来のプロジェクト レベルの Datadog 統合 (ベータ版) の場合、**ダッシュボード**リンクをクリックすると従来のダッシュボードが開きますが、これにはクラスター レベルの Datadog 統合で導入された最新のメトリックは含まれません。

## Datadogで利用可能なメトリクス {#metrics-available-to-datadog}

Datadog は、TiDB クラスターの次のメトリクスを追跡します。

| メトリック名                                     | メトリックタイプ | ラベル                                                                                                               | 説明                                                                                                    |
| :----------------------------------------- | :------- | :---------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------- |
| tidb_cloud.db_database_time                | ゲージ      | sql_type: 選択|挿入|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                   | すべてのプロセスの CPU 時間とアイドル状態ではない待機時間を含む、TiDB で実行されているすべての SQL ステートメントによって 1 秒あたりに消費される合計時間。                |
| tidb_cloud.db_query_per_second             | ゲージ      | タイプ: 選択|挿入|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                        | すべての TiDB インスタンスで 1 秒あたりに実行された SQL ステートメントの数。ステートメント タイプ ( `SELECT` 、または`UPDATE` ) `INSERT`にカウントされます。 |
| tidb_cloud.db_平均クエリ実行時間                    | ゲージ      | sql_type: 選択|挿入|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                   | クライアントのネットワーク要求が TiDB に送信されてから、TiDB が要求を実行した後にクライアントに返されるまでの期間。                                       |
| tidb_cloud.db_failed_queries               | ゲージ      | タイプ: executor:xxxx|parser:xxxx|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`    | 各 TiDB インスタンスで 1 秒あたりに発生する SQL 実行エラーに応じたエラー タイプ (構文エラーや主キーの競合など) の統計。                                 |
| tidb_cloud.db_total_connection             | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                                           | TiDBサーバーの現在の接続数。                                                                                      |
| tidb_cloud.db_active_connections           | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                                           | アクティブな接続の数。                                                                                           |
| tidb_cloud.db_disconnections               | ゲージ      | 結果: OK|エラー|未定<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                         | 切断されたクライアントの数。                                                                                        |
| tidb_cloud.db_command_per_second           | ゲージ      | タイプ: Query|StmtPrepare|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`            | TiDB が 1 秒あたりに処理したコマンドの数。コマンド実行結果の成功または失敗によって分類されます。                                                  |
| tidb_cloud.db_queries_using_plan_cache_ops | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                                           | [プランキャッシュ](/sql-prepared-plan-cache.md)回使用されるクエリの統計。実行プランキャッシュは、プリペアドステートメントコマンドのみをサポートします。           |
| tidb_cloud.db_transaction_per_second       | ゲージ      | txn_mode:悲観的|楽観的<br/>タイプ: 中止|コミット|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb` | 1 秒あたりに実行されるトランザクションの数。                                                                               |
| tidb_cloud.node_storage_used_bytes         | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/>コンポーネント: tikv|tiflash                | TiKV/ TiFlashノードのディスク使用量（バイト単位）。                                                                      |
| tidb_cloud.node_storage_capacity_bytes     | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/>コンポーネント: tikv|tiflash                | TiKV/ TiFlashノードのディスク容量 (バイト単位)。                                                                      |
| tidb_cloud.node_cpu_seconds_total          | カウント     | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードの CPU 使用率。                                                                       |
| tidb_cloud.node_cpu_capacity_cores         | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードの CPU コアの制限。                                                                     |
| tidb_cloud.node_memory_used_bytes          | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードの使用済みメモリ(バイト単位)。                                                                 |
| tidb_cloud.node_memory_capacity_bytes      | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードのメモリ容量 (バイト単位)。                                                                  |

クラスターレベルの Datadog 統合では、次の追加メトリクスも利用できます。

| メトリック名                                                                  | メトリックタイプ | ラベル                                                                                                                          | 説明                                                                                                                     |
| :---------------------------------------------------------------------- | :------- | :--------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------- |
| tidb_cloud.node_storage_available_bytes                                 | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv\|tiflash`<br/>クラスター名: `<cluster name>`                                      | TiKV/ TiFlashノードで使用可能なディスク容量 (バイト単位)。                                                                                  |
| tidb_cloud.node_disk_read_latency                                       | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv\|tiflash`<br/>クラスター名: `<cluster name>`<br/> `device`時`nvme.*\|dm.*`         | storageデバイスあたりの読み取りレイテンシー(秒)。                                                                                          |
| tidb_cloud.node_disk_write_latency                                      | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv\|tiflash`<br/>クラスター名: `<cluster name>`<br/> `device`時`nvme.*\|dm.*`         | storageデバイスあたりの書き込みレイテンシー(秒)。                                                                                          |
| tidb_cloud.db_kv_request_duration                                       | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv`<br/>クラスター名: `<cluster name>`<br/> `type`時`BatchGet\|Commit\|Prewrite\|...` | タイプ別の TiKV リクエストの継続時間（秒）。                                                                                              |
| tidb_cloud.db_component_uptime                                          | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tidb\|tikv\|tiflash`<br/>クラスター名: `<cluster name>`                                | TiDB コンポーネントの稼働時間 (秒単位)。                                                                                               |
| tidb_cloud.cdc_changefeed_latency (別名 cdc_changefeed_checkpoint_ts_lag) | ゲージ      | チェンジフィードID: `<changefeed-id>`<br/>クラスター名: `<cluster name>`                                                                   | 変更フィード所有者のチェックポイント タイムスタンプの遅延 (秒単位)。                                                                                   |
| tidb_cloud.cdc_changefeed_resolved_ts_lag                               | ゲージ      | チェンジフィードID: `<changefeed-id>`<br/>クラスター名: `<cluster name>`                                                                   | 変更フィード所有者の解決されたタイムスタンプの遅延 (秒単位)。                                                                                       |
| tidb_cloud.cdc_changefeed_status                                        | ゲージ      | チェンジフィードID: `<changefeed-id>`<br/>クラスター名: `<cluster name>`                                                                   | チェンジフィードステータス:<br/> `-1` ：不明<br/>`0` ：正常<br/>`1` : 警告<br/>`2` : 失敗<br/>`3` : 停止<br/>`4` ：終了<br/>`6` : 警告<br/>`7` : その他 |
| tidb_cloud.resource_manager_resource_unit_read_request_unit             | ゲージ      | クラスター名: `<cluster name>`<br/>リソースグループ: `<group-name>`                                                                        | リソース マネージャーによって消費される読み取り要求単位 (RU)。                                                                                     |
| tidb_cloud.resource_manager_resource_unit_write_request_unit            | ゲージ      | クラスター名: `<cluster name>`<br/>リソースグループ: `<group-name>`                                                                        | リソース マネージャーによって消費される書き込み要求単位 (RU)。                                                                                     |
| tidb_cloud.dm_task_state                                                | ゲージ      | インスタンス: `instance`<br/>タスク: `task`<br/>クラスター名: `<cluster name>`                                                              | データ移行のタスクの状態:<br/> 0: 無効<br/>1: 新しい<br/>2: ランニング<br/>3: 一時停止<br/>4: 停止<br/>5: 完了<br/>15: エラー                           |
| tidb_cloud.dm_syncer_replication_lag_bucket                             | ゲージ      | インスタンス: `instance`<br/>クラスター名: `<cluster name>`                                                                              | データ移行の遅延 (バケット) を複製します。                                                                                                |
| tidb_cloud.dm_syncer_replication_lag_gauge                              | ゲージ      | インスタンス: `instance`<br/>タスク: `task`<br/>クラスター名: `<cluster name>`                                                              | データ移行の遅延 (ゲージ) を複製します。                                                                                                 |
| tidb_cloud.dm_relay_read_error_count                                    | ゲージ      | インスタンス: `instance`<br/>クラスター名: `<cluster name>`                                                                              | マスターからのbinlogの読み取りに失敗しました。                                                                                             |
| tidb_cloud.node_memory_available_bytes                                  | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash                        | TiDB/TiKV/ TiFlashノードの使用可能なメモリ(バイト単位)。                                                                                 |
| tidb_cloud.cdc_changefeed_replica_rows                                  | ゲージ      | チェンジフィードID: `<changefeed-id>`<br/>クラスター名: `<cluster name>`                                                                   | TiCDC ノードが 1 秒あたりにダウンストリームに書き込むイベントの数。                                                                                 |
