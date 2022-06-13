---
title: TiDB Binlog Monitoring
summary: Learn how to monitor the cluster version of TiDB Binlog.
---

# TiDBBinlogモニタリング {#tidb-binlog-monitoring}

TiDB Binlogを正常にデプロイしたら、Grafana Web（デフォルトのアドレス： [http：// grafana_ip：3000](http://grafana_ip:3000) 、デフォルトのアカウント：admin、パスワード：admin）にアクセスして、PumpandDrainerの状態を確認できます。

## モニタリング指標 {#monitoring-metrics}

TiDB Binlogは、ポンプとドレイナーの2つのコンポーネントで構成されています。このセクションでは、ポンプとドレイナーの監視メトリックを示します。

### ポンプ監視メトリクス {#pump-monitoring-metrics}

ポンプ監視メトリックを理解するには、次の表を確認してください。

| ポンプ監視メトリクス              | 説明                                                                                       |
| ----------------------- | ---------------------------------------------------------------------------------------- |
| ストレージサイズ                | 合計ディスク容量（容量）と使用可能なディスク容量（使用可能）を記録します                                                     |
| メタデータ                   | 各Pumpノードが削除できるbinlogの最大TSO（ `gc_tso` ）と、保存されたbinlogの最大コミットTSO（ `max_commit_tso` ）を記録します。 |
| インスタンスごとのBinlogQPSの書き込み | 各Pumpノードが受信したbinlog要求の書き込みのQPSを表示します                                                     |
| Binlogレイテンシを書き込む        | binlogを書き込む各Pumpノードのレイテンシー時間を記録します                                                       |
| ストレージ書き込みビンログサイズ        | Pumpによって書き込まれたbinlogデータのサイズを表示します                                                        |
| ストレージ書き込みBinlogレイテンシ    | binlogを書き込むポンプストレージモジュールの待ち時間を記録します                                                      |
| タイプ別の揚水発電エラー            | エラーのタイプに基づいてカウントされた、Pumpで発生したエラーの数を記録します                                                 |
| TiKVを照会する               | PumpがTiKVを介してトランザクションステータスを照会する回数                                                        |

### ドレイナーモニタリングメトリクス {#drainer-monitoring-metrics}

Drainerの監視メトリックを理解するには、次の表を確認してください。

| ドレイナーモニタリングメトリクス         | 説明                                                                                                                                                   |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| チェックポイントTSO              | Drainerがすでにダウンストリームに複製したbinlogの最大TSO時間を示します。現在の時刻を使用してbinlogタイムスタンプを差し引くことにより、ラグを取得できます。ただし、タイムスタンプはマスタークラスタのPDによって割り当てられ、PDの時刻によって決定されることに注意してください。 |
| ポンプハンドルTSO               | Drainerが各Pumpノードから取得するbinlogファイルの中で最大のTSO時間を記録します                                                                                                    |
| ポンプNodeIDによるBinlogQPSのプル | Drainerが各Pumpノードからbinlogを取得したときのQPSを表示します                                                                                                            |
| ポンプによる95％のBinlogリーチ期間    | binlogがPumpに書き込まれてから、binlogがDrainerによって取得されるまでの遅延を記録します。                                                                                             |
| タイプ別エラー                  | エラーのタイプに基づいてカウントされた、Drainerが遭遇したエラーの数を示します                                                                                                           |
| SQLクエリ時間                 | DrainerがダウンストリームでSQLステートメントを実行するのにかかる時間を記録します                                                                                                        |
| ドレイナーイベント                | 「ddl」、「insert」、「delete」、「update」、「flush」、「savepoint」など、さまざまな種類のイベントの数を表示します                                                                          |
| 実行時間                     | binlogをダウンストリーム同期モジュールに書き込むのにかかる時間を記録します                                                                                                             |
| 95％のビンログサイズ              | Drainerが各Pumpノードから取得するbinlogデータのサイズを示します                                                                                                             |
| DDLジョブ数                  | Drainerによって処理されたDDLステートメントの数を記録します                                                                                                                   |
| キューサイズ                   | 作業キューのサイズをDrainerに記録します                                                                                                                              |

## アラートルール {#alert-rules}

このセクションでは、TiDBBinlogのアラートルールについて説明します。重大度レベルに応じて、TiDB Binlogアラートルールは、緊急レベル、クリティカルレベル、および警告レベルの3つのカテゴリ（高から低）に分類されます。

### 緊急レベルのアラート {#emergency-level-alerts}

緊急レベルのアラートは、多くの場合、サービスまたはノードの障害によって発生します。すぐに手動で介入する必要があります。

#### <code>binlog_pump_storage_error_count</code> {#code-binlog-pump-storage-error-count-code}

-   アラートルール：

    `changes(binlog_pump_storage_error_count[1m]) > 0`

-   説明：

    Pumpはbinlogデータをローカルストレージに書き込めません。

-   解決：

    `pump_storage_error`モニタリングにエラーが存在するかどうかを確認し、ポンプログを確認して原因を特定します。

### クリティカルレベルのアラート {#critical-level-alerts}

クリティカルレベルのアラートの場合、異常なメトリックを注意深く監視する必要があります。

#### <code>binlog_drainer_checkpoint_high_delay</code> {#code-binlog-drainer-checkpoint-high-delay-code}

-   アラートルール：

    `(time() - binlog_drainer_checkpoint_tso / 1000) > 3600`

-   説明：

    Drainerレプリケーションの遅延が1時間を超えています。

-   解決：

    -   Pumpからデータを取得するには遅すぎるかどうかを確認します。

        ポンプの`handle tso`をチェックして、各ポンプの最新メッセージの時間を取得できます。ポンプに高い待ち時間が存在するかどうかを確認し、対応するポンプが正常に動作していることを確認します。

    -   `event`と`execute latency`に基づいて、ダウンストリームでデータを複製するには遅すぎるかどうかを確認します。

        -   Drainer `execute time`が大きすぎる場合は、Drainerが展開されているマシンとターゲットデータベースが展開されているマシンの間のネットワーク帯域幅と遅延、およびターゲットデータベースの状態を確認してください。
        -   ドレイナー`execute time`が大きすぎず、ドレイナー`event`が小さすぎる場合は、 `work count`と`batch`を追加して、再試行してください。

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

    Pumpのローカルディスクの状態を確認し、問題を修正します。

#### <code>binlog_pump_storage_available_size_less_than_20G</code> {#code-binlog-pump-storage-available-size-less-than-20g-code}

-   アラートルール：

    `binlog_pump_storage_storage_size_bytes{type="available"} < 20 * 1024 * 1024 * 1024`

-   説明：

    Pumpの使用可能なディスク容量は20GB未満です。

-   解決：

    ポンプ`gc_tso`が正常か確認してください。そうでない場合は、ポンプのGC時間構成を調整するか、対応するポンプをオフラインにします。

#### <code>binlog_drainer_checkpoint_tso_no_change_for_1m</code> {#code-binlog-drainer-checkpoint-tso-no-change-for-1m-code}

-   アラートルール：

    `changes(binlog_drainer_checkpoint_tso[1m]) < 1`

-   説明：

    ドレイナー`checkpoint`は1分間更新されていません。

-   解決：

    オフラインではないすべてのポンプが正常に動作しているかどうかを確認します。

#### <code>binlog_drainer_execute_duration_time_more_than_10s</code> {#code-binlog-drainer-execute-duration-time-more-than-10s-code}

-   アラートルール：

    `histogram_quantile(0.9, rate(binlog_drainer_execute_duration_time_bucket[1m])) > 10`

-   説明：

    DrainerがデータをTiDBに複製するのにかかるトランザクション時間。大きすぎると、データのDrainerレプリケーションが影響を受けます。

-   解決：

    -   TiDBクラスタの状態を確認してください。
    -   ドレイナーログまたはモニターを確認してください。 DDL操作によってこの問題が発生する場合は、無視してかまいません。
