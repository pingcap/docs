---
title: TiDB Monitoring API Overview
summary: TiDB 監視サービスの API を学習します。
---

# TiDB モニタリング API の概要 {#tidb-monitoring-api-overview}

TiDB モニタリングフレームワークは、 [Prometheus](https://prometheus.io)と[Grafana](https://grafana.com/grafana)という2つのオープンソースプロジェクトを使用しています。TiDB は、監視およびパフォーマンスメトリクスの保存に Prometheus を使用し、これらのメトリクスの可視化には Grafana を使用しています。また、TiDB は TiDB クラスターの監視と診断用に組み込みの[TiDB Dashboard](/dashboard/dashboard-intro.md)を提供しています。

次のインターフェースを使用して、TiDB クラスターのステータスを監視できます。

-   [ステータスインターフェース](/tidb-monitoring-api.md#use-the-status-interface) : 現在の TiDBサーバーの[実行ステータス](/tidb-monitoring-api.md#running-status)とテーブルの[ストレージ情報](/tidb-monitoring-api.md#storage-information)を監視します。
-   [メトリクスインターフェース](/tidb-monitoring-api.md#use-the-metrics-interface) : コンポーネント内のさまざまな操作に関する詳細情報を取得し、Grafana を使用してこれらのメトリックを表示します。

リクエストパラメータ、レスポンス例、使用方法など、各 API の詳細については、 [TiDB モニタリング API](/tidb-monitoring-api.md)を参照してください。
