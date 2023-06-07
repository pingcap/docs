---
title: Integrate TiDB Cloud with Prometheus and Grafana
summary: Learn how to monitor your TiDB cluster with the Prometheus and Grafana integration.
---

# TiDB CloudをPrometheus および Grafana と統合する {#integrate-tidb-cloud-with-prometheus-and-grafana}

TiDB Cloud は[<a href="https://prometheus.io/">プロメテウス</a>](https://prometheus.io/) API エンドポイントを提供します。 Prometheus サービスをお持ちの場合は、 TiDB Cloudの主要なメトリクスをエンドポイントから簡単に監視できます。

このドキュメントでは、 TiDB Cloudエンドポイントから主要なメトリクスを読み取るように Prometheus サービスを構成する方法と、 [<a href="https://grafana.com/">グラファナ</a>](https://grafana.com/)使用してメトリクスを表示する方法について説明します。

## 前提条件 {#prerequisites}

-   TiDB Cloudを Prometheus と統合するには、セルフホスト型またはマネージド型の Prometheus サービスが必要です。

-   TiDB Cloudのサードパーティ統合設定を編集するには、組織への`Organization Owner`アクセス権、またはTiDB Cloudのターゲット プロジェクトへの`Project Member`アクセス権が必要です。

## 制限 {#limitation}

-   [<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">TiDB サーバーレス</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターでは Prometheus と Grafana の統合を使用できません。

-   Prometheus と Grafana の統合は、クラスターのステータスが**CREATING** 、 **RESTORING** 、 **PAused** 、または**RESUMING**の場合は使用できません。

## ステップ {#steps}

### ステップ1. Prometheusのscrape_configファイルを取得する {#step-1-get-a-scrape-config-file-for-prometheus}

TiDB Cloudのメトリクスを読み取るように Prometheus サービスを構成する前に、まずTiDB Cloudでscrape_config YAML ファイルを生成する必要があります。 scrape_config ファイルには、Prometheus サービスが現在のプロジェクト内のデータベース クラスターを監視できるようにする一意のベアラー トークンが含まれています。

Prometheus のscrape_config ファイルを取得するには、次の手順を実行します。

1.  [<a href="https://tidbcloud.com">TiDB Cloudコンソール</a>](https://tidbcloud.com)にログインします。

2.  [<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページの左側のナビゲーション ウィンドウで、次のいずれかを実行します。

    -   複数のプロジェクトがある場合は、ターゲット プロジェクトに切り替えて、 **[管理]** &gt; **[統合]**をクリックします。
    -   プロジェクトが 1 つだけの場合は、 **[管理]** &gt; **[統合]**をクリックします。

3.  **「Prometheus への統合」を**クリックします。

4.  **「ファイルの追加」**をクリックして、現在のプロジェクトのscrape_configファイルを生成して表示します。

5.  後で使用できるように、scrape_config ファイルの内容のコピーを作成します。

    > **ノート：**
    >
    > セキュリティ上の理由から、 TiDB Cloudは新しく生成されたscrape_config ファイルを 1 回だけ表示します。ファイル ウィンドウを閉じる前に、必ず内容をコピーしてください。これを忘れた場合は、 TiDB Cloudのscrape_config ファイルを削除し、新しいファイルを生成する必要があります。 Scrape_config ファイルを削除するには、ファイルを選択して**[...]**をクリックし、 **[削除]**をクリックします。

### ステップ 2. Prometheus との統合 {#step-2-integrate-with-prometheus}

1.  Prometheus サービスによって指定された監視ディレクトリで、Prometheus 構成ファイルを見つけます。

    たとえば、 `/etc/prometheus/prometheus.yml` 。

2.  Prometheus 構成ファイルで`scrape_configs`セクションを見つけ、 TiDB Cloudから取得したscrape_config ファイルの内容をそのセクションにコピーします。

3.  Prometheus サービスで、 **[ステータス]** &gt; **[ターゲット]**をチェックして、新しいscrape_config ファイルが読み取られていることを確認します。そうでない場合は、Prometheus サービスを再起動する必要がある場合があります。

### ステップ 3. Grafana GUI ダッシュボードを使用してメトリクスを視覚化する {#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics}

Prometheus サービスがTiDB Cloudからメトリクスを読み取った後、次のように Grafana GUI ダッシュボードを使用してメトリクスを視覚化できます。

1.  TiDB Cloud [<a href="https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-grafana-dashboard-UI.json">ここ</a>](https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-grafana-dashboard-UI.json)の Grafana ダッシュボード JSON をダウンロードします。
2.  [<a href="https://grafana.com/docs/grafana/v8.5/dashboards/export-import/#import-dashboard">この JSON を独自の Grafana GUI にインポートします</a>](https://grafana.com/docs/grafana/v8.5/dashboards/export-import/#import-dashboard)を指定すると、メトリクスが視覚化されます。
3.  (オプション) パネルの追加または削除、データ ソースの変更、表示オプションの変更により、必要に応じてダッシュボードをカスタマイズします。

Grafana の使用方法の詳細については、 [<a href="https://grafana.com/docs/grafana/latest/getting-started/getting-started-prometheus/">Grafana のドキュメント</a>](https://grafana.com/docs/grafana/latest/getting-started/getting-started-prometheus/)を参照してください。

## Scrape_config をローテーションするベスト プラクティス {#best-practice-of-rotating-scrape-config}

データのセキュリティを向上させるには、scrape_config ファイルのベアラー トークンを定期的にローテーションすることが一般的なベスト プラクティスです。

1.  [<a href="#step-1-get-a-scrape_config-file-for-prometheus">ステップ1</a>](#step-1-get-a-scrape_config-file-for-prometheus)に従って、Prometheus用の新しいscrape_configファイルを作成します。
2.  新しいファイルの内容を Prometheus 構成ファイルに追加します。
3.  Prometheus サービスがまだTiDB Cloudから読み取ることができることを確認したら、古いscrape_config ファイルの内容を Prometheus 構成ファイルから削除します。
4.  プロジェクトの**「統合」**ページで、対応する古いscrape_config ファイルを削除して、他のユーザーがこのファイルを使用してTiDB Cloud Prometheus エンドポイントから読み取ることをブロックします。

## Prometheus で利用可能なメトリクス {#metrics-available-to-prometheus}

Prometheus は、TiDB クラスターの次のメトリック データを追跡します。

| メトリクス名                                | メトリックタイプ | ラベル                                                                                                                   | 説明                                         |
| :------------------------------------ | :------- | :-------------------------------------------------------------------------------------------------------------------- | :----------------------------------------- |
| tidbcloud_db_queries_total            | カウント     | SQL_type: `Select\|Insert\|...`<br/>クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb`        | 実行されたステートメントの総数                            |
| tidbcloud_db_failed_queries_total     | カウント     | タイプ: `planner:xxx\|executor:2345\|...`<br/>クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb` | 実行エラーの合計数                                  |
| tidbcloud_db_connections              | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb`                                            | TiDBサーバーの現在の接続数                            |
| tidbcloud_db_query_duration_秒         | ヒストグラム   | SQL_type: `Select\|Insert\|...`<br/>クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb`        | ステートメントの長さのヒストグラム                          |
| tidbcloud_changefeed_latency          | ゲージ      | フィードIDの変更                                                                                                             | 変更フィードの上流と下流の間のデータ レプリケーションのレイテンシー         |
| tidbcloud_changefeed_replica_rows     | ゲージ      | フィードIDの変更                                                                                                             | チェンジフィードが 1 秒あたりにダウンストリームに書き込むレプリケートされた行の数 |
| tidbcloud_node_storage_used_bytes     | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>コンポーネント: `tikv\|tiflash`            | TiKV/ TiFlashノードのディスク使用量バイト                |
| tidbcloud_node_storage_capacity_bytes | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>コンポーネント: `tikv\|tiflash`            | TiKV/ TiFlashノードのディスク容量バイト                 |
| tidbcloud_node_cpu_seconds_total      | カウント     | クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`        | TiDB/TiKV/ TiFlashノードの CPU 使用率             |
| tidbcloud_node_cpu_capacity_cores     | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`        | TiDB/TiKV/ TiFlashノードの CPU 制限コア            |
| tidbcloud_node_memory_used_bytes      | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`        | TiDB/TiKV/ TiFlashノードの使用メモリバイト             |
| tidbcloud_node_memory_capacity_bytes  | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`        | TiDB/TiKV/ TiFlashノードのメモリ容量バイト             |

## FAQ {#faq}

-   Grafana とTiDB Cloudコンソールで同じメトリクスが同時に異なる値を持つのはなぜですか?

    Grafana とTiDB Cloudでは集計計算ロジックが異なるため、表示される集計値が異なる場合があります。 Grafana で`mini step`構成を調整して、より詳細なメトリック値を取得できます。
