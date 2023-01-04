---
title: TiDB Binlog Monitoring
summary: Learn how to monitor the cluster version of TiDB Binlog.
---

# Binlogバイナリログ監視 {#tidb-binlog-monitoring}

TiDB Binlogを正常にデプロイしたら、Grafana Web (デフォルトのアドレス: [http://grafana_ip:3000](http://grafana_ip:3000) 、デフォルトのアカウント: admin、パスワード: admin) にアクセスして、 PumpとDrainer とDrainer の状態を確認できます。

## 指標のモニタリング {#monitoring-metrics}

TiDB Binlogは、 PumpとDrainer とDrainer の 2 つのコンポーネントで構成されています。このセクションでは、 PumpとDrainerの監視メトリクスを示します。

### Pump監視指標 {#pump-monitoring-metrics}

Pumpモニタリング メトリックを理解するには、次の表を確認してください。

| Pump監視指標                  | 説明                                                                                                |
| ------------------------- | ------------------------------------------------------------------------------------------------- |
| 収納サイズ                     | 合計ディスク容量 (容量) と使用可能なディスク容量 (使用可能) を記録します。                                                         |
| メタデータ                     | 各Pumpノードが削除できるバイナリログの最大の TSO ( `gc_tso` ) と、保存されたバイナリ ログの最大のコミット TSO ( `max_commit_tso` ) を記録します。 |
| インスタンスごとにBinlog QPS を書き込む | 各Pumpノードが受信した binlog リクエストの書き込みの QPS を表示します                                                       |
| Binlogレイテンシーの書き込み         | バイナリログを書き込む各Pumpノードのレイテンシーを記録します。                                                                 |
| ストレージ書き込みBinlogサイズ        | Pumpによって書き込まれた binlog データのサイズを表示します                                                               |
| ストレージ書き込みBinlogレイテンシ      | Pumpストレージモジュールのバイナリログ書き込みのレイテンシーを記録します                                                            |
| タイプPump保管エラー              | エラーの種類に基づいてカウントされた、 Pumpで発生したエラーの数を記録します                                                          |
| TiKV のクエリ                 | Pumpが TiKV を介してトランザクション ステータスを照会する回数                                                              |

### Drainerモニタリング指標 {#drainer-monitoring-metrics}

Drainerモニタリング メトリックを理解するには、次の表を確認してください。

| Drainerモニタリング指標               | 説明                                                                                                                                                            |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| チェックポイント TSO                  | Drainerがすでにダウンストリームにレプリケートしたバイナリログの最大 TSO 時間を示します。現在の時刻を使用してバイナリログのタイムスタンプを差し引くことで、ラグを取得できます。ただし、タイムスタンプはマスター クラスタの PD によって割り当てられ、PD の時刻によって決定されることに注意してください。 |
| Pumpハンドル TSO                  | Drainer が各Pumpノードから取得したDrainerファイルの中で最大の TSO 時間を記録します                                                                                                         |
| Pump NodeID によるBinlog QPS のプル | Drainer が各PumpノードからDrainerを取得したときの QPS を表示します                                                                                                                 |
| Pumpによる 95%の Binlogリーチ期間      | binlog がPumpに書き込まれてから Drainer がDrainerを取得するまでの遅延を記録します。                                                                                                       |
| タイプ別エラー                       | Drainerで発生したエラーの数を、エラーの種類に基づいてカウントして表示します                                                                                                                     |
| SQL クエリ時間                     | Drainerがダウンストリームで SQL ステートメントを実行するのにかかる時間を記録します                                                                                                               |
| Drainerイベント                   | 「ddl」、「insert」、「delete」、「update」、「flush」、「savepoint」など、さまざまなタイプのイベントの数を表示します                                                                                  |
| 実行時間                          | binlog をダウンストリーム同期モジュールに書き込むのにかかる時間を記録します                                                                                                                     |
| 95%のBinlogサイズ                 | Drainer が各Pumpノードから取得するDrainerデータのサイズを表示します                                                                                                                   |
| DDL ジョブ数                      | Drainerによって処理された DDL ステートメントの数を記録します                                                                                                                          |
| キューサイズ                        | ワーク キューのサイズをDrainerに記録する                                                                                                                                      |

## アラート ルール {#alert-rules}

このセクションでは、TiDB Binlogのアラート ルールを示します。重大度レベルに応じて、TiDB Binlogアラート ルールは 3 つのカテゴリ (高から低) に分類されます: 緊急レベル、重大レベル、警告レベルです。

### 緊急レベルのアラート {#emergency-level-alerts}

緊急レベルのアラートは、多くの場合、サービスまたはノードの障害によって発生します。手動による介入がすぐに必要です。

#### <code>binlog_pump_storage_error_count</code> {#code-binlog-pump-storage-error-count-code}

-   アラート ルール:

    `changes(binlog_pump_storage_error_count[1m]) > 0`

-   説明：

    Pumpはバイナリログ データをローカル ストレージに書き込むことができません。

-   解決：

    `pump_storage_error`の監視に異常がないか確認し、 Pumpのログを確認して原因を突き止めてください。

### 重大レベルのアラート {#critical-level-alerts}

重大レベルのアラートについては、異常なメトリックを注意深く監視する必要があります。

#### <code>binlog_drainer_checkpoint_high_delay</code> {#code-binlog-drainer-checkpoint-high-delay-code}

-   アラート ルール:

    `(time() - binlog_drainer_checkpoint_tso / 1000) > 3600`

-   説明：

    Drainerレプリケーションの遅延が 1 時間を超えています。

-   解決：

    -   Pumpからデータを取得するのが遅すぎるかどうかを確認します。

        Pumpの`handle tso`をチェックして、各Pumpの最新メッセージの時刻を取得できます。Pumpのレイテンシーが大きいかどうかを確認し、対応するPumpが正常に動作していることを確認します。

    -   Drainer `event`とDrainer `execute latency`に基づいて、ダウンストリームでデータをレプリケートするのが遅すぎるかどうかを確認します。

        -   Drainer `execute time`が大きすぎる場合は、 Drainerがデプロイされたマシンとターゲット データベースがデプロイされたマシンの間のネットワーク帯域幅とレイテンシー時間、およびターゲット データベースの状態を確認します。
        -   Drainer`execute time`が大きすぎず、Drainer`event`が小さすぎる場合は、 `work count`と`batch`を追加して再試行します。

    -   上記の 2 つの解決策がうまくいかない場合は、 [support@pingcap.com](mailto:support@pingcap.com)にお問い合わせください。

### 警告レベルのアラート {#warning-level-alerts}

警告レベルのアラートは、問題またはエラーのリマインダーです。

#### <code>binlog_pump_write_binlog_rpc_duration_seconds_bucket</code> {#code-binlog-pump-write-binlog-rpc-duration-seconds-bucket-code}

-   アラート ルール:

    `histogram_quantile(0.9, rate(binlog_pump_rpc_duration_seconds_bucket{method="WriteBinlog"}[5m])) > 1`

-   説明：

    Pumpが binlog を書き込む TiDB 要求を処理するのに時間がかかりすぎます。

-   解決：

    -   ディスク パフォーマンスのプレッシャーを確認し、 `node exported`でディスク パフォーマンスの監視を確認します。
    -   `disk latency`と`util`の両方が低い場合は、 [support@pingcap.com](mailto:support@pingcap.com)に連絡してください。

#### <code>binlog_pump_storage_write_binlog_duration_time_bucket</code> {#code-binlog-pump-storage-write-binlog-duration-time-bucket-code}

-   アラート ルール:

    `histogram_quantile(0.9, rate(binlog_pump_storage_write_binlog_duration_time_bucket{type="batch"}[5m])) > 1`

-   説明：

    Pumpがローカル binlog をローカル ディスクに書き込むのにかかる時間。

-   解決：

    Pumpのローカルディスクの状態を確認し、問題を修正してください。

#### <code>binlog_pump_storage_available_size_less_than_20G</code> {#code-binlog-pump-storage-available-size-less-than-20g-code}

-   アラート ルール:

    `binlog_pump_storage_storage_size_bytes{type="available"} < 20 * 1024 * 1024 * 1024`

-   説明：

    Pumpの使用可能なディスク容量は 20 GB 未満です。

-   解決：

    Pump`gc_tso`が正常かどうかを確認します。そうでない場合は、 Pumpの GC 時間構成を調整するか、対応するPumpをオフラインにします。

#### <code>binlog_drainer_checkpoint_tso_no_change_for_1m</code> {#code-binlog-drainer-checkpoint-tso-no-change-for-1m-code}

-   アラート ルール:

    `changes(binlog_drainer_checkpoint_tso[1m]) < 1`

-   説明：

    Drainer `checkpoint`は 1 分間更新されていません。

-   解決：

    オフラインになっていないすべてのポンプが正常に動作しているかどうかを確認します。

#### <code>binlog_drainer_execute_duration_time_more_than_10s</code> {#code-binlog-drainer-execute-duration-time-more-than-10s-code}

-   アラート ルール:

    `histogram_quantile(0.9, rate(binlog_drainer_execute_duration_time_bucket[1m])) > 10`

-   説明：

    Drainer がデータをDrainerにレプリケートするのにかかるトランザクション時間。大きすぎると、データのDrainerレプリケーションが影響を受けます。

-   解決：

    -   TiDB クラスターの状態を確認します。
    -   Drainerログまたはモニターを確認してください。 DDL 操作がこの問題の原因である場合は、無視してかまいません。
