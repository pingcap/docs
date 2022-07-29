---
title: Monitoring FAQs
summary: Learn about the FAQs related to TiDB Monitoring.
---

# モニタリングに関するFAQ {#monitoring-faqs}

このドキュメントは、TiDBモニタリングに関連するFAQをまとめたものです。

-   Prometheusモニタリングフレームワークの詳細については、 [モニタリングフレームワークの概要](/tidb-monitoring-framework.md)を参照してください。
-   モニタリングの主要な指標の詳細については、 [主要な指標](/grafana-overview-dashboard.md)を参照してください。

## 主要な指標を監視するためのより良い方法はありますか？ {#is-there-a-better-way-of-monitoring-the-key-metrics}

TiDBの監視システムは、PrometheusとGrafanaで構成されています。 Grafanaのダッシュボードから、システムリソース、クライアント接続とSQL操作、内部通信、リージョンスケジューリングの監視メトリックを含む、TiDBのさまざまな実行メトリックを監視できます。これらのメトリックを使用すると、データベース管理者は、システムの実行ステータス、実行中のボトルネックなどをよりよく理解できます。これらのメトリックを監視する実際には、各TiDBコンポーネントの主要なメトリックをリストします。通常、これらの一般的な指標にのみ注意を払う必要があります。詳細については、 [公式ドキュメント](/grafana-overview-dashboard.md)を参照してください。

## Prometheusモニタリングデータは、デフォルトで15日ごとに削除されます。 2か月に設定することはできますか、それとも監視データを手動で削除することはできますか？ {#the-prometheus-monitoring-data-is-deleted-every-15-days-by-default-could-i-set-it-to-two-months-or-delete-the-monitoring-data-manually}

はい。 Prometheusが起動しているマシンで起動スクリプトを見つけ、起動パラメータを編集してPrometheusを再起動します。

```config
--storage.tsdb.retention="60d"
```

## リージョンの健康モニター {#region-health-monitor}

TiDB 2.0では、リージョンの状態はPDメトリックモニタリングページでモニタリングされます。このページでは、 `Region Health`のモニタリング項目にすべてのリージョンレプリカステータスの統計が表示されます。 `miss`はレプリカの不足を意味し、 `extra`は余分なレプリカが存在することを意味します。さらに、 `Region Health`は`label`による分離レベルも示します。 `level-1`は、リージョンレプリカが最初の`label`レベルで物理的に分離されていることを意味します。 `location label`が構成されていない場合、すべてのリージョンは`level-0`になります。

## ステートメントカウントモニターの<code>selectsimplefull</code>の意味は何ですか？ {#what-is-the-meaning-of-code-selectsimplefull-code-in-statement-count-monitor}

これは全表スキャンを意味しますが、テーブルは小さなシステムテーブルである可能性があります。

## モニターの<code>QPS</code>と<code>Statement OPS</code>の違いは何ですか？ {#what-is-the-difference-between-code-qps-code-and-code-statement-ops-code-in-the-monitor}

`QPS`の`begin`は、 `use database` 、 `show` `load data`を`insert`すべてのSQLステートメント`select` `set` `commit` 。

`Statement OPS`の統計は、 `select` 、および`insert`を含むアプリケーション関連のSQLステートメントに関するものであるため、 `Statement OPS` `update`統計はアプリケーションとの一致度が高くなります。
