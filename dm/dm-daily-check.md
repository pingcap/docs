---
title: Daily Check for TiDB Data Migration
summary: Learn about the daily check of TiDB Data Migration (DM).
---

# TiDB データ移行の毎日のチェック {#daily-check-for-tidb-data-migration}

このドキュメントでは、TiDB Data Migration (DM) の日常チェックを実行する方法をまとめます。

-   方法 1: `query-status`コマンドを実行して、タスクの実行ステータスとエラー出力 (存在する場合) を確認します。詳細は[クエリステータス](/dm/dm-query-status.md)を参照してください。

-   方法 2: TiUPを使用して DM クラスターをデプロイするときに Prometheus と Grafana が正しくデプロイされている場合は、Grafana で DM 監視メトリックを表示できます。たとえば、Grafana のアドレスが`172.16.10.71`であると仮定し、 [http://172.16.10.71:3000](http://172.16.10.71:3000)に移動して Grafana ダッシュボードに入り、DM ダッシュボードを選択して DM の監視メトリクスを確認します。これらのメトリクスの詳細については、 [DM監視メトリクス](/dm/monitor-a-dm-cluster.md)を参照してください。

-   方法 3: ログ ファイルを使用して、DM の実行ステータスとエラー (存在する場合) を確認します。

    -   DM マスター ログ ディレクトリ: `--log-file` DM マスター プロセス パラメーターによって指定されます。 DM がTiUPを使用してデプロイされている場合、ログ ディレクトリは DM マスター ノードの`{log_dir}`です。
    -   DM-worker ログ ディレクトリ: `--log-file` DM-worker プロセス パラメーターで指定されます。 DM がTiUPを使用してデプロイされている場合、ログ ディレクトリは DM ワーカー ノードの`{log_dir}`です。
