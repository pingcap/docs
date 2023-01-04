---
title: TiDB Monitoring Framework Overview
summary: Use Prometheus and Grafana to build the TiDB monitoring framework.
---

# TiDB 監視フレームワークの概要 {#tidb-monitoring-framework-overview}

TiDB 監視フレームワークは、Prometheus と Grafana の 2 つのオープン ソース プロジェクトを採用しています。 TiDB は[プロメテウス](https://prometheus.io)を使用して監視およびパフォーマンス メトリックを格納し、 [グラファナ](https://grafana.com/grafana)を使用してこれらのメトリックを視覚化します。

## TiDB のプロメテウスについて {#about-prometheus-in-tidb}

時系列データベースである Prometheus には、多次元データ モデルと柔軟なクエリ言語があります。最も人気のあるオープン ソース プロジェクトの 1 つとして、Prometheus は多くの企業や組織に採用されており、非常に活発なコミュニティがあります。 PingCAP は、TiDB、TiKV、および PD での監視とアラートのための Prometheus のアクティブな開発者および採用者の 1 つです。

Prometheus は複数のコンポーネントで構成されています。現在、TiDB は次のものを使用しています。

-   時系列データをスクレイピングして保存するための Prometheus サーバー
-   アプリケーションで必要な指標をカスタマイズするためのクライアント ライブラリ
-   アラート メカニズムの Alertmanager

回路図は以下の通りです：

![diagram](/media/prometheus-in-tidb.png)

## TiDB の Grafana について {#about-grafana-in-tidb}

Grafana は、メトリクスを分析および視覚化するためのオープン ソース プロジェクトです。 TiDB は Grafana を使用して、次のようにパフォーマンス メトリックを表示します。

![Grafana monitored\_groups](/media/grafana-monitored-groups.png)

-   {TiDB_Cluster_name}-Backup-Restore: バックアップと復元に関連するメトリックを監視します。
-   {TiDB_Cluster_name}- Binlog: TiDB Binlogに関連するモニタリング メトリック。
-   {TiDB_Cluster_name}-Blackbox_exporter: ネットワーク プローブに関連するモニタリング メトリック。
-   {TiDB_Cluster_name}-Disk-Performance: ディスクのパフォーマンスに関連するメトリックを監視します。
-   {TiDB_Cluster_name}-Kafka-Overview: Kafka に関連するモニタリング メトリック。
-   {TiDB_Cluster_name}-Lightning: TiDB Lightningに関連するモニタリング メトリック。
-   {TiDB_Cluster_name}-Node_exporter: オペレーティング システムに関連するモニタリング メトリック。
-   {TiDB_Cluster_name}-概要: 重要なコンポーネントに関連する監視の概要。
-   {TiDB_Cluster_name}-PD: PDサーバーに関連するモニタリング メトリック。
-   {TiDB_Cluster_name}-Performance-Read: 読み取りパフォーマンスに関連するメトリックを監視します。
-   {TiDB_Cluster_name}-Performance-Write: 書き込みパフォーマンスに関連するモニタリング メトリック。
-   {TiDB_Cluster_name}-TiDB: TiDBサーバーに関連する詳細な監視メトリック。
-   {TiDB_Cluster_name}-TiDB-Summary: TiDB に関連する監視の概要。
-   {TiDB_Cluster_name}- TiFlash -Proxy-Summary: データをTiFlashに複製するために使用されるプロキシサーバーの監視の概要。
-   {TiDB_Cluster_name}- TiFlash-Summary: TiFlashに関連する監視の概要。
-   {TiDB_Cluster_name}-TiKV-Details: TiKVサーバーに関連する詳細な監視メトリック。
-   {TiDB_Cluster_name}-TiKV-Summary: TiKVサーバーに関連する監視の概要。
-   {TiDB_Cluster_name}-TiKV-Trouble-Shooting: TiKV エラー診断に関連するモニタリング メトリック。
-   {TiDB_Cluster_name}-TiCDC: TiCDC に関連する詳細な監視メトリック。

各グループにはモニタリング メトリックの複数のパネル ラベルがあり、各パネルには複数のモニタリング メトリックの詳細情報が含まれています。たとえば、**概要**監視グループには 5 つのパネル ラベルがあり、各ラベルは監視パネルに対応します。次の UI を参照してください。

![Grafana Overview](/media/grafana-monitor-overview.png)
