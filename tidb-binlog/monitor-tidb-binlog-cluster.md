---
title: TiDB Binlog Monitoring
summary: Learn how to monitor the cluster version of TiDB Binlog.
---

# Binlogモニタリング {#tidb-binlog-monitoring}

TiDB Binlogを正常にデプロイしたら、Grafana Web（デフォルトのアドレス： [http：// grafana_ip：3000](http://grafana_ip:3000) 、デフォルトのアカウント：admin、パスワード：admin）にアクセスして、 PumpとDrainerの状態を確認できます。

## モニタリング指標 {#monitoring-metrics}

TiDB Binlogは、 PumpとDrainerとDrainerの2つのコンポーネントで構成されています。このセクションでは、PumpとDrainerの監視メトリックを示します。

### Pump監視メトリック {#pump-monitoring-metrics}

Pump監視メトリックを理解するには、次の表を確認してください。

| Pump監視メトリック          | 説明                                                                                       |
| -------------------- | ---------------------------------------------------------------------------------------- |
| ストレージサイズ             | 合計ディスク容量（容量）と使用可能なディスク容量（使用可能）を記録します                                                     |
| メタデータ                | 各Pumpノードが削除できるbinlogの最大TSO（ `gc_tso` ）と、保存されたbinlogの最大コミットTSO（ `max_commit_tso` ）を記録します。 |
| インスタンスごとにBinlogを書き込む | 各Pumpノードが受信したbinlog要求の書き込みのQPSを表示します                                                     |
| Binlogレイテンシを書き込む     | binlogを書き込む各Pumpノードの待ち時間を記録します                                                           |
| ストレージ書き込みBinlogサイズ   | Pumpによって書き込まれたbinlogデータのサイズを示します                                                         |
| ストレージ書き込みBinlogレイテンシ | binlogを書き込むPumpストレージモジュールの待ち時間を記録します                                                     |
| タイプ別のPump発電エラー       | エラーのタイプに基づいてカウントされた、 Pumpが遭遇したエラーの数を記録します                                                |
| TiKVを照会する            | PumpがTiKVを介してトランザクションステータスを照会する回数                                                        |

### Drainerモニタリングメトリクス {#drainer-monitoring-metrics}

Drainerの監視メトリックを理解するには、次の表を確認してください。

| Drainerモニタリングメトリクス     | 説明                                                                                                                                                   |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| チェックポイントTSO            | Drainerがすでにダウンストリームに複製したbinlogの最大TSO時間を示します。現在の時刻を使用してbinlogタイムスタンプを差し引くことにより、ラグを取得できます。ただし、タイムスタンプはマスタークラスタのPDによって割り当てられ、PDの時刻によって決定されることに注意してください。 |
| PumpハンドルTSO            | Drainerが各Pumpノードから取得するDrainerファイルの中で最大のTSO時間を記録します                                                                                                   |
| PumpNodeIDによるBinlogのプル | Drainerが各PumpノードからDrainerを取得したときのQPSを表示します                                                                                                           |
| Pumpによる95％のBinlogリーチ期間 | binlogがPumpに書き込まれてから、DrainerによってDrainerが取得されるまでの遅延を記録します。                                                                                            |
| タイプ別エラー                | エラーのタイプに基づいてカウントされた、 Drainerが遭遇したエラーの数を示します                                                                                                          |
| SQLクエリ時間               | DrainerがダウンストリームでSQLステートメントを実行するのにかかる時間を記録します                                                                                                        |
| Drainerイベント            | 「ddl」、「挿入」、「削除」、「更新」、「フラッシュ」、「セーブポイント」など、さまざまなタイプのイベントの数を表示します                                                                                       |
| 実行時間                   | binlogをダウンストリーム同期モジュールに書き込むのにかかる時間を記録します                                                                                                             |
| 95％のBinlogサイズ          | Drainerが各Pumpノードから取得するDrainerデータのサイズを示します                                                                                                            |
| DDLジョブ数                | Drainerによって処理されたDDLステートメントの数を記録します                                                                                                                   |
| キューサイズ                 | 作業キューのサイズをDrainerに記録します                                                                                                                              |

## アラートルール {#alert-rules}

このセクションでは、 Binlogのアラートルールについて説明します。重大度レベルに応じて、TiDB Binlogアラートルールは、緊急レベル、クリティカルレベル、および警告レベルの3つのカテゴリ（高から低）に分類されます。

### 緊急レベルのアラート {#emergency-level-alerts}

緊急レベルのアラートは、多くの場合、サービスまたはノードの障害によって発生します。すぐに手動による介入が必要です。

#### <code>binlog_pump_storage_error_count</code> {#code-binlog-pump-storage-error-count-code}

-   アラートルール：

    `changes(binlog_pump_storage_error_count[1m]) > 0`

-   説明：

    Pumpはbinlogデータをローカルストレージに書き込めません。

-   解決：

    `pump_storage_error`モニタリングにエラーが存在するかどうかを確認し、Pumpログを確認して原因を特定します。

### クリティカルレベルのアラート {#critical-level-alerts}

クリティカルレベルのアラートの場合、異常なメトリックを注意深く監視する必要があります。

#### <code>binlog_drainer_checkpoint_high_delay</code> {#code-binlog-drainer-checkpoint-high-delay-code}

-   アラートルール：

    `(time() - binlog_drainer_checkpoint_tso / 1000) > 3600`

-   説明：

    Drainerレプリケーションの遅延が1時間を超えています。

-   解決：

    -   Pumpからデータを取得するには遅すぎるかどうかを確認します。

        Pumpの`handle tso`をチェックして、各Pumpの最新メッセージの時間を取得できます。Pumpに高い待ち時間が存在するかどうかを確認し、対応するPumpが正常に動作していることを確認します。

    -   Drainerと`event`に基づいDrainer、ダウンストリームでデータを複製するには遅すぎるかどうかを確認し`execute latency` 。

        -   Drainer `execute time`が大きすぎる場合は、 Drainerが展開されているマシンとターゲットデータベースが展開されているマシンの間のネットワーク帯域幅と遅延、およびターゲットデータベースの状態を確認してください。
        -   Drainer`execute time`が大きすぎず、Drainer`event`が小さすぎる場合は、 `work count`と`batch`を追加して再試行します。

    -   上記の2つの解決策が機能しない場合は、 [support@pingcap.com](mailto:support@pingcap.com)に連絡してください。

### 警告レベルのアラート {#warning-level-alerts}

警告レベルのアラートは、問題またはエラーのリマインダーです。

#### <code>binlog_pump_write_binlog_rpc_duration_seconds_bucket</code> {#code-binlog-pump-write-binlog-rpc-duration-seconds-bucket-code}

-   アラートルール：

    `histogram_quantile(0.9, rate(binlog_pump_rpc_duration_seconds_bucket{method="WriteBinlog"}[5m])) > 1`

-   説明：

    Pumpがbinlogを書き込むTiDB要求を処理するのに時間がかかりすぎます。

-   解決：

    -   ディスクパフォーマンスの圧力を確認し、 `node exported`を介してディスクパフォーマンスの監視を確認します。
    -   `disk latency`と`util`の両方が低い場合は、 [support@pingcap.com](mailto:support@pingcap.com)に連絡してください。

#### <code>binlog_pump_storage_write_binlog_duration_time_bucket</code> {#code-binlog-pump-storage-write-binlog-duration-time-bucket-code}

-   アラートルール：

    `histogram_quantile(0.9, rate(binlog_pump_storage_write_binlog_duration_time_bucket{type="batch"}[5m])) > 1`

-   説明：

    Pumpがローカルbinlogをローカルディスクに書き込むのにかかる時間。

-   解決：

    Pumpのローカルディスクの状態を確認し、問題を修正してください。

#### <code>binlog_pump_storage_available_size_less_than_20G</code> {#code-binlog-pump-storage-available-size-less-than-20g-code}

-   アラートルール：

    `binlog_pump_storage_storage_size_bytes{type="available"} < 20 * 1024 * 1024 * 1024`

-   説明：

    Pumpの使用可能なディスク容量は20GB未満です。

-   解決：

    Pump`gc_tso`が正常か確認してください。そうでない場合は、PumpのGC時間構成を調整するか、対応するPumpをオフラインにします。

#### <code>binlog_drainer_checkpoint_tso_no_change_for_1m</code> {#code-binlog-drainer-checkpoint-tso-no-change-for-1m-code}

-   アラートルール：

    `changes(binlog_drainer_checkpoint_tso[1m]) < 1`

-   説明：

    Drainer`checkpoint`は1分間更新されていません。

-   解決：

    オフラインではないすべてのポンプが正常に動作しているかどうかを確認します。

#### <code>binlog_drainer_execute_duration_time_more_than_10s</code> {#code-binlog-drainer-execute-duration-time-more-than-10s-code}

-   アラートルール：

    `histogram_quantile(0.9, rate(binlog_drainer_execute_duration_time_bucket[1m])) > 10`

-   説明：

    DrainerがデータをDrainerに複製するのにかかるトランザクション時間。大きすぎると、データのDrainerレプリケーションが影響を受けます。

-   解決：

    -   TiDBクラスタの状態を確認してください。
    -   Drainerまたはモニターを確認してください。 DDL操作によってこの問題が発生する場合は、無視してかまいません。
