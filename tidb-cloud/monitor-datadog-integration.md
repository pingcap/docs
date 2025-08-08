---
title: Integrate TiDB Cloud with Datadog (Preview)
summary: Datadog 統合を使用して TiDB クラスターを監視する方法を学習します。
---

# TiDB Cloudと Datadog の統合 (プレビュー) {#integrate-tidb-cloud-with-datadog-preview}

TiDB CloudはDatadogとの連携（プレビュー）をサポートしています。TiDB TiDB Cloudを設定して、TiDBクラスターのメトリクスを[データドッグ](https://www.datadoghq.com/)に送信できます。その後、これらのメトリクスをDatadogダッシュボードで直接確認できるようになります。

## Datadog統合バージョン {#datadog-integration-version}

TiDB Cloud は、 2022 年 3 月 4 日から Datadog 統合 (ベータ版) をサポートしています。2025 年 7 月 31 日から、 TiDB Cloud は統合の拡張プレビュー バージョンを導入します。

-   **Datadog 統合 (プレビュー)** : 2025 年 7 月 31 日までに組織内に削除されていない Datadog または New Relic 統合がない場合、 TiDB Cloud は組織が最新の機能強化を体験できるように、Datadog 統合のプレビュー バージョンを提供します。
-   **Datadog 連携（ベータ版）** ：2025年7月31日までに組織内で Datadog または New Relic 連携が少なくとも1つ削除されていない場合、 TiDB Cloud は既存の連携と新規の連携の両方をベータ版で保持し、現在のダッシュボードへの影響を回避します。また、適切な移行プランとタイムラインについてご相談させていただきます。

## 前提条件 {#prerequisites}

-   TiDB Cloudを Datadog と統合するには、Datadog アカウントと[Datadog APIキー](https://app.datadoghq.com/organization-settings/api-keys)必要です。Datadog アカウントを初めて作成すると、Datadog から API キーが付与されます。

    Datadog アカウントをお持ちでない場合は、 [https://app.datadoghq.com/signup](https://app.datadoghq.com/signup)でサインアップしてください。

-   TiDB Cloudのサードパーティメトリクス統合を設定するには、 TiDB Cloudの`Organization Owner`または`Project Owner`アクセス権が必要です。統合ページを表示したり、提供されているリンクを介して設定済みのダッシュボードにアクセスしたりするには、 TiDB Cloudのプロジェクト内のターゲットクラスターにアクセスするための`Project Viewer`以上のロールが必要です。

## 制限 {#limitation}

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターでは Datadog 統合を使用できません。

-   クラスターのステータスが**CREATING** 、 **RESTORING** 、 **PAUSED** 、または**RESUMING**の場合、Datadog 統合は使用できません。

-   Datadog 統合を備えたクラスターが削除されると、それに関連付けられている統合サービスも削除されます。

## 手順 {#steps}

### ステップ1. Datadog APIキーとの統合 {#step-1-integrate-with-your-datadog-api-key}

[Datadog統合バージョン](#datadog-integration-version)に応じて、統合ページにアクセスする手順は異なります。

<SimpleTab>
<div label="Datadog integration (Preview)">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  左側のナビゲーション ペインで、 **[設定]** &gt; **[統合]**をクリックします。

3.  **[統合]**ページで、 **[Datadog への統合 (プレビュー)]**をクリックします。

4.  Datadog API キーを入力し、Datadog サイトを選択します。

5.  **[統合のテスト]**をクリックします。

    -   テストが成功すると、 **「確認」**ボタンが表示されます。
    -   テストに失敗した場合はエラーメッセージが表示されます。メッセージに従ってトラブルシューティングを行い、統合を再試行してください。

6.  **「確認」**をクリックして統合を完了します。

</div>
<div label="Datadog integration (Beta)">

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボ ボックスを使用してターゲット プロジェクトに切り替えます。

2.  左側のナビゲーション ペインで、 **[プロジェクト設定]** &gt; **[統合]**をクリックします。

3.  **[統合]**ページで、 **[Datadog への統合 (ベータ版)]**をクリックします。

4.  Datadog API キーを入力し、Datadog サイトを選択します。

5.  **[統合のテスト]**をクリックします。

    -   テストが成功すると、 **「確認」**ボタンが表示されます。
    -   テストに失敗した場合はエラーメッセージが表示されます。メッセージに従ってトラブルシューティングを行い、統合を再試行してください。

6.  **「確認」**をクリックして統合を完了します。

</div>
</SimpleTab>

### ステップ2. DatadogにTiDB Cloud統合をインストールする {#step-2-install-tidb-cloud-integration-in-datadog}

[Datadog統合バージョン](#datadog-integration-version)に応じて手順は異なります。

<SimpleTab>
<div label="Datadog integration (Preview)">

保留中の[広報](https://github.com/DataDog/integrations-extras/pull/2751) Datadogによってマージされると、新しいTiDB CloudダッシュボードがDatadogで利用可能になります。それ以前に、以下の手順でダッシュボードをDatadogに手動でインポートできます。

1.  新しいダッシュボード[ここ](https://github.com/pingcap/diag/blob/integration/integration/dashboards/datadog-dashboard.json)の JSON ファイルをダウンロードします。
2.  [データドッグ](https://app.datadoghq.com)にログインし、左側のナビゲーション ペインで**[ダッシュボード]**をクリックして、右上隅の**[+ 新しいダッシュボード]**をクリックします。
3.  表示されたダイアログで、 **「新しいダッシュボード」**をクリックして、新しい空のダッシュボードを作成します。
4.  新しく作成されたダッシュボード ページで、右上隅の**[構成]**をクリックし、表示されたペインの一番下までスクロールして、 **[ダッシュボード JSON のインポート...]**をクリックします。
5.  表示されたダイアログで、ダウンロードした JSON ファイルをアップロードしてダッシュボードのセットアップを完了します。

</div>
<div label="Datadog integration (Beta)">

1.  [データドッグ](https://app.datadoghq.com)にログインします。
2.  Datadog の[**TiDB Cloud統合**ページ](https://app.datadoghq.com/account/settings#integrations/tidb-cloud)へ進みます。
3.  **「コンフィグレーション」**タブで、 **「統合をインストール」を**クリックします。 [**TiDB Cloudクラスタの概要**](https://app.datadoghq.com/dash/integration/30586/tidbcloud-cluster-overview)ダッシュボードが[**ダッシュボードリスト**](https://app.datadoghq.com/dashboard/lists)に表示されます。

</div>
</SimpleTab>

## あらかじめ構築されたダッシュボードをビュー {#view-the-pre-built-dashboard}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、 **「統合」**ページに移動します。
2.  [Datadog統合バージョン](#datadog-integration-version)に応じて、次のいずれかを実行します。

    -   Datadog 統合 (ベータ版) の場合は、 **Datadog**セクションの**ダッシュボード**リンクをクリックします。

    -   Datadog 統合 (プレビュー) の場合は、 **Datadog**セクションの**[ダッシュボード]**リンクをクリックし、開いたページの左側のナビゲーション ペインで**[ダッシュボード] を**クリックしてから、 **[TiDB Cloud Dynamic Tracker]**をクリックして、完全なメトリックを含む新しいダッシュボードを表示します。

    > **注記：**
    >
    > Datadog 統合 (プレビュー) については、次の点に注意してください。
    >
    > -   保留中の[広報](https://github.com/DataDog/integrations-extras/pull/2751) Datadog によってマージされる前は、**ダッシュボード**リンクは、プレビュー バージョンで導入された最新のメトリックが含まれないレガシー ダッシュボードにリダイレクトされます。
    > -   保留中の[広報](https://github.com/DataDog/integrations-extras/pull/2751)マージされると、 **Datadog**セクションの**ダッシュボード**リンクが新しいダッシュボードにリダイレクトされます。

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
| tidb_cloud.db_queries_using_plan_cache_ops | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb`                                           | [プランキャッシュ](/sql-prepared-plan-cache.md)回使用するクエリの統計。実行プランキャッシュは、プリペアドステートメントコマンドのみをサポートします。            |
| tidb_cloud.db_transaction_per_second       | ゲージ      | txn_mode:悲観的|楽観的<br/>タイプ: 中止|コミット|...<br/>クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…<br/>コンポーネント: `tidb` | 1 秒あたりに実行されるトランザクションの数。                                                                               |
| tidb_cloud.node_storage_used_bytes         | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/>コンポーネント: tikv|tiflash                | TiKV/ TiFlashノードのディスク使用量（バイト単位）。                                                                      |
| tidb_cloud.node_storage_capacity_bytes     | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/>コンポーネント: tikv|tiflash                | TiKV/ TiFlashノードのディスク容量 (バイト単位)。                                                                      |
| tidb_cloud.node_cpu_seconds_total          | カウント     | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードの CPU 使用率。                                                                       |
| tidb_cloud.node_cpu_capacity_cores         | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードの CPU コアの制限。                                                                     |
| tidb_cloud.node_memory_used_bytes          | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードの使用済みメモリ(バイト単位)。                                                                 |
| tidb_cloud.node_memory_capacity_bytes      | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/>コンポーネント: tidb|tikv|tiflash             | TiDB/TiKV/ TiFlashノードのメモリ容量 (バイト単位)。                                                                  |

Datadog 統合 (プレビュー) では、次の追加メトリックも利用できます。

| メトリック名                                                      | メトリックタイプ | ラベル                                                                                                                          | 説明                                                                                                                    |
| :---------------------------------------------------------- | :------- | :--------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------- |
| tidbcloud.node_storage_available_bytes                      | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv\|tiflash`<br/>クラスター名: `<cluster name>`                                      | TiKV/ TiFlashノードで使用可能なディスク容量 (バイト単位)。                                                                                 |
| tidbcloud.ディスク読み取りレイテンシー                                    | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv\|tiflash`<br/>クラスター名: `<cluster name>`<br/> `device`時`nvme.*\|dm.*`         | storageデバイスあたりの読み取りレイテンシー(秒)。                                                                                         |
| tidbcloud.disk_write_latency                                | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv\|tiflash`<br/>クラスター名: `<cluster name>`<br/> `device`時`nvme.*\|dm.*`         | storageデバイスあたりの書き込みレイテンシー(秒単位)。                                                                                       |
| tidbcloud.kv_request_duration                               | ヒストグラム   | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv`<br/>クラスター名: `<cluster name>`<br/> `type`時`BatchGet\|Commit\|Prewrite\|...` | タイプ別の TiKV リクエストの継続時間（秒）。                                                                                             |
| tidbcloud.コンポーネントの稼働時間                                      | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tidb\|tikv\|tiflash`<br/>クラスター名: `<cluster name>`                                | TiDB コンポーネントの稼働時間 (秒単位)。                                                                                              |
| tidbcloud.ticdc_owner_checkpoint_ts_lag                     | ゲージ      | チェンジフィードID: `<changefeed-id>`<br/>クラスター名: `<cluster name>`                                                                   | 変更フィード所有者のチェックポイント タイムスタンプの遅延 (秒単位)。                                                                                  |
| tidbcloud.ticdc_owner_resolved_ts_lag                       | ゲージ      | チェンジフィードID: `<changefeed-id>`<br/>クラスター名: `<cluster name>`                                                                   | 変更フィード所有者の解決されたタイムスタンプの遅延 (秒単位)。                                                                                      |
| tidbcloud.changefeed_status                                 | ゲージ      | チェンジフィードID: `<changefeed-id>`<br/>クラスター名: `<cluster name>`                                                                   | チェンジフィードステータス:<br/> `-1` ：不明<br/>`0` ：正常<br/>`1` : 警告<br/>`2` : 失敗<br/>`3` : 停止<br/>`4` ：終了<br/>`6` ：警告<br/>`7` : その他 |
| tidbcloud.resource_manager_resource_unit_read_request_unit  | ゲージ      | クラスター名: `<cluster name>`<br/>リソースグループ: `<group-name>`                                                                        | リソース マネージャーによって消費される読み取り要求単位 (RU)。                                                                                    |
| tidbcloud.resource_manager_resource_unit_write_request_unit | ゲージ      | クラスター名: `<cluster name>`<br/>リソースグループ: `<group-name>`                                                                        | リソース マネージャーによって消費される書き込み要求単位 (RU)。                                                                                    |
| tidb_cloud.dm_task_state                                    | ゲージ      | インスタンス: `instance`<br/>タスク: `task`<br/>クラスター名: `<cluster name>`                                                              | データ移行のタスクの状態:<br/> 0: 無効<br/>1: 新しい<br/>2: ランニング<br/>3: 一時停止<br/>4: 停止<br/>5: 完了<br/>15: エラー                          |
| tidb_cloud.dm_syncer_replication_lag_bucket                 | ゲージ      | インスタンス: `instance`<br/>クラスター名: `<cluster name>`                                                                              | データ移行の遅延 (バケット) を複製します。                                                                                               |
| tidb_cloud.dm_syncer_replication_lag_gauge                  | ゲージ      | インスタンス: `instance`<br/>タスク: `task`<br/>クラスター名: `<cluster name>`                                                              | データ移行の遅延 (ゲージ) を複製します。                                                                                                |
| tidb_cloud.dm_relay_read_error_count                        | ゲージ      | インスタンス: `instance`<br/>クラスター名: `<cluster name>`                                                                              | マスターからのbinlogの読み取りに失敗しました。                                                                                            |
