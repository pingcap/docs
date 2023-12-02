---
title: Monitoring and Alert for Backup and Restore
summary: Learn the monitoring and alert of the backup and restore feature.
---

# バックアップと復元の監視とアラート {#monitoring-and-alert-for-backup-and-restore}

このドキュメントでは、監視コンポーネント、監視メトリック、一般的なアラートの展開方法など、バックアップおよび復元機能の監視とアラートについて説明します。

## ログバックアップの監視 {#log-backup-monitoring}

ログ バックアップでは、 [プロメテウス](https://prometheus.io/)を使用したモニタリング メトリックの収集がサポートされています。現在、すべての監視メトリックは TiKV に組み込まれています。

### 監視構成 {#monitoring-configuration}

-   TiUPを使用してデプロイされたクラスターの場合、Prometheus はモニタリング メトリックを自動的に収集します。
-   手動でデプロイされたクラスターの場合は、 [TiDBクラスタモニタリングの展開](/deploy-monitoring-services.md)の手順に従って、TiKV 関連のジョブを Prometheus 構成ファイルの`scrape_configs`セクションに追加します。

### グラファナの構成 {#grafana-configuration}

-   TiUPを使用してデプロイされたクラスターの場合、 [グラファナ](https://grafana.com/)ダッシュボードにはポイントインタイム リカバリ (PITR) パネルが含まれています。 TiKV-Details ダッシュボードの**バックアップ ログ**パネルは PITR パネルです。
-   手動でデプロイされたクラスターの場合は、 [Grafana ダッシュボードをインポートする](/deploy-monitoring-services.md#step-2-import-a-grafana-dashboard)を参照し、 [tikv_details](https://github.com/tikv/tikv/blob/release-7.5/metrics/grafana/tikv_details.json) JSON ファイルを Grafana にアップロードします。次に、TiKV-Details ダッシュボードで**[バックアップ ログ]**パネルを見つけます。

### モニタリング指標 {#monitoring-metrics}

| メトリクス                                                 | タイプ    | 説明                                                                                                                                                 |
| ----------------------------------------------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **tikv_log_backup_interal_actor_acting_duration_sec** | ヒストグラム | すべての内部メッセージとイベントを処理する期間。<br/> `message :: TaskType`                                                                                                |
| **tikv_log_backup_initial_scan_reason**               | カウンター  | 初期スキャンがトリガーされる理由の統計。主な理由は、リーダーの異動またはリージョンのバージョン変更です。<br/> `reason :: {"leader-changed", "region-changed", "retry"}`                                |
| **tikv_log_backup_event_handle_duration_sec**         | ヒストグラム | KV イベントの処理期間。 `tikv_log_backup_on_event_duration_seconds`と比較すると、この指標には内部コンバージョンの期間も含まれます。<br/> `stage :: {"to_stream_event", "save_to_temp_file"}` |
| **tikv_log_backup_handle_kv_batch**                   | ヒストグラム | Raftstoreによって送信された KV ペア バッチのサイズのリージョン レベルの統計。                                                                                                     |
| **tikv_log_backup_initial_scan_disk_read**            | カウンター  | 初期スキャン中にディスクから読み取られたデータのサイズ。 Linux では、この情報は procfs から取得されます。これは、ブロック デバイスから実際に読み取られたデータのサイズです。構成項目`initial-scan-rate-limit`は、このメトリックに適用されます。       |
| **tikv_log_backup_incremental_scan_bytes**            | ヒストグラム | 初期スキャン中に実際に生成される KV ペアのサイズ。圧縮と読み取り増幅のため、この値は`tikv_log_backup_initial_scan_disk_read`の値とは異なる場合があります。                                                |
| **tikv_log_backup_skip_kv_count**                     | カウンター  | バックアップに役立たないため、ログのバックアップ中にスキップされたRaftイベントの数。                                                                                                       |
| **tikv_log_backup_errors**                            | カウンター  | ログのバックアップ中に再試行または無視できるエラー。<br/> `type :: ErrorType`                                                                                                |
| **tikv_log_backup_fatal_errors**                      | カウンター  | ログのバックアップ中に再試行または無視できないエラー。このタイプのエラーが発生すると、ログのバックアップは一時停止されます。<br/> `type :: ErrorType`                                                            |
| **tikv_log_backup_heap_memory**                       | ゲージ    | 未消費で、ログ バックアップ中の初期スキャンで検出されたイベントによって占有されるメモリ。                                                                                                      |
| **tikv_log_backup_on_event_duration_秒**               | ヒストグラム | KV イベントを一時ファイルに保存する期間。<br/> `stage :: {"write_to_tempfile", "syscall_write"}`                                                                      |
| **tikv_log_backup_store_checkpoint_ts**               | ゲージ    | ストアレベルのチェックポイント TS (非推奨)。現在のストアによって登録されている GC セーフポイントに近いです。<br/> `task :: string`                                                                  |
| **tidb_log_backup_last_checkpoint**                   | ゲージ    | グローバル チェックポイント TS。どの時点までのログデータがバックアップされているかの時点です。<br/> `task :: string`                                                                            |
| **tikv_log_backup_flush_duration_sec**                | ヒストグラム | ローカル一時ファイルを外部storageに移動する期間。<br/> `stage :: {"generate_metadata", "save_files", "clear_temp_files"}`                                               |
| **tikv_log_backup_flush_file_size**                   | ヒストグラム | バックアップ中に生成されたファイルのサイズの統計。                                                                                                                          |
| **tikv_log_backup_initial_scan_duration_sec**         | ヒストグラム | 初期スキャンの全体的な期間の統計。                                                                                                                                  |
| **tikv_log_backup_skip_retry_observe**                | カウンター  | ログのバックアップ中に無視できるエラーの統計、または再試行がスキップされる理由。<br/> `reason :: {"region-absent", "not-leader", "stale-command"}`                                         |
| **tikv_log_backup_initial_scan_operations**           | カウンター  | 初期スキャン中の RocksDB 関連の操作の統計。<br/> `cf :: {"default", "write", "lock"}, op :: RocksDBOP`                                                              |
| **tikv_log_backup_enabled**                           | カウンター  | ログのバックアップを有効にするかどうか。値が`0`より大きい場合、ログのバックアップが有効になります。                                                                                                |
| **tikv_log_backup_observed_region**                   | ゲージ    | リッスンされているリージョンの数。                                                                                                                                  |
| **tikv_log_backup_task_status**                       | ゲージ    | ログ バックアップ タスクのステータス。 `0`実行を意味します。 `1`一時停止を意味します。 `2`エラーを意味します。<br/> `task :: string`                                                               |
| **tikv_log_backup_pending_initial_scan**              | ゲージ    | 保留中の初期スキャンの統計。<br/> `stage :: {"queuing", "executing"}`                                                                                            |

### ログバックアップアラート {#log-backup-alerts}

#### アラート設定 {#alert-configuration}

現在、PITR には組み込みのアラート項目がありません。このセクションでは、PITR でアラート項目を構成する方法と、いくつかの推奨項目を紹介します。

PITR でアラート項目を構成するには、次の手順に従います。

1.  Prometheus が配置されているノード上にアラート ルールの構成ファイル (たとえば、 `pitr.rules.yml` ) を作成します。ファイルには、 [プロメテウスのドキュメント](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/) 、以下の推奨アラート項目、設定サンプルに従ってアラートルールを記述します。
2.  Prometheus 構成ファイルの`rule_files`フィールドに、アラート ルール ファイルのパスを追加します。
3.  `SIGHUP`シグナルを Prometheus プロセス ( `kill -HUP pid` ) に送信するか、HTTP `POST`リクエストを`http://prometheus-addr/-/reload`に送信します (HTTP リクエストを送信する前に、Prometheus の起動時に`--web.enable-lifecycle`パラメーターを追加します)。

推奨されるアラート項目は次のとおりです。

#### ログバックアップ実行RPO10m以上 {#logbackuprunningrpomorethan10m}

-   警告項目: `max(time() - tidb_log_backup_last_checkpoint / 262144000) by (task) / 60 > 10 and max(tidb_log_backup_last_checkpoint) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 0`
-   警戒レベル：警告
-   説明: ログ データがstorageに 10 分を超えて保存されません。このアラート項目はリマインダーです。ほとんどの場合、ログのバックアップには影響しません。

このアラート項目の設定サンプルは以下のとおりです。

```yaml
groups:
- name: PiTR
  rules:
  - alert: LogBackupRunningRPOMoreThan10m
    expr: max(time() - tidb_log_backup_last_checkpoint / 262144000) by (task) / 60 > 10 and max(tidb_log_backup_last_checkpoint) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 0
    labels:
      severity: warning
    annotations:
      summary: RPO of log backup is high
      message: RPO of the log backup task {{ $labels.task }} is more than 10m
```

#### ログバックアップ実行RPO30m以上 {#logbackuprunningrpomorethan30m}

-   警告項目: `max(time() - tidb_log_backup_last_checkpoint / 262144000) by (task) / 60 > 30 and max(tidb_log_backup_last_checkpoint) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 0`
-   警告レベル: クリティカル
-   説明: ログ データはstorageに 30 分を超えて保存されません。このアラートは多くの場合、異常を示します。 TiKV ログを確認して原因を見つけることができます。

#### ログバックアップ一時停止2時間以上 {#logbackuppausingmorethan2h}

-   警告項目: `max(time() - tidb_log_backup_last_checkpoint / 262144000) by (task) / 3600 > 2 and max(tidb_log_backup_last_checkpoint) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 1`
-   警戒レベル：警告
-   説明: ログ バックアップ タスクが 2 時間以上一時停止されています。このアラート項目はリマインダーであり、できるだけ早く`br log resume`を実行することが期待されます。

#### ログバックアップ一時停止12 時間以上 {#logbackuppausingmorethan12h}

-   警告項目: `max(time() - tidb_log_backup_last_checkpoint / 262144000) by (task) / 3600 > 12 and max(tidb_log_backup_last_checkpoint) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 1`
-   警告レベル: クリティカル
-   説明: ログ バックアップ タスクが 12 時間以上一時停止されています。タスクを再開するには、できるだけ早く`br log resume`を実行する必要があります。ログタスクの一時停止が長すぎると、データが失われるリスクがあります。

#### ログバックアップ失敗 {#logbackupfailed}

-   警告項目: `max(tikv_log_backup_task_status) by (task) == 2 and max(tidb_log_backup_last_checkpoint) by (task) > 0`
-   警告レベル: クリティカル
-   説明: ログバックアップタスクが失敗しました。失敗の理由を確認するには、 `br log status`を実行する必要があります。必要に応じて、TiKV ログをさらに確認する必要があります。

#### LogBackupGCSafePointExceedsCheckpoint {#logbackupgcsafepointexceedscheckpoint}

-   警告項目: `min(tidb_log_backup_last_checkpoint) by (instance) - max(tikv_gcworker_autogc_safe_point) by (instance) < 0`
-   警告レベル: クリティカル
-   説明: 一部のデータはバックアップ前にガベージ コレクションされました。これは、一部のデータが失われ、サービスに影響を与える可能性が非常に高いことを意味します。
