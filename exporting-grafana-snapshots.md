---
title: Export Grafana Snapshots
summary: Grafana ダッシュボードのスナップショットをエクスポートする方法と、これらのファイルを視覚化する方法を学びます。
---

> **警告：**
>
> -   TiDB v6.0.0以降、PingCAPはMetricsToolのメンテナンスを終了しました。v6.1.0以降、PingCAPはMetricsToolドキュメントのメンテナンスを終了しました。
> -   監視メトリック データをエクスポートするには、 [PingCAPクリニック診断サービス](/clinic/clinic-introduction.md)使用して、監視メトリック、ログ、クラスター トポロジ、構成、パラメーターなど、TiDB クラスターの診断に必要な情報を取得します。

# Grafanaスナップショットのエクスポート {#export-grafana-snapshots}

> **注記：**
>
> 現在、MetricsToolはGrafana v6.xxでのみ使用できます。

メトリクスデータはトラブルシューティングにおいて重要です。リモートアシスタンスを依頼した場合、サポートスタッフが問題を診断するためにGrafanaダッシュボードを確認する必要がある場合があります。1 [メトリクスツール](https://metricstool.pingcap.net/) 、Grafanaダッシュボードのスナップショットをローカルファイルとしてエクスポートし、可視化するのに役立ちます。これらのスナップショットを外部の担当者と共有することで、Grafanaサーバー上の他の機密情報へのアクセスを外部に漏らすことなく、グラフを正確に読み取ることができます。

## 使用法 {#usage}

MetricsToolは[https://metricstool.pingcap.net/](https://metricstool.pingcap.net/)からアクセスできます。MetricsToolは3つのツールセットで構成されています。

-   **エクスポート**: ブラウザの開発者ツールで実行されるユーザー スクリプト。これにより、任意の Grafana v6.xxサーバー上の現在のダッシュボードに表示されているすべてのパネルのスナップショットをダウンロードできます。

    ![Screenshot of MetricsTool Exporter after running the user script](/media/metricstool-export.png)

-   **Visualize** : エクスポートされたスナップショットファイルを視覚化するWebページ。視覚化されたスナップショットは、ライブGrafanaダッシュボードと同じように操作できます。

    ![Screenshot of MetricsTool Visualizer](/media/metricstool-visualize.png)

-   **インポート**: エクスポートされたスナップショットを実際の Grafana インスタンスにインポートする手順。

## よくある質問 {#faqs}

### スクリーンショットや PDF 印刷と比べて、このツールの利点は何ですか? {#what-is-the-advantage-of-this-tool-compared-with-screenshot-or-pdf-printing}

MetricsToolによってエクスポートされるスナップショットファイルには、取得時の実際の値が含まれています。また、Visualizerを使用すると、レンダリングされたグラフをライブGrafanaダッシュボードのように操作でき、シリーズの切り替え、より狭い時間範囲へのズームイン、特定の時点の正確な値の確認などの操作が可能です。これにより、MetricsToolは画像やPDFよりもはるかに強力になります。

### スナップショット ファイルには何が含まれていますか? {#what-are-included-in-the-snapshot-file}

スナップショットファイルには、選択した時間範囲におけるすべてのグラフとパネルの値が含まれます。データソースの元のメトリックは保存されません（そのため、ビジュアライザーでクエリ式を編集することはできません）。

### Visualizer はアップロードされたスナップショット ファイルを PingCAP のサーバーに保存しますか? {#will-the-visualizer-save-the-uploaded-snapshot-files-in-pingcap-s-servers}

いいえ、Visualizerはスナップショットファイルをすべてブラウザ内で解析します。PingCAPには何も送信されません。機密性の高いソースから受信したスナップショットファイルは自由に閲覧でき、Visualizerを通じて第三者に漏洩する心配はありません。

### すべてのメトリックがロードされる前にスクリプトを実行すると問題が発生しますか? {#will-there-be-problems-to-execute-the-script-before-all-metrics-are-loaded}

いいえ、スクリプトUIはすべてのメトリックが読み込まれるまで待つように通知します。ただし、一部のメトリックの読み込みに時間がかかりすぎる場合は、手動で待機をスキップしてスナップショットをエクスポートできます。

### 視覚化されたスナップショットへのリンクを共有できますか? {#can-we-share-a-link-to-a-visualized-snapshot}

いいえ、ただしスナップショットファイルを共有し、Visualizer での表示方法の説明を添えることは可能です。誰でも閲覧可能な URL が必要な場合は、Grafana に組み込まれている public `snapshot.raintank.io`サービスもお試しください。ただし、使用する前にプライバシーに関する懸念事項をすべてクリアしていることをご確認ください。
