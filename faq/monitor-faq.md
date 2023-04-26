---
title: TiDB Monitoring FAQs
summary: Learn about the FAQs related to TiDB Monitoring.
---

# TiDB モニタリングに関するよくある質問 {#tidb-monitoring-faqs}

このドキュメントは、TiDB の監視に関連する FAQ をまとめたものです。

-   Prometheus 監視フレームワークの詳細については、 [監視フレームワークの概要](/tidb-monitoring-framework.md)を参照してください。
-   モニタリングの主要なメトリックの詳細については、 [主な指標](/grafana-overview-dashboard.md)を参照してください。

## 主要な指標を監視するためのより良い方法はありますか? {#is-there-a-better-way-of-monitoring-the-key-metrics}

TiDB の監視システムは、Prometheus と Grafana で構成されています。 Grafana のダッシュボードから、TiDB のさまざまな実行中のメトリックを監視できます。これには、システム リソース、クライアント接続と SQL 操作、内部通信とリージョンスケジューリングの監視メトリックが含まれます。これらのメトリックを使用すると、データベース管理者は、システムの実行ステータス、実行中のボトルネックなどをよりよく理解できます。これらのメトリックを監視する際に、各 TiDBコンポーネントの主要なメトリックをリストします。通常、これらの一般的な指標にのみ注意を払う必要があります。詳細については、 [公式文書](/grafana-overview-dashboard.md)を参照してください。

## Prometheus の監視データは、デフォルトで 15 日ごとに削除されます。 2 か月に設定したり、監視データを手動で削除したりできますか? {#the-prometheus-monitoring-data-is-deleted-every-15-days-by-default-could-i-set-it-to-two-months-or-delete-the-monitoring-data-manually}

はい。 Prometheus が開始されたマシンで起動スクリプトを見つけ、起動パラメーターを編集して、Prometheus を再起動します。

```config
--storage.tsdb.retention="60d"
```

## リージョンヘルス モニター {#region-health-monitor}

TiDB 2.0 では、リージョンの正常性は PD メトリック監視ページで監視されます。このページでは、 `Region Health`監視項目にすべてのリージョンレプリカ ステータスの統計が表示されます。 `miss`レプリカが不足していることを意味し、 `extra`余分なレプリカが存在することを意味します。また、 `Region Health` `label`による分離レベルも示しています。 `level-1`リージョンのレプリカが最初の`label`レベルで物理的に分離されていることを意味します。 `location label`が設定されていない場合、すべてのリージョンは`level-0`にあります。

## Statement Count モニターでの<code>selectsimplefull</code>の意味は何ですか? {#what-is-the-meaning-of-code-selectsimplefull-code-in-statement-count-monitor}

これはフル テーブル スキャンを意味しますが、テーブルは小さなシステム テーブルである可能性があります。

## モニターにおける<code>QPS</code>と<code>Statement OPS</code>の違いは何ですか? {#what-is-the-difference-between-code-qps-code-and-code-statement-ops-code-in-the-monitor}

`QPS`統計は`use database` 、 `load data` 、 `begin` 、 `commit` 、 `set` 、 `show` 、 `insert`および`select`を含むすべての SQL ステートメントに関するものです。

`Statement OPS`統計は、 `select` 、 `update` 、および`insert`を含むアプリケーション関連の SQL ステートメントのみに関するものであるため、 `Statement OPS`統計はアプリケーションとよりよく一致します。
