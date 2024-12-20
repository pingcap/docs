---
title: Daily Check for TiDB Data Migration
summary: TiDB データ移行 (DM) の毎日のチェックについて説明します。
---

# TiDBデータ移行の毎日のチェック {#daily-check-for-tidb-data-migration}

このドキュメントでは、TiDB データ移行 (DM) の毎日のチェックを実行する方法をまとめています。

-   方法 1: `query-status`コマンドを実行して、タスクの実行ステータスとエラー出力 (ある場合) を確認します。詳細については、 [クエリステータス](/dm/dm-query-status.md)参照してください。

-   方法 2: TiUP を使用して DM クラスターをデプロイするときに Prometheus と Grafana が正しくデプロイされていれば、Grafana で DM モニタリング メトリックを表示できます。たとえば、Grafana のアドレスが`172.16.10.71`であるとすると、 [http://172.16.10.71:3000](http://172.16.10.71:3000)に進み、Grafana ダッシュボードに入り、DM ダッシュボードを選択して DM のモニタリング メトリックを確認します。これらのメトリックの詳細については、 [DM モニタリング メトリック](/dm/monitor-a-dm-cluster.md)参照してください。

-   方法 3: ログ ファイルを使用して、DM の実行ステータスとエラー (ある場合) を確認します。

    -   DM マスター ログ ディレクトリ: `--log-file` DM マスター プロセス パラメータで指定します。DM がTiUP を使用して展開されている場合、ログ ディレクトリは DM マスター ノードの`{log_dir}`になります。
    -   DM-worker ログ ディレクトリ: `--log-file` DM-worker プロセス パラメータで指定します。DM がTiUP を使用してデプロイされている場合、ログ ディレクトリは DM-worker ノードの`{log_dir}`になります。
