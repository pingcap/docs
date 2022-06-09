---
title: TiDB Monitoring Framework Overview
summary: Use Prometheus and Grafana to build the TiDB monitoring framework.
---

# TiDBモニタリングフレームワークの概要 {#tidb-monitoring-framework-overview}

TiDB監視フレームワークは、PrometheusとGrafanaの2つのオープンソースプロジェクトを採用しています。 TiDBは、 [プロメテウス](https://prometheus.io)を使用して監視とパフォーマンスのメトリックを保存し、 [Grafana](https://grafana.com/grafana)を使用してこれらのメトリックを視覚化します。

## TiDBのプロメテウスについて {#about-prometheus-in-tidb}

時系列データベースとして、Prometheusは多次元データモデルと柔軟なクエリ言語を備えています。最も人気のあるオープンソースプロジェクトの1つとして、Prometheusは多くの企業や組織に採用されており、非常に活発なコミュニティがあります。 PingCAPは、TiDB、TiKV、およびPDでの監視とアラートのためのPrometheusの積極的な開発者および採用者の1人です。

Prometheusは複数のコンポーネントで構成されています。現在、TiDBは次のものを使用しています。

-   時系列データをスクレイプして保存するPrometheusサーバー
-   アプリケーションで必要なメトリックをカスタマイズするためのクライアントライブラリ
-   アラートメカニズムのAlertmanager

回路図は以下の通りです：

![diagram](/media/prometheus-in-tidb.png)

## TiDBのGrafanaについて {#about-grafana-in-tidb}

Grafanaは、メトリックを分析および視覚化するためのオープンソースプロジェクトです。 TiDBはGrafanaを使用して、パフォーマンスメトリックを次のように表示します。

![Grafana monitored\_groups](/media/grafana-monitored-groups.png)

-   {TiDB_Cluster_name}-バックアップと復元：バックアップと復元に関連するメトリックを監視します。
-   {TiDB_Cluster_name}-Binlog：TiDBBinlogに関連するメトリックを監視します。
-   {TiDB_Cluster_name}-Blackbox_exporter：ネットワークプローブに関連するメトリックを監視します。
-   {TiDB_Cluster_name}-ディスク-パフォーマンス：ディスクパフォーマンスに関連するメトリックを監視します。
-   {TiDB_Cluster_name}-Kafka-概要：Kafkaに関連するメトリックの監視。
-   {TiDB_Cluster_name}-Lightning：TiDBLightningに関連するメトリックを監視します。
-   {TiDB_Cluster_name}-Node_exporter：オペレーティングシステムに関連するメトリックを監視します。
-   {TiDB_Cluster_name}-概要：重要なコンポーネントに関連する監視の概要。
-   {TiDB_Cluster_name}-PD：PDサーバーに関連するメトリックを監視します。
-   {TiDB_Cluster_name}-パフォーマンス-読み取り：読み取りパフォーマンスに関連するメトリックを監視します。
-   {TiDB_Cluster_name}-パフォーマンス-書き込み：書き込みパフォーマンスに関連するメトリックを監視します。
-   {TiDB_Cluster_name}-TiDB：TiDBサーバーに関連する詳細な監視メトリック。
-   {TiDB_Cluster_name}-TiDB-概要：TiDBに関連する監視の概要。
-   {TiDB_Cluster_name}-TiFlash-Proxy-概要：データをTiFlashにレプリケートするために使用されるプロキシサーバーの概要を監視します。
-   {TiDB_Cluster_name}-TiFlash-概要：TiFlashに関連する監視の概要。
-   {TiDB_Cluster_name}-TiKV-詳細：TiKVサーバーに関連する詳細な監視メトリック。
-   {TiDB_Cluster_name}-TiKV-概要：TiKVサーバーに関連する監視の概要。
-   {TiDB_Cluster_name}-TiKV-トラブルシューティング：TiKVエラー診断に関連するメトリックを監視します。
-   {TiDB_Cluster_name}-TiCDC：TiCDCに関連する詳細な監視メトリック。

各グループには、監視メトリックの複数のパネルラベルがあり、各パネルには、複数の監視メトリックの詳細情報が含まれています。たとえば、**概要**監視グループには5つのパネルラベルがあり、各ラベルは監視パネルに対応しています。次のUIを参照してください。

![Grafana Overview](/media/grafana-monitor-overview.png)
