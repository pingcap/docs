---
title: Handle Alerts
summary: Understand how to deal with the alert information in DM.
---

# アラートを処理する {#handle-alerts}

このドキュメントでは、DMでアラート情報を処理する方法を紹介します。

## 高可用性に関連するアラート {#alerts-related-to-high-availability}

### <code>DM_master_all_down</code> {#code-dm-master-all-down-code}

-   説明：

    すべてのDMマスターノードがオフラインの場合、このアラートがトリガーされます。

-   解決：

    アラートを処理するには、次の手順を実行できます。

    1.  クラスタの環境を確認してください。
    2.  トラブルシューティングについては、すべてのDMマスターノードのログを確認してください。

### <code>DM_worker_offline</code> {#code-dm-worker-offline-code}

-   説明：

    DMワーカーノードが1時間以上オフラインの場合、このアラートがトリガーされます。高可用性アーキテクチャでは、このアラートはタスクを直接中断しない可能性がありますが、中断のリスクが高まります。

-   解決：

    アラートを処理するには、次の手順を実行できます。

    1.  対応するDM-workerノードの動作ステータスをビューします。
    2.  ノードが接続されているか確認してください。
    3.  ログを介してエラーをトラブルシューティングします。

### <code>DM_DDL_error</code> {#code-dm-ddl-error-code}

-   説明：

    このエラーは、DMがシャーディングDDL操作を処理しているときに発生します。

-   解決：

    [DMのトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_pending_DDL</code> {#code-dm-pending-ddl-code}

-   説明：

    シャーディングDDL操作が1時間以上保留されている場合、このアラートがトリガーされます。

-   解決：

    一部のシナリオでは、保留中のシャーディングDDL操作がユーザーの期待どおりになる場合があります。それ以外の場合、解決策については[DMでシャーディングDDLロックを手動で処理する](/dm/manually-handling-sharding-ddl-locks.md)を参照してください。

## タスクステータスに関連するアラートルール {#alert-rules-related-to-task-status}

### <code>DM_task_state</code> {#code-dm-task-state-code}

-   説明：

    DM-workerのサブタスクが20分を超えて`Paused`状態になると、アラートがトリガーされます。

-   解決：

    [DMのトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

## リレーログに関連するアラートルール {#alert-rules-related-to-relay-log}

### <code>DM_relay_process_exits_with_error</code> {#code-dm-relay-process-exits-with-error-code}

-   説明：

    リレーログ処理ユニットでエラーが発生すると、このユニットは`Paused`状態に移行し、すぐにアラートがトリガーされます。

-   解決：

    [DMのトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_remain_storage_of_relay_log</code> {#code-dm-remain-storage-of-relay-log-code}

-   説明：

    リレーログが配置されているディスクの空き容量が10G未満の場合、アラートがトリガーされます。

-   ソリューション：

    アラートを処理するには、次の方法を使用できます。

    -   不要なデータを手動で削除して、空きディスク容量を増やします。
    -   [リレーログの自動データパージ戦略](/dm/relay-log.md#automatic-data-purge)または[データを手動でパージする](/dm/relay-log.md#manual-data-purge)を再構成します。
    -   コマンド`pause-relay`を実行して、リレーログプルプロセスを一時停止します。十分な空きディスク容量ができたら、コマンド`resume-relay`を実行してプロセスを再開します。リレーログプルプロセスが一時停止した後、プルされていないアップストリームbinlogファイルをパージしてはならないことに注意してください。

### <code>DM_relay_log_data_corruption</code> {#code-dm-relay-log-data-corruption-code}

-   説明：

    リレーログ処理ユニットがアップストリームから読み取ったbinlogイベントを検証し、異常なチェックサム情報を検出すると、このユニットは`Paused`状態に移行し、すぐにアラートがトリガーされます。

-   解決：

    [DMのトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_fail_to_read_binlog_from_master</code> {#code-dm-fail-to-read-binlog-from-master-code}

-   説明：

    リレーログ処理ユニットがアップストリームからbinlogイベントを読み取ろうとしたときにエラーが発生した場合、このユニットは`Paused`状態に移行し、すぐにアラートがトリガーされます。

-   解決：

    [DMのトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_fail_to_write_relay_log</code> {#code-dm-fail-to-write-relay-log-code}

-   説明：

    リレーログ処理ユニットがbinlogイベントをリレーログファイルに書き込もうとしたときにエラーが発生した場合、このユニットは`Paused`状態に移行し、すぐにアラートがトリガーされます。

-   解決：

    [DMのトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_binlog_file_gap_between_master_relay</code> {#code-dm-binlog-file-gap-between-master-relay-code}

-   説明：

    現在のアップストリームMySQL/MariaDB内のbinlogファイルの数が、リレーログ処理ユニットによってプルされた最新のbinlogファイルの数を10分間1**以上超える**と、アラートがトリガーされます。

-   解決：

    [DMのトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

## ダンプ/ロードに関連するアラートルール {#alert-rules-related-to-dump-load}

### <code>DM_dump_process_exists_with_error</code> {#code-dm-dump-process-exists-with-error-code}

-   説明：

    ダンプ処理ユニットでエラーが発生すると、このユニットは`Paused`状態に移行し、すぐにアラートがトリガーされます。

-   解決：

    [DMのトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_load_process_exists_with_error</code> {#code-dm-load-process-exists-with-error-code}

-   説明：

    負荷処理ユニットでエラーが発生すると、このユニットは`Paused`状態に移行し、すぐにアラートがトリガーされます。

-   解決：

    [DMのトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

## binlogレプリケーションに関連するアラートルール {#alert-rules-related-to-binlog-replication}

### <code>DM_sync_process_exists_with_error</code> {#code-dm-sync-process-exists-with-error-code}

-   説明：

    binlogレプリケーション処理ユニットでエラーが発生すると、このユニットは`Paused`状態に移行し、すぐにアラートがトリガーされます。

-   解決：

    [DMのトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_binlog_file_gap_between_master_syncer</code> {#code-dm-binlog-file-gap-between-master-syncer-code}

-   説明：

    現在のアップストリームMySQL/MariaDB内のbinlogファイルの数が、リレーログ処理ユニットによって処理された最新のbinlogファイルの数を10分間1**以上超える**と、アラートがトリガーされます。

-   解決：

    [パフォーマンスの問題を処理する](/dm/dm-handle-performance-issues.md)を参照してください。

### <code>DM_binlog_file_gap_between_relay_syncer</code> {#code-dm-binlog-file-gap-between-relay-syncer-code}

-   説明：

    現在のリレーログ処理装置内のbinlogファイルの数が、binlog複製処理装置によって処理された最新のbinlogファイルの数を10分間1**以上超える**と、アラートがトリガーされます。

-   解決：

    [パフォーマンスの問題を処理する](/dm/dm-handle-performance-issues.md)を参照してください。
