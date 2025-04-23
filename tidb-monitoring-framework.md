---
title: TiDB Monitoring Framework Overview
summary: Prometheus、Grafana、TiDB ダッシュボードを使用して、TiDB 監視フレームワークを構築します。
---

# TiDB 監視フレームワークの概要 {#tidb-monitoring-framework-overview}

TiDB監視フレームワークは、PrometheusとGrafanaという2つのオープンソースプロジェクトを採用しています。TiDBは、監視およびパフォーマンスメトリクスの保存に[プロメテウス](https://prometheus.io)使用し、これらのメトリクスの可視化に[グラファナ](https://grafana.com/grafana)使用します。また、TiDBは、TiDBクラスターの監視と診断のための組み込みの[TiDBダッシュボード](/dashboard/dashboard-intro.md)提供しています。

## TiDBにおけるPrometheusについて {#about-prometheus-in-tidb}

時系列データベースであるPrometheusは、多次元データモデルと柔軟なクエリ言語を備えています。最も人気のあるオープンソースプロジェクトの一つであるPrometheusは、多くの企業や組織に採用されており、非常に活発なコミュニティを擁しています。PingCAPは、TiDB、TiKV、PDにおける監視とアラート機能にPrometheusを積極的に開発・導入している企業の一つです。

Prometheusは複数のコンポーネントで構成されています。現在、TiDBは以下のコンポーネントを使用しています。

-   時系列データをスクレイピングして保存するためのPrometheusサーバー
-   アプリケーションで必要なメトリックをカスタマイズするためのクライアントライブラリ
-   アラートメカニズムのためのAlertmanager

図は次のとおりです。

![diagram](/media/prometheus-in-tidb.png)

## TiDBにおけるGrafanaについて {#about-grafana-in-tidb}

Grafanaは、メトリクスを分析および視覚化するためのオープンソースプロジェクトです。TiDBはGrafanaを使用して、次のようにパフォーマンスメトリクスを表示します。

![Grafana monitored\_groups](/media/grafana-monitored-groups.png)

-   {TiDB_Cluster_name}-Backup-Restore: バックアップと復元に関連するメトリックを監視します。
-   {TiDB_Cluster_name}- Binlog: TiDB Binlogに関連するメトリックを監視します。
-   {TiDB_Cluster_name}-Blackbox_exporter: ネットワーク プローブに関連するメトリックを監視します。
-   {TiDB_Cluster_name}-Disk-Performance: ディスク パフォーマンスに関連するメトリックを監視します。
-   {TiDB_Cluster_name}-Kafka-Overview: Kafka に関連するメトリックを監視します。
-   {TiDB_Cluster_name}-Lightning: TiDB Lightningに関連するメトリックを監視します。
-   {TiDB_Cluster_name}-Node_exporter: オペレーティング システムに関連するメトリックを監視します。
-   {TiDB_Cluster_name}-概要: 重要なコンポーネントに関連する監視の概要。
-   {TiDB_Cluster_name}-PD: PDサーバーに関連するメトリックを監視します。
-   {TiDB_Cluster_name}-Performance-Read: 読み取りパフォーマンスに関連するメトリックを監視します。
-   {TiDB_Cluster_name}-Performance-Write: 書き込みパフォーマンスに関連するメトリックを監視します。
-   {TiDB_Cluster_name}-TiDB: TiDBサーバーに関連する詳細な監視メトリック。
-   {TiDB_Cluster_name}-TiDB-Summary: TiDB に関連する監視の概要。
-   {TiDB_Cluster_name}- TiFlash -Proxy-Summary: TiFlashにデータを複製するために使用されるプロキシサーバーの監視概要。
-   {TiDB_Cluster_name}- TiFlash- 概要: TiFlashに関連する監視の概要。
-   {TiDB_Cluster_name}-TiKV-Details: TiKVサーバーに関連する詳細な監視メトリック。
-   {TiDB_Cluster_name}-TiKV-Summary: TiKVサーバーに関連する監視の概要。
-   {TiDB_Cluster_name}-TiKV-Trouble-Shooting: TiKV エラー診断に関連するメトリックを監視します。
-   {TiDB_Cluster_name}-TiCDC: TiCDC に関連する詳細な監視メトリック。
-   {TiDB_Cluster_name}-TiProxy-Summary: TiProxy に関連する監視の概要。

各グループには監視指標の複数のパネルラベルがあり、各パネルには複数の監視指標の詳細情報が表示されます。例えば、 **「概要」**監視グループには5つのパネルラベルがあり、各ラベルは1つの監視パネルに対応しています。以下のUIをご覧ください。

![Grafana Overview](/media/grafana-monitor-overview.png)

## TiDBダッシュボード {#tidb-dashboard}

TiDBダッシュボードは、TiDBクラスタの監視、診断、管理のためのWeb UIで、v4.0で導入されました。PDコンポーネントに組み込まれているため、別途導入する必要はありません。詳細については、 [TiDBダッシュボードの紹介](/dashboard/dashboard-intro.md)ご覧ください。
