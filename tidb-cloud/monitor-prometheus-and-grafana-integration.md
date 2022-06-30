---
title: Prometheus and Grafana Integration (Third-Party Monitoring Service)
summary: Learn how to monitor your TiDB cluster with the Prometheus and Grafana integration.
---

# PrometheusとGrafanaの統合 {#prometheus-and-grafana-integration}

TiDB Cloudは[プロメテウス](https://prometheus.io/)のAPIエンドポイントを提供します。 Prometheusサービスを使用している場合は、エンドポイントからTiDB Cloudの主要なメトリックを簡単に監視できます。

このドキュメントでは、 TiDB Cloudエンドポイントから主要なメトリックを読み取るようにPrometheusサービスを構成する方法と、 [Grafana](https://grafana.com/)を使用してメトリックを表示する方法について説明します。

## 前提条件 {#prerequisites}

-   TiDB CloudをPrometheusと統合するには、自己ホスト型または管理型のPrometheusサービスが必要です。

-   TiDB Cloudのサードパーティ統合設定を編集するには、組織への`Organization Owner`つのアクセス、またはTiDB Cloudのターゲットプロジェクトへの`Project Member`のアクセスが必要です。

## 制限 {#limitation}

PrometheusとGrafanaの統合を[開発者層](/tidb-cloud/select-cluster-tier.md#developer-tier)で使用することはできません。

## 手順 {#steps}

### 手順1.Prometheusのscrape_configファイルを取得します {#step-1-get-a-scrape-config-file-for-prometheus}

TiDB Cloudのメトリックを読み取るようにPrometheusサービスを構成する前に、まずTiDBCloudでTiDB Cloudファイルを生成する必要があります。 scare_configファイルには、Prometheusサービスが現在のプロジェクトのデータベースクラスターを監視できるようにする一意のベアラートークンが含まれています。

Prometheusのscrape_configファイルを取得するには、次の手順を実行します。

1.  TiDB Cloudコンソールで、Prometheus統合のターゲットプロジェクトを選択し、[**プロジェクト設定**]タブをクリックします。

2.  左側のペインで、[**統合**]をクリックします。

3.  **Prometheusへの統合を**クリックします。

4.  [ファイルの**追加**]をクリックして、現在のプロジェクトのscrape_configファイルを生成して表示します。

5.  後で使用するために、scrape_configファイルの内容のコピーを作成します。

    > **ノート：**
    >
    > セキュリティ上の理由から、 TiDB Cloudは新しく生成されたscrap_configファイルを1回だけ表示します。ファイルウィンドウを閉じる前に、必ずコンテンツをコピーしてください。そうするのを忘れた場合は、 TiDB Cloudのscrape_configファイルを削除して、新しいファイルを生成する必要があります。 scare_configファイルを削除するには、ファイルを選択し、[ **...** ]をクリックして、[<strong>削除</strong>]をクリックします。

### ステップ2.Prometheusと統合する {#step-2-integrate-with-prometheus}

1.  Prometheusサービスによって指定された監視ディレクトリで、Prometheus構成ファイルを見つけます。

    たとえば、 `/etc/prometheus/prometheus.yml` 。

2.  Prometheus構成ファイルで`scrape_configs`セクションを見つけ、 TiDB Cloudから取得したscrape_configファイルの内容をそのセクションにコピーします。

3.  Prometheusサービスで、[**ステータス**]&gt; [<strong>ターゲット</strong>]をチェックして、新しいscrap_configファイルが読み取られたことを確認します。そうでない場合は、Prometheusサービスを再起動する必要があります。

### ステップ3.GrafanaGUIダッシュボードを使用してメトリックを視覚化する {#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics}

PrometheusサービスがTiDB Cloudからメトリックを読み取った後、GrafanaGUIダッシュボードを使用してメトリックを視覚化できます。

Grafanaの使用方法の詳細については、 [Grafanaのドキュメント](https://grafana.com/docs/grafana/latest/getting-started/getting-started-prometheus/)を参照してください。

## 回転するscrap_configのベストプラクティス {#best-practice-of-rotating-scrape-config}

データのセキュリティを向上させるには、scrap_configファイルベアラートークンを定期的にローテーションするのが一般的なベストプラクティスです。

1.  [ステップ1](#step-1-get-a-scrape_config-file-for-prometheus)に従って、Prometheusの新しいscrap_configファイルを作成します。
2.  新しいファイルの内容をPrometheus構成ファイルに追加します。
3.  Prometheusサービスが引き続きTiDB Cloudから読み取ることができることを確認したら、Prometheus構成ファイルから古いscrap_configファイルの内容を削除します。
4.  プロジェクトの[**統合**]ページで、対応する古いscrap_configファイルを削除して、他のユーザーがそのファイルを使用してTiDB Cloudエンドポイントから読み取るのをブロックします。

## Prometheusで利用可能なメトリック {#metrics-available-to-prometheus}

Prometheusは、TiDBクラスターの次のメトリックデータを追跡します。

| メトリック名                                | メトリックタイプ | ラベル                                                                                                                          | 説明                                              |
| :------------------------------------ | :------- | :--------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------- |
| tidbcloud_db_queries_total            | カウント     | sql_type： `Select\|Insert\|...`<br/> cluster_name： `<cluster name>`<br/>インスタンス： `tidb-0\|tidb-1…`<br/>コンポーネント： `tidb`        | 実行されたステートメントの総数                                 |
| tidbcloud_db_failed_queries_total     | カウント     | タイプ： `planner:xxx\|executor:2345\|...`<br/> cluster_name： `<cluster name>`<br/>インスタンス： `tidb-0\|tidb-1…`<br/>コンポーネント： `tidb` | 実行エラーの総数                                        |
| tidbcloud_db_connections              | ゲージ      | cluster_name： `<cluster name>`<br/>インスタンス： `tidb-0\|tidb-1…`<br/>コンポーネント： `tidb`                                             | TiDBサーバーの現在の接続数                                 |
| tidbcloud_db_query_duration_seconds   | ヒストグラム   | sql_type： `Select\|Insert\|...`<br/> cluster_name： `<cluster name>`<br/>インスタンス： `tidb-0\|tidb-1…`<br/>コンポーネント： `tidb`        | ステートメントの期間ヒストグラム                                |
| tidbcloud_node_storage_used_bytes     | ゲージ      | cluster_name： `<cluster name>`<br/>インスタンス： `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>コンポーネント： `tikv\|tiflash`             | TiKV/TiFlash<sup>ベータ</sup>ノードのディスク使用量バイト        |
| tidbcloud_node_storage_capacity_bytes | ゲージ      | cluster_name： `<cluster name>`<br/>インスタンス： `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>コンポーネント： `tikv\|tiflash`             | TiKV/TiFlash<sup>ベータ</sup>ノードのディスク容量バイト         |
| tidbcloud_node_cpu_seconds_total      | カウント     | cluster_name： `<cluster name>`<br/>インスタンス： `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント： `tidb\|tikv\|tiflash`         | TiDB / TiKV/TiFlash<sup>ベータ</sup>ノードのCPU使用率     |
| tidbcloud_node_cpu_capacity_cores     | ゲージ      | cluster_name： `<cluster name>`<br/>インスタンス： `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント： `tidb\|tikv\|tiflash`         | TiDB / TiKV/TiFlash<sup>ベータ</sup>ノードのCPU制限コア    |
| tidbcloud_node_memory_used_bytes      | ゲージ      | cluster_name： `<cluster name>`<br/>インスタンス： `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント： `tidb\|tikv\|tiflash`         | TiDB / TiKV/TiFlash<sup>ベータ</sup>ノードの使用済みメモリバイト |
| tidbcloud_node_memory_capacity_bytes  | ゲージ      | cluster_name： `<cluster name>`<br/>インスタンス： `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント： `tidb\|tikv\|tiflash`         | TiDB / TiKV/TiFlash<sup>ベータ</sup>ノードのメモリ容量バイト   |
