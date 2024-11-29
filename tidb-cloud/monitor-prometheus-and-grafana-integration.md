---
title: Integrate TiDB Cloud with Prometheus and Grafana (Beta)
summary: Prometheus と Grafana の統合を使用して TiDB クラスターを監視する方法を学びます。
---

# TiDB Cloud をPrometheus および Grafana と統合する (ベータ版) {#integrate-tidb-cloud-with-prometheus-and-grafana-beta}

TiDB Cloud は[プロメテウス](https://prometheus.io/) API エンドポイント (ベータ版) を提供します。Prometheus サービスをお持ちの場合は、エンドポイントからTiDB Cloudの主要なメトリクスを簡単に監視できます。

このドキュメントでは、 TiDB Cloudエンドポイントから主要なメトリックを読み取るように Prometheus サービスを構成する方法と、 [グラファナ](https://grafana.com/)使用してメトリックを表示する方法について説明します。

## 前提条件 {#prerequisites}

-   TiDB Cloud をPrometheus と統合するには、セルフホスト型またはマネージド型の Prometheus サービスが必要です。

-   TiDB Cloudのサードパーティ統合設定を編集するには、組織への`Organization Owner`アクセス権またはTiDB Cloudの対象プロジェクトへの`Project Member`アクセス権が必要です。

## 制限 {#limitation}

-   [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターでは Prometheus と Grafana の統合は使用できません。

-   クラスターのステータスが**CREATING** 、 **RESTORING** 、 **PAUSED** 、または**RESUMING**の場合、Prometheus と Grafana の統合は使用できません。

## 手順 {#steps}

### ステップ1. Prometheusのscrape_configファイルを取得する {#step-1-get-a-scrape-config-file-for-prometheus}

Prometheus サービスを設定してTiDB Cloudのメトリックを読み取る前に、まずTiDB Cloudで`scrape_config` YAML ファイルを生成する必要があります。この`scrape_config`ファイルには、Prometheus サービスが現在のプロジェクト内の任意のデータベース クラスターを監視できるようにする一意のベアラー トークンが含まれています。

Prometheus の`scrape_config`ファイルを取得するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。

2.  クリック<mdsvgicon name="icon-left-projects">左下隅で、複数のプロジェクトがある場合は対象プロジェクトに切り替えて、 **[プロジェクト設定]**をクリックします。</mdsvgicon>

3.  プロジェクトの「**プロジェクト設定」**ページで、左側のナビゲーション ペインの**「統合」**をクリックし、 **「Prometheus への統合 (ベータ版)」**をクリックします。

4.  **「ファイルの追加」**をクリックすると、現在のプロジェクトの scrape_config ファイルを生成して表示します。

5.  後で使用するために、 `scrape_config`ファイルの内容のコピーを作成します。

    > **注記：**
    >
    > セキュリティ上の理由から、 TiDB Cloud は新しく生成された`scrape_config`ファイルを 1 回だけ表示します。ファイル ウィンドウを閉じる前に、必ず内容をコピーしてください。コピーを忘れた場合は、 TiDB Cloudの`scrape_config`ファイルを削除して、新しいファイルを生成する必要があります。5 ファイルを削除するには、ファイルを選択し、 **... を**クリックしてから、**削除 を**`scrape_config`します。

### ステップ2. Prometheusとの統合 {#step-2-integrate-with-prometheus}

1.  Prometheus サービスによって指定された監視ディレクトリで、Prometheus 構成ファイルを見つけます。

    たとえば、 `/etc/prometheus/prometheus.yml` 。

2.  Prometheus 構成ファイルで、 `scrape_configs`セクションを見つけて、 TiDB Cloudから取得した`scrape_config`のファイル コンテンツをそのセクションにコピーします。

3.  Prometheus サービスで、 **[ステータス]** &gt; **[ターゲット]**をチェックして、新しい`scrape_config`ファイルが読み取られていることを確認します。読み取られていない場合は、Prometheus サービスを再起動する必要がある可能性があります。

### ステップ3. Grafana GUIダッシュボードを使用してメトリックを視覚化する {#step-3-use-grafana-gui-dashboards-to-visualize-the-metrics}

Prometheus サービスがTiDB Cloudからメトリックを読み取った後、Grafana GUI ダッシュボードを使用して、次のようにメトリックを視覚化できます。

1.  TiDB Cloud [ここ](https://github.com/pingcap/docs/blob/master/tidb-cloud/monitor-prometheus-and-grafana-integration-grafana-dashboard-UI.json)の Grafana ダッシュボード JSON をダウンロードします。
2.  メトリックを視覚化するには[このJSONを自分のGrafana GUIにインポートする](https://grafana.com/docs/grafana/v8.5/dashboards/export-import/#import-dashboard)使用します。
3.  (オプション) パネルを追加または削除したり、データ ソースを変更したり、表示オプションを変更したりして、必要に応じてダッシュボードをカスタマイズします。

Grafana の使用方法の詳細については、 [Grafana ドキュメント](https://grafana.com/docs/grafana/latest/getting-started/getting-started-prometheus/)参照してください。

## scrape_config のローテーションのベストプラクティス {#best-practice-of-rotating-scrape-config}

データのセキュリティを向上させるには、 `scrape_config`ファイル ベアラー トークンを定期的にローテーションすることが一般的なベスト プラクティスです。

1.  [ステップ1](#step-1-get-a-scrape_config-file-for-prometheus)に従って、Prometheus 用の新しい`scrape_config`ファイルを作成します。
2.  新しいファイルの内容を Prometheus 構成ファイルに追加します。
3.  Prometheus サービスがTiDB Cloudから引き続き読み取ることができることを確認したら、Prometheus 構成ファイルから古い`scrape_config`ファイルの内容を削除します。
4.  プロジェクトの**統合**ページで、対応する古い`scrape_config`ファイルを削除して、他のユーザーがそれを使用してTiDB Cloud Prometheus エンドポイントから読み取るのをブロックします。

## Prometheusで利用可能なメトリクス {#metrics-available-to-prometheus}

Prometheus は、TiDB クラスターの次のメトリック データを追跡します。

| メトリック名                                | メトリックタイプ | ラベル                                                                                                                   | 説明                                                                   |
| :------------------------------------ | :------- | :-------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------- |
| tidbcloud_db_クエリ合計                    | カウント     | SQL_type: `Select\|Insert\|...`<br/>クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb`        | 実行されたステートメントの合計数                                                     |
| tidbcloud_db_失敗したクエリの合計               | カウント     | タイプ: `planner:xxx\|executor:2345\|...`<br/>クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb` | 実行エラーの総数                                                             |
| tidbcloud_db_接続                       | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb`                                            | TiDBサーバーの現在の接続数                                                      |
| tidbcloud_db_query_duration_seconds   | ヒストグラム   | SQL_type: `Select\|Insert\|...`<br/>クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…`<br/>コンポーネント: `tidb`        | 発言の持続時間ヒストグラム                                                        |
| tidbcloud_changefeed_latency          | ゲージ      | フィードIDの変更                                                                                                             | チェンジフィードの上流と下流の間のデータ複製のレイテンシー                                        |
| tidbcloud_changefeed_checkpoint_ts    | ゲージ      | フィードIDの変更                                                                                                             | ダウンストリームに正常に書き込まれた最大のTSO（Timestamp Oracle）を表す、変更フィードのチェックポイントタイムスタンプ |
| tidbcloud_changefeed_レプリカ行            | ゲージ      | フィードIDの変更                                                                                                             | チェンジフィードが1秒あたりにダウンストリームに書き込む複製行の数                                    |
| tidbcloud_node_storage_used_bytes     | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>コンポーネント: `tikv\|tiflash`            | TiKV/ TiFlashノードのディスク使用量バイト                                          |
| tidbcloud_node_storage_capacity_bytes | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tikv-0\|tikv-1…\|tiflash-0\|tiflash-1…`<br/>コンポーネント: `tikv\|tiflash`            | TiKV/ TiFlashノードのディスク容量バイト                                           |
| tidbcloud_node_cpu_秒数_合計              | カウント     | クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`        | TiDB/TiKV/ TiFlashノードのCPU使用率                                         |
| tidbcloud_node_cpu_capacity_cores     | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`        | TiDB/TiKV/ TiFlashノードのCPU制限コア                                        |
| tidbcloud_node_memory_used_bytes      | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`        | TiDB/TiKV/ TiFlashノードの使用メモリバイト                                       |
| tidbcloud_node_memory_capacity_bytes  | ゲージ      | クラスター名: `<cluster name>`<br/>インスタンス: `tidb-0\|tidb-1…\|tikv-0…\|tiflash-0…`<br/>コンポーネント: `tidb\|tikv\|tiflash`        | TiDB/TiKV/ TiFlashノードのメモリ容量バイト                                       |

## FAQ {#faq}

-   同じメトリックが Grafana とTiDB Cloudコンソールで同時に異なる値になるのはなぜですか?

    Grafana とTiDB Cloudでは集計計算ロジックが異なるため、表示される集計値が異なる場合があります。Grafana の`mini step`構成を調整して、よりきめ細かいメトリック値を取得できます。
