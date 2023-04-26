---
title: Daily Check for TiDB Data Migration
summary: Learn about the daily check of TiDB Data Migration (DM).
---

# TiDB データ移行の毎日のチェック {#daily-check-for-tidb-data-migration}

このドキュメントでは、TiDB Data Migration (DM) で日常的なチェックを実行する方法をまとめています。

-   方法 1: `query-status`コマンドを実行して、タスクの実行ステータスとエラー出力 (ある場合) を確認します。詳細については、 [クエリのステータス](/dm/dm-query-status.md)を参照してください。

-   方法 2: TiUPを使用して DM クラスターをデプロイするときに Prometheus と Grafana が正しくデプロイされている場合は、Grafana で DM 監視メトリックを表示できます。たとえば、Grafana のアドレスが`172.16.10.71`である場合、 [http://172.16.10.71:3000](http://172.16.10.71:3000)に移動し、Grafana ダッシュボードに入り、DM ダッシュボードを選択して DM のモニタリング メトリックを確認します。これらのメトリックの詳細については、 [DM モニタリング指標](/dm/monitor-a-dm-cluster.md)を参照してください。

-   方法 3: ログ ファイルを使用して、DM の実行状態とエラー (ある場合) を確認します。

    -   DM-master ログ ディレクトリ: `--log-file` DM-master プロセス パラメータによって指定されます。 DM がTiUPを使用してデプロイされている場合、ログ ディレクトリは DM-master ノードの`{log_dir}`です。
    -   DM-worker ログ ディレクトリ: `--log-file` DM-worker プロセス パラメータで指定されます。 DM がTiUPを使用してデプロイされている場合、ログ ディレクトリは DM-worker ノードの`{log_dir}`です。
