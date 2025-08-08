---
title: Monitoring and Alert for Backup and Restore
summary: このドキュメントでは、ログバックアップの監視、設定、Grafanaの設定、監視メトリクス、ログバックアップアラートなど、バックアップとリストアの監視とアラートについて説明します。PITRに推奨されるアラート項目とその設定についても説明します。
---

# バックアップと復元の監視とアラート {#monitoring-and-alert-for-backup-and-restore}

このドキュメントでは、監視コンポーネント、監視メトリック、一般的なアラートを展開する方法など、バックアップと復元機能の監視とアラートについて説明します。

## スナップショットのバックアップと復元の監視 {#snapshot-backup-and-restore-monitoring}

スナップショットのバックアップと復元のメトリックを表示するには、Grafana の[**TiKV詳細**&gt;**バックアップとインポート**ダッシュボード](/grafana-tikv-dashboard.md#backup--import)に移動します。

## ログバックアップ監視 {#log-backup-monitoring}

ログバックアップは、監視メトリックの収集に[プロメテウス](https://prometheus.io/)使用をサポートしています。現在、すべての監視メトリックはTiKVに組み込まれています。

### 監視構成 {#monitoring-configuration}

-   TiUPを使用してデプロイされたクラスターの場合、Prometheus は監視メトリックを自動的に収集します。
-   手動でデプロイされたクラスターの場合は、 [TiDBクラスタ監視の展開](/deploy-monitoring-services.md)の手順に従って、Prometheus 構成ファイルの`scrape_configs`セクションに TiKV 関連のジョブを追加します。

### Grafanaの設定 {#grafana-configuration}

-   TiUPを使用してデプロイされたクラスターの場合、ダッシュボード[グラファナ](https://grafana.com/)にポイントインタイムリカバリ (PITR) パネルが表示されます。TiKV-Details ダッシュボードの**バックアップログ**パネルが PITR パネルです。
-   手動でデプロイされたクラスターの場合は、 [Grafanaダッシュボードをインポートする](/deploy-monitoring-services.md#step-2-import-a-grafana-dashboard)を参照し、 [tikv_詳細](https://github.com/tikv/tikv/blob/release-8.5/metrics/grafana/tikv_details.json) JSON ファイルを Grafana にアップロードしてください。その後、TiKV-Details ダッシュボードの**バックアップログ**パネルを見つけてください。

### 監視メトリクス {#monitoring-metrics}

| メトリクス                                                  | タイプ    | 説明                                                                                                                                         |
| ------------------------------------------------------ | ------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **tikv_log_backup_internal_actor_acting_duration_sec** | ヒストグラム | すべての内部メッセージとイベントを処理する期間。<br/> `message :: TaskType`                                                                                        |
| **tikv_log_backup_initial_scan_reason**                | カウンタ   | 初期スキャンがトリガーされた理由の統計。主な理由は、リーダーの交代またはリージョンバージョンの変更です。<br/> `reason :: {"leader-changed", "region-changed", "retry"}`                        |
| **tikv_log_backup_event_handle_duration_sec**          | ヒストグラム | KVイベントの処理時間`tikv_log_backup_on_event_duration_seconds`と比較すると、この指標には内部変換の期間も含まれます。<br/> `stage :: {"to_stream_event", "save_to_temp_file"}` |
| **tikv_log_backup_handle_kv_batch**                    | ヒストグラム | Raftstoreによって送信された KV ペア バッチのサイズの領域レベルの統計。                                                                                                 |
| **tikv_log_backup_initial_scan_disk_read**             | カウンタ   | 初期スキャン中にディスクから読み取られたデータのサイズ。Linuxでは、この情報はprocfsから取得され、ブロックデバイスから実際に読み取られたデータのサイズです。このメトリックには、設定項目`initial-scan-rate-limit`適用されます。          |
| **tikv_log_backup_incremental_scan_bytes**             | ヒストグラム | 初期スキャン中に実際に生成されたKVペアのサイズ。圧縮とリードアンプリフィケーションのため、この値は`tikv_log_backup_initial_scan_disk_read`と異なる場合があります。                                     |
| **tikv_log_backup_skip_kv_count**                      | カウンタ   | バックアップに役立たないため、ログ バックアップ中にスキップされるRaftイベントの数。                                                                                               |
| **tikv_log_backup_errors**                             | カウンタ   | ログ バックアップ中に再試行または無視できるエラー。<br/> `type :: ErrorType`                                                                                        |
| **tikv_log_backup_fatal_errors**                       | カウンタ   | ログバックアップ中に再試行または無視できないエラー。このタイプのエラーが発生すると、ログバックアップは一時停止されます。<br/> `type :: ErrorType`                                                      |
| **tikv_log_backup_heap_memory**                        | ゲージ    | ログ バックアップ中の初期スキャンで検出された、消費されていないイベントによって占有されているメモリ。                                                                                        |
| **tikv_log_backup_on_event_duration_seconds**          | ヒストグラム | KV イベントを一時ファイルに保存する期間。<br/> `stage :: {"write_to_tempfile", "syscall_write"}`                                                              |
| **tikv_log_backup_store_checkpoint_ts**                | ゲージ    | ストアレベルのチェックポイントTSは非推奨です。現在のストアによって登録されたGCセーフポイントに近いです。<br/> `task :: string`                                                               |
| **tidb_log_backup_last_checkpoint**                    | ゲージ    | グローバルチェックポイントTS。ログデータがバックアップされている時点です。<br/> `task :: string`                                                                               |
| **tikv_log_backup_flush_duration_sec**                 | ヒストグラム | ローカルの一時ファイルを外部storageに移動する時間。<br/> `stage :: {"generate_metadata", "save_files", "clear_temp_files"}`                                      |
| **tikv_log_backup_flush_file_size**                    | ヒストグラム | バックアップ中に生成されたファイルのサイズの統計。                                                                                                                  |
| **tikv_log_backup_initial_scan_duration_sec**          | ヒストグラム | 初期スキャンの全体的な所要時間の統計。                                                                                                                        |
| **tikv_log_backup_skip_retry_observe**                 | カウンタ   | ログ バックアップ中に無視できるエラーの統計、または再試行がスキップされる理由。<br/> `reason :: {"region-absent", "not-leader", "stale-command"}`                                 |
| **tikv_log_backup_initial_scan_operations**            | カウンタ   | 初期スキャン中の RocksDB 関連操作の統計。<br/> `cf :: {"default", "write", "lock"}, op :: RocksDBOP`                                                       |
| **tikv_log_backup_enabled**                            | カウンタ   | ログバックアップを有効にするかどうか。値が`0`より大きい場合、ログバックアップは有効になります。                                                                                          |
| **tikv_log_backup_observed_region**                    | ゲージ    | リッスンされているリージョンの数。                                                                                                                          |
| **tikv_log_backup_task_status**                        | ゲージ    | ログ バックアップ タスクのステータス。1 `0`実行中、 `1`一時停止中、 `2`エラーを意味します。<br/> `task :: string`                                                                |
| **tikv_log_backup_pending_initial_scan**               | ゲージ    | 保留中の初期スキャンの統計。<br/> `stage :: {"queuing", "executing"}`                                                                                    |

### ログバックアップアラート {#log-backup-alerts}

#### アラート設定 {#alert-configuration}

現在、PITRにはアラート項目が組み込まれていません。このセクションでは、PITRでアラート項目を設定する方法と、推奨されるアラート項目をいくつか紹介します。

PITR でアラート項目を構成するには、次の手順に従います。

1.  Prometheusが配置されているノードのアラートルール用の設定ファイル（例： `pitr.rules.yml` ）を作成します。このファイルには、 [Prometheusのドキュメント](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/) 、以下の推奨アラート項目、および設定サンプルに従ってアラートルールを記述します。
2.  Prometheus 構成ファイルの`rule_files`フィールドに、アラート ルール ファイルのパスを追加します。
3.  Prometheusプロセスにシグナル`SIGHUP`送信するか（ `kill -HUP pid` ）、HTTPリクエスト`POST`を`http://prometheus-addr/-/reload`に送信します（HTTPリクエストを送信する前に、Prometheusの起動時にパラメータ`--web.enable-lifecycle`を追加します）。

推奨されるアラート項目は次のとおりです。

#### ログバックアップ実行RPO10分以上 {#logbackuprunningrpomorethan10m}

-   警告項目: `max(time() - tidb_log_backup_last_checkpoint / 262144000) by (task) / 60 > 10 and max(tidb_log_backup_last_checkpoint) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 0`
-   警戒レベル：警告
-   説明: ログデータが10分以上storageに保存されていません。このアラートはリマインダーです。ほとんどの場合、ログバックアップには影響しません。

このアラート項目の構成サンプルは次のとおりです。

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

#### ログバックアップ実行RPO30分以上 {#logbackuprunningrpomorethan30m}

-   警告項目: `max(time() - tidb_log_backup_last_checkpoint / 262144000) by (task) / 60 > 30 and max(tidb_log_backup_last_checkpoint) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 0`
-   警戒レベル: 重大
-   説明: ログデータが30分以上storageに保存されていません。このアラートは多くの場合、異常を示しています。原因を特定するには、TiKVログを確認してください。

#### ログバックアップ一時停止中 (2 時間以上) {#logbackuppausingmorethan2h}

-   警告項目: `max(time() - tidb_log_backup_last_checkpoint / 262144000) by (task) / 3600 > 2 and max(tidb_log_backup_last_checkpoint) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 1`
-   警戒レベル：警告
-   説明: ログバックアップタスクが2時間以上一時停止されています。このアラートはリマインダーであり、できるだけ早く`br log resume`実行してください。

#### ログバックアップ一時停止中（12時間以上） {#logbackuppausingmorethan12h}

-   警告項目: `max(time() - tidb_log_backup_last_checkpoint / 262144000) by (task) / 3600 > 12 and max(tidb_log_backup_last_checkpoint) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 1`
-   警戒レベル: 重大
-   説明: ログバックアップタスクが12時間以上一時停止されています。タスクを再開するには、できるだけ早く`br log resume`実行してください。ログタスクの一時停止時間が長すぎると、データが失われるリスクがあります。

#### ログバックアップ失敗 {#logbackupfailed}

-   警告項目: `max(tikv_log_backup_task_status) by (task) == 2 and max(tidb_log_backup_last_checkpoint) by (task) > 0`
-   警戒レベル: 重大
-   説明: ログバックアップタスクが失敗しました。失敗の原因を確認するには、 `br log status`実行する必要があります。必要に応じて、TiKV ログをさらに確認する必要があります。

#### ログバックアップGCセーフポイントがチェックポイントを超える {#logbackupgcsafepointexceedscheckpoint}

-   警告項目: `min(tidb_log_backup_last_checkpoint) by (instance) - max(tikv_gcworker_autogc_safe_point) by (instance) < 0`
-   警戒レベル: 重大
-   説明: バックアップ前に一部のデータがガベージコレクションされました。これは、一部のデータが失われており、サービスに影響を与える可能性が非常に高いことを意味します。
