---
title: Integrate TiDB Cloud with Prometheus and Grafana
summary: PrometheusとGrafanaを統合してTiDBクラスタを監視する方法を学びましょう。
---

# TiDB CloudをPrometheusおよびGrafanaと統合する {#integrate-tidb-cloud-with-prometheus-and-grafana}

TiDB Cloudは[プロメテウス](https://prometheus.io/)APIエンドポイントを提供しています。Prometheusサービスをお持ちの場合は、このエンドポイントからTiDB Cloudの主要なメトリクスを簡単に監視できます。

このドキュメントでは、Prometheus サービスを構成してTiDB Cloudエンドポイントから主要なメトリックを読み取る方法と、[グラファナ](https://grafana.com/)を使用してメトリックを表示する方法について説明します。

## Prometheus統合バージョン {#prometheus-integration-versions}

TiDB Cloudは、2022年3月15日よりプロジェクトレベルのPrometheus統合（ベータ版）をサポートしてきました。2025年10月21日より、TiDB CloudレベルのPrometheus統合（プレビュー版）を導入します。2025年12月2日より、クラスターレベルのPrometheus統合が一般提供（GA）となります。

-   **クラスタレベルのPrometheus統合**：2025年10月21日までに組織内に削除されていない従来のプロジェクトレベルのPrometheus統合が残っていない場合、 TiDB Cloudは組織が最新の機能強化を体験できるように、クラスタレベルのPrometheus統合を提供します。

-   **従来のプロジェクトレベルの Prometheus 統合 (ベータ版)** : 2025 年 10 月 21 日時点で組織内に少なくとも 1 つの従来のプロジェクトレベルの Prometheus 統合が削除されずに残っている場合、 TiDB Cloud は、現在のダッシュボードへの影響を回避するために、組織向けにプロジェクトレベルで既存および新規の統合の両方を保持します。

    > **注記**
    >
    > 従来のプロジェクトレベルのPrometheus統合は、2026年1月9日に廃止されます。組織がまだこれらの従来の統合を使用している場合は、 [Prometheus統合の移行](/tidb-cloud/migrate-prometheus-metrics-integrations.md)手順に従って、新しいクラスタレベルの統合に移行し、メトリクス関連サービスへの影響を最小限に抑えてください。

## 前提条件 {#prerequisites}

-   TiDB CloudをPrometheusと統合するには、自己ホスト型またはマネージド型のPrometheusサービスが必要です。

-   TiDB Cloudのサードパーティ メトリクス統合を設定するには、 TiDB Cloudで`Organization Owner`または`Project Owner`アクセス権が必要です。統合ページを表示するには、 TiDB Cloudのプロジェクト内の対象のTiDB Cloud Dedicatedクラスターにアクセスするための`Project Viewer`ロール以上が必要です。

## 制限 {#limitation}

-   PrometheusとGrafanaの統合機能は、現在[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターでのみ利用可能です。
-   クラスターの状態が**CREATING** 、 **RESTORING** 、 **PAUSED** 、または**RESUMING**の場合、Prometheus および Grafana の統合は利用できません。

## 手順 {#steps}

### ステップ1. Prometheus用のscrape_configファイルを取得する {#step-1-get-a-scrape-config-file-for-prometheus}

Prometheus サービスでTiDB Cloudのメトリクスを読み取るように設定する前に、まずTiDB Cloudで`scrape_config` YAML ファイルを生成する必要があります。 `scrape_config`ファイルには、Prometheus サービスが対象のTiDB Cloud Dedicatedクラスターを監視できるようにする一意のベアラー トークンが含まれています。

[Prometheus統合バージョン](#prometheus-integration-versions)バージョンに応じて、Prometheus の`scrape_config`ファイルを取得して統合ページにアクセスする手順は異なります。

<SimpleTab>
<div label="Cluster-level Prometheus integration">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Dedicatedクラスターの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーションペインで、 **[設定]** &gt; **[統合]**をクリックします。
3.  **「統合」**ページで、 **「Prometheusとの統合」**をクリックします。
4.  **「ファイルを追加」を**クリックすると、現在のクラスター用の`scrape_config`ファイルが生成されて表示されます。
5.  `scrape_config`ファイルの内容のコピーを作成して、後で使用してください。

</div>
<div label="Legacy project-level Prometheus integration (Beta)">

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、 **[プロジェクト ビュー]**タブをクリックします。
2.  プロジェクトビューで、対象のプロジェクトを見つけて、そのプロジェクトの<MDSvgIcon name="icon-project-settings" />をクリックします。
3.  左側のナビゲーションペインで、 **「プロジェクト設定」**の下にある**「統合」**をクリックします。
4.  **「統合」**ページで、 **「Prometheusとの統合（ベータ版）」**をクリックします。
5.  **「ファイルを追加」**をクリックすると、現在のプロジェクトのscrape_configファイルが生成されて表示されます。
6.  `scrape_config`ファイルの内容のコピーを作成して、後で使用できるようにします。

</div>
</SimpleTab>

> **注記：**
>
> セキュリティ上の理由から、 TiDB Cloud新しく生成された`scrape_config`ファイルは一度しか表示されません。ファイル ウィンドウを閉じる前に、必ず内容をコピーしてください。コピーを忘れた場合は、 TiDB Cloudで`scrape_config`ファイルを削除して、新しいファイルを生成する必要があります。 `scrape_config`ファイルを削除するには、ファイルを選択し、[ **...]**をクリックしてから [**削除]**をクリックします。

### ステップ2．Prometheusとの統合 {#step-2-integrate-with-prometheus}

1.  Prometheusサービスで指定された監視ディレクトリ内で、Prometheusの設定ファイルを探してください。

    例えば、 `/etc/prometheus/prometheus.yml` 。

2.  Prometheus の設定ファイルで、 `scrape_configs`セクションを探し、 TiDB Cloudから取得した`scrape_config`ファイルの内容をそのセクションにコピーします。

3.  Prometheusサービスで、 **[ステータス]** &gt; **[ターゲット]**を確認し、新しい`scrape_config`ファイルが読み込まれていることを確認してください。読み込まれていない場合は、Prometheusサービスを再起動する必要があるかもしれません。

### ステップ3. Grafana GUIダッシュボードを使用してメトリクスを視覚化する {#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics}

PrometheusサービスがTiDB Cloudからメトリクスを読み取るようになったら、Grafana GUIダッシュボードを使用して、次のようにメトリクスを視覚化できます。

1.  [Prometheus統合バージョン](#prometheus-integration-versions)バージョンに応じて、 TiDB Cloud for Prometheus の Grafana ダッシュボード JSON をダウンロードするリンクは異なります。

    -   クラスターレベルでのPrometheus統合については、 [ここ](https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-tidb-cloud-dynamic-tracker.json)GrafanaダッシュボードJSONファイルをダウンロードしてください。
    -   従来のプロジェクトレベルでのPrometheus統合（ベータ版）については、 [ここ](https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-grafana-dashboard-UI.json)GrafanaダッシュボードJSONファイルをダウンロードしてください。

2.  メトリクスを視覚化するには、 [このJSONをGrafana GUIにインポートしてください。](https://grafana.com/docs/grafana/v8.5/dashboards/export-import/#import-dashboard)

    > **注記：**
    >
    > 既にPrometheusとGrafanaを使用してTiDB Cloudを監視しており、新たに利用可能になったメトリクスを組み込みたい場合は、既存のダッシュボードのJSONを直接更新するのではなく、新しいダッシュボードを作成することをお勧めします。

3.  （オプション）パネルの追加や削除、データソースの変更、表示オプションの修正などにより、必要に応じてダッシュボードをカスタマイズできます。

Grafana の使用方法の詳細については、 [Grafanaのドキュメント](https://grafana.com/docs/grafana/latest/getting-started/getting-started-prometheus/)を参照してください。

## scrape_configをローテーションするベストプラクティス {#best-practice-of-rotating-scrape-config}

データセキュリティを向上させるために、 `scrape_config`ファイルベアラートークンを定期的にローテーションすることが一般的なベストプラクティスです。

1.  [ステップ1](#step-1-get-a-scrape_config-file-for-prometheus)に従って、Prometheus 用の新しい`scrape_config`ファイルを作成します。
2.  新しいファイルの内容をPrometheusの設定ファイルに追加してください。
3.  Prometheus サービスがTiDB Cloudから引き続き読み取れることを確認したら、Prometheus 設定ファイルから古い`scrape_config`ファイルの内容を削除します。
4.  プロジェクトまたはクラスターの**統合**ページで、対応する古い`scrape_config`ファイルを削除して、他のユーザーがTiDB Cloud Prometheus エンドポイントから読み取るために使用できないようにします。

## Prometheusで利用可能なメトリクス {#metrics-available-to-prometheus}

Prometheusは、TiDBクラスタに関して以下のメトリックデータを追跡します。

| メトリック名                                                      | メトリックタイプ | ラベル                                                                                                                            | 説明                                                                                                                                                                                                                                                                                                                         |
| :---------------------------------------------------------- | :------- | :----------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| tidbcloud_db_queries_total                                  | カウント     | sql_type: `Select\|Insert\|...`<br/>クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb`                 | 実行されたステートメントの総数                                                                                                                                                                                                                                                                                                            |
| tidbcloud_db_failed_queries_total                           | カウント     | タイプ: `planner:xxx\|executor:2345\|...`<br/>クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb`          | 実行エラーの総数                                                                                                                                                                                                                                                                                                                   |
| tidbcloud_db_connections                                    | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb`                                                     | TiDBサーバーの現在の接続数                                                                                                                                                                                                                                                                                                            |
| tidbcloud_db_query_duration_seconds                         | ヒストグラム   | sql_type: `Select\|Insert\|...`<br/>クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb`                 | ステートメントの期間ヒストグラム                                                                                                                                                                                                                                                                                                           |
| tidbcloud_changefeed_latency                                | ゲージ      | changefeed_id                                                                                                                  | 変更フィードの上流と下流間のデータ複製レイテンシー                                                                                                                                                                                                                                                                                                  |
| tidbcloud_changefeed_checkpoint_ts                          | ゲージ      | changefeed_id                                                                                                                  | 変更フィードのチェックポイントタイムスタンプ。ダウンストリームに正常に書き込まれた最大のTSO（タイムスタンプオラクル）を表す。                                                                                                                                                                                                                                                           |
| tidbcloud_changefeed_replica_rows                           | ゲージ      | changefeed_id                                                                                                                  | 変更フィードがダウンストリームに1秒あたりに書き込む複製行数                                                                                                                                                                                                                                                                                             |
| tidbcloud_node_storage_used_bytes                           | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>コンポーネント: `tikv\|tiflash`                     | TiKV またはTiFlashノードのディスク使用量（バイト単位）。このメトリックは主にstorageエンジンの論理データ サイズを表し、WAL ファイルと一時ファイルは除外されます。実際のディスク使用率を計算するには、代わりに`(capacity - available) / capacity`を使用してください。TiKV のstorage使用率が 80% を超えると、レイテンシーの急増が発生する可能性があり、使用率が高くなるとリクエストが失敗する可能性があります。すべてのTiFlashノードのstorage使用率が 80% に達すると、 TiFlashレプリカを追加する DDL ステートメントは無期限にハングします。 |
| tidbcloud_node_storage_capacity_bytes                       | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>コンポーネント: `tikv\|tiflash`                     | TiKV/ TiFlashノードのディスク容量（バイト）                                                                                                                                                                                                                                                                                               |
| tidbcloud_node_cpu_seconds_total                            | カウント     | クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`                 | TiDB/TiKV/ TiFlashノードのCPU使用率                                                                                                                                                                                                                                                                                               |
| tidbcloud_node_cpu_capacity_cores                           | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`                 | TiDB/TiKV/ TiFlashノードのCPU制限コア数                                                                                                                                                                                                                                                                                             |
| tidbcloud_node_memory_used_bytes                            | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`                 | TiDB/TiKV/ TiFlashノードで使用されているメモリバイト数                                                                                                                                                                                                                                                                                       |
| tidbcloud_node_memory_capacity_bytes                        | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`                 | TiDB/TiKV/ TiFlashノードのメモリ容量（バイト）                                                                                                                                                                                                                                                                                           |
| tidbcloud_node_storage_available_bytes                      | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv\|tiflash`<br/>クラスター名: `<cluster name>`                                        | TiKV/ TiFlashノードで使用可能なディスク容量（バイト単位）                                                                                                                                                                                                                                                                                        |
| tidbcloud_disk_read_latency                                 | ヒストグラム   | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv\|tiflash`<br/>クラスター名: `<cluster name>`<br/> `device` : `nvme.*\|dm.*`         | storageあたりの読み取りレイテンシー（秒）                                                                                                                                                                                                                                                                                                   |
| tidbcloud_disk_write_latency                                | ヒストグラム   | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv\|tiflash`<br/>クラスター名: `<cluster name>`<br/> `device` : `nvme.*\|dm.*`         | storageあたりの書き込みレイテンシー（秒）                                                                                                                                                                                                                                                                                                   |
| tidbcloud_kv_request_duration                               | ヒストグラム   | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv`<br/>クラスター名: `<cluster name>`<br/> `type` : `BatchGet\|Commit\|Prewrite\|...` | TiKVリクエストの種類別の所要時間（秒）                                                                                                                                                                                                                                                                                                      |
| tidbcloud_component_uptime                                  | ヒストグラム   | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tidb\|tikv\|tiflash`<br/>クラスター名: `<cluster name>`                                  | TiDBコンポーネントの稼働時間（秒）                                                                                                                                                                                                                                                                                                        |
| tidbcloud_ticdc_owner_resolved_ts_lag                       | ゲージ      | changefeed_id: `<changefeed-id>`<br/>クラスター名: `<cluster name>`                                                                  | 変更フィード所有者の解決済みタイムスタンプ遅延（秒単位）                                                                                                                                                                                                                                                                                               |
| tidbcloud_changefeed_status                                 | ゲージ      | changefeed_id: `<changefeed-id>`<br/>クラスター名: `<cluster name>`                                                                  | 変更フィードのステータス:<br/> `-1` : 不明<br/>`0` : 通常<br/>`1` : 警告<br/>`2` : 失敗<br/>`3` : 停止しました<br/>`4` : 完了<br/>`6` : 警告<br/>`7` : その他                                                                                                                                                                                               |
| tidbcloud_resource_manager_resource_unit_read_request_unit  | ゲージ      | クラスター名: `<cluster name>`<br/>リソースグループ: `<group-name>`                                                                          | リソースマネージャが消費する読み取りリクエストユニット                                                                                                                                                                                                                                                                                                |
| tidbcloud_resource_manager_resource_unit_write_request_unit | ゲージ      | クラスター名: `<cluster name>`<br/>リソースグループ: `<group-name>`                                                                          | リソースマネージャが消費する書き込みリクエストユニット                                                                                                                                                                                                                                                                                                |

クラスターレベルのPrometheus統合では、以下の追加メトリクスも利用可能です。

| メトリック名                                     | メトリックタイプ | ラベル                                                             | 説明                                                                                     |
| :----------------------------------------- | :------- | :-------------------------------------------------------------- | :------------------------------------------------------------------------------------- |
| tidbcloud_dm_task_status                   | ゲージ      | インスタンス: `instance`<br/>タスク: `task`<br/>クラスター名: `<cluster name>` | データ移行のタスク状態:<br/> 0: 無効<br/>1: 新着<br/>2：ランニング<br/>3：一時停止<br/>4：停止<br/>5：完了<br/>15: エラー |
| tidbcloud_dm_syncer_replication_lag_bucket | ゲージ      | インスタンス: `instance`<br/>クラスター名: `<cluster name>`                 | データ移行の遅延（バケット）を複製します。                                                                  |
| tidbcloud_dm_syncer_replication_lag_gauge  | ゲージ      | インスタンス: `instance`<br/>タスク: `task`<br/>クラスター名: `<cluster name>` | データ移行の遅延（ゲージ）を複製します。                                                                   |
| tidbcloud_dm_relay_read_error_count        | カウント     | インスタンス: `instance`<br/>クラスター名: `<cluster name>`                 | マスターからbinlogを読み取ろうとした際の失敗回数。                                                           |

## FAQ {#faq}

-   なぜ同じメトリックが、GrafanaとTiDB Cloudコンソールで同時に異なる値を示すのでしょうか？

    GrafanaとTiDB Cloudでは集計計算ロジックが異なるため、表示される集計値が異なる場合があります。より詳細なメトリック値を取得するには、Grafanaの`mini step`設定を調整してください。
