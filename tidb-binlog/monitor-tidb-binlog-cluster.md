---
title: TiDB Binlog Monitoring
summary: Learn how to monitor the cluster version of TiDB Binlog.
---

# TiDBBinlogのモニタリング {#tidb-binlog-monitoring}

TiDB Binlog を正常にデプロイした後、Grafana Web (デフォルトのアドレス: [http://grafana_ip:3000](http://grafana_ip:3000) 、デフォルトのアカウント: admin、パスワード: admin) に移動して、 PumpとDrainerの状態を確認できます。

## モニタリング指標 {#monitoring-metrics}

TiDB Binlog は、 PumpとDrainerの 2 つのコンポーネントで構成されます。このセクションでは、 PumpとDrainerの監視メトリクスを示します。

### Pump監視メトリクス {#pump-monitoring-metrics}

Pump監視メトリクスを理解するには、次の表を確認してください。

| Pump監視メトリクス               | 説明                                                                                             |
| ------------------------- | ---------------------------------------------------------------------------------------------- |
| ストレージサイズ                  | 合計ディスク容量 (capacity) と利用可能なディスク容量 (available) を記録します。                                           |
| メタデータ                     | 各Pumpノードが削除できるbinlogの最大 TSO ( `gc_tso` ) と、保存されたbinlogの最大コミット TSO ( `max_commit_tso` ) を記録します。 |
| インスタンスごとにBinlog QPS を書き込む | 各Pumpノードが受信した書き込みbinlogリクエストの QPS を表示します。                                                      |
| Binlog書き込みレイテンシ           | binlogを書き込む各Pumpノードのレイテンシーを記録します。                                                              |
| ストレージ書き込みBinlogサイズ        | Pumpによって書き込まれたbinlogデータのサイズを示します。                                                              |
| ストレージ書き込みBinlog遅延         | Pumpstorageモジュールのbinlog書き込みのレイテンシーを記録します。                                                      |
| タイプ別のPump保管エラー            | Pumpで発生したエラーの数をエラーの種類に基づいてカウントして記録します。                                                         |
| TiKV のクエリ                 | Pump がTiKV を通じてトランザクション ステータスをクエリした回数                                                          |

### Drainer監視メトリクス {#drainer-monitoring-metrics}

Drainer監視メトリクスを理解するには、次の表を確認してください。

| Drainer監視メトリクス                | 説明                                                                                                                                                          |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| チェックポイント TSO                  | Drainer が既にダウンストリームにレプリケートしたbinlogの最大 TSO 時間を示します。現在の時刻からbinlogのタイムスタンプを減算することで、ラグを取得できます。ただし、タイムスタンプはマスター クラスターの PD によって割り当てられ、PD の時刻によって決定されることに注意してください。 |
| Pumpハンドル TSO                  | Drainer が各Pumpノードから取得したbinlogファイルの中で最大の TSO 時間を記録します。                                                                                                       |
| Pump NodeID によるBinlog QPS のプル | Drainer が各Pumpノードからbinlogを取得するときの QPS を表示します                                                                                                                |
| PumpによるBinlog到達時間の 95%        | binlogがPumpに書き込まれてから、binlogがDrainerによって取得されるまでの遅延を記録します。                                                                                                    |
| タイプ別エラー                       | エラーの種類に基づいてカウントされた、 Drainerで発生したエラーの数を示します。                                                                                                                 |
| SQLクエリ時間                      | Drainerがダウンストリームで SQL ステートメントを実行するのにかかる時間を記録します。                                                                                                            |
| Drainerイベント                   | 「ddl」、「insert」、「delete」、「update」、「flush」、「savepoint」などのさまざまなタイプのイベントの数を表示します。                                                                               |
| 実行時間                          | ダウンストリーム同期モジュールにbinlogを書き込むのにかかる時間を記録します。                                                                                                                   |
| 95% のBinlogサイズ                | Drainer が各Pumpノードから取得するbinlogデータのサイズを示します。                                                                                                                  |
| DDL ジョブ数                      | Drainerによって処理された DDL ステートメントの数を記録します。                                                                                                                       |
| キューのサイズ                       | ワークキューのサイズをDrainerに記録します                                                                                                                                    |

## アラートルール {#alert-rules}

このセクションでは、TiDB Binlogのアラート ルールを説明します。重大度レベルに応じて、TiDB Binlogアラート ルールは (高から低の順に) 緊急レベル、重大レベル、警告レベルの 3 つのカテゴリに分類されます。

### 緊急レベルの警報 {#emergency-level-alerts}

緊急レベルのアラートは、多くの場合、サービスまたはノードの障害によって発生します。直ちに手動による介入が必要です。

#### <code>binlog_pump_storage_error_count</code> {#code-binlog-pump-storage-error-count-code}

-   アラート ルール:

    `changes(binlog_pump_storage_error_count[1m]) > 0`

-   説明：

    Pumpはローカルstorageへのbinlogデータの書き込みに失敗します。

-   解決：

    `pump_storage_error`監視に異常がないか確認し、Pumpログを確認して原因を特定してください。

### 重大レベルのアラート {#critical-level-alerts}

クリティカルレベルのアラートについては、異常なメトリクスを注意深く監視する必要があります。

#### <code>binlog_drainer_checkpoint_high_delay</code> {#code-binlog-drainer-checkpoint-high-delay-code}

-   アラート ルール:

    `(time() - binlog_drainer_checkpoint_tso / 1000) > 3600`

-   説明：

    Drainerレプリケーションの遅延が 1 時間を超えています。

-   解決：

    -   Pumpからデータを取得するのが遅すぎるかどうかを確認します。

        Pumpの`handle tso`をチェックすると、各Pumpの最新メッセージの時間を取得できます。Pumpに長いレイテンシーが存在するかどうかを確認し、対応するPumpが正常に実行されていることを確認してください。

    -   Drainer `event`とDrainer `execute latency`に基づいて、ダウンストリームでのデータの複製が遅すぎるかどうかを確認します。

        -   Drainer `execute time`が大きすぎる場合は、 Drainerがデプロイされているマシンとターゲット データベースがデプロイされているマシン間のネットワーク帯域幅とレイテンシー、およびターゲット データベースの状態を確認してください。
        -   Drainer`execute time`が大きすぎず、Drainer`event`が小さすぎる場合は、 `work count`と`batch`を追加して再試行します。

    -   上記の 2 つの解決策が機能しない場合は、 [支持を得ます](/support.md) PingCAP またはコミュニティからの解決策。

### 警報レベルのアラート {#warning-level-alerts}

警告レベルのアラートは、問題またはエラーを通知するものです。

#### <code>binlog_pump_write_binlog_rpc_duration_seconds_bucket</code> {#code-binlog-pump-write-binlog-rpc-duration-seconds-bucket-code}

-   アラート ルール:

    `histogram_quantile(0.9, rate(binlog_pump_rpc_duration_seconds_bucket{method="WriteBinlog"}[5m])) > 1`

-   説明：

    Pump がbinlogを書き込む TiDB リクエストを処理するには時間がかかりすぎます。

-   解決：

    -   ディスク パフォーマンスの負荷を確認し、 `node exported`を介してディスク パフォーマンスの監視を確認します。
    -   `disk latency`と`util`が両方とも低い場合は、PingCAP またはコミュニティからの[支持を得ます](/support.md) 。

#### <code>binlog_pump_storage_write_binlog_duration_time_bucket</code> {#code-binlog-pump-storage-write-binlog-duration-time-bucket-code}

-   アラート ルール:

    `histogram_quantile(0.9, rate(binlog_pump_storage_write_binlog_duration_time_bucket{type="batch"}[5m])) > 1`

-   説明：

    Pump がローカルbinlogをローカル ディスクに書き込むのにかかる時間。

-   解決：

    Pumpのローカル ディスクの状態を確認し、問題を解決してください。

#### <code>binlog_pump_storage_available_size_less_than_20G</code> {#code-binlog-pump-storage-available-size-less-than-20g-code}

-   アラート ルール:

    `binlog_pump_storage_storage_size_bytes{type="available"} < 20 * 1024 * 1024 * 1024`

-   説明：

    Pumpの使用可能なディスク容量は 20 GB 未満です。

-   解決：

    Pump`gc_tso`が正常か確認してください。そうでない場合は、Pumpの GC 時間構成を調整するか、対応するPumpをオフラインにします。

#### <code>binlog_drainer_checkpoint_tso_no_change_for_1m</code> {#code-binlog-drainer-checkpoint-tso-no-change-for-1m-code}

-   アラート ルール:

    `changes(binlog_drainer_checkpoint_tso[1m]) < 1`

-   説明：

    Drainer`checkpoint`は 1 分間更新されていません。

-   解決：

    オフラインではないすべてのポンプが正常に動作しているかどうかを確認します。

#### <code>binlog_drainer_execute_duration_time_more_than_10s</code> {#code-binlog-drainer-execute-duration-time-more-than-10s-code}

-   アラート ルール:

    `histogram_quantile(0.9, rate(binlog_drainer_execute_duration_time_bucket[1m])) > 10`

-   説明：

    Drainer がデータを TiDB に複製するのにかかるトランザクション時間。大きすぎると、データのDrainerレプリケーションが影響を受けます。

-   解決：

    -   TiDB クラスターの状態を確認します。
    -   Drainerログまたはモニターを確認してください。 DDL 操作によってこの問題が発生する場合は、無視してかまいません。
