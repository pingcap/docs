---
title: TiDB Monitoring FAQs
summary: TiDB モニタリングに関連する FAQ について説明します。
---

# TiDB モニタリングに関するよくある質問 {#tidb-monitoring-faqs}

このドキュメントでは、TiDB 監視に関連する FAQ をまとめています。

- Prometheus 監視フレームワークの詳細については、 [監視フレームワークの概要](/tidb-monitoring-framework.md)を参照してください。
- 監視の主な指標の詳細については、 [主要な指標](/grafana-overview-dashboard.md)を参照してください。

## 主要な指標を監視するより良い方法はありますか? {#is-there-a-better-way-of-monitoring-the-key-metrics}

TiDBの監視システムは、PrometheusとGrafanaで構成されています。Grafanaのダッシュボードから、システムリソース、クライアント接続とSQL操作、内部通信、リージョンスケジューリングなど、TiDBのさまざまな稼働メトリクスを監視できます。これらのメトリクスを活用することで、データベース管理者はシステムの稼働状況やボトルネックなどをより深く理解できます。これらのメトリクスを監視する実践的な方法として、TiDBの各コンポーネントの主要なメトリクスを以下に挙げます。一般的には、これらの共通メトリクスのみに注意を払う必要があります。詳細については、 [公式文書](/grafana-overview-dashboard.md)を参照してください。

## Prometheusの監視データはデフォルトで15日ごとに削除されます。これを2か月に設定したり、監視データを手動で削除したりすることはできますか？ {#the-prometheus-monitoring-data-is-deleted-every-15-days-by-default-could-i-set-it-to-two-months-or-delete-the-monitoring-data-manually}

はい。Prometheus が起動されているマシンで起動スクリプトを見つけ、起動パラメータを編集して Prometheus を再起動してください。

```
--storage.tsdb.retention="60d"
```

## リージョンヘルスモニター {#region-health-monitor}

TiDB 2.0では、リージョンの健全性はPDメトリック監視ページで監視されます。監視項目`Region Health`には、すべてのリージョンレプリカのステータスの統計が表示されます。`miss`はレプリカ不足、 `extra`は余分なレプリカが存在することを示します。さらに、 `Region Health`は`label`による分離レベルも示します。`level-1`は、リージョンレプリカが最初の`label`レベルで物理的に分離されていることを示します。`location label`が設定されていない場合、すべてのリージョンは`level-0`になります。

## ステートメントカウントモニターの`selectsimplefull`の意味は何ですか? {#what-is-the-meaning-of-selectsimplefull-in-statement-count-monitor}

これは完全なテーブルスキャンを意味しますが、テーブルは小さなシステムテーブルである可能性があります。

## モニターの`QPS`と`Statement OPS`の違いは何ですか? {#what-is-the-difference-between-qps-and-statement-ops-in-the-monitor}

`QPS`統計は、 `use database` 、 `load data` 、 `begin` 、 `commit` 、 `set` 、 `show` 、 `insert` 、 `select`を含むすべての SQL ステートメントに関するものです。

`Statement OPS`統計は、 `select` 、 `update` 、 `insert`を含むアプリケーション関連の SQL ステートメントのみに関するものであるため、 `Statement OPS`統計の方がアプリケーションにより適合します。
