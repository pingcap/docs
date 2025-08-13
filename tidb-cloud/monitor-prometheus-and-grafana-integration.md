---
title: Integrate TiDB Cloud with Prometheus and Grafana (Beta)
summary: Prometheus と Grafana の統合を使用して TiDB クラスターを監視する方法を学びます。
---

# TiDB Cloud をPrometheus および Grafana と統合する (ベータ版) {#integrate-tidb-cloud-with-prometheus-and-grafana-beta}

TiDB Cloudは[プロメテウス](https://prometheus.io/) APIエンドポイント（ベータ版）を提供しています。Prometheusサービスをお持ちの場合は、エンドポイントからTiDB Cloudの主要なメトリクスを簡単に監視できます。

このドキュメントでは、 TiDB Cloudエンドポイントから主要なメトリックを読み取るように Prometheus サービスを構成する方法と、 [グラファナ](https://grafana.com/)使用してメトリックを表示する方法について説明します。

## 前提条件 {#prerequisites}

-   TiDB Cloudを Prometheus と統合するには、セルフホスト型または管理型の Prometheus サービスが必要です。

-   TiDB Cloudのサードパーティ統合設定を編集するには、組織への`Organization Owner`アクセス権またはTiDB Cloudの対象プロジェクトへの`Project Member`アクセス権が必要です。

## 制限 {#limitation}

-   [TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)または[TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential)クラスターでは Prometheus と Grafana の統合は使用できません。

-   クラスターのステータスが**CREATING** 、 **RESTORING** 、 **PAUSED** 、または**RESUMING**の場合、Prometheus と Grafana の統合は使用できません。

## 手順 {#steps}

### ステップ1. Prometheusのscrape_configファイルを取得する {#step-1-get-a-scrape-config-file-for-prometheus}

Prometheus サービスがTiDB Cloudのメトリクスを読み取るように設定する前に、まずTiDB Cloudで YAML ファイル`scrape_config`生成する必要があります。この YAML ファイル`scrape_config`には、Prometheus サービスが現在のプロジェクト内の任意のデータベースクラスターを監視できるようにする一意のベアラートークンが含まれています。

Prometheus の`scrape_config`ファイルを取得するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボ ボックスを使用してターゲット プロジェクトに切り替えます。

2.  左側のナビゲーション ペインで、 **[プロジェクト設定]** &gt; **[統合]**をクリックします。

3.  **「統合」**ページで、 **「Prometheus への統合 (ベータ版)」**をクリックします。

4.  **「ファイルの追加」を**クリックすると、現在のプロジェクトの scrape_config ファイルを生成して表示します。

5.  後で使用するために、 `scrape_config`ファイルの内容のコピーを作成します。

    > **注記：**
    >
    > セキュリティ上の理由から、 TiDB Cloud新しく生成された`scrape_config`ファイルは一度しか表示されません。ファイルウィンドウを閉じる前に、必ず内容をコピーしてください。コピーを忘れた場合は、 TiDB Cloud内の`scrape_config`ファイルを削除し、新しいファイルを生成する必要があります。5 ファイル`scrape_config`削除するには、ファイルを選択し、 **...**をクリックしてから、**削除**をクリックします。

### ステップ2. Prometheusとの統合 {#step-2-integrate-with-prometheus}

1.  Prometheus サービスによって指定された監視ディレクトリで、Prometheus 構成ファイルを見つけます。

    たとえば、 `/etc/prometheus/prometheus.yml` 。

2.  Prometheus 構成ファイルで、 `scrape_configs`セクションを見つけて、 TiDB Cloudから取得した`scrape_config`ファイル コンテンツをそのセクションにコピーします。

3.  Prometheusサービスで、 **「ステータス」** &gt; **「ターゲット」**を確認し、新しい`scrape_config`ファイルが読み込まれていることを確認してください。読み込まれていない場合は、Prometheusサービスを再起動する必要があるかもしれません。

### ステップ3. Grafana GUIダッシュボードを使用してメトリックを視覚化する {#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics}

Prometheus サービスがTiDB Cloudからメトリックを読み取った後、Grafana GUI ダッシュボードを使用して、次のようにメトリックを視覚化できます。

1.  TiDB Cloud [ここ](https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-grafana-dashboard-UI.json)の Grafana ダッシュボード JSON をダウンロードします。

2.  メトリックを視覚化するには[このJSONを自分のGrafana GUIにインポートする](https://grafana.com/docs/grafana/v8.5/dashboards/export-import/#import-dashboard)使用します。

    > **注記：**
    >
    > すでに Prometheus と Grafana を使用してTiDB Cloud を監視しており、新しく利用可能になったメトリックを組み込みたい場合は、既存のダッシュボードの JSON を直接更新するのではなく、新しいダッシュボードを作成することをお勧めします。

3.  (オプション) パネルを追加または削除したり、データ ソースを変更したり、表示オプションを変更したりして、必要に応じてダッシュボードをカスタマイズします。

Grafana の使用方法の詳細については、 [Grafanaのドキュメント](https://grafana.com/docs/grafana/latest/getting-started/getting-started-prometheus/)参照してください。

## scrape_config のローテーションのベストプラクティス {#best-practice-of-rotating-scrape-config}

データのセキュリティを向上させるには、 `scrape_config`ファイル ベアラー トークンを定期的にローテーションすることが一般的なベスト プラクティスです。

1.  [ステップ1](#step-1-get-a-scrape_config-file-for-prometheus)に従って、Prometheus 用の新しい`scrape_config`ファイルを作成します。
2.  新しいファイルの内容を Prometheus 構成ファイルに追加します。
3.  Prometheus サービスがTiDB Cloudから引き続き読み取り可能であることを確認したら、Prometheus 構成ファイルから古い`scrape_config`ファイルの内容を削除します。
4.  プロジェクトの**統合**ページで、対応する古い`scrape_config`ファイルを削除して、他のユーザーがそれを使用してTiDB Cloud Prometheus エンドポイントから読み取ることをブロックします。

## Prometheusで利用可能なメトリクス {#metrics-available-to-prometheus}

Prometheus は、TiDB クラスターの次のメトリック データを追跡します。

| メトリック名                                                      | メトリックタイプ | ラベル                                                                                                                          | 説明                                                                                                                    |
| :---------------------------------------------------------- | :------- | :--------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------- |
| tidbcloud_db_queries_total                                  | カウント     | SQL_type: `Select\|Insert\|...`<br/>クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb`               | 実行されたステートメントの合計数                                                                                                      |
| tidbcloud_db_failed_queries_total                           | カウント     | タイプ: `planner:xxx\|executor:2345\|...`<br/>クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb`        | 実行エラーの総数                                                                                                              |
| tidbcloud_db_connections                                    | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb`                                                   | TiDBサーバーの現在の接続数                                                                                                       |
| tidbcloud_db_query_duration_seconds                         | ヒストグラム   | SQL_type: `Select\|Insert\|...`<br/>クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb`               | 発言の持続時間ヒストグラム                                                                                                         |
| tidbcloud_changefeed_latency                                | ゲージ      | チェンジフィードID                                                                                                                   | チェンジフィードの上流と下流間のデータ複製のレイテンシー                                                                                          |
| tidbcloud_changefeed_checkpoint_ts                          | ゲージ      | チェンジフィードID                                                                                                                   | ダウンストリームに正常に書き込まれた最大のTSO（Timestamp Oracle）を表す、変更フィードのチェックポイントタイムスタンプ                                                  |
| tidbcloud_changefeed_replica_rows                           | ゲージ      | チェンジフィードID                                                                                                                   | チェンジフィードが下流に1秒あたりに書き込む複製行の数                                                                                           |
| tidbcloud_node_storage_used_bytes                           | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>コンポーネント: `tikv\|tiflash`                   | TiKV/ TiFlashノードのディスク使用量バイト                                                                                           |
| tidbcloud_node_storage_capacity_bytes                       | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>コンポーネント: `tikv\|tiflash`                   | TiKV/ TiFlashノードのディスク容量バイト                                                                                            |
| tidbcloud_node_cpu_seconds_total                            | カウント     | クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`               | TiDB/TiKV/ TiFlashノードのCPU使用率                                                                                          |
| tidbcloud_node_cpu_capacity_cores                           | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`               | TiDB/TiKV/ TiFlashノードのCPU制限コア                                                                                         |
| tidbcloud_node_memory_used_bytes                            | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`               | TiDB/TiKV/ TiFlashノードの使用メモリバイト                                                                                        |
| tidbcloud_node_memory_capacity_bytes                        | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`               | TiDB/TiKV/ TiFlashノードのメモリ容量バイト                                                                                        |
| tidbcloud_node_storage_available_bytes                      | ゲージ      | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv\|tiflash`<br/>クラスター名: `<cluster name>`                                      | TiKV/ TiFlashノードで使用可能なディスク容量（バイト単位）                                                                                   |
| tidbcloud_disk_read_latency                                 | ヒストグラム   | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv\|tiflash`<br/>クラスター名: `<cluster name>`<br/> `device`時`nvme.*\|dm.*`         | storageデバイスあたりの読み取りレイテンシー（秒）                                                                                          |
| tidbcloud_disk_write_latency                                | ヒストグラム   | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv\|tiflash`<br/>クラスター名: `<cluster name>`<br/> `device`時`nvme.*\|dm.*`         | storageデバイスあたりの書き込みレイテンシー（秒）                                                                                          |
| tidbcloud_kv_request_duration                               | ヒストグラム   | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tikv`<br/>クラスター名: `<cluster name>`<br/> `type`時`BatchGet\|Commit\|Prewrite\|...` | タイプ別の TiKV リクエストの継続時間（秒）                                                                                              |
| tidbcloud_component_uptime                                  | ヒストグラム   | インスタンス: `tidb-0\|tidb-1\|...`<br/>コンポーネント: `tidb\|tikv\|tiflash`<br/>クラスター名: `<cluster name>`                                | TiDBコンポーネントの稼働時間（秒）                                                                                                   |
| tidbcloud_ticdc_owner_resolved_ts_lag                       | ゲージ      | チェンジフィードID: `<changefeed-id>`<br/>クラスター名: `<cluster name>`                                                                   | チェンジフィード所有者の解決されたタイムスタンプの遅延（秒）                                                                                        |
| tidbcloud_changefeed_status                                 | ゲージ      | チェンジフィードID: `<changefeed-id>`<br/>クラスター名: `<cluster name>`                                                                   | チェンジフィードステータス:<br/> `-1` ：不明<br/>`0` ：正常<br/>`1` : 警告<br/>`2` : 失敗<br/>`3` : 停止<br/>`4` ：終了<br/>`6` ：警告<br/>`7` : その他 |
| tidbcloud_resource_manager_resource_unit_read_request_unit  | ゲージ      | クラスター名: `<cluster name>`<br/>リソースグループ: `<group-name>`                                                                        | リソースマネージャによって消費される読み取り要求単位                                                                                            |
| tidbcloud_resource_manager_resource_unit_write_request_unit | ゲージ      | クラスター名: `<cluster name>`<br/>リソースグループ: `<group-name>`                                                                        | リソースマネージャによって消費される書き込み要求ユニット                                                                                          |

## FAQ {#faq}

-   同じメトリックが Grafana とTiDB Cloudコンソールで同時に異なる値になるのはなぜですか?

    GrafanaとTiDB Cloudでは集計ロジックが異なるため、表示される集計値が異なる場合があります。Grafanaの`mini step`の設定を調整することで、よりきめ細かなメトリック値を取得できます。
