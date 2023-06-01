---
title: TiDB Monitoring FAQs
summary: Learn about the FAQs related to TiDB Monitoring.
---

# TiDB モニタリングに関するよくある質問 {#tidb-monitoring-faqs}

このドキュメントには、TiDB モニタリングに関連する FAQ がまとめられています。

-   Prometheus 監視フレームワークの詳細については、 [監視フレームワークの概要](/tidb-monitoring-framework.md)を参照してください。
-   モニタリングの主要な指標の詳細については、 [主要な指標](/grafana-overview-dashboard.md)を参照してください。

## 主要な指標を監視するより良い方法はあるでしょうか? {#is-there-a-better-way-of-monitoring-the-key-metrics}

TiDB の監視システムは Prometheus と Grafana で構成されます。 Grafana のダッシュボードから、システム リソース、クライアント接続と SQL 操作、内部通信とリージョンスケジューリングの監視メトリクスを含む、TiDB のさまざまな実行メトリクスを監視できます。これらのメトリックを使用すると、データベース管理者はシステムの実行ステータスや実行のボトルネックなどをより深く理解できるようになります。これらのメトリクスを監視する実践では、各 TiDBコンポーネントの主要なメトリクスをリストします。通常、これらの一般的な指標にのみ注意する必要があります。詳細は[公式ドキュメント](/grafana-overview-dashboard.md)を参照してください。

## Prometheus 監視データは、デフォルトでは 15 日ごとに削除されます。 2か月に設定するか、監視データを手動で削除できますか? {#the-prometheus-monitoring-data-is-deleted-every-15-days-by-default-could-i-set-it-to-two-months-or-delete-the-monitoring-data-manually}

はい。 Prometheus が起動されているマシン上で起動スクリプトを見つけ、起動パラメータを編集して Prometheus を再起動します。

```config
--storage.tsdb.retention="60d"
```

## リージョンヘルスモニター {#region-health-monitor}

TiDB 2.0 では、リージョンの健全性は PD メトリック監視ページで監視されます。このページの`Region Health`監視項目には、すべてのリージョンレプリカ ステータスの統計が表示されます。 `miss`レプリカが不足していることを意味し、 `extra`余分なレプリカが存在することを意味します。また、 `Region Health` `label`による分離レベルも示します。 `level-1`リージョンレプリカが最初の`label`レベルで物理的に分離されていることを意味します。 `location label`が構成されていない場合、すべてのリージョンは`level-0`になります。

## ステートメント数モニターの<code>selectsimplefull</code>の意味は何ですか? {#what-is-the-meaning-of-code-selectsimplefull-code-in-statement-count-monitor}

これはテーブル全体のスキャンを意味しますが、テーブルは小さなシステムテーブルである可能性があります。

## モニターにおける<code>QPS</code>と<code>Statement OPS</code>の違いは何ですか? {#what-is-the-difference-between-code-qps-code-and-code-statement-ops-code-in-the-monitor}

`QPS`統計は、 `use database` 、 `load data` 、 `begin` 、 `commit` 、 `set` 、 `show` 、 `insert` 、 `select`を含むすべての SQL ステートメントに関するものです。

`Statement OPS`統計は、 `select` 、 `update` 、 `insert`を含むアプリケーション関連の SQL ステートメントのみに関するものであるため、 `Statement OPS`統計の方がアプリケーションとよりよく一致します。
