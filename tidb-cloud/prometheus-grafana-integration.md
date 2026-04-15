---
title: Integrate TiDB Cloud with Prometheus and Grafana (Preview)
summary: PrometheusとGrafanaの連携機能を使って、 TiDB Cloudインスタンスを監視する方法を学びましょう。
---

# TiDB CloudとPrometheusおよびGrafanaの統合（プレビュー版） {#integrate-tidb-cloud-with-prometheus-and-grafana-preview}

TiDB Cloudは[プロメテウス](https://prometheus.io/)APIエンドポイントを提供しています。Prometheusサービスをお持ちの場合は、このエンドポイントからTiDB Cloudの主要なメトリクスを簡単に監視できます。

このドキュメントでは、Prometheus サービスを構成して<CustomContent plan="essential">TiDB Cloud Essential</CustomContent> <CustomContent plan="premium">TiDB Cloud Premium</CustomContent>エンドポイントから主要なメトリックを読み取る方法と、[グラファナ](https://grafana.com/)を使用してメトリックを表示する方法について説明します。

## 前提条件 {#prerequisites}

-   TiDB CloudをPrometheusと統合するには、自己ホスト型またはマネージド型のPrometheusサービスが必要です。

-   TiDB Cloudのサードパーティ メトリクス統合を設定するには、TiDB Cloud で`Organization Owner`または`Instance Manager`アクセス権が必要です。統合ページを表示するには、 TiDB Cloud の組織内の対象の TiDB Cloud <CustomContent plan="essential">TiDB Cloud Essential</CustomContent> <CustomContent plan="premium">TiDB Cloud Premium</CustomContent> Premium インスタンスにアクセスするための {{B-PLACEHOLDER-2 -`Project Viewer`または`Instance Viewer`ロール以上が必要です。

## 制限 {#limitation}

-   [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter)インスタンスでは、PrometheusおよびGrafanaとの連携機能は利用できません。
-   <CustomContent plan="essential">TiDB Cloud Essential</CustomContent> <CustomContent plan="premium">TiDB Cloud Premium</CustomContent>インスタンスのステータスが**CREATING** 、 **RESTORING** 、 **PAUSED** 、または**RESUMING**の場合、Prometheus および Grafana の統合は利用できません。

## 手順 {#steps}

### ステップ1. Prometheus用の<code>scrape_config</code>ファイルを取得する {#step-1-get-a-code-scrape-config-code-file-for-prometheus}

Prometheus サービスでTiDB Cloudのメトリクスを読み取るように設定する前に、まずTiDB Cloudで`scrape_config` YAML ファイルを生成する必要があります。 `scrape_config`ファイルには、Prometheus サービスが対象の<CustomContent plan="essential">TiDB Cloud Essential</CustomContent> <CustomContent plan="premium">TiDB Cloudプレミアム</CustomContent>インスタンスを監視できるようにする一意のベアラー トークンが含まれています。

<CustomContent plan="essential">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Essentialインスタンスの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーションペインで、 **[統合]** &gt; **[Prometheusとの統合（プレビュー）]**をクリックします。
3.  **「ファイルを追加」を**クリックすると、現在のTiDB Cloud Essentialインスタンス用の`scrape_config`ファイルが生成されて表示されます。
4.  `scrape_config`ファイルの内容のコピーを作成して、後で使用してください。

</CustomContent>

<CustomContent plan="premium">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Premiumインスタンスの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーション ペインで、 **[設定]** &gt; **[統合]** &gt; **[Prometheus との統合 (プレビュー)]**をクリックします。
3.  **「ファイルを追加」を**クリックすると、現在のTiDB Cloud Premium インスタンス用の`scrape_config`ファイルが生成されて表示されます。
4.  `scrape_config`ファイルの内容のコピーを作成して、後で使用してください。

</CustomContent>

> **注記：**
>
> -   セキュリティ上の理由から、 TiDB Cloud新しく生成された`scrape_config`ファイルは一度しか表示されません。ファイルウィンドウを閉じる前に、必ず内容をコピーしてください。
> -   忘れた場合は、 TiDB Cloudの`scrape_config`ファイルを削除して、新しいファイルを生成してください。 `scrape_config`ファイルを削除するには、ファイルを選択し、[ **...]**をクリックしてから**[削除]**をクリックします。

### ステップ2．Prometheusとの統合 {#step-2-integrate-with-prometheus}

1.  Prometheusサービスで指定された監視ディレクトリ内で、Prometheusの設定ファイルを探してください。

    例えば、 `/etc/prometheus/prometheus.yml` 。

2.  Prometheus の設定ファイルで、 `scrape_configs`セクションを探し、 TiDB Cloudから取得した`scrape_config`ファイルの内容をそのセクションにコピーします。

3.  Prometheusサービスで、 **[ステータス]** &gt; **[ターゲット]**を確認し、新しい`scrape_config`ファイルが読み込まれていることを確認してください。読み込まれていない場合は、Prometheusサービスを再起動する必要があるかもしれません。

### ステップ3. Grafana GUIダッシュボードを使用してメトリクスを視覚化する {#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics}

PrometheusサービスがTiDB Cloudからメトリクスを読み取った後、Grafana GUIダッシュボードを使用して、次のようにメトリクスを視覚化できます。

1.  <CustomContent plan="essential">TiDB Cloud Essential</CustomContent> <CustomContent plan="premium">TiDB Cloud Premium</CustomContent>用のGrafanaダッシュボードJSONファイルは、以下のリンクからダウンロードできます。

    <CustomContent plan="essential">

    [https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-tidb-cloud-dynamic-tracker-essential.json](https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-tidb-cloud-dynamic-tracker-essential.json)

    </CustomContent>
    <CustomContent plan="premium">

    [https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-tidb-cloud-dynamic-tracker-premium.json](https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-tidb-cloud-dynamic-tracker-premium.json)

    </CustomContent>

2.  メトリクスを視覚化するには、 [このJSONをGrafana GUIにインポートしてください。](https://grafana.com/docs/grafana/v8.5/dashboards/export-import/#import-dashboard)

    > **注記：**
    >
    > 既にPrometheusとGrafanaを使用して<CustomContent plan="essential">TiDB Cloud Essential</CustomContent>および<CustomContent plan="premium">TiDB Cloud Premium</CustomContent>インスタンスを監視しており、新たに利用可能になったメトリクスを組み込みたい場合は、既存のダッシュボードのJSONを直接更新するのではなく、新しいダッシュボードを作成することをお勧めします。

3.  （オプション）パネルの追加や削除、データソースの変更、表示オプションの修正などにより、必要に応じてダッシュボードをカスタマイズできます。

Grafana の使用方法の詳細については、 [Grafanaのドキュメント](https://grafana.com/docs/grafana/latest/getting-started/getting-started-prometheus/)を参照してください。

## <code>scrape_config</code>をローテーションするためのベストプラクティス {#best-practice-for-rotating-code-scrape-config-code}

データセキュリティを向上させるため、 `scrape_config`ファイルベアラートークンを定期的にローテーションしてください。

1.  [ステップ1](#step-1-get-a-scrape_config-file-for-prometheus)に従って、Prometheus 用の新しい`scrape_config`ファイルを作成します。
2.  新しいファイルの内容をPrometheusの設定ファイルに追加してください。
3.  Prometheus サービスがTiDB Cloudから読み取れることを確認したら、Prometheus 設定ファイルから古い`scrape_config`ファイルの内容を削除します。
4.  <CustomContent plan="essential">TiDB Cloud Essential</CustomContent> <CustomContent plan="premium">TiDB Cloudプレミアム</CustomContent>インスタンスの**統合**ページで、対応する古い`scrape_config`ファイルを削除して、他のユーザーがTiDB Cloud Prometheusエンドポイントから読み取るために使用できないようにします。

## Prometheusで利用可能なメトリクス {#metrics-available-to-prometheus}

Prometheusは、お客様の<CustomContent plan="essential">TiDB Cloud Essential</CustomContent> <CustomContent plan="premium">TiDB Cloud Premium</CustomContent>インスタンスについて、以下のメトリックデータを追跡します。

<CustomContent plan="essential">

> **注記：**
>
> TiDB Cloud Essential はTiCDC コンポーネントをサポートしていないため、 `tidbcloud_changefeed_*`メトリックは現在利用できません。

| メトリック名                                                   | メトリックタイプ | ラベル                                                                                                                                         | 説明                                                                            |
| :------------------------------------------------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------ | :---------------------------------------------------------------------------- |
| `tidbcloud_db_total_connection`                          | ゲージ      | `instance_id: <instance id>`<br/>`instance_name: <instance name>`                                                                           | TiDBサーバーの現在の接続数                                                               |
| `tidbcloud_db_active_connections`                        | ゲージ      | `instance_id: <instance id>`<br/>`instance_name: <instance name>`                                                                           | アクティブな接続数                                                                     |
| `tidbcloud_db_disconnections`                            | ゲージ      | `result: Error\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>`                                                  | 接続結果によって切断されたクライアントの数                                                         |
| `tidbcloud_db_database_time`                             | ゲージ      | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>`                                       | すべてのプロセスのCPU消費量の合計と、アイドル状態ではない待機時間の合計を表す時間モデル統計。                              |
| `tidbcloud_db_query_per_second`                          | ゲージ      | `type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>`                                           | 1秒あたりに実行されるSQLステートメントの数（ステートメントの種類ごとにカウント）                                    |
| `tidbcloud_db_failed_queries`                            | ゲージ      | `type: planner:xxx\|executor:2345\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>`                               | SQL文を1秒あたりに実行した際に発生したエラーの種類（構文エラー、主キーの競合など）の統計情報                              |
| `tidbcloud_db_command_per_second`                        | ゲージ      | `type: Query\|Ping\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>`                                              | TiDBが1秒あたりに処理するコマンド数                                                          |
| `tidbcloud_db_queries_using_plan_cache_ops`              | ゲージ      | `instance_id: <instance id>`<br/>`instance_name: <instance name>`                                                                           | 1秒あたりに実行プランキャッシュにヒットするクエリの統計情報                                                |
| `tidbcloud_db_average_query_duration`                    | ゲージ      | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>`                                       | TiDBにネットワークリクエストが送信されてからクライアントに返されるまでの時間                                      |
| `tidbcloud_db_transaction_per_second`                    | ゲージ      | `type: Commit\|Rollback\|...`<br/>`txn_mode: optimistic\|pessimistic`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 1秒あたりに実行されるトランザクション数                                                          |
| `tidbcloud_db_row_storage_used_bytes`                    | ゲージ      | `instance_id: <instance id>`<br/>`instance_name: <instance name>`                                                                           | TiDB Cloud Essentialインスタンスの行ベースのstorageサイズ（バイト単位）                             |
| `tidbcloud_db_columnar_storage_used_bytes`               | ゲージ      | `instance_id: <instance id>`<br/>`instance_name: <instance name>`                                                                           | TiDB Cloud Essentialインスタンスのカラム型storageのサイズ（バイト単位）。TiFlashが有効になっていない場合は0を返します。 |
| `tidbcloud_resource_manager_resource_request_unit_total` | ゲージ      | `instance_id: <instance id>`<br/>`instance_name: <instance name>`                                                                           | 消費されたリクエストユニット（RU）の合計。                                                        |

</CustomContent>

<CustomContent plan="premium">

| メトリック名                                                   | メトリックタイプ | ラベル                                                                                                                                         | 説明                                                                                                                           |
| :------------------------------------------------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------- |
| `tidbcloud_db_total_connection`                          | ゲージ      | `instance_id: <instance id>`<br/>`instance_name: <instance name>`                                                                           | TiDBサーバーの現在の接続数                                                                                                              |
| `tidbcloud_db_active_connections`                        | ゲージ      | `instance_id: <instance id>`<br/>`instance_name: <instance name>`                                                                           | アクティブな接続数                                                                                                                    |
| `tidbcloud_db_disconnections`                            | ゲージ      | `result: Error\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>`                                                  | 接続結果によって切断されたクライアントの数                                                                                                        |
| `tidbcloud_db_database_time`                             | ゲージ      | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>`                                       | すべてのプロセスのCPU消費量の合計と、アイドル状態ではない待機時間の合計を表す時間モデル統計。                                                                             |
| `tidbcloud_db_query_per_second`                          | ゲージ      | `type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>`                                           | 1秒あたりに実行されるSQLステートメントの数（ステートメントの種類ごとにカウント）                                                                                   |
| `tidbcloud_db_failed_queries`                            | ゲージ      | `type: planner:xxx\|executor:2345\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>`                               | SQL文を1秒あたりに実行した際に発生したエラーの種類（構文エラー、主キーの競合など）の統計情報                                                                             |
| `tidbcloud_db_command_per_second`                        | ゲージ      | `type: Query\|Ping\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>`                                              | TiDBが1秒あたりに処理するコマンド数                                                                                                         |
| `tidbcloud_db_queries_using_plan_cache_ops`              | ゲージ      | `instance_id: <instance id>`<br/>`instance_name: <instance name>`                                                                           | 1秒あたりに実行プランキャッシュにヒットするクエリの統計情報                                                                                               |
| `tidbcloud_db_average_query_duration`                    | ゲージ      | `sql_type: Select\|Insert\|...`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>`                                       | TiDBにネットワークリクエストが送信されてからクライアントに返されるまでの時間                                                                                     |
| `tidbcloud_db_transaction_per_second`                    | ゲージ      | `type: Commit\|Rollback\|...`<br/>`txn_mode: optimistic\|pessimistic`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>` | 1秒あたりに実行されるトランザクション数                                                                                                         |
| `tidbcloud_db_row_storage_used_bytes`                    | ゲージ      | `instance_id: <instance id>`<br/>`instance_name: <instance name>`                                                                           | TiDB Cloud Premiumインスタンスの行ベースのstorageサイズ（バイト単位）                                                                              |
| `tidbcloud_db_columnar_storage_used_bytes`               | ゲージ      | `instance_id: <instance id>`<br/>`instance_name: <instance name>`                                                                           | TiDB Cloud Premiumインスタンスのカラム型storageのサイズ（バイト単位）。                                                                             |
| `tidbcloud_resource_manager_resource_request_unit_total` | ゲージ      | `instance_id: <instance id>`<br/>`instance_name: <instance name>`                                                                           | 消費されたリクエストユニット（RU）の合計。                                                                                                       |
| `tidbcloud_changefeed_latency`                           | ゲージ      | `changefeed: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>`                                         | 変更フィードの上流と下流間のデータ複製レイテンシー                                                                                                    |
| `tidbcloud_changefeed_status`                            | ゲージ      | `changefeed: <changefeed-id>`<br/>`instance_id: <instance id>`<br/>`instance_name: <instance name>`                                         | 変更フィードのステータス:<br/> `-1` : 不明<br/>`0` : 通常<br/>`1` : 警告<br/>`2` : 失敗<br/>`3` : 停止しました<br/>`4` : 完了<br/>`6` : 警告<br/>`7` : その他 |

</CustomContent>

## FAQ {#faq}

-   なぜ同じメトリックが、GrafanaとTiDB Cloudコンソールで同時に異なる値を示すのでしょうか？

    GrafanaとTiDB Cloudは集計計算ロジックが異なるため、表示される集計値が異なる場合があります。より詳細なメトリック値を取得するには、Grafanaの`mini step`設定を調整してください。
