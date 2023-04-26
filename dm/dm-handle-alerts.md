---
title: Handle Alerts in TiDB Data Migration
summary: Understand how to deal with the alert information in DM.
---

# TiDB データ移行でアラートを処理する {#handle-alerts-in-tidb-data-migration}

このドキュメントでは、DM でアラート情報を処理する方法を紹介します。

## 高可用性に関連するアラート {#alerts-related-to-high-availability}

### <code>DM_master_all_down</code> {#code-dm-master-all-down-code}

-   説明：

    すべての DM マスター ノードがオフラインの場合、このアラートがトリガーされます。

-   解決：

    アラートを処理するには、次の手順を実行できます。

    1.  クラスタの環境を確認してください。
    2.  トラブルシューティングのために、すべての DM マスター ノードのログを確認します。

### <code>DM_worker_offline</code> {#code-dm-worker-offline-code}

-   説明：

    DM-worker ノードが 1 時間以上オフラインの場合、このアラートがトリガーされます。高可用性アーキテクチャでは、このアラートによってタスクが直接中断されることはありませんが、中断のリスクが高まります。

-   解決：

    アラートを処理するには、次の手順を実行できます。

    1.  対応する DM-worker ノードの動作ステータスをビュー。
    2.  ノードが接続されているかどうかを確認します。
    3.  ログを使用してエラーをトラブルシューティングします。

### <code>DM_DDL_error</code> {#code-dm-ddl-error-code}

-   説明：

    このエラーは、DM がシャーディング DDL 操作を処理しているときに発生します。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_pending_DDL</code> {#code-dm-pending-ddl-code}

-   説明：

    シャーディング DDL 操作が 1 時間以上保留されている場合、このアラートがトリガーされます。

-   解決：

    一部のシナリオでは、保留中のシャーディング DDL 操作は、ユーザーが期待するものである可能性があります。それ以外の場合は、解決策について[DM でシャーディング DDL ロックを手動で処理する](/dm/manually-handling-sharding-ddl-locks.md)を参照してください。

## タスク ステータスに関連するアラート ルール {#alert-rules-related-to-task-status}

### <code>DM_task_state</code> {#code-dm-task-state-code}

-   説明：

    DM-worker のサブタスクが 20 分以上`Paused`の状態にある場合、アラートがトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

## 中継ログに関するアラートルール {#alert-rules-related-to-relay-log}

### <code>DM_relay_process_exits_with_error</code> {#code-dm-relay-process-exits-with-error-code}

-   説明：

    リレー ログ処理ユニットでエラーが発生すると、このユニットは`Paused`状態に移行し、アラートがすぐにトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_remain_storage_of_relay_log</code> {#code-dm-remain-storage-of-relay-log-code}

-   説明：

    中継ログが配置されているディスクの空き容量が 10G 未満になると、アラートがトリガーされます。

-   ソリューション:

    アラートを処理するには、次の方法を使用できます。

    -   不要なデータを手動で削除して、ディスクの空き容量を増やします。
    -   [リレー ログの自動データ パージ戦略](/dm/relay-log.md#automatic-data-purge)または[データを手動で消去する](/dm/relay-log.md#manual-data-purge)を再設定します。
    -   コマンド`pause-relay`を実行して、リレー ログのプル プロセスを一時停止します。十分な空きディスク領域ができたら、コマンド`resume-relay`を実行してプロセスを再開します。リレー ログのプル プロセスが一時停止された後は、プルされていないアップストリームのbinlogファイルを削除しないでください。

### <code>DM_relay_log_data_corruption</code> {#code-dm-relay-log-data-corruption-code}

-   説明：

    中継ログ処理部は、上流から読み込んだbinlogイベントを検証し、異常なチェックサム情報を検出すると`Paused`状態に移行し、即座にアラートを発します。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_fail_to_read_binlog_from_master</code> {#code-dm-fail-to-read-binlog-from-master-code}

-   説明：

    リレー ログ処理ユニットが上流からbinlogイベントを読み込もうとしてエラーが発生した場合、このユニットは`Paused`状態に移行し、すぐにアラートがトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_fail_to_write_relay_log</code> {#code-dm-fail-to-write-relay-log-code}

-   説明：

    リレー ログ処理ユニットがbinlogイベントをリレー ログ ファイルに書き込もうとしたときにエラーが発生した場合、このユニットは状態`Paused`に移行し、すぐにアラートがトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_binlog_file_gap_between_master_relay</code> {#code-dm-binlog-file-gap-between-master-relay-code}

-   説明：

    現在の上流の MySQL/MariaDB 内のbinlogファイルの数が、リレー ログ処理ユニットによってプルされた最新のbinlogファイルの数を 10 分間で 1**つ以上**超えると、アラートがトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

## Dump/Load に関連するアラート ルール {#alert-rules-related-to-dump-load}

### <code>DM_dump_process_exists_with_error</code> {#code-dm-dump-process-exists-with-error-code}

-   説明：

    Dump 処理ユニットでエラーが発生すると、このユニットは`Paused`状態に移行し、アラートがすぐにトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_load_process_exists_with_error</code> {#code-dm-load-process-exists-with-error-code}

-   説明：

    Load 処理ユニットでエラーが発生すると、このユニットは`Paused`状態に移行し、アラートがすぐにトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

## binlogレプリケーションに関連するアラート ルール {#alert-rules-related-to-binlog-replication}

### <code>DM_sync_process_exists_with_error</code> {#code-dm-sync-process-exists-with-error-code}

-   説明：

    binlogレプリケーション処理ユニットでエラーが発生すると、このユニットは`Paused`状態に移行し、アラートがすぐにトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_binlog_file_gap_between_master_syncer</code> {#code-dm-binlog-file-gap-between-master-syncer-code}

-   説明：

    現在の上流の MySQL/MariaDB 内のbinlogファイルの数が、リレー ログ処理ユニットによって処理された最新のbinlogファイルの数を 10 分間**以上**1 つ超えると、アラートがトリガーされます。

-   解決：

    [パフォーマンスの問題を処理する](/dm/dm-handle-performance-issues.md)を参照してください。

### <code>DM_binlog_file_gap_between_relay_syncer</code> {#code-dm-binlog-file-gap-between-relay-syncer-code}

-   説明：

    現在のリレー ログ処理ユニット内のbinlogファイルの数が、binlogレプリケーション処理ユニットによって処理された最新のbinlogファイルの数を 10 分間**以上**1 つ超えると、アラートがトリガーされます。

-   解決：

    [パフォーマンスの問題を処理する](/dm/dm-handle-performance-issues.md)を参照してください。
