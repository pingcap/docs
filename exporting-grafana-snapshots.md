---
title: Export Grafana Snapshots
summary: Learn how to export snapshots of Grafana Dashboard, and how to visualize these files.
---

> **警告：**
>
> -   TiDB v6.0.0以降、PingCAPはMetricsToolを維持しなくなりました。 v6.1.0以降、PingCAPはMetricsToolドキュメントを維持しなくなりました。
> -   監視メトリックデータをエクスポートするには、 [PingCAPクリニック診断サービス](/clinic/clinic-introduction.md)を使用して、監視メトリック、ログ、クラスタトポロジ、構成、パラメーターなど、TiDBクラスタの診断に必要な情報を取得します。

# Grafanaスナップショットのエクスポート {#export-grafana-snapshots}

メトリックデータは、トラブルシューティングで重要です。リモートアシスタンスをリクエストする場合、サポートスタッフが問題を診断するためにGrafanaダッシュボードを表示する必要がある場合があります。 [MetricsTool](https://metricstool.pingcap.com/)は、Grafanaダッシュボードのスナップショットをローカルファイルとしてエクスポートし、これらのスナップショットを視覚化するのに役立ちます。これらのスナップショットを部外者と共有し、Grafanaサーバー上の他の機密情報へのアクセスを許可することなく、部外者がグラフを正確に読み取れるようにすることができます。

## 使用法 {#usage}

MetricsToolには[https://metricstool.pingcap.com/](https://metricstool.pingcap.com/)からアクセスできます。これは、次の3セットのツールで構成されています。

-   **エクスポート**：ブラウザの開発者ツールで実行されているユーザースクリプト。Grafanav6.xxサーバーの現在のダッシュボードに表示されているすべてのパネルのスナップショットをダウンロードできます。

    ![Screenshot of MetricsTool Exporter after running the user script](/media/metricstool-export.png)

-   **視覚化**：エクスポートされたスナップショットファイルを視覚化するWebページ。視覚化されたスナップショットは、ライブのGrafanaダッシュボードと同じ方法で操作できます。

    ![Screenshot of MetricsTool Visualizer](/media/metricstool-visualize.png)

-   **インポート**：エクスポートされたスナップショットを実際のGrafanaインスタンスにインポートして戻す手順。

## よくある質問 {#faqs}

### スクリーンショットやPDF印刷と比較した場合のこのツールの利点は何ですか？ {#what-is-the-advantage-of-this-tool-compared-with-screenshot-or-pdf-printing}

MetricsToolによってエクスポートされたスナップショットファイルには、取得時の実際の値が含まれています。また、ビジュアライザーを使用すると、レンダリングされたグラフをライブのGrafanaダッシュボードであるかのように操作でき、シリーズの切り替え、より狭い時間範囲へのズームイン、特定の時間の正確な値の確認などの操作をサポートします。これにより、MetricsToolは画像やPDFよりもはるかに強力になります。

### スナップショットファイルには何が含まれていますか？ {#what-are-included-in-the-snapshot-file}

スナップショットファイルには、選択した時間範囲のすべてのグラフとパネルの値が含まれています。データソースからの元のメトリックは保存されません（したがって、ビジュアライザーでクエリ式を編集することはできません）。

### ビジュアライザーはアップロードされたスナップショットファイルをPingCAPのサーバーに保存しますか？ {#will-the-visualizer-save-the-uploaded-snapshot-files-in-pingcap-s-servers}

いいえ、ビジュアライザーはスナップショットファイルを完全にブラウザー内で解析します。 PingCAPには何も送信されません。機密性の高いソースから受信したスナップショットファイルを自由に表示でき、ビジュアライザーを介してこれらがサードパーティに漏洩することを心配する必要はありません。

### Grafana以外のメトリックをエクスポートできますか？ {#can-it-export-metrics-besides-grafana}

いいえ、現時点ではGrafanav6.xxのみをサポートしています。

### すべてのメトリックがロードされる前にスクリプトを実行するのに問題はありますか？ {#will-there-be-problems-to-execute-the-script-before-all-metrics-are-loaded}

いいえ、スクリプトUIは、すべてのメトリックがロードされるのを待つように通知します。ただし、一部のメトリックのロードが長すぎる場合は、手動で待機をスキップしてスナップショットをエクスポートできます。

### 視覚化されたスナップショットへのリンクを共有できますか？ {#can-we-share-a-link-to-a-visualized-snapshot}

いいえ。ただし、スナップショットファイルを共有して、ビジュアライザーを使用して表示する方法を説明することはできます。世界中で読み取り可能なURLが本当に必要な場合は、Grafanaに組み込まれているパブリック`snapshot.raintank.io`サービスを試すこともできますが、そうする前に、プライバシーに関するすべての懸念事項がクリアされていることを確認してください。
