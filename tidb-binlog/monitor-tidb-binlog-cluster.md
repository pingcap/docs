---
title: TiDB Binlog Monitoring
summary: TiDB Binlogのクラスター バージョンを監視する方法を学習します。
---

# TiDBBinlog監視 {#tidb-binlog-monitoring}

TiDB Binlog を正常にデプロイしたら、Grafana Web (デフォルト アドレス: [http://grafana_ip:3000](http://grafana_ip:3000) 、デフォルト アカウント: admin、パスワード: admin) にアクセスして、 PumpとDrainerの状態を確認できます。

## 監視メトリクス {#monitoring-metrics}

TiDB Binlog は、 PumpとDrainer の2 つのコンポーネントで構成されています。このセクションでは、 PumpとDrainerの監視メトリックを示します。

### Pump監視メトリクス {#pump-monitoring-metrics}

Pump監視メトリックを理解するには、次の表を確認してください。

| Pump監視メトリクス               | 説明                                                                                     |
| ------------------------- | -------------------------------------------------------------------------------------- |
| ストレージサイズ                  | ディスクの総容量（容量）と使用可能なディスク容量（使用可能）を記録します                                                   |
| メタデータ                     | 各Pumpノードが削除できるbinlogの最大TSO（ `gc_tso` ）と保存されたbinlogの最大コミットTSO（ `max_commit_tso` ）を記録する。 |
| インスタンスごとのBinlog QPS の書き込み | 各Pumpノードが受信したbinlog書き込み要求のQPSを表示します。                                                   |
| Binlog書き込み遅延              | 各Pumpノードがbinlogを書き込む際のレイテンシーを記録します。                                                    |
| ストレージ書き込みBinlogサイズ        | Pumpによって書き込まれたbinlogデータのサイズを表示します                                                      |
| ストレージ書き込みBinlogレイテンシ      | Pumpstorageモジュールのbinlog書き込みのレイテンシーを記録します。                                              |
| Pumpストレージエラーの種類           | Pumpが遭遇したエラーの数をエラーの種類に基づいて記録します。                                                       |
| クエリ TiKV                  | PumpがTiKVを通じてトランザクションステータスを照会する回数                                                      |

### Drainer監視メトリクス {#drainer-monitoring-metrics}

Drainer の監視メトリックを理解するには、次の表を確認してください。

| Drainer監視メトリクス                | 説明                                                                                                                                                             |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| チェックポイントTSO                   | Drainer がダウンストリームにすでに複製したbinlogの最大 TSO 時間を表示します。現在の時間を使用してbinlogログのタイムスタンプを減算することで、遅延を取得できます。ただし、タイムスタンプはマスター クラスターの PD によって割り当てられ、PD の時間によって決定されることに注意してください。 |
| PumpハンドルTSO                   | Drainerが各Pumpノードから取得したbinlogファイルの中で最大のTSO時間を記録します。                                                                                                             |
| Pump NodeID によるBinlog QPS の取得 | Drainerが各Pumpノードからbinlogを取得したときのQPSを表示します。                                                                                                                     |
| Pumpによる 95%Binlog到達期間         | binlogがPumpに書き込まれた時点から、binlogがDrainerによって取得された時点までの遅延を記録します。                                                                                                   |
| エラーの種類                        | Drainerが遭遇したエラーの数を、エラーの種類に基づいてカウントして表示します。                                                                                                                     |
| SQLクエリ時間                      | Drainerが下流でSQL文を実行するのにかかる時間を記録します。                                                                                                                             |
| Drainerイベント                   | 「ddl」、「insert」、「delete」、「update」、「flush」、「savepoint」など、さまざまな種類のイベントの数を表示します。                                                                                   |
| 実行時間                          | 下流の同期モジュールにbinlogを書き込むのにかかる時間を記録します。                                                                                                                           |
| 95%Binlogサイズ                  | Drainerが各Pumpノードから取得するbinlogデータのサイズを表示します。                                                                                                                     |
| DDLジョブ数                       | Drainerによって処理された DDL ステートメントの数を記録します。                                                                                                                          |
| キューサイズ                        | Drainerの作業キューのサイズを記録します                                                                                                                                        |

## アラートルール {#alert-rules}

このセクションでは、 TiDB Binlogのアラート ルールについて説明します。重大度レベルに応じて、 TiDB Binlogアラート ルールは、緊急レベル、重大レベル、警告レベルの 3 つのカテゴリ (高から低) に分類されます。

### 緊急レベルの警報 {#emergency-level-alerts}

緊急レベルのアラートは、多くの場合、サービスまたはノードの障害によって発生します。直ちに手動による介入が必要です。

#### <code>binlog_pump_storage_error_count</code> {#code-binlog-pump-storage-error-count-code}

-   アラートルール:

    `changes(binlog_pump_storage_error_count[1m]) > 0`

-   説明：

    Pumpはbinlogデータをローカルstorageに書き込むことができません。

-   解決：

    `pump_storage_error`監視にエラーが存在するかどうかを確認し、Pumpログを確認して原因を見つけます。

### 重大レベルのアラート {#critical-level-alerts}

重大レベルのアラートの場合、異常なメトリックを注意深く監視する必要があります。

#### <code>binlog_drainer_checkpoint_high_delay</code> {#code-binlog-drainer-checkpoint-high-delay-code}

-   アラートルール:

    `(time() - binlog_drainer_checkpoint_tso / 1000) > 3600`

-   説明：

    Drainerレプリケーションの遅延が 1 時間を超えています。

-   解決：

    -   Pumpからデータを取得するのが遅すぎないか確認します。

        Pumpの`handle tso`チェックすると、各Pumpの最新メッセージの時間を取得できます。Pump に高いレイテンシーが存在するかどうかを確認し、対応するPumpが正常に動作していることを確認します。

    -   Drainer `event`とDrainer `execute latency`に基づいて、ダウンストリームでデータを複製するのが遅すぎるかどうかを確認します。

        -   Drainer `execute time`が大きすぎる場合は、 Drainerがデプロイされているマシンとターゲット データベースがデプロイされているマシン間のネットワーク帯域幅とレイテンシー、およびターゲット データベースの状態を確認します。
        -   Drainer`execute time`が大きすぎず、Drainer`event`が小さすぎる場合は、 `work count`と`batch`追加して再試行してください。

    -   上記の 2 つの解決策が機能しない場合は、PingCAP またはコミュニティから[サポートを受ける](/support.md)試してください。

### 警告レベルのアラート {#warning-level-alerts}

警告レベルのアラートは、問題またはエラーを通知するものです。

#### <code>binlog_pump_write_binlog_rpc_duration_seconds_bucket</code> {#code-binlog-pump-write-binlog-rpc-duration-seconds-bucket-code}

-   アラートルール:

    `histogram_quantile(0.9, rate(binlog_pump_rpc_duration_seconds_bucket{method="WriteBinlog"}[5m])) > 1`

-   説明：

    Pumpがbinlog を書き込む TiDB 要求を処理するのに時間がかかりすぎます。

-   解決：

    -   ディスクパフォーマンスの負荷を確認し、 `node exported`介してディスクパフォーマンスの監視をチェックします。
    -   `disk latency`と`util`両方が低い場合は、PingCAP またはコミュニティから[サポートを受ける](/support.md)取得します。

#### <code>binlog_pump_storage_write_binlog_duration_time_bucket</code> {#code-binlog-pump-storage-write-binlog-duration-time-bucket-code}

-   アラートルール:

    `histogram_quantile(0.9, rate(binlog_pump_storage_write_binlog_duration_time_bucket{type="batch"}[5m])) > 1`

-   説明：

    Pumpがローカルbinlogをローカル ディスクに書き込むのにかかる時間。

-   解決：

    Pumpのローカル ディスクの状態を確認し、問題を修正します。

#### <code>binlog_pump_storage_available_size_less_than_20G</code> {#code-binlog-pump-storage-available-size-less-than-20g-code}

-   アラートルール:

    `binlog_pump_storage_storage_size_bytes{type="available"} < 20 * 1024 * 1024 * 1024`

-   説明：

    Pumpの使用可能なディスク容量は 20 GB 未満です。

-   解決：

    Pump`gc_tso`が正常かどうかを確認します。正常でない場合は、Pumpの GC 時間設定を調整するか、対応するPumpをオフラインにします。

#### <code>binlog_drainer_checkpoint_tso_no_change_for_1m</code> {#code-binlog-drainer-checkpoint-tso-no-change-for-1m-code}

-   アラートルール:

    `changes(binlog_drainer_checkpoint_tso[1m]) < 1`

-   説明：

    Drainer `checkpoint`は 1 分間更新されていません。

-   解決：

    オフラインではないすべてのポンプが正常に動作しているかどうかを確認します。

#### <code>binlog_drainer_execute_duration_time_more_than_10s</code> {#code-binlog-drainer-execute-duration-time-more-than-10s-code}

-   アラートルール:

    `histogram_quantile(0.9, rate(binlog_drainer_execute_duration_time_bucket[1m])) > 10`

-   説明：

    Drainer がTiDB にデータを複製するのにかかるトランザクション時間。この時間が長すぎると、 Drainerによるデータの複製に影響します。

-   解決：

    -   TiDB クラスターの状態を確認します。
    -   Drainerログまたはモニターを確認してください。DDL 操作によってこの問題が発生した場合は無視できます。
