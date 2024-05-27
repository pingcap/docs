---
title: Export Grafana Snapshots
summary: Grafana ダッシュボードのスナップショットをエクスポートする方法と、これらのファイルを視覚化する方法について学習します。
---

> **警告：**
>
> -   TiDB v6.0.0 以降、PingCAP は MetricsTool を保守しなくなりました。v6.1.0 以降、PingCAP は MetricsTool ドキュメントを保守しなくなりました。
> -   監視メトリック データをエクスポートするには、 [PingCAPクリニック診断サービス](/clinic/clinic-introduction.md)を使用して、監視メトリック、ログ、クラスター トポロジ、構成、パラメーターなど、TiDB クラスターの診断に必要な情報を取得します。

# Grafana スナップショットのエクスポート {#export-grafana-snapshots}

> **注記：**
>
> 現在、MetricsToolはGrafana v6.xxでのみ使用できます。

メトリクス データはトラブルシューティングに重要です。リモート アシスタンスをリクエストすると、サポート スタッフが Grafana ダッシュボードを表示して問題を診断する必要がある場合があります。1 [メトリクスツール](https://metricstool.pingcap.net/) Grafana ダッシュボードのスナップショットをローカル ファイルとしてエクスポートし、これらのスナップショットを視覚化するのに役立ちます。これらのスナップショットを部外者と共有して、Grafanaサーバー上の他の機密情報へのアクセス権を与えることなく、グラフを正確に読み取ることができるようにすることができます。

## 使用法 {#usage}

MetricsTool は[翻訳: 翻訳者: 渡辺 俊之](https://metricstool.pingcap.net/)からアクセスできます。これは 3 つのツール セットで構成されています。

-   **エクスポート**: ブラウザの開発者ツールで実行されるユーザー スクリプト。これにより、任意の Grafana v6.xxサーバー上の現在のダッシュボードに表示されているすべてのパネルのスナップショットをダウンロードできます。

    ![Screenshot of MetricsTool Exporter after running the user script](/media/metricstool-export.png)

-   **Visualize** : エクスポートされたスナップショット ファイルを視覚化する Web ページ。視覚化されたスナップショットは、ライブ Grafana ダッシュボードと同じように操作できます。

    ![Screenshot of MetricsTool Visualizer](/media/metricstool-visualize.png)

-   **インポート**: エクスポートされたスナップショットを実際の G​​rafana インスタンスにインポートする手順。

## よくある質問 {#faqs}

### スクリーンショットや PDF 印刷と比較して、このツールの利点は何ですか? {#what-is-the-advantage-of-this-tool-compared-with-screenshot-or-pdf-printing}

MetricsTool によってエクスポートされたスナップショット ファイルには、取得時の実際の値が含まれています。また、Visualizer を使用すると、レンダリングされたグラフをライブ Grafana ダッシュボードのように操作でき、シリーズの切り替え、より狭い時間範囲へのズーム、特定の時間における正確な値の確認などの操作がサポートされます。これにより、MetricsTool は画像や PDF よりもはるかに強力になります。

### スナップショット ファイルには何が含まれていますか? {#what-are-included-in-the-snapshot-file}

スナップショット ファイルには、選択した時間範囲のすべてのグラフとパネルの値が含まれます。データ ソースからの元のメトリックは保存されません (したがって、Visualizer でクエリ式を編集することはできません)。

### Visualizer はアップロードされたスナップショット ファイルを PingCAP のサーバーに保存しますか? {#will-the-visualizer-save-the-uploaded-snapshot-files-in-pingcap-s-servers}

いいえ、Visualizer はスナップショット ファイルをすべてブラウザ内で解析します。PingCAP には何も送信されません。機密情報源から受信したスナップショット ファイルは自由に表示できます。Visualizer を通じて第三者に漏洩する心配はありません。

### すべてのメトリックがロードされる前にスクリプトを実行すると問題が発生しますか? {#will-there-be-problems-to-execute-the-script-before-all-metrics-are-loaded}

いいえ、スクリプト UI は、すべてのメトリックがロードされるまで待機するように通知します。ただし、一部のメトリックのロードに時間がかかりすぎる場合は、手動で待機をスキップしてスナップショットをエクスポートできます。

### 視覚化されたスナップショットへのリンクを共有できますか? {#can-we-share-a-link-to-a-visualized-snapshot}

いいえ。ただし、スナップショット ファイルを共有し、Visualizer を使用して表示する方法の説明を添えることはできます。世界中で読み取り可能な URL が本当に必要な場合は、Grafana に組み込まれている public `snapshot.raintank.io`サービスを試すこともできますが、その前にプライバシーに関する懸念がすべて解消されていることを確認してください。
