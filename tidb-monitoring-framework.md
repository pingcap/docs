---
title: TiDB Monitoring Framework Overview
summary: Use Prometheus and Grafana to build the TiDB monitoring framework.
---

# TiDB モニタリング フレームワークの概要 {#tidb-monitoring-framework-overview}

TiDB モニタリング フレームワークは、Prometheus と Grafana という 2 つのオープン ソース プロジェクトを採用しています。 TiDB は、モニタリングとパフォーマンスのメトリクスを保存するために[プロメテウス](https://prometheus.io)を使用し、これらのメトリクスを視覚化するために[グラファナ](https://grafana.com/grafana)使用します。

## TiDB のプロメテウスについて {#about-prometheus-in-tidb}

時系列データベースとして、Prometheus は多次元データ モデルと柔軟なクエリ言語を備えています。 Prometheus は最も人気のあるオープンソース プロジェクトの 1 つとして、多くの企業や組織に採用されており、非常に活発なコミュニティがあります。 PingCAP は、TiDB、TiKV、PD の監視とアラートを目的とした Prometheus の積極的な開発者および採用者の 1 つです。

Prometheus は複数のコンポーネントで構成されています。現在、TiDB では次のものが使用されています。

-   時系列データを収集して保存するための Prometheus サーバー
-   アプリケーションで必要なメトリクスをカスタマイズするためのクライアント ライブラリ
-   アラート メカニズムの Alertmanager

回路図は以下の通りです：

![diagram](/media/prometheus-in-tidb.png)

## TiDB の Grafana について {#about-grafana-in-tidb}

Grafana は、メトリクスを分析および視覚化するためのオープンソース プロジェクトです。 TiDB は Grafana を使用して、次のようにパフォーマンス メトリックを表示します。

![Grafana monitored\_groups](/media/grafana-monitored-groups.png)

-   {TiDB_Cluster_name}-Backup-Restore: バックアップと復元に関連するモニタリング メトリック。
-   {TiDB_Cluster_name}- Binlog: TiDB Binlogに関連するモニタリング メトリック。
-   {TiDB_Cluster_name}-Blackbox_exporter: ネットワーク プローブに関連するモニタリング メトリック。
-   {TiDB_Cluster_name}-Disk-Performance: ディスク パフォーマンスに関連するモニタリング メトリック。
-   {TiDB_Cluster_name}-Kafka-Overview: Kafka に関連するモニタリング メトリック。
-   {TiDB_Cluster_name}-Lightning: TiDB Lightningに関連するモニタリング指標。
-   {TiDB_Cluster_name}-Node_exporter: オペレーティング システムに関連するモニタリング メトリック。
-   {TiDB_Cluster_name}-概要: 重要なコンポーネントに関連するモニタリングの概要。
-   {TiDB_Cluster_name}-PD: PDサーバーに関連するモニタリング メトリック。
-   {TiDB_Cluster_name}-Performance-Read: 読み取りパフォーマンスに関連するモニタリング指標。
-   {TiDB_Cluster_name}-Performance-Write: 書き込みパフォーマンスに関連するモニタリング指標。
-   {TiDB_Cluster_name}-TiDB: TiDBサーバーに関連する詳細な監視メトリクス。
-   {TiDB_Cluster_name}-TiDB-summary: TiDB に関連するモニタリングの概要。
-   {TiDB_Cluster_name}- TiFlash -Proxy-summary: データをTiFlashに複製するために使用されるプロキシサーバーのモニタリングの概要。
-   {TiDB_Cluster_name}- TiFlash- Summary: TiFlashに関連するモニタリングの概要。
-   {TiDB_Cluster_name}-TiKV-Details: TiKVサーバーに関連する詳細な監視メトリクス。
-   {TiDB_Cluster_name}-TiKV-summary: TiKVサーバーに関連するモニタリングの概要。
-   {TiDB_Cluster_name}-TiKV-Trouble-Shooting: TiKV エラー診断に関連するモニタリング メトリック。
-   {TiDB_Cluster_name}-TiCDC: TiCDC に関連する詳細なモニタリング メトリック。

各グループには監視メトリックの複数のパネル ラベルがあり、各パネルには複数の監視メトリックの詳細情報が含まれています。たとえば、**概要**監視グループには 5 つのパネル ラベルがあり、各ラベルは監視パネルに対応します。次の UI を参照してください。

![Grafana Overview](/media/grafana-monitor-overview.png)
