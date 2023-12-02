---
title: Handle Alerts in TiDB Data Migration
summary: Understand how to deal with the alert information in DM.
---

# TiDB データ移行でのアラートの処理 {#handle-alerts-in-tidb-data-migration}

本書では、DM内のアラート情報への対処方法を紹介します。

## 高可用性に関するアラート {#alerts-related-to-high-availability}

### <code>DM_master_all_down</code> {#code-dm-master-all-down-code}

-   説明：

    すべての DM マスター ノードがオフラインの場合、このアラートがトリガーされます。

-   解決：

    次の手順を実行してアラートを処理できます。

    1.  クラスタの環境を確認してください。
    2.  トラブルシューティングのためにすべての DM マスター ノードのログを確認します。

### <code>DM_worker_offline</code> {#code-dm-worker-offline-code}

-   説明：

    DM ワーカー ノードが 1 時間以上オフラインになっている場合、このアラートがトリガーされます。高可用性アーキテクチャでは、このアラートはタスクを直接中断しない可能性がありますが、中断のリスクは増加します。

-   解決：

    次の手順を実行してアラートを処理できます。

    1.  対応する DM ワーカー ノードの動作ステータスをビュー。
    2.  ノードが接続されているかどうかを確認します。
    3.  ログを通じてエラーのトラブルシューティングを行います。

### <code>DM_DDL_error</code> {#code-dm-ddl-error-code}

-   説明：

    このエラーは、DM がシャーディング DDL 操作を処理しているときに発生します。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_pending_DDL</code> {#code-dm-pending-ddl-code}

-   説明：

    シャーディング DDL 操作が 1 時間以上保留されている場合、このアラートがトリガーされます。

-   解決：

    シナリオによっては、保留中のシャーディング DDL 操作がユーザーの期待どおりである場合があります。それ以外の場合は、解決策について[DM でシャーディング DDL ロックを手動で処理する](/dm/manually-handling-sharding-ddl-locks.md)を参照してください。

## タスクのステータスに関連するアラート ルール {#alert-rules-related-to-task-status}

### <code>DM_task_state</code> {#code-dm-task-state-code}

-   説明：

    DM ワーカーのサブタスクが 20 分以上`Paused`状態になると、アラートがトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

## リレーログに関するアラートルール {#alert-rules-related-to-relay-log}

### <code>DM_relay_process_exits_with_error</code> {#code-dm-relay-process-exits-with-error-code}

-   説明：

    リレー ログ処理ユニットで自動回復不可能なエラー (たとえば、 binlogファイルが見つからない) が発生したとき、または短期間に複数の回復可能なエラー (たとえば、ネットワークの問題) が発生したとき (たとえば、3 回以上) 2 分以内)、このアラートがトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_remain_storage_of_relay_log</code> {#code-dm-remain-storage-of-relay-log-code}

-   説明：

    リレー ログが保存されているディスクの空き容量が 10G 未満になると、アラートがトリガーされます。

-   解決策:

    アラートを処理するには、次の方法を使用できます。

    -   不要なデータを手動で削除して、ディスクの空き容量を増やします。
    -   [リレーログの自動データパージ戦略](/dm/relay-log.md#automatic-purge)または[データを手動で消去する](/dm/relay-log.md#manual-purge)を再構成します。
    -   コマンド`pause-relay`を実行して中継ログの取得処理を一時停止します。十分な空きディスク容量が確保できたら、コマンド`resume-relay`を実行してプロセスを再開します。リレー ログの取得プロセスが一時停止された後は、取得されていないアップストリームのbinlogファイルを削除しないでください。

### <code>DM_relay_log_data_corruption</code> {#code-dm-relay-log-data-corruption-code}

-   説明：

    リレー ログ処理ユニットが上流から読み取ったbinlogイベントを検証し、異常なチェックサム情報を検出すると、このユニットは`Paused`状態に移行し、アラートがトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_fail_to_read_binlog_from_master</code> {#code-dm-fail-to-read-binlog-from-master-code}

-   説明：

    リレー ログ処理ユニットがアップストリームからbinlogイベントを読み取ろうとしたときにエラーが発生した場合、このユニットは`Paused`状態に移行し、アラートがトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_fail_to_write_relay_log</code> {#code-dm-fail-to-write-relay-log-code}

-   説明：

    リレー ログ処理ユニットがbinlogイベントをリレー ログ ファイルに書き込もうとしたときにエラーが発生した場合、このユニットは`Paused`状態に移行し、アラートがトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_binlog_file_gap_between_master_relay</code> {#code-dm-binlog-file-gap-between-master-relay-code}

-   説明：

    現在のアップストリーム MySQL/MariaDB 内のbinlogファイルの数が、リレー ログ処理ユニットによってプルされた最新のbinlogファイルの数を 10 分間に 1**つ以上**超えると、アラートがトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

## ダンプ/ロードに関連するアラート ルール {#alert-rules-related-to-dump-load}

### <code>DM_dump_process_exists_with_error</code> {#code-dm-dump-process-exists-with-error-code}

-   説明：

    ダンプ処理ユニットで自動回復不可能なエラー (たとえば、 binlogファイルが見つからない) が発生したとき、または短期間に複数の回復可能なエラー (たとえば、ネットワークの問題) が発生したとき (たとえば、3 回以上) 2 分)、このアラートがトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_load_process_exists_with_error</code> {#code-dm-load-process-exists-with-error-code}

-   説明：

    ロード処理ユニットで自動回復不可能なエラー (たとえば、 binlogファイルが見つからない) が発生したとき、または短期間に複数の回復可能なエラー (たとえば、ネットワークの問題) が発生したとき (たとえば、3 回以上) 2 分)、このアラートがトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

## binlogレプリケーションに関連するアラートルール {#alert-rules-related-to-binlog-replication}

### <code>DM_sync_process_exists_with_error</code> {#code-dm-sync-process-exists-with-error-code}

-   説明：

    binlogレプリケーション処理ユニットで自動回復不可能なエラー (たとえば、binlogファイルが見つからない) が発生したとき、または短期間 (たとえば、3 回以上) に複数の回復可能なエラー (たとえば、ネットワークの問題) が発生したとき。 2 分以内)、このアラートがトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_binlog_file_gap_between_master_syncer</code> {#code-dm-binlog-file-gap-between-master-syncer-code}

-   説明：

    現在のアップストリーム MySQL/MariaDB 内のbinlogファイルの数が、リレー ログ処理ユニットによって処理された最新のbinlogファイルの数を 10 分間に 1**つ以上**超えると、アラートがトリガーされます。

-   解決：

    [パフォーマンスの問題に対処する](/dm/dm-handle-performance-issues.md)を参照してください。

### <code>DM_binlog_file_gap_between_relay_syncer</code> {#code-dm-binlog-file-gap-between-relay-syncer-code}

-   説明：

    現在のリレー ログ処理ユニット内のbinlogファイルの数が、binlogレプリケーション処理ユニットによって処理される最新のbinlogファイルの数を 10 分間に 1**つ以上**超えると、アラートがトリガーされます。

-   解決：

    [パフォーマンスの問題に対処する](/dm/dm-handle-performance-issues.md)を参照してください。
