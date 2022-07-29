---
title: Daily Check
summary: Learn about the daily check of TiDB Data Migration (DM).
---

# デイリーチェック {#daily-check}

このドキュメントは、TiDBデータ移行（DM）の毎日のチェックを実行する方法をまとめたものです。

-   方法1： `query-status`コマンドを実行して、タスクの実行ステータスとエラー出力（存在する場合）を確認します。詳細については、 [クエリステータス](/dm/dm-query-status.md)を参照してください。

-   方法2：TiUPを使用してDMクラスタをデプロイするときにPrometheusとGrafanaが正しくデプロイされている場合、GrafanaでDMモニタリングメトリックを表示できます。たとえば、Grafanaのアドレスが`172.16.10.71`であるとし、 [http://172.16.10.71：3000](http://172.16.10.71:3000)に移動し、Grafanaダッシュボードに入り、DMダッシュボードを選択してDMのモニタリングメトリックを確認します。これらのメトリックの詳細については、 [DMモニタリングメトリクス](/dm/monitor-a-dm-cluster.md)を参照してください。

-   方法3：ログファイルを使用して、DMの実行ステータスとエラー（存在する場合）を確認します。

    -   DM-masterログディレクトリ： `--log-file`のDM-masterプロセスパラメータで指定されます。 DMがTiUPを使用して展開されている場合、ログディレクトリはDMマスターノードで`{log_dir}`です。
    -   DM-workerログディレクトリ： `--log-file`のDM-workerプロセスパラメータで指定されます。 DMがTiUPを使用してデプロイされている場合、ログディレクトリはDM-workerノードで`{log_dir}`です。
