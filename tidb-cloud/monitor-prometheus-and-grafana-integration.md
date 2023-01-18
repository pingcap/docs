---
title: Integrate TiDB Cloud with Prometheus and Grafana
summary: Learn how to monitor your TiDB cluster with the Prometheus and Grafana integration.
---

# TiDB Cloudを Prometheus および Grafana と統合する {#integrate-tidb-cloud-with-prometheus-and-grafana}

TiDB Cloudは[プロメテウス](https://prometheus.io/)の API エンドポイントを提供します。 Prometheus サービスをお持ちの場合は、エンドポイントからTiDB Cloudの主要なメトリックを簡単に監視できます。

このドキュメントでは、Prometheus サービスを構成してTiDB Cloudエンドポイントから主要なメトリクスを読み取る方法と、 [グラファナ](https://grafana.com/)を使用してメトリクスを表示する方法について説明します。

## 前提条件 {#prerequisites}

-   TiDB Cloudを Prometheus と統合するには、自己ホスト型または管理型の Prometheus サービスが必要です。

-   TiDB Cloudのサードパーティ統合設定を編集するには、組織への`Organization Owner`つのアクセス権またはTiDB Cloudのターゲット プロジェクトへの`Project Member`のアクセス権が必要です。

## 制限 {#limitation}

[Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)で Prometheus と Grafana の統合を使用することはできません。

## 手順 {#steps}

### ステップ 1. Prometheus 用の Scrape_config ファイルを取得する {#step-1-get-a-scrape-config-file-for-prometheus}

Prometheus サービスを構成してTiDB CloudでScrape_config YAML ファイルを生成する必要があります。 Scrape_config ファイルには、Prometheus サービスが現在のプロジェクト内のデータベース クラスターを監視できるようにする一意のベアラー トークンが含まれています。

Prometheus の Scrape_config ファイルを取得するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。

2.  [**クラスター**](https://tidbcloud.com/console/clusters)ページの左側のナビゲーション ペインで、次のいずれかを実行します。

    -   複数のプロジェクトがある場合は、ターゲット プロジェクトに切り替えてから、[**管理**] &gt; [<strong>統合</strong>] をクリックします。
    -   プロジェクトが 1 つしかない場合は、[**管理**] &gt; [<strong>統合</strong>] をクリックします。

3.  **Integration to Prometheus を**クリックします。

4.  [ファイルを**追加**] をクリックして、現在のプロジェクトの Scrape_config ファイルを生成して表示します。

5.  後で使用するために、scrape_config ファイルの内容のコピーを作成します。

    > **ノート：**
    >
    > セキュリティ上の理由から、 TiDB Cloudは新しく生成された Scrape_config ファイルを 1 回だけ表示します。ファイル ウィンドウを閉じる前に、必ずコンテンツをコピーしてください。そうするのを忘れた場合は、 TiDB Cloudの Scrape_config ファイルを削除して、新しいファイルを生成する必要があります。 Scrape_config ファイルを削除するには、ファイルを選択して [ **...** ] をクリックし、[<strong>削除</strong>] をクリックします。

### ステップ 2. Prometheus と統合する {#step-2-integrate-with-prometheus}

1.  Prometheus サービスで指定された監視ディレクトリで、Prometheus 構成ファイルを見つけます。

    たとえば、 `/etc/prometheus/prometheus.yml`です。

2.  Prometheus 構成ファイルで`scrape_configs`セクションを見つけ、 TiDB Cloudから取得した Scrape_config ファイルの内容をそのセクションにコピーします。

3.  Prometheus サービスで、[**ステータス**] &gt; [<strong>ターゲット</strong>] をチェックして、新しい Scrape_config ファイルが読み込まれたことを確認します。そうでない場合は、Prometheus サービスを再起動する必要がある場合があります。

### ステップ 3.Grafana GUI ダッシュボードを使用してメトリックを視覚化する {#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics}

Prometheus サービスがTiDB Cloudからメトリックを読み取った後、Grafana GUI ダッシュボードを使用して、次のようにメトリックを視覚化できます。

1.  TiDB Cloud [ここ](https://github.com/pingcap/docs/blob/release-6.1/tidb-cloud/monitor-prometheus-and-grafana-integration-grafana-dashboard-UI.json)の Grafana ダッシュボード JSON をダウンロードします。
2.  メトリクスを視覚化する場合は[この JSON を独自の Grafana GUI にインポートします](https://grafana.com/docs/grafana/v8.5/dashboards/export-import/#import-dashboard) 。
3.  (オプション) パネルを追加または削除したり、データ ソースを変更したり、表示オプションを変更したりして、必要に応じてダッシュボードをカスタマイズします。

Grafana の使用方法について詳しくは、 [グラファナのドキュメント](https://grafana.com/docs/grafana/latest/getting-started/getting-started-prometheus/)を参照してください。

## Scrape_config のローテーションのベスト プラクティス {#best-practice-of-rotating-scrape-config}

データ セキュリティを向上させるために、scrape_config ファイルのベアラー トークンを定期的にローテーションすることが一般的なベスト プラクティスです。

1.  [ステップ1](#step-1-get-a-scrape_config-file-for-prometheus)に従って、Prometheus用の新しいscrape_configファイルを作成します。
2.  新しいファイルの内容を Prometheus 構成ファイルに追加します。
3.  Prometheus サービスがまだTiDB Cloudから読み取ることができることを確認したら、Prometheus 構成ファイルから古い Scrape_config ファイルの内容を削除します。
4.  プロジェクトの**統合**ページで、対応する古い Scrape_config ファイルを削除して、他のユーザーがそのファイルを使用してTiDB Cloud Prometheus エンドポイントから読み取れないようにします。

## Prometheus で利用可能なメトリクス {#metrics-available-to-prometheus}

Prometheus は、TiDB クラスターの次のメトリック データを追跡します。

| 指標名                                   | 指標タイプ  | ラベル                                                                                                                  | 説明                              |
| :------------------------------------ | :----- | :------------------------------------------------------------------------------------------------------------------- | :------------------------------ |
| tidbcloud_db_queries_total            | カウント   | sql_type: `Select\|Insert\|...`<br/>クラスタ名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb`        | 実行されたステートメントの総数                 |
| tidbcloud_db_failed_queries_total     | カウント   | タイプ: `planner:xxx\|executor:2345\|...`<br/>クラスタ名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb` | 実行エラーの総数                        |
| tidbcloud_db_connections              | ゲージ    | クラスタ名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb`                                            | TiDBサーバーの現在の接続数                 |
| tidbcloud_db_query_duration_seconds   | ヒストグラム | sql_type: `Select\|Insert\|...`<br/>クラスタ名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb`        | ステートメントの期間ヒストグラム                |
| tidbcloud_node_storage_used_bytes     | ゲージ    | クラスタ名: `<cluster name>`<br/>インスタンス: `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>コンポーネント: `tikv\|tiflash`            | TiKV/ TiFlashノードのディスク使用量バイト     |
| tidbcloud_node_storage_capacity_bytes | ゲージ    | クラスタ名: `<cluster name>`<br/>インスタンス: `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>コンポーネント: `tikv\|tiflash`            | TiKV/ TiFlashノードのディスク容量バイト      |
| tidbcloud_node_cpu_seconds_total      | カウント   | クラスタ名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`        | TiDB/TiKV/ TiFlashノードの CPU 使用率  |
| tidbcloud_node_cpu_capacity_cores     | ゲージ    | クラスタ名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`        | TiDB/TiKV/ TiFlashノードの CPU 制限コア |
| tidbcloud_node_memory_used_bytes      | ゲージ    | クラスタ名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`        | TiDB/TiKV/ TiFlashノードの使用メモリバイト  |
| tidbcloud_node_memory_capacity_bytes  | ゲージ    | クラスタ名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`        | TiDB/TiKV/ TiFlashノードのメモリ容量バイト  |
