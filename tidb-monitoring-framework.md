---
title: TiDB Monitoring Framework Overview
summary: Prometheus と Grafana を使用して、TiDB 監視フレームワークを構築します。
---

# TiDB 監視フレームワークの概要 {#tidb-monitoring-framework-overview}

TiDB 監視フレームワークは、Prometheus と Grafana という 2 つのオープン ソース プロジェクトを採用しています。TiDB は、 [プロメテウス](https://prometheus.io)を使用して監視およびパフォーマンス メトリックを保存し、 [グラファナ](https://grafana.com/grafana)使用してこれらのメトリックを視覚化します。

## TiDB の Prometheus について {#about-prometheus-in-tidb}

時系列データベースである Prometheus には、多次元データ モデルと柔軟なクエリ言語があります。最も人気のあるオープン ソース プロジェクトの 1 つである Prometheus は、多くの企業や組織に採用されており、非常に活発なコミュニティがあります。PingCAP は、TiDB、TiKV、PD での監視とアラートに Prometheus を積極的に開発および採用している企業の 1 つです。

Prometheus は複数のコンポーネントで構成されています。現在、TiDB では以下のコンポーネントが使用されています。

-   時系列データをスクレイピングして保存するPrometheusサーバー
-   アプリケーションで必要なメトリックをカスタマイズするためのクライアントライブラリ
-   アラートメカニズム用のAlertmanager

回路図は以下の通りです：

![diagram](/media/prometheus-in-tidb.png)

## TiDB の Grafana について {#about-grafana-in-tidb}

Grafana は、メトリックを分析および視覚化するためのオープンソース プロジェクトです。TiDB は Grafana を使用して、次のようにパフォーマンス メトリックを表示します。

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

各グループには監視メトリックの複数のパネル ラベルがあり、各パネルには複数の監視メトリックの詳細情報が含まれています。たとえば、**概要**監視グループには 5 つのパネル ラベルがあり、各ラベルは監視パネルに対応しています。次の UI を参照してください。

![Grafana Overview](/media/grafana-monitor-overview.png)
