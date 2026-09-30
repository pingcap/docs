---
title: Data Migration Monitoring Metrics
summary: Data Migration を使用してデータを移行する場合の監視メトリックについて説明します。
---

# データ移行監視メトリクス {#data-migration-monitoring-metrics}

DM クラスターがTiUPを使用してデプロイされている場合、 [監視システム](/dm/migrate-data-using-dm.md#step-8-monitor-the-task-and-check-logs)も同時にデプロイされます。このドキュメントでは、DM-worker が提供する監視メトリクスについて説明します。

## タスク {#task}

Grafana ダッシュボードでは、DM のデフォルト名は`DM-task`です。

### `overview` {#overview}

`Overview`には、現在選択されているタスク内のすべての DM-workerおよび DM-masterインスタンスまたはソースのいくつかの監視メトリクスが含まれています。現在のデフォルトのアラートルールは、単一の DM-worker/DM-masterインスタンス/ソースのみに適用されます。

| メトリック名                       | 説明                                                                                | 警告   | 重大度レベル |
| :--------------------------- | :-------------------------------------------------------------------------------- | :--- | :----- |
| task state | 移行のサブタスクの状態                                                                       | 該当なし | 該当なし   |
| storage capacity | リレーログが占めるディスクの総ストレージ容量                                                          | 該当なし | 該当なし   |
| storage remain | リレーログが占めるディスクの残りストレージ容量                                                         | 該当なし | 該当なし   |
| binlog file gap between master and relay | `relay`処理ユニットが上流マスターより遅れているbinlogファイルの数                                           | 該当なし | 該当なし   |
| load progress | ロードユニットの完了したロードプロセスの割合。値は0%～100%です。                                               | 該当なし | 該当なし   |
| binlog file gap between master and syncer | binlogレプリケーションユニットが上流マスターより遅れているbinlogファイルの数                                      | 該当なし | 該当なし   |
| shard lock resolving | 現在のサブタスクがシャーディングDDLの移行を待機しているかどうか。0より大きい値は、現在のサブタスクがシャーディングDDLの移行を待機していることを意味します。 | 該当なし | 該当なし   |

### 操作エラー {#operation-errors}

| メトリック名       | 説明                    | 警告   | 重大度レベル |
| :----------- | :-------------------- | :--- | :----- |
| before any operate error | 操作前のエラー数              | 該当なし | 該当なし   |
| source bound error | データソースバインディング操作のエラー数  | 該当なし | 該当なし   |
| start error | サブタスクの開始時に発生したエラーの数   | 該当なし | 該当なし   |
| pause error | サブタスクの一時停止中に発生したエラーの数 | 該当なし | 該当なし   |
| resume error | サブタスクの再開中に発生したエラーの数   | 該当なし | 該当なし   |
| auto-resume error | サブタスクの自動再開中に発生したエラーの数 | 該当なし | 該当なし   |
| update error | サブタスクの更新中に発生したエラーの数   | 該当なし | 該当なし   |
| stop error | サブタスクの停止中に発生したエラーの数   | 該当なし | 該当なし   |

### 高可用性 {#high-availability}

| メトリック名                      | 説明                                          | 警告                               | 重大度レベル |
| :-------------------------- | :------------------------------------------ | :------------------------------- | :----- |
| number of dm-masters start leader components per minute | DM-masterがリーダー関連コンポーネントを有効にしようとする 1分あたりの試行回数 | 該当なし                             | 該当なし   |
| number of workers in different state | さまざまな状態のDM-workerの数                          | 一部の DM-workerが 1時間以上オフラインになっています  | 致命的    |
| workers' state | DM-workerの状態                                   | 該当なし                             | 該当なし   |
| number of worker event error | DM-workerエラーのさまざまなタイプの数                        | 該当なし                             | 該当なし   |
| shard ddl error per minute | 1分あたりのさまざまな種類のシャーディング DDL エラーの数            | シャーディングDDLエラーが発生した場合             | 致命的    |
| number of pending shard ddl | 保留中のシャーディングDDL操作の数                          | 保留中のシャーディング DDL 操作が 1時間以上経過している | 致命的    |

### タスクの状態 {#task-state}

| メトリック名 | 説明       | 警告                                     | 重大度レベル |
| :----- | :------- | :------------------------------------- | :----- |
| task state | サブタスクの状態 | サブタスクが20分以上`Paused`状態にある場合、アラートが発生します。 | 致命的    |

### ダンプ/ロードユニット {#dump-load-unit}

次のメトリックは、 `task-mode`が`full`または`all`モードの場合にのみ表示されます。

| メトリック名             | 説明                                                                 | 警告     | 重大度レベル |
| :----------------- | :----------------------------------------------------------------- | :----- | :----- |
| dump progress | ダンプユニットの完了したダンプ処理の割合。値の範囲は0%～100%です。                               | 該当なし   | 該当なし   |
| load progress | ロードユニットの完了したロードプロセスの割合。値の範囲は0%～100%です。                             | 該当なし   | 該当なし   |
| checksum progress | ロードユニットがダンプを終了した後のチェックサム処理の完了率。値の範囲は0%～100%です。                     | 該当なし   | 該当なし   |
| total bytes for load unit | ロードユニットによるインポートプロセスの解析、データKVの生成、およびインデックスKVの生成の各段階で処理されたバイト        | 該当なし   | 該当なし   |
| chunk process duration | ロードユニットがデータソースファイルチャンクを処理する時間（秒）                                   | 該当なし   | 該当なし   |
| data file size | ロードユニットによってインポートされた完全なデータ内のデータファイルの合計サイズ（ `INSERT INTO`文を含む） | 該当なし   | 該当なし   |
| dump process exits with error | ダンプユニットはDM-worker内でエラーに遭遇し、終了します。                                     | 即時アラート | 致命的    |
| load process exits with error | ロードユニットはDM-worker内でエラーに遭遇し、終了します。                                     | 即時アラート | 致命的    |

### Binlogレプリケーション {#binlog-replication}

次のメトリックは、 `task-mode`が`incremental`または`all`モードの場合にのみ表示されます。

| メトリック名                       | 説明                                                                       | 警告                                                                                     | 重大度レベル |
| :--------------------------- | :----------------------------------------------------------------------- | :------------------------------------------------------------------------------------- | :----- |
| remaining time to sync | `syncer`がアップストリーム マスターに完全に移行されるまでにかかる予測残り時間 (分)                           | 該当なし                                                                                   | 該当なし   |
| replicate lag gauge | binlogを上流から下流に複製するのにかかるレイテンシー時間（秒）                                       | 該当なし                                                                                   | 該当なし   |
| replicate lag histogram | 上流から下流へのbinlogの複製のヒストグラム（秒単位）。統計メカニズムが異なるため、データが不正確になる可能性があることに注意してください。 | 該当なし                                                                                   | 該当なし   |
| process exist with error | binlogレプリケーションユニットはDM-worker内でエラーに遭遇し、終了します。                                | 即時アラート                                                                                 | 致命的    |
| binlog file gap between master and syncer | `syncer`処理ユニットが上流マスターより遅れているbinlogファイルの数                                 | `syncer`処理ユニットが上流マスターより遅れているbinlogファイルの数が1つ（&gt; 1）を超え、その状態が10分以上続くと、アラートが発生します。       | 致命的    |
| binlog file gap between relay and syncer | `syncer`が`relay`より遅れているbinlogファイルの数                                        | `syncer`処理ユニットが`relay`処理ユニットより遅れているbinlogファイルの数が1つを超え（&gt;1）、その状態が10分以上続くと、アラートが発生します。 | 致命的    |
| binlog event QPS | 単位時間あたりに受信したbinlogイベントの数 (この数にはスキップする必要があるイベントは含まれません)                   | 該当なし                                                                                   | 該当なし   |
| skipped binlog event QPS | スキップする必要がある単位時間あたりに受信されたbinlogイベントの数                                     | 該当なし                                                                                   | 該当なし   |
| read binlog event duration | binlogレプリケーションユニットがリレーログまたは上流のMySQLからbinlogを読み取る時間（秒）                    | 該当なし                                                                                   | 該当なし   |
| transform binlog event duration | binlogレプリケーションユニットがbinlogを解析してSQL文に変換する時間（秒）                             | 該当なし                                                                                   | 該当なし   |
| dispatch binlog event duration | binlogレプリケーションユニットがbinlogイベントを送信する期間（秒）                                  | 該当なし                                                                                   | 該当なし   |
| transaction execution latency | binlogレプリケーションユニットが下流へのトランザクションを実行する期間（秒）                                | 該当なし                                                                                   | 該当なし   |
| binlog event size | binlogレプリケーションユニットがリレーログまたは上流のMySQLから読み取るbinlogイベントのサイズ                  | 該当なし                                                                                   | 該当なし   |
| DML queue remain length | 残りのDMLジョブキューの長さ                                                          | 該当なし                                                                                   | 該当なし   |
| total sqls jobs | 単位時間あたりに新しく追加されたジョブの数                                                            | 該当なし                                                                                   | 該当なし   |
| finished sqls jobs | 単位時間あたりに完了したジョブの数                                                         | 該当なし                                                                                   | 該当なし   |
| statement execution latency | binlogレプリケーションユニットが下流へのステートメントを実行する期間（秒）                                 | 該当なし                                                                                   | 該当なし   |
| add job duration | binlogレプリケーションユニットがキューにジョブを追加する期間（秒）                                     | 該当なし                                                                                   | 該当なし   |
| DML conflict detect duration | binlogレプリケーションユニットがDMLの競合を検出する期間（秒）                                      | 該当なし                                                                                   | 該当なし   |
| skipped event duration | binlogレプリケーションユニットがbinlogイベントをスキップする期間（秒）                                | 該当なし                                                                                   | 該当なし   |
| unsynced tables | 現在のサブタスクでシャードDDL文を受け取っていないテーブルの数                                         | 該当なし                                                                                   | 該当なし   |
| shard lock resolving | 現在のサブタスクがシャードDDLロックの解決を待機しているかどうか。0より大きい値は、シャードDDLロックの解決を待機していることを示します。  | 該当なし                                                                                   | 該当なし   |
| ideal QPS | DMの実行時間が0のときに達成できる最高のQPS                                                 | 該当なし                                                                                   | 該当なし   |
| binlog event row | binlogイベントの行数                                                            | 該当なし                                                                                   | 該当なし   |
| finished transaction total | 完了したトランザクションの合計数                                                               | 該当なし                                                                                   | 該当なし   |
| replication transaction batch | 下流に実行されたトランザクション内のSQL行の数                                                 | 該当なし                                                                                   | 該当なし   |
| flush checkpoints time interval | チェックポイントをフラッシュする時間間隔（秒）                                                  | 該当なし                                                                                   | 該当なし   |

### リレーログ {#relay-log}

> **Note:**
>
> 現在、DM v2.0 ではリレーログ機能の有効化はサポートされていません。

| メトリック名                    | 説明                                                            | 警告                                                                              | 重大度レベル |
| :------------------------ | :------------------------------------------------------------ | :------------------------------------------------------------------------------ | :----- |
| storage capacity | リレーログが占有するディスクのストレージ容量                                      | 該当なし                                                                            | 該当なし   |
| storage remain | リレーログが占有するディスクの残りストレージ容量                                    | 値が10G未満になるとアラートが必要になります                                                         | 致命的    |
| process exits with error | リレーログはDM-worker内でエラーが発生し、終了します。                                  | 即時アラート                                                                          | 致命的    |
| relay log data corruption | 破損したリレーログファイルの数                                               | 即時アラート                                                                          | 緊急     |
| fail to read binlog from master | リレーログが上流のMySQLからbinlogを読み込む際に発生したエラーの数                        | 即時アラート                                                                          | 致命的    |
| fail to write relay log | リレーログがbinlogをディスクに書き込むときに発生したエラーの数                            | 即時アラート                                                                          | 致命的    |
| binlog file index | リレーログファイルの最大インデックス番号。例えば、"value = 1"は"relay-log.000001"を示します。 | 該当なし                                                                            | 該当なし   |
| binlog file gap between master and relay | 上流マスターの背後にあるリレーログ内のbinlogファイルの数                               | `relay`処理ユニットが上流マスターより遅れているbinlogファイルの数が1つ（&gt; 1）を超え、その状態が10分以上続くと、アラートが発生します。 | 致命的    |
| binlog pos | 最新のリレーログファイルの書き込みオフセット                                        | 該当なし                                                                            | 該当なし   |
| read binlog event duration | リレーログが上流のMySQLからbinlogを読み取る時間（秒）                              | 該当なし                                                                            | 該当なし   |
| write relay log duration | リレーログが毎回ディスクにbinlogを書き込む時間（秒）                                 | 該当なし                                                                            | 該当なし   |
| binlog event size | リレーログがディスクに書き込む単一のbinlogイベントのサイズ                              | 該当なし                                                                            | 該当なし   |

## インスタンス {#instance}

Grafana ダッシュボードでは、インスタンスのデフォルト名は`DM-instance`です。

### リレーログ {#relay-log}

| メトリック名                    | 説明                                                            | 警告                                                                              | 重大度レベル |
| :------------------------ | :------------------------------------------------------------ | :------------------------------------------------------------------------------ | :----- |
| storage capacity | リレーログが占有するディスクの総ストレージ容量                                     | 該当なし                                                                            | 該当なし   |
| storage remain | リレーログが占めるディスク内の残りのストレージ容量                                   | 値が10G未満になるとアラートが発生します                                                           | 致命的    |
| process exits with error | リレーログはDM-workerでエラーが発生し、終了します                                    | 即時アラート                                                                          | 致命的    |
| relay log data corruption | 破損したリレーログの数                                                   | 即時アラート                                                                          | 緊急     |
| fail to read binlog from master | リレーログが上流のMySQLからbinlogを読み込む際に発生したエラーの数                        | 即時アラート                                                                          | 致命的    |
| fail to write relay log | リレーログがbinlogをディスクに書き込むときに発生したエラーの数                            | 即時アラート                                                                          | 致命的    |
| binlog file index | リレーログファイルの最大インデックス番号。例えば、"value = 1"は"relay-log.000001"を示します。 | 該当なし                                                                            | 該当なし   |
| binlog file gap between master and relay | `relay`処理ユニットが上流マスターより遅れているbinlogファイルの数                       | `relay`処理ユニットが上流マスターより遅れているbinlogファイルの数が1つ（&gt; 1）を超え、その状態が10分以上続くと、アラートが発生します。 | 致命的    |
| binlog pos | 最新のリレーログファイルの書き込みオフセット                                        | 該当なし                                                                            | 該当なし   |
| read binlog duration | リレーログが上流のMySQLからbinlogを読み取る時間（秒）                              | 該当なし                                                                            | 該当なし   |
| write relay log duration | リレーログがbinlogをディスクに書き込む時間（秒）                                   | 該当なし                                                                            | 該当なし   |
| binlog size | リレーログがディスクに書き込む単一のbinlogイベントのサイズ                              | 該当なし                                                                            | 該当なし   |

### タスク {#task}

| メトリック名                       | 説明                                                                                | 警告                            | 重大度レベル |
| :--------------------------- | :-------------------------------------------------------------------------------- | :---------------------------- | :----- |
| task state | 移行のサブタスクの状態                                                                       | サブタスクが10分以上一時停止されるとアラートが発生します | 致命的    |
| load progress | ロードユニットの完了したロードプロセスの割合。値の範囲は0%～100%です。                                            | 該当なし                          | 該当なし   |
| binlog file gap between master and syncer | binlogレプリケーションユニットが上流マスターより遅れているbinlogファイルの数                                      | 該当なし                          | 該当なし   |
| shard lock resolving | 現在のサブタスクがシャーディングDDLの移行を待機しているかどうか。0より大きい値は、現在のサブタスクがシャーディングDDLの移行を待機していることを意味します。 | 該当なし                          | 該当なし   |
