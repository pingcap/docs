---
title: Monitoring and Alert for Backup and Restore
summary: Learn the monitoring and alert of the backup and restore feature.
---

# バックアップと復元の監視とアラート {#monitoring-and-alert-for-backup-and-restore}

このドキュメントでは、バックアップおよび復元機能の監視とアラートについて説明します。これには、監視コンポーネントのデプロイ方法、監視メトリック、および一般的なアラートが含まれます。

## ログバックアップ監視 {#log-backup-monitoring}

ログ バックアップでは、監視メトリックを収集するために[プロメテウス](https://prometheus.io/)を使用することがサポートされています。現在、すべての監視メトリクスは TiKV に組み込まれています。

### 監視構成 {#monitoring-configuration}

-   TiUPを使用してデプロイされたクラスターの場合、Prometheus はモニタリング メトリックを自動的に収集します。
-   手動でデプロイされたクラスターの場合、 [TiDBクラスタ監視の展開](/deploy-monitoring-services.md)の手順に従って、TiKV 関連のジョブを Prometheus 構成ファイルの`scrape_configs`セクションに追加します。

### グラファナ構成 {#grafana-configuration}

-   TiUPを使用してデプロイされたクラスターの場合、 [グラファナ](https://grafana.com/)ダッシュボードにはポイントインタイム リカバリー (PITR) パネルが含まれます。 TiKV-Details ダッシュボードの**Backup Log**パネルは PITR パネルです。
-   手動でデプロイされたクラスターの場合は、 [Grafana ダッシュボードをインポートする](/deploy-monitoring-services.md#step-2-import-a-grafana-dashboard)を参照し、 [tikv_details](https://github.com/tikv/tikv/blob/master/metrics/grafana/tikv_details.json) JSON ファイルを Grafana にアップロードします。次に、TiKV-Details ダッシュボードで**[Backup Log]**パネルを見つけます。

### 指標のモニタリング {#monitoring-metrics}

| 指標                                                    | タイプ    | 説明                                                                                                                                                    |
| ----------------------------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **tikv_log_backup_interal_actor_acting_duration_sec** | ヒストグラム | すべての内部メッセージとイベントを処理する期間。<br/> `message :: TaskType`                                                                                                   |
| **tikv_log_backup_initial_scan_reason**               | カウンター  | 初期スキャンがトリガーされた理由の統計。主な理由は、リーダーの移動またはリージョンのバージョンの変更です。<br/> `reason :: {"leader-changed", "region-changed", "retry"}`                                  |
| **tikv_log_backup_event_handle_duration_sec**         | ヒストグラム | KV イベントの処理期間。 `tikv_log_backup_on_event_duration_seconds`と比較すると、このメトリックには内部コンバージョンの期間も含まれます。<br/> `stage :: {"to_stream_event", "save_to_temp_file"}` |
| **tikv_log_backup_handle_kv_batch**                   | ヒストグラム | Raftstoreによって送信された KV ペア バッチのサイズのリージョン レベルの統計。                                                                                                        |
| **tikv_log_backup_initial_scan_disk_read**            | カウンター  | 初期スキャン中にディスクから読み取られたデータのサイズ。 Linux では、この情報はブロック デバイスから実際に読み取られたデータのサイズである procfs からのものです。構成項目`initial-scan-rate-limit`がこのメトリックに適用されます。                |
| **tikv_log_backup_incremental_scan_bytes**            | ヒストグラム | 初期スキャン中に実際に生成された KV ペアのサイズ。圧縮と読み取り増幅のため、この値は`tikv_log_backup_initial_scan_disk_read`の値とは異なる場合があります。                                                   |
| **tikv_log_backup_skip_kv_count**                     | カウンター  | バックアップに役立たないため、ログ バックアップ中にスキップされたRaftイベントの数。                                                                                                          |
| **tikv_log_backup_errors**                            | カウンター  | ログ バックアップ中に再試行または無視できるエラー。<br/> `type :: ErrorType`                                                                                                   |
| **tikv_log_backup_fatal_errors**                      | カウンター  | ログ バックアップ中に再試行または無視できないエラー。このタイプのエラーが発生すると、ログ バックアップは一時停止されます。<br/> `type :: ErrorType`                                                               |
| **tikv_log_backup_heap_memory**                       | ゲージ    | ログ バックアップ中に初期スキャンで検出された未使用のイベントが占めるメモリ。                                                                                                               |
| **tikv_log_backup_on_event_duration_seconds**         | ヒストグラム | KV イベントを一時ファイルに保存する期間。<br/> `stage :: {"write_to_tempfile", "syscall_write"}`                                                                         |
| **tikv_log_backup_store_checkpoint_ts**               | ゲージ    | 非推奨のストア レベル チェックポイント TS。現店舗が登録しているGCセーフポイントに近いです。<br/> `task :: string`                                                                               |
| **tidb_log_backup_last_checkpoint**                   | ゲージ    | グローバル チェックポイント TS。ログデータをバックアップした時点までです。<br/> `task :: string`                                                                                         |
| **tikv_log_backup_flush_duration_sec**                | ヒストグラム | ローカルの一時ファイルを外部storageに移動する期間。<br/> `stage :: {"generate_metadata", "save_files", "clear_temp_files"}`                                                 |
| **tikv_log_backup_flush_file_size**                   | ヒストグラム | バックアップ中に生成されたファイルのサイズの統計。                                                                                                                             |
| **tikv_log_backup_initial_scan_duration_sec**         | ヒストグラム | 初期スキャンの全体的な期間の統計。                                                                                                                                     |
| **tikv_log_backup_skip_retry_observe**                | カウンター  | ログ バックアップ中に無視できるエラーの統計、または再試行がスキップされた理由。<br/> `reason :: {"region-absent", "not-leader", "stale-command"}`                                            |
| **tikv_log_backup_initial_scan_operations**           | カウンター  | 初期スキャン中の RocksDB 関連操作の統計。<br/> `cf :: {"default", "write", "lock"}, op :: RocksDBOP`                                                                  |
| **tikv_log_backup_enabled**                           | カウンター  | ログのバックアップを有効にするかどうか。値が`0`より大きい場合、ログ バックアップは有効です。                                                                                                      |
| **tikv_log_backup_observed_region**                   | ゲージ    | リッスンされているリージョンの数。                                                                                                                                     |
| **tikv_log_backup_task_status**                       | ゲージ    | ログ バックアップ タスクのステータス。 `0`実行中を意味します。 `1`一時停止を意味します。 `2`エラーを意味します。<br/> `task :: string`                                                                 |
| **tikv_log_backup_pending_initial_scan**              | ゲージ    | 保留中の初期スキャンの統計。<br/> `stage :: {"queuing", "executing"}`                                                                                               |

### バックアップ アラートをログに記録する {#log-backup-alerts}

#### アラート構成 {#alert-configuration}

現在、PITR には組み込みのアラート項目がありません。このセクションでは、PITR でアラート項目を構成する方法と、いくつかの項目を推奨する方法を紹介します。

PITR でアラート アイテムを構成するには、次の手順に従います。

1.  Prometheus が配置されているノードで、アラート ルールの構成ファイル (たとえば、 `pitr.rules.yml` ) を作成します。ファイルには、 [プロメテウスのドキュメント](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/) 、次の推奨されるアラート項目、および構成サンプルに従って、アラート ルールを入力します。
2.  Prometheus 構成ファイルの`rule_files`フィールドに、アラート ルール ファイルのパスを追加します。
3.  Prometheus プロセスに`SIGHUP`シグナルを送信する ( `kill -HUP pid` ) か、HTTP `POST`リクエストを`http://prometheus-addr/-/reload`に送信します (HTTP リクエストを送信する前に、Prometheus の起動時に`--web.enable-lifecycle`パラメーターを追加します)。

推奨されるアラート項目は次のとおりです。

#### LogBackupRunningRPO10m 以上 {#logbackuprunningrpomorethan10m}

-   アラート項目: `max(time() - tidb_log_backup_last_checkpoint / 262144000) by (task) / 60 > 10 and max(tidb_log_backup_last_checkpoint) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 0`
-   アラート レベル: 警告
-   説明: ログ データがstorageに 10 分以上保存されていません。このアラート項目はリマインダーです。ほとんどの場合、ログ バックアップには影響しません。

このアラート項目の構成例は次のとおりです。

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

#### ログバックアップの実行中の RPO は 30 分以上 {#logbackuprunningrpomorethan30m}

-   アラート項目: `max(time() - tidb_log_backup_last_checkpoint / 262144000) by (task) / 60 > 30 and max(tidb_log_backup_last_checkpoint) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 0`
-   警告レベル: 重大
-   説明: ログ データがstorageに 30 分以上保存されていません。このアラートは多くの場合、異常を示します。 TiKV ログをチェックして、原因を見つけることができます。

#### LogBackupPausingMoreThan2h {#logbackuppausingmorethan2h}

-   アラート項目: `max(time() - tidb_log_backup_last_checkpoint / 262144000) by (task) / 3600 > 2 and max(tidb_log_backup_last_checkpoint) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 1`
-   アラート レベル: 警告
-   説明: ログ バックアップ タスクが 2 時間以上一時停止しています。この警告項目はリマインダーであり、できるだけ早く`br log resume`を実行する必要があります。

#### LogBackupPausingMoreThan12h {#logbackuppausingmorethan12h}

-   アラート項目: `max(time() - tidb_log_backup_last_checkpoint / 262144000) by (task) / 3600 > 12 and max(tidb_log_backup_last_checkpoint) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 1`
-   警告レベル: 重大
-   説明: ログ バックアップ タスクが 12 時間以上一時停止しています。タスクを再開するには、できるだけ早く`br log resume`を実行する必要があります。一時停止したログ タスクが長すぎると、データ損失のリスクがあります。

#### ログバックアップ失敗 {#logbackupfailed}

-   アラート項目: `max(tikv_log_backup_task_status) by (task) == 2 and max(tidb_log_backup_last_checkpoint) by (task) > 0`
-   警告レベル: 重大
-   説明: ログ バックアップ タスクが失敗します。失敗の理由を確認するには、 `br log status`を実行する必要があります。必要に応じて、TiKV ログをさらに確認する必要があります。

#### LogBackupGCSafePointExceedsCheckpoint {#logbackupgcsafepointexceedscheckpoint}

-   アラート項目: `min(tidb_log_backup_last_checkpoint) by (instance) - max(tikv_gcworker_autogc_safe_point) by (instance) < 0`
-   警告レベル: 重大
-   説明: 一部のデータは、バックアップの前にガベージ コレクションされました。これは、一部のデータが失われ、サービスに影響を与える可能性が非常に高いことを意味します。
