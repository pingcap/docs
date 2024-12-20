---
title: Handle Alerts in TiDB Data Migration
summary: DM 内のアラート情報を処理する方法を理解します。
---

# TiDB データ移行におけるアラートの処理 {#handle-alerts-in-tidb-data-migration}

このドキュメントでは、DM でアラート情報を処理する方法について説明します。

## 高可用性に関連するアラート {#alerts-related-to-high-availability}

### <code>DM_master_all_down</code> {#code-dm-master-all-down-code}

-   説明：

    すべての DM マスター ノードがオフラインの場合、このアラートがトリガーされます。

-   解決：

    アラートを処理するには、次の手順を実行できます。

    1.  クラスターの環境を確認します。
    2.  トラブルシューティングのために、すべての DM マスター ノードのログを確認します。

### <code>DM_worker_offline</code> {#code-dm-worker-offline-code}

-   説明：

    DM ワーカー ノードが 1 時間以上オフラインの場合、このアラートがトリガーされます。高可用性アーキテクチャでは、このアラートによってタスクが直接中断されることはありませんが、中断のリスクが高まります。

-   解決：

    アラートを処理するには、次の手順を実行できます。

    1.  対応する DM ワーカー ノードの動作ステータスをビュー。
    2.  ノードが接続されているかどうかを確認します。
    3.  ログを通じてエラーをトラブルシューティングします。

### <code>DM_DDL_error</code> {#code-dm-ddl-error-code}

-   説明：

    このエラーは、DM がシャーディング DDL 操作を処理しているときに発生します。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_pending_DDL</code> {#code-dm-pending-ddl-code}

-   説明：

    シャーディング DDL 操作が 1 時間以上保留になっている場合、このアラートがトリガーされます。

-   解決：

    シナリオによっては、保留中のシャーディング DDL 操作がユーザーの期待どおりになる場合があります。それ以外の場合は、解決策については[DM でシャーディング DDL ロックを手動で処理する](/dm/manually-handling-sharding-ddl-locks.md)を参照してください。

## タスクステータスに関連するアラートルール {#alert-rules-related-to-task-status}

### <code>DM_task_state</code> {#code-dm-task-state-code}

-   説明：

    DM ワーカーのサブタスクが 20 分以上`Paused`状態にある場合、アラートがトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

## リレーログに関連するアラートルール {#alert-rules-related-to-relay-log}

### <code>DM_relay_process_exits_with_error</code> {#code-dm-relay-process-exits-with-error-code}

-   説明：

    リレー ログ処理ユニットで自動回復不可能なエラー (たとえば、 binlogファイルが見つからない) が発生した場合、または短時間 (たとえば、2 分間に 3 回以上) に回復可能なエラー (たとえば、ネットワークの問題) が複数発生した場合、このアラートがトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_remain_storage_of_relay_log</code> {#code-dm-remain-storage-of-relay-log-code}

-   説明：

    リレーログが保存されているディスクの空き容量が 10G 未満になると、アラートがトリガーされます。

-   解決策:

    アラートを処理するには、次の方法があります。

    -   不要なデータを手動で削除して、空きディスク容量を増やします。
    -   [リレーログの自動データ消去戦略](/dm/relay-log.md#automatic-purge)または[データを手動で消去する](/dm/relay-log.md#manual-purge)再構成します。
    -   コマンド`pause-relay`を実行して、リレー ログ プル プロセスを一時停止します。十分な空きディスク領域が確保されたら、コマンド`resume-relay`を実行してプロセスを再開します。リレー ログ プル プロセスが一時停止された後、プルされていないアップストリームbinlogファイルを消去してはならないことに注意してください。

### <code>DM_relay_log_data_corruption</code> {#code-dm-relay-log-data-corruption-code}

-   説明：

    リレーログ処理ユニットが上流から読み取ったbinlogイベントを検証し、異常なチェックサム情報を検出すると、このユニットは`Paused`状態に移行し、アラートがトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_fail_to_read_binlog_from_master</code> {#code-dm-fail-to-read-binlog-from-master-code}

-   説明：

    リレーログ処理ユニットが上流からbinlogイベントを読み取ろうとしたときにエラーが発生した場合、このユニットは`Paused`状態に移行し、アラートがトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_fail_to_write_relay_log</code> {#code-dm-fail-to-write-relay-log-code}

-   説明：

    リレー ログ処理ユニットがbinlogイベントをリレー ログ ファイルに書き込もうとしたときにエラーが発生すると、このユニットは`Paused`状態に移行し、アラートがトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_binlog_file_gap_between_master_relay</code> {#code-dm-binlog-file-gap-between-master-relay-code}

-   説明：

    現在のアップストリーム MySQL/MariaDB 内のbinlogファイルの数が、リレー ログ処理ユニットによってプルされた最新のbinlogファイルの数を 10 分間で 1**以上**超過すると、アラートがトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

## ダンプ/ロードに関連するアラートルール {#alert-rules-related-to-dump-load}

### <code>DM_dump_process_exists_with_error</code> {#code-dm-dump-process-exists-with-error-code}

-   説明：

    ダンプ処理ユニットで自動回復不可能なエラー (たとえば、 binlogファイルが見つからない) が発生した場合、または短時間 (たとえば、2 分間に 3 回以上) に複数の回復可能なエラー (たとえば、ネットワークの問題) が発生した場合、このアラートがトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_load_process_exists_with_error</code> {#code-dm-load-process-exists-with-error-code}

-   説明：

    ロード処理ユニットで自動回復不可能なエラー (たとえば、 binlogファイルが見つからない) が発生した場合、または短期間に (たとえば、2 分間に 3 回以上) 回復可能なエラー (たとえば、ネットワークの問題) が複数発生した場合、このアラートがトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

## binlogレプリケーションに関連するアラートルール {#alert-rules-related-to-binlog-replication}

### <code>DM_sync_process_exists_with_error</code> {#code-dm-sync-process-exists-with-error-code}

-   説明：

    binlogログ レプリケーション処理ユニットで自動回復不可能なエラー (binlogファイルが見つからないなど) が発生した場合、または短期間に (たとえば、2 分間に 3 回以上) 回復可能なエラー (たとえば、ネットワークの問題) が複数発生した場合、このアラートがトリガーされます。

-   解決：

    [DM のトラブルシューティング](/dm/dm-error-handling.md#troubleshooting)を参照してください。

### <code>DM_binlog_file_gap_between_master_syncer</code> {#code-dm-binlog-file-gap-between-master-syncer-code}

-   説明：

    現在のアップストリーム MySQL/MariaDB 内のbinlogファイルの数が、リレー ログ処理ユニットによって処理された最新のbinlogファイルの数を 10 分間で 1**以上**超えると、アラートがトリガーされます。

-   解決：

    [パフォーマンスの問題に対処する](/dm/dm-handle-performance-issues.md)を参照してください。

### <code>DM_binlog_file_gap_between_relay_syncer</code> {#code-dm-binlog-file-gap-between-relay-syncer-code}

-   説明：

    現在のリレーログ処理単位内のbinlogファイルの数が、binlogログレプリケーション処理単位で処理された最新のbinlogファイルの数より 10 分間に 1**以上**超過すると、アラートがトリガーされます。

-   解決：

    [パフォーマンスの問題に対処する](/dm/dm-handle-performance-issues.md)を参照してください。
