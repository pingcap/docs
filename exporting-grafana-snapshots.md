---
title: Export Grafana Snapshots
summary: Learn how to export snapshots of Grafana Dashboard, and how to visualize these files.
---

> **警告：**
>
> -   TiDB v6.0.0 以降、PingCAP は MetricsTool を維持しなくなりました。 v6.1.0 以降、PingCAP は MetricsTool ドキュメントを維持しなくなりました。
> -   監視メトリック データをエクスポートするには、 [PingCAPクリニック診断サービス](/clinic/clinic-introduction.md)を使用して、監視メトリック、ログ、クラスター トポロジ、構成、パラメーターなど、TiDB クラスターの診断に必要な情報を取得します。

# Grafana スナップショットのエクスポート {#export-grafana-snapshots}

メトリクス データは、トラブルシューティングにおいて重要です。リモート アシスタンスを要求すると、サポート スタッフが Grafana ダッシュボードを表示して問題を診断することが必要になる場合があります。 [メトリクスツール](https://metricstool.pingcap.net/) Grafana ダッシュボードのスナップショットをローカル ファイルとしてエクスポートし、これらのスナップショットを視覚化するのに役立ちます。これらのスナップショットを部外者と共有し、Grafanaサーバー上の他の機密情報へのアクセスを許可することなく、部外者がグラフを正確に読み取れるようにすることができます。

## 使用法 {#usage}

MetricsTool は[https://metricstool.pingcap.net/](https://metricstool.pingcap.net/)からアクセスできます。これは、次の 3 つのツール セットで構成されています。

-   **エクスポート**: ブラウザーの開発者ツールで実行されるユーザー スクリプト。Grafana v6.xxサーバーの現在のダッシュボードに表示されているすべてのパネルのスナップショットをダウンロードできます。

    ![Screenshot of MetricsTool Exporter after running the user script](/media/metricstool-export.png)

-   **Visualize** : エクスポートされたスナップショット ファイルを視覚化する Web ページ。可視化されたスナップショットは、ライブの Grafana ダッシュボードと同じ方法で操作できます。

    ![Screenshot of MetricsTool Visualizer](/media/metricstool-visualize.png)

-   **Import** : エクスポートされたスナップショットを実際の Grafana インスタンスにインポートする手順。

## よくある質問 {#faqs}

### スクリーンショットや PDF 印刷と比較して、このツールの利点は何ですか? {#what-is-the-advantage-of-this-tool-compared-with-screenshot-or-pdf-printing}

MetricsTool によってエクスポートされたスナップショット ファイルには、取得時の実際の値が含まれています。また、ビジュアライザーを使用すると、レンダリングされたグラフをライブの Grafana ダッシュボードであるかのように操作でき、シリーズの切り替え、より短い時間範囲へのズーム、特定の時点での正確な値の確認などの操作がサポートされます。これにより、MetricsTool は画像や PDF よりもはるかに強力になります。

### スナップショット ファイルには何が含まれていますか? {#what-are-included-in-the-snapshot-file}

スナップショット ファイルには、選択した時間範囲内のすべてのグラフとパネルの値が含まれています。データ ソースからの元のメトリックは保存されません (したがって、ビジュアライザーでクエリ式を編集することはできません)。

### Visualizer は、アップロードされたスナップショット ファイルを PingCAP のサーバーに保存しますか? {#will-the-visualizer-save-the-uploaded-snapshot-files-in-pingcap-s-servers}

いいえ、ビジュアライザーはブラウザー内でスナップショット ファイルを完全に解析します。 PingCAP には何も送信されません。重要なソースから受け取ったスナップショット ファイルを自由に表示でき、これらがビジュアライザーを通じて第三者に漏洩することを心配する必要はありません。

### Grafana 以外にメトリクスをエクスポートできますか? {#can-it-export-metrics-besides-grafana}

いいえ、現時点では Grafana v6.xx のみをサポートしています。

### すべてのメトリックがロードされる前にスクリプトを実行すると問題が発生しますか? {#will-there-be-problems-to-execute-the-script-before-all-metrics-are-loaded}

いいえ、スクリプト UI は、すべてのメトリックが読み込まれるまで待機するように通知します。ただし、一部のメトリクスの読み込みに時間がかかりすぎる場合は、手動で待機をスキップしてスナップショットをエクスポートできます。

### 視覚化されたスナップショットへのリンクを共有できますか? {#can-we-share-a-link-to-a-visualized-snapshot}

いいえ。ただし、ビジュアライザーを使用して表示する方法を説明したスナップショット ファイルを共有できます。誰でも読める URL が本当に必要な場合は、Grafana に組み込まれているパブリック`snapshot.raintank.io`サービスを試すこともできますが、その前にプライバシーに関するすべての懸念が解消されていることを確認してください。
