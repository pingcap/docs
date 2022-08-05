---
title: PiTR Monitoring and Alert
summary: Learn the monitoring and alert of the PiTR feature.
---

# PiTR Monitoring and Alert

PiTR supports using [Prometheus](https://prometheus.io/) to collect monitoring metrics. Currently all monitoring metrics are built into TiKV.

## Monitoring configuration

- For clusters deployed using TiUP, [Prometheus](https://prometheus.io/) automatically collects monitoring metrics.
- For clusters deployed manually, follow the instructions in [TiDB Cluster Monitoring Deployment](/deploy-monitoring-services.md) to add TiKV-related jobs to the `scrape_configs` section of the Prometheus configuration file.

## Monitoring metrics

| Metrics                                                | Type    |  Description                                                                                                                                                 |
|-------------------------------------------------------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| **tikv_log_backup_interal_actor_acting_duration_sec** | Histogram | The duration of handling all internal message events. <br/>`message :: TaskType`                                                                                                            |
| **tikv_log_backup_initial_scan_reason**               | Counter   | Statistics of the reasons why initial scan is triggered. The main reason is leader transfer or Region version change. <br/> `reason :: {"leader-changed", "region-changed", "retry"}`                                           |
| **tikv_log_backup_event_handle_duration_sec**         | Histogram | The duration of handling KV events. Compared with `tikv_log_backup_on_event_duration_seconds`, this metric also includes the duration of internal conversion. <br/>`stage :: {"to_stream_event", "save_to_temp_file"}` |
| **tikv_log_backup_handle_kv_batch**                   | Histogram |  Region-level statistics of the sizes of KV pair batches sent by Raftstore.                                                                                                    |
| **tikv_log_backup_initial_scan_disk_read**            | Counter   | The size of data read from the disk during initial scan. In Linux, this information is from procfs, which is the data size actually read from the block device. The configuration item `initial-scan-rate-limit` also imposes limit on this data size value.                                   |
| **tikv_log_backup_incremental_scan_bytes**            | Histogram | The size of KV pairs actually generated during initial scan. Because of compression and read amplification, this value might be different from that of `tikv_log_backup_initial_scan_disk_read`.                                                                  |
| **tikv_log_backup_skip_kv_count**                     | Counter   |  The number of Raft events being skipped during the log backup because they are not helpful to the backup.                                                                                                                   |
| **tikv_log_backup_errors**                            | Counter   | The errors that can be retried or ignored during the log backup. <br/>`type :: ErrorType`                                                                                                       |
| **tikv_log_backup_fatal_errors**                      | Counter   | The errors that cannot be retried or ignored during the log backup. When an error of this type occurs, the log backup is paused. <br/>`type :: ErrorType`                                                                                   |
| **tikv_log_backup_heap_memory**                       | Gauge     |  The memory occupied by events that are unconsumed and found by initial scan during log backup.                                                                                                                         |
| **tikv_log_backup_on_event_duration_seconds**         | Histogram |  The duration of storing KV events to temporary files. <br/>`stage :: {"write_to_tempfile", "syscall_write"}`                                                                        |
| **tikv_log_backup_store_checkpoint_ts**               | Gauge     | The store-level Checkpoint TS, which is deprecated. It is close to the GC safepoint registered by the current store. <br/>`task :: string`                                                                    |
| **tikv_log_backup_flush_duration_sec**                | Histogram |  The duration of moving local temporary files to the external storage. <br/>`stage :: {"generate_metadata", "save_files", "clear_temp_files"}`                                                                |
| **tikv_log_backup_flush_file_size**                   | Histogram |  Statistics of the sizes of files generated during the backup.                                                                                                                                          |
| **tikv_log_backup_initial_scan_duration_sec**         | Histogram | The statistics of the overall duration of initial scan.                                                                                                                                           |
| **tikv_log_backup_skip_retry_observe**                | Counter   | Statistics of the errors that can be ignored during log backup, which skips the retries.  <br/>`reason :: {"region-absent", "not-leader", "stale-command"}`                                                   |
| **tikv_log_backup_initial_scan_operations**           | Counter   | Statistics of RocksDB-related operations during initial scan. <br/>`cf :: {"default", "write", "lock"}, op :: RocksDBOP`                                                                       |
| **tikv_log_backup_enabled**                           | Counter   |  Whether to enable log backup. If the value is greater than `0`, log backup is enabled.                                                                                                                                |
| **tikv_log_backup_observed_region**                   | Gauge     | The number of Regions being listened to.                                                                                                                                        |
| **tikv_log_backup_task_status**                       | Gauge     | The status of the log backup task. `0` means running. `1` means paused. `2` means error.  <br/>`task :: string`                                                                                                |
| **tikv_log_backup_pending_initial_scan**              | Gauge     | Statistics of pending initial scans. <br/>`stage :: {"queuing", "executing"}`                                                                                                     |

## Grafana configuration

- For clusters deployed using TiUP, the [Grafana](https://grafana.com/) dashboard contains the PiTR panel. The **Backup Log** panel in the TiKV-Details dashboard is the PiTR panel.
- For clusters deployed manually, refer to [Import a Grafana dashboard](/deploy-monitoring-services.md#step-2-import-a-grafana-dashboard) and upload the [tikv_details](https://github.com/tikv/tikv/blob/master/metrics/grafana/tikv_details.json) JSON file to Grafana. Then find the **Backup Log** panel in the TiKV-Details dashboard.

## Alert configuration

Currently, PiTR does not have built-in alert items, but the following alert items are recommended.

### LogBackupRunningRPOMoreThan10m

- Alert item: `max(time() - tikv_stream_store_checkpoint_ts / 262144000) by (task) / 60 > 10 and max(tikv_stream_store_checkpoint_ts) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 0`
- Alert level: warning
- Description: The log data is not persisted to the storage for more than 10 minutes. This alert item is a reminder. In most cases, it does not affect log backup.

### LogBackupRunningRPOMoreThan30m

- Alert item: `max(time() - tikv_stream_store_checkpoint_ts / 262144000) by (task) / 60 > 30 and max(tikv_stream_store_checkpoint_ts) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 0`
- Alert level: critical
- Description: The log data is not persisted to the storage for more than 30 minutes. This alert often indicates anomalies. You can check the TiKV logs to find the cause.

### LogBackupPausingMoreThan2h

- Alert item: `max(time() - tikv_stream_store_checkpoint_ts / 262144000) by (task) / 3600 > 2 and max(tikv_stream_store_checkpoint_ts) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 1`
- Alert level: warning
- Description: The log backup task is paused for more than 2 hours. This alert item is a reminder and you are expected to run `br log resume` as soon as possible.

### LogBackupPausingMoreThan12h

- Alert item: `max(time() - tikv_stream_store_checkpoint_ts / 262144000) by (task) / 3600 > 12 and max(tikv_stream_store_checkpoint_ts) by (task) > 0 and max(tikv_log_backup_task_status) by (task) == 1`
- Alert level: critical
- Description: The log backup task is paused for more than 12 hours. You are expected to run `br log resume` as soon as possible to resume the task. Log tasks paused for too long have the risk of data loss.

### LogBackupFailed

- Alert item: `max(tikv_log_backup_task_status) by (task) == 2 and max(tikv_stream_store_checkpoint_ts) by (task) > 0`
- Alert level: critical
- Description: The log backup task fails. You need to run `br log status` to see the failure reason. If necessary, you need to further check the TiKV logs.

### LogBackupGCSafePointExceedsCheckpoint

- Alert item: `min(tikv_stream_store_checkpoint_ts) by (instance) - max(tikv_gcworker_autogc_safe_point) by (instance) < 0`
- Alert level: critical
- Description: Some data has been garbage-collected before the backup. This means that some data has been lost and are very likely to affect your application.
