---
title: TiDB Monitoring FAQs
summary: TiDB モニタリングに関連する FAQ について説明します。
---

# TiDB モニタリングに関するよくある質問 {#tidb-monitoring-faqs}

このドキュメントでは、TiDB 監視に関連する FAQ をまとめています。

-   Prometheus 監視フレームワークの詳細については、 [監視フレームワークの概要](/tidb-monitoring-framework.md)参照してください。
-   モニタリングの主要な指標の詳細については、 [主要指標](/grafana-overview-dashboard.md)を参照してください。

## 主要な指標を監視するより良い方法はありますか? {#is-there-a-better-way-of-monitoring-the-key-metrics}

TiDB の監視システムは、Prometheus と Grafana で構成されています。Grafana のダッシュボードから、システム リソース、クライアント接続と SQL 操作、内部通信、リージョンスケジューリングの監視メトリクスを含む、TiDB のさまざまな実行メトリクスを監視できます。これらのメトリクスを使用すると、データベース管理者はシステムの実行ステータス、実行中のボトルネックなどをよりよく理解できます。これらのメトリクスを監視する実践では、各 TiDBコンポーネントの主要なメトリクスをリストします。通常は、これらの共通メトリクスのみに注意する必要があります。詳細については、 [公式文書](/grafana-overview-dashboard.md)参照してください。

## Prometheus 監視データは、デフォルトでは 15 日ごとに削除されます。これを 2 か月に設定したり、監視データを手動で削除したりすることはできますか? {#the-prometheus-monitoring-data-is-deleted-every-15-days-by-default-could-i-set-it-to-two-months-or-delete-the-monitoring-data-manually}

はい。Prometheus が起動されているマシンで起動スクリプトを見つけ、起動パラメータを編集して Prometheus を再起動します。

    --storage.tsdb.retention="60d"

## リージョンヘルスモニター {#region-health-monitor}

TiDB 2.0 では、リージョンの健全性は PD メトリック監視ページで監視され、監視項目`Region Health`にはすべてのリージョンレプリカ ステータスの統計が表示されます。3 `miss`レプリカ不足、 `extra`余分なレプリカが存在することを意味します。さらに、 `Region Health` `label`による分離レベルも示します。11 `level-1` 、リージョンレプリカが最初の`label`レベルで物理的に分離されていることを意味します。17 `location label`構成されていない場合、すべてのリージョンは`level-0`になります。

## ステートメント カウント モニターの<code>selectsimplefull</code>の意味は何ですか? {#what-is-the-meaning-of-code-selectsimplefull-code-in-statement-count-monitor}

これは完全なテーブルスキャンを意味しますが、テーブルは小さなシステム テーブルである可能性があります。

## モニターの<code>QPS</code>と<code>Statement OPS</code>の違いは何ですか? {#what-is-the-difference-between-code-qps-code-and-code-statement-ops-code-in-the-monitor}

`QPS`統計は、 `use database` 、 `load data` 、 `begin` 、 `commit` 、 `set` 、 `show` 、 `insert` 、および`select`を含むすべての SQL ステートメントに関するものです。

`Statement OPS`統計は、 `select` 、 `update` 、 `insert`を含むアプリケーション関連の SQL ステートメントのみに関するものであるため、 `Statement OPS`統計の方がアプリケーションにより適合します。
