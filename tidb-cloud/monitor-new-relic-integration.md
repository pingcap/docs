---
title: Integrate TiDB Cloud with New Relic (Preview)
summary: New Relic 統合を使用して TiDB クラスターを監視する方法を学習します。
---

# TiDB Cloudと New Relic の統合（プレビュー） {#integrate-tidb-cloud-with-new-relic-preview}

TiDB CloudはNew Relicとの連携（プレビュー）をサポートしています。TiDB TiDB Cloudを設定して、TiDBクラスターのメトリクスを[ニューレリック](https://newrelic.com/)に送信できます。その後、これらのメトリクスをNew Relicダッシュボードで直接確認できるようになります。

## New Relic統合バージョン {#new-relic-integration-version}

TiDB Cloud は、 2023 年 4 月 11 日から New Relic 統合 (ベータ版) をサポートしています。2025 年 7 月 31 日から、 TiDB Cloud は統合の拡張プレビュー バージョンを導入します。

-   **New Relic 統合 (プレビュー)** : 2025 年 7 月 31 日までに組織内に削除されていない Datadog または New Relic 統合がない場合、 TiDB Cloud はNew Relic 統合のプレビュー バージョンを提供して、最新の機能強化を体験できるようにします。
-   **New Relic 連携（ベータ版）** ：2025年7月31日までに組織内で Datadog または New Relic 連携が少なくとも1つ削除されていない場合、 TiDB Cloud は既存の連携と新規の連携の両方をベータ版で保持し、現在のダッシュボードへの影響を回避します。また、適切な移行プランとタイムラインについてご相談させていただきます。

## 前提条件 {#prerequisites}

-   TiDB Cloud をNew Relic と統合するには、アカウントを[ニューレリック](https://newrelic.com/) 、 `Ingest - License`タイプのうち[New Relic APIキーを作成する](https://one.newrelic.com/admin-portal/api-keys/home?)必要です。

    New Relic アカウントをお持ちでない場合は、サインアップしてください[ここ](https://newrelic.com/signup) 。

-   TiDB Cloudのサードパーティメトリクス統合を設定するには、 TiDB Cloudの`Organization Owner`または`Project Owner`アクセス権が必要です。統合ページを表示したり、提供されているリンクを介して設定済みのダッシュボードにアクセスしたりするには、 TiDB Cloudのプロジェクト内のターゲットクラスターにアクセスするための`Project Viewer`以上のロールが必要です。

## 制限 {#limitation}

-   [TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)または[TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential)クラスターでは New Relic 統合を使用できません。

-   クラスターのステータスが**CREATING** 、 **RESTORING** 、 **PAUSED** 、または**RESUMING**の場合、New Relic 統合は使用できません。

-   New Relic 統合を備えたクラスターが削除されると、それに関連付けられている統合サービスも削除されます。

## 手順 {#steps}

### ステップ1. New Relic APIキーとの統合 {#step-1-integrate-with-your-new-relic-api-key}

[New Relic統合バージョン](#new-relic-integration-version)に応じて、統合ページにアクセスする手順は異なります。

<SimpleTab>
<div label="New Relic integration (Preview)">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  左側のナビゲーション ペインで、 **[設定]** &gt; **[統合]**をクリックします。

3.  **「統合」**ページで、 **「New Relic への統合 (プレビュー)」**をクリックします。

4.  New Relic の API キーを入力し、New Relic のサイトを選択します。

5.  **[統合のテスト]**をクリックします。

    -   テストが成功すると、 **「確認」**ボタンが表示されます。
    -   テストに失敗した場合はエラーメッセージが表示されます。メッセージに従ってトラブルシューティングを行い、統合を再試行してください。

6.  **「確認」**をクリックして統合を完了します。

</div>
<div label="New Relic integration (Beta)">

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボ ボックスを使用してターゲット プロジェクトに切り替えます。

2.  左側のナビゲーション ペインで、 **[プロジェクト設定]** &gt; **[統合]**をクリックします。

3.  **「統合」**ページで、 **「New Relic への統合 (ベータ版)」**をクリックします。

4.  New Relic の API キーを入力し、New Relic のサイトを選択します。

5.  **[統合のテスト]**をクリックします。

    -   テストが成功すると、 **「確認」**ボタンが表示されます。
    -   テストに失敗した場合はエラーメッセージが表示されます。メッセージに従ってトラブルシューティングを行い、統合を再試行してください。

6.  **「確認」**をクリックして統合を完了します。

</div>
</SimpleTab>

### ステップ2. New RelicにTiDB Cloudダッシュボードを追加する {#step-2-add-tidb-cloud-dashboard-in-new-relic}

[New Relic統合バージョン](#new-relic-integration-version)に応じて手順は異なります。

<SimpleTab>
<div label="New Relic integration (Preview)">

保留中の[広報](https://github.com/newrelic/newrelic-quickstarts/pull/2681) New Relicにマージされると、新しいTiDB CloudダッシュボードがNew Relicで利用できるようになります。それ以前に、以下の手順でダッシュボードをNew Relicに手動でインポートできます。

1.  新しいダッシュボード用の JSON ファイルを準備します。

    1.  テンプレート JSON ファイル[ここ](https://github.com/pingcap/diag/blob/integration/integration/dashboards/newrelic-dashboard.json)をダウンロードします。

    2.  JSON ファイルで、次のように 4 行目に`"permissions": "PUBLIC_READ_WRITE"`追加します。

        ```json
        {
          "name": "TiDB Cloud Dynamic Tracker",
          "description": null,
          "permissions": "PUBLIC_READ_WRITE",
          ...
        }
        ```

    3.  JSON ファイル内のすべての`"accountIds": []`フィールドに New Relic アカウント ID を追加します。

        例えば：

        ```json
        "accountIds": [
          1234567
        ],
        ```

        > **注記**：
        >
        > 統合エラーを回避するには、JSON ファイル内のすべての`"accountIds"`フィールドにアカウント ID が追加されていることを確認してください。

2.  [ニューレリック](https://one.newrelic.com/)にログインし、左側のナビゲーション バーで**[ダッシュボード]**をクリックして、右上隅の**[ダッシュボードのインポート] を**クリックします。

3.  表示されたダイアログで、準備した JSON ファイルのすべてのコンテンツをテキスト領域に貼り付け、 **[ダッシュボードのインポート]**をクリックします。

</div>
<div label="New Relic integration (Beta)">

1.  [ニューレリック](https://one.newrelic.com/)にログインします。
2.  **「データを追加」**をクリックし、 `TiDB Cloud`を検索して**TiDB Cloud監視**ページに移動します。または、「 [リンク](https://one.newrelic.com/marketplace?state=79bf274b-0c01-7960-c85c-3046ca96568e)をクリックして直接ページにアクセスすることもできます。
3.  アカウント ID を選択し、New Relic でダッシュボードを作成します。

</div>
</SimpleTab>

## あらかじめ構築されたダッシュボードをビュー {#view-the-pre-built-dashboard}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、 **「統合」**ページに移動します。

2.  **New Relic**セクションの**ダッシュボード**リンクをクリックすると、TiDB クラスターの事前構築されたダッシュボードが表示されます。

3.  [New Relic統合バージョン](#new-relic-integration-version)に応じて、次のいずれかを実行します。

    -   New Relic 統合 (プレビュー) の場合は、 **TiDB Cloud Dynamic Tracker**をクリックして新しいダッシュボードを表示します。
    -   New Relic 統合 (ベータ版) の場合は、 **TiDB Cloud Monitoring**をクリックしてレガシー ダッシュボードを表示します。

## New Relicで利用可能なメトリクス {#metrics-available-to-new-relic}

New Relic は、TiDB クラスターの次のメトリクスを追跡します。

| メトリック名                                     | メトリックタイプ | ラベル                                                                                                                                   | 説明                                                                                                     |
| :----------------------------------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------ | :----------------------------------------------------------------------------------------------------- |
| tidb_cloud.db_database_time                | ゲージ      | sql_type: 選択|挿入|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                        | すべてのプロセスの CPU 時間とアイドル状態ではない待機時間を含む、TiDB で実行されているすべての SQL ステートメントによって 1 秒あたりに消費される合計時間。                 |
| tidb_cloud.db_query_per_second             | ゲージ      | タイプ: 選択|挿入|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                             | すべての TiDB インスタンスで 1 秒あたりに実行された SQL ステートメントの数。1 、 `SELECT` 、 `UPDATE` 、およびその他のタイプの`INSERT`に従ってカウントされます。 |
| tidb_cloud.db_平均クエリ実行時間                    | ゲージ      | sql_type: 選択|挿入|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                        | クライアントのネットワーク要求が TiDB に送信されてから、TiDB が要求を実行した後にクライアントに返されるまでの期間。                                        |
| tidb_cloud.db_failed_queries               | ゲージ      | タイプ: executor:xxxx|parser:xxxx|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`         | 各 TiDB インスタンスで 1 秒あたりに発生する SQL 実行エラーに応じたエラー タイプ (構文エラーや主キーの競合など) の統計。                                  |
| tidb_cloud.db_total_connection             | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                                                     | TiDBサーバーの現在の接続数。                                                                                       |
| tidb_cloud.db_active_connections           | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                                                     | アクティブな接続の数。                                                                                            |
| tidb_cloud.db_disconnections               | ゲージ      | 結果: OK|エラー|未定<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                              | 切断されたクライアントの数。                                                                                         |
| tidb_cloud.db_command_per_second           | ゲージ      | タイプ: Query|StmtPrepare|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                 | TiDB が 1 秒あたりに処理したコマンドの数。コマンド実行結果の成功または失敗によって分類されます。                                                   |
| tidb_cloud.db_queries_using_plan_cache_ops | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb`                                                     | [プランキャッシュ](/sql-prepared-plan-cache.md)回使用するクエリの統計。実行プランキャッシュは、プリペアドステートメントコマンドのみをサポートします。             |
| tidb_cloud.db_transaction_per_second       | ゲージ      | txn_mode:悲観的|楽観的<br/><br/>タイプ: 中止|コミット|...<br/><br/>クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…<br/><br/>コンポーネント: `tidb` | 1 秒あたりに実行されるトランザクションの数。                                                                                |
| tidb_cloud.node_storage_used_bytes         | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/><br/>コンポーネント: tikv|tiflash                          | TiKV/ TiFlashノードのディスク使用量（バイト単位）。                                                                       |
| tidb_cloud.node_storage_capacity_bytes     | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tikv-0|tikv-1…|tiflash-0|tiflash-1…<br/><br/>コンポーネント: tikv|tiflash                          | TiKV/ TiFlashノードのディスク容量 (バイト単位)。                                                                       |
| tidb_cloud.node_cpu_seconds_total          | カウント     | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/><br/>コンポーネント: tidb|tikv|tiflash                       | TiDB/TiKV/ TiFlashノードの CPU 使用率。                                                                        |
| tidb_cloud.node_cpu_capacity_cores         | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/><br/>コンポーネント: tidb|tikv|tiflash                       | TiDB/TiKV/ TiFlashノードの CPU コアの制限。                                                                      |
| tidb_cloud.node_memory_used_bytes          | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/><br/>コンポーネント: tidb|tikv|tiflash                       | TiDB/TiKV/ TiFlashノードの使用済みメモリ(バイト単位)。                                                                  |
| tidb_cloud.node_memory_capacity_bytes      | ゲージ      | クラスター名: `<cluster name>`<br/><br/>インスタンス: tidb-0|tidb-1…|tikv-0…|tiflash-0…<br/><br/>コンポーネント: tidb|tikv|tiflash                       | TiDB/TiKV/ TiFlashノードのメモリ容量 (バイト単位)。                                                                   |

New Relic 統合 (プレビュー) では、次の追加メトリックも利用できます。

| メトリック名                                                      | メトリックタイプ | ラベル                                                                                                                          | 説明                                                                                                                    |
| :---------------------------------------------------------- | :------- | :--------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------- |
| tidbcloud.node_storage_available_bytes                      | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv\|tiflash`<br/>クラスター名: `<cluster name>`                                      | TiKV またはTiFlashノードで使用可能なディスク容量 (バイト単位)。                                                                               |
| tidbcloud.ディスク読み取りレイテンシー                                    | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv\|tiflash`<br/>クラスター名: `<cluster name>`<br/> `device`時`nvme.*\|dm.*`         | storageデバイスごとの読み取りレイテンシー(秒単位)。                                                                                        |
| tidbcloud.disk_write_latency                                | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv\|tiflash`<br/>クラスター名: `<cluster name>`<br/> `device`時`nvme.*\|dm.*`         | storageデバイスごとの書き込みレイテンシー(秒単位)。                                                                                        |
| tidbcloud.kv_request_duration                               | ヒストグラム   | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv`<br/>クラスター名: `<cluster name>`<br/> `type`時`BatchGet\|Commit\|Prewrite\|...` | タイプ別の TiKV リクエストの期間 (秒単位)。                                                                                            |
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
