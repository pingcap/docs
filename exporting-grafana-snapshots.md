---
title: Export Grafana Snapshots
summary: Learn how to export snapshots of Grafana Dashboard, and how to visualize these files.
---

> **警告：**
>
> -   TiDB v6.0.0 以降、PingCAP は MetricsTool を保守しなくなりました。 v6.1.0 以降、PingCAP は MetricsTool ドキュメントを管理しなくなりました。
> -   モニタリング メトリック データをエクスポートするには、 [PingCAPクリニック診断サービス](/clinic/clinic-introduction.md)を使用して、モニタリング メトリック、ログ、クラスター トポロジ、構成、パラメーターなど、TiDB クラスターの診断に必要な情報を取得します。

# Grafana スナップショットのエクスポート {#export-grafana-snapshots}

> **注記：**
>
> 現在、MetricsTool は Grafana v6.xx でのみ使用できます。

メトリクス データはトラブルシューティングにおいて重要です。リモート アシスタンスをリクエストすると、サポート スタッフが問題を診断するために Grafana ダッシュボードを表示する必要がある場合があります。 [メトリクスツール](https://metricstool.pingcap.net/) Grafana ダッシュボードのスナップショットをローカル ファイルとしてエクスポートし、これらのスナップショットを視覚化するのに役立ちます。これらのスナップショットを部外者と共有すると、Grafanaサーバー上の他の機密情報へのアクセスを与えることなく、部外者がグラフを正確に読み取れるようになります。

## 使用法 {#usage}

MetricsTool には[https://metricstool.pingcap.net/](https://metricstool.pingcap.net/)からアクセスできます。これは、次の 3 つのツール セットで構成されます。

-   **エクスポート**: ブラウザの開発者ツールで実行されるユーザー スクリプト。これにより、任意の Grafana v6.xxサーバー上の現在のダッシュボードに表示されているすべてのパネルのスナップショットをダウンロードできます。

    ![Screenshot of MetricsTool Exporter after running the user script](/media/metricstool-export.png)

-   **Visualize** : エクスポートされたスナップショット ファイルを視覚化する Web ページ。視覚化されたスナップショットは、ライブ Grafana ダッシュボードと同じ方法で操作できます。

    ![Screenshot of MetricsTool Visualizer](/media/metricstool-visualize.png)

-   **Import** : エクスポートされたスナップショットを実際の G​​rafana インスタンスにインポートして戻す手順。

## よくある質問 {#faqs}

### スクリーンショットや PDF 印刷と比較したこのツールの利点は何ですか? {#what-is-the-advantage-of-this-tool-compared-with-screenshot-or-pdf-printing}

MetricsTool によってエクスポートされたスナップショット ファイルには、取得時の実際の値が含まれています。また、Visualizer を使用すると、ライブ Grafana ダッシュボードであるかのようにレンダリングされたグラフを操作できるようになり、系列の切り替え、狭い時間範囲へのズーム、特定の時点での正確な値の確認などの操作がサポートされます。これにより、MetricsTool は画像や PDF よりもはるかに強力になります。

### スナップショット ファイルには何が含まれますか? {#what-are-included-in-the-snapshot-file}

スナップショット ファイルには、選択した時間範囲内のすべてのグラフとパネルの値が含まれています。データ ソースからの元のメトリックは保存されません (したがって、ビジュアライザーでクエリ式を編集することはできません)。

### Visualizer はアップロードされたスナップショット ファイルを PingCAP のサーバーに保存しますか? {#will-the-visualizer-save-the-uploaded-snapshot-files-in-pingcap-s-servers}

いいえ、ビジュアライザーはブラウザー内でスナップショット ファイルを完全に解析します。 PingCAP には何も送信されません。機密ソースから受信したスナップショット ファイルを自由に表示でき、Visualizer を通じてこれらのファイルが第三者に漏洩することを心配する必要はありません。

### すべてのメトリクスがロードされる前にスクリプトを実行すると問題が発生しますか? {#will-there-be-problems-to-execute-the-script-before-all-metrics-are-loaded}

いいえ、スクリプト UI は、すべてのメトリクスがロードされるまで待つように通知します。ただし、一部のメトリクスの読み込みが長すぎる場合は、手動で待機をスキップしてスナップショットをエクスポートできます。

### 視覚化されたスナップショットへのリンクを共有できますか? {#can-we-share-a-link-to-a-visualized-snapshot}

いいえ、ただし、ビジュアライザーを使用して表示する方法を説明したスナップショット ファイルを共有することはできます。世界中で読み取り可能な URL が本当に必要な場合は、Grafana に組み込まれている public `snapshot.raintank.io`サービスを試すこともできますが、その前にプライバシーに関する懸念がすべて解消されていることを確認してください。
