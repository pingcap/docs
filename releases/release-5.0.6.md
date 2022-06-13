---
title: TiDB 5.0.6 Release Notes
category: Releases
---

# TiDB5.0.6リリースノート {#tidb-5-0-6-release-notes}

発売日：2021年12月31日

TiDBバージョン：5.0.6

## 互換性の変更 {#compatibility-changes}

-   ツール

    -   TiCDC

        -   `cdc server`コマンドエラーの出力をstdoutから[＃3133](https://github.com/pingcap/tiflow/issues/3133)に変更します。
        -   Kafkaシンク`max-message-bytes`のデフォルト値を[＃3081](https://github.com/pingcap/tiflow/issues/3081)に設定し`10M`
        -   Kafka Sink `partition-num`のデフォルト値を3に変更して、TiCDCがKafkaパーティション間でメッセージをより均等に分散するようにします[＃3337](https://github.com/pingcap/ticdc/issues/3337)

## 改善 {#improvements}

-   TiDB

    -   コプロセッサーがロックに遭遇したときに、影響を受けるSQLステートメントをデバッグログに表示します。これは、問題の診断に役立ちます[＃27718](https://github.com/pingcap/tidb/issues/27718)

-   TiKV

    -   検証プロセスを`Apply`スレッドプールから`Import`スレッドプールに移動して、SSTファイルの挿入速度を上げます[＃11239](https://github.com/tikv/tikv/issues/11239)
    -   モジュール[＃11374](https://github.com/tikv/tikv/issues/11374)のパフォーマンスの問題を特定するために、Raftログのガベージコレクションモジュールのメトリックを追加します。
    -   Grafanaダッシュボード[＃11681](https://github.com/tikv/tikv/issues/11681)でいくつかの一般的でないストレージ関連のメトリックを折りたたむ

-   PD

    -   スケジューラーの終了プロセスを高速化する[＃4146](https://github.com/tikv/pd/issues/4146)
    -   スケジューラーが空のリージョンをスケジュールし、スケジューラーの構成を修正できるようにすることで、 `scatter-range-scheduler`のスケジューラーのスケジューリング結果をさらに向上させます[＃4497](https://github.com/tikv/pd/issues/4497)
    -   エビクトリーダースケジューラが異常なピアを持つリージョンをスケジュールできることをサポートする[＃4093](https://github.com/tikv/pd/issues/4093)

-   ツール

    -   TiCDC

        -   TiKVリロードのレート制限制御を最適化して、チェンジフィード初期化中のgPRC輻輳を低減します[＃3110](https://github.com/pingcap/ticdc/issues/3110)
        -   EtcdWorkerにティック頻度制限を追加して、頻繁なetcd書き込みがPDサービスに影響を与えないようにします[＃3112](https://github.com/pingcap/ticdc/issues/3112)
        -   Kafkaシンク[＃3352](https://github.com/pingcap/tiflow/issues/3352)に`config.Metadata.Timeout`のデフォルト構成を追加します
        -   Kafkaメッセージを送信できない可能性を減らすために、デフォルト値の`max-message-bytes`を設定し[＃3081](https://github.com/pingcap/tiflow/issues/3081) `10M`
        -   `no owner alert` `buffer sink total row` [＃4054](https://github.com/pingcap/tiflow/issues/4054)など、 [＃1606](https://github.com/pingcap/tiflow/issues/1606)と`mounter row`の監視メトリックとアラートをさらに追加し`table sink total row`

    -   バックアップと復元（BR）

        -   PD要求エラーまたはTiKVI/ Oタイムアウトエラーが発生した場合は、BRタスクを再試行してください[＃27787](https://github.com/pingcap/tidb/issues/27787)
        -   復元の堅牢性を向上させる[＃27421](https://github.com/pingcap/tidb/issues/27421)

    -   TiDB Lightning

        -   式インデックスまたは仮想生成列に依存するインデックスを持つテーブルへのデータのインポートをサポート[＃1404](https://github.com/pingcap/br/issues/1404)

## バグの修正 {#bug-fixes}

-   TiDB

    -   楽観的なトランザクションの競合により、トランザクションが互いにブロックする可能性があるという問題を修正します[＃11148](https://github.com/tikv/tikv/issues/11148)
    -   MPPクエリ[＃1791](https://github.com/pingcap/tics/issues/1791)の誤検知エラーログ`invalid cop task execution summaries length`の問題を修正します
    -   DMLステートメントとDDLステートメントが同時に実行されるときに発生する可能性のあるパニックを修正します[＃30940](https://github.com/pingcap/tidb/issues/30940)
    -   グローバルレベルの特権を付与および取り消すために`grant`および`revoke`の操作を実行するときの`privilege check fail`のエラーを修正します[＃29675](https://github.com/pingcap/tidb/issues/29675)
    -   場合によっては`ALTER TABLE.. ADD INDEX`ステートメントを実行するときのTiDBパニックを修正します[＃27687](https://github.com/pingcap/tidb/issues/27687)
    -   `enforce-mpp`構成が[＃29252](https://github.com/pingcap/tidb/issues/29252)で有効にならない問題を修正します。
    -   `ENUM`データ型[＃29357](https://github.com/pingcap/tidb/issues/29357)で`CASE WHEN`関数を使用するときのパニックを修正します
    -   ベクトル化された式[＃29244](https://github.com/pingcap/tidb/issues/29244)の`microsecond`関数の誤った結果を修正します
    -   `auto analyze`の結果からの不完全なログ情報の問題を修正します[＃29188](https://github.com/pingcap/tidb/issues/29188)
    -   ベクトル化された式[＃28643](https://github.com/pingcap/tidb/issues/28643)の`hour`関数の誤った結果を修正します
    -   サポートされていない`cast`がTiFlash5にプッシュダウンされたときの`tidb_cast to Int32 is not supported`などの予期しないエラーを修正し[＃23907](https://github.com/pingcap/tidb/issues/23907)
    -   一部のコーナーケースでMPPノードの可用性検出が機能しないバグを修正します[＃3118](https://github.com/pingcap/tics/issues/3118)
    -   35を割り当てるときの`DATA RACE` [＃27952](https://github.com/pingcap/tidb/issues/27952)問題を修正し`MPP task ID`
    -   空の[＃28250](https://github.com/pingcap/tidb/issues/28250)を削除した後のMPPクエリの`INDEX OUT OF RANGE`エラーを修正し`dual table`
    -   無効な日付値を同時に挿入するときのTiDBパニックを修正[＃25393](https://github.com/pingcap/tidb/issues/25393)
    -   MPPモード[＃30980](https://github.com/pingcap/tidb/issues/30980)でのクエリの予期しない`can not found column in Schema column`エラーを修正します
    -   TiFlashがシャットダウンしているときにTiDBがパニックになる可能性がある問題を修正します[＃28096](https://github.com/pingcap/tidb/issues/28096)
    -   プランナーが結合再注文[＃24095](https://github.com/pingcap/tidb/issues/24095)を実行しているときに予期しない`index out of range`エラーを修正します
    -   `ENUM`種類のデータをそのような関数のパラメーターとして使用する場合の制御関数（ `IF`や`CASE WHEN`など）の誤った結果を修正します[＃23114](https://github.com/pingcap/tidb/issues/23114)
    -   [＃29498](https://github.com/pingcap/tidb/issues/29498)の間違った結果を修正し`CONCAT(IFNULL(TIME(3))`
    -   符号なし`BIGINT`引数を渡すときの`GREATEST`と`LEAST`の誤った結果を修正します[＃30101](https://github.com/pingcap/tidb/issues/30101)
    -   JSON型の列が`CHAR`型の列に結合するとSQL操作がキャンセルされる問題を修正します[＃29401](https://github.com/pingcap/tidb/issues/29401)
    -   怠惰な存在チェックと手つかずのキーの最適化の誤った使用によって引き起こされるデータの不整合の問題を修正します[＃30410](https://github.com/pingcap/tidb/issues/30410)
    -   トランザクションを使用するかどうかにかかわらず、ウィンドウ関数が異なる結果を返す可能性がある問題を修正します[＃29947](https://github.com/pingcap/tidb/issues/29947)
    -   `cast(integer as char) union string`を含むSQLステートメントが間違った結果を返す問題を修正します[＃29513](https://github.com/pingcap/tidb/issues/29513)
    -   `Decimal`から[＃29417](https://github.com/pingcap/tidb/issues/29417)をキャストするときに長さ情報が間違っている問題を修正し`String`
    -   SQLステートメントに自然結合[＃25041](https://github.com/pingcap/tidb/issues/25041)が含まれている場合に`Column 'col_name' in field list is ambiguous`エラーが予期せず報告される問題を修正します
    -   `tidb_enable_vectorized_expression`の値が異なるために`GREATEST`関数が一貫性のない結果を返す問題を修正します（ `on`または`off`に設定） [＃29434](https://github.com/pingcap/tidb/issues/29434)
    -   プランナーが`join` 、場合によっては[＃28087](https://github.com/pingcap/tidb/issues/28087)の無効なプランをキャッシュする可能性がある問題を修正します
    -   SQLステートメントが結合の結果の集計結果を評価するときに`index out of range [1] with length 1`エラーが報告される問題を修正します[＃1978](https://github.com/pingcap/tics/issues/1978)

-   TiKV

    -   TiKVノードがダウンすると、解決されたタイムスタンプが[＃11351](https://github.com/tikv/tikv/issues/11351)遅れる問題を修正します。
    -   Raftクライアントの実装でバッチメッセージが大きすぎるという問題を修正します[＃9714](https://github.com/tikv/tikv/issues/9714)
    -   リージョンマージ、ConfChange、およびスナップショットが極端な条件で同時に発生するときに発生するパニックの問題を修正します[＃11475](https://github.com/tikv/tikv/issues/11475)
    -   TiKVが逆テーブルスキャンを実行すると、TiKVがメモリロックを検出できない問題を修正します[＃11440](https://github.com/tikv/tikv/issues/11440)
    -   10進数の除算結果がゼロの場合の負の符号の問題を修正します[＃29586](https://github.com/pingcap/tidb/issues/29586)
    -   GCタスクの蓄積によりTiKVがOOM（メモリ不足）になる可能性がある問題を修正します[＃11410](https://github.com/tikv/tikv/issues/11410)
    -   インスタンスごとのgRPCリクエストの平均レイテンシがTiKVメトリクス[＃11299](https://github.com/tikv/tikv/issues/11299)で不正確であるという問題を修正します
    -   統計スレッド[＃11195](https://github.com/tikv/tikv/issues/11195)の監視データによって引き起こされるメモリリークを修正します
    -   ダウンストリームデータベースが欠落しているときに発生するTiCDCパニックの問題を修正します[＃11123](https://github.com/tikv/tikv/issues/11123)
    -   輻輳エラー[＃11082](https://github.com/tikv/tikv/issues/11082)が原因でTiCDCがスキャンの再試行を頻繁に追加する問題を修正します
    -   チャネルがいっぱいになるとラフト接続が切断される問題を修正します[＃11047](https://github.com/tikv/tikv/issues/11047)
    -   TiDBLightningがデータをインポートするときにファイルが存在しない場合に発生するTiKVパニックの問題を修正します[＃10438](https://github.com/tikv/tikv/issues/10438)
    -   `Max`関数の`Int64`タイプが符号付き整数であるかどうかを[＃10158](https://github.com/tikv/tikv/issues/10158)が正しく識別できない問題を修正し`Min` 。これにより、 `Max` /911の誤った計算結果が発生し`Min` 。
    -   TiKVはメタデータを正確に変更できないため、ノードがスナップショットを取得した後にTiKVレプリカのノードがダウンする問題を修正します[＃10225](https://github.com/tikv/tikv/issues/10225)
    -   バックアップスレッドプール[＃10287](https://github.com/tikv/tikv/issues/10287)のリークの問題を修正します
    -   不正な文字列を浮動小数点数にキャストする問題を修正[＃23322](https://github.com/pingcap/tidb/issues/23322)

-   PD

    -   TiKVノードが削除された後に発生するパニックの問題を修正します[＃4344](https://github.com/tikv/pd/issues/4344)
    -   ダウンストア[＃3353](https://github.com/tikv/pd/issues/3353)が原因でオペレーターがブロックされる可能性がある問題を修正します
    -   スタックしたリージョンシンカー[＃3936](https://github.com/tikv/pd/issues/3936)によって引き起こされる遅いリーダー選出を修正
    -   ダウンノードを修復するときにピアを削除する速度が制限される問題を修正します[＃4090](https://github.com/tikv/pd/issues/4090)
    -   リージョンのハートビートが60秒未満の場合にホットスポットキャッシュをクリアできない問題を修正します[＃4390](https://github.com/tikv/pd/issues/4390)

-   TiFlash

    -   主キー列をより大きなintデータ型に変更した後の潜在的なデータの不整合を修正
    -   `libnsl.so`のライブラリがないために、ARMなどの一部のプラットフォームでTiFlashが起動しない問題を修正します
    -   `Store size`のメトリックがディスク上の実際のデータサイズと一致しない問題を修正します
    -   `Cannot open file`のエラーが原因でTiFlashがクラッシュする問題を修正します
    -   MPPクエリが強制終了されたときにTiFlashがクラッシュすることがある問題を修正しました
    -   予期しないエラーを修正する`3rd arguments of function substringUTF8 must be constants`
    -   過度の`OR`条件によって引き起こされるクエリの失敗を修正
    -   `where <string>`の結果が間違っているバグを修正します
    -   TiFlashとTiDB/TiKVの間で一貫性のない`CastStringAsDecimal`の動作を修正
    -   エラー`different types: expected Nullable(Int64), got Int64`によって引き起こされたクエリの失敗を修正します
    -   エラー`Unexpected type of column: Nullable(Nothing)`によって引き起こされたクエリの失敗を修正します
    -   `DECIMAL`のデータ型のデータを比較するときにオーバーフローが原因で発生するクエリの失敗を修正

-   ツール

    -   TiCDC

        -   `force-replicate`が有効になっている場合、有効なインデックスのない一部のパーティションテーブルが無視される可能性がある問題を修正します[＃2834](https://github.com/pingcap/tiflow/issues/2834)
        -   `cdc cli`予期しないパラメーターを受信すると、ユーザーパラメーターをサイレントに切り捨てて、ユーザー入力パラメーターが失われる問題を修正します[＃2303](https://github.com/pingcap/tiflow/issues/2303)
        -   Kafkaメッセージの書き込み中にエラーが発生したときにTiCDC同期タスクが一時停止する可能性がある問題を修正します[＃2978](https://github.com/pingcap/tiflow/issues/2978)
        -   一部のタイプの列をOpenProtocol形式にエンコードするときに発生する可能性のあるパニックの問題を修正します[＃2758](https://github.com/pingcap/tiflow/issues/2758)
        -   デフォルト値の`max-message-bytes`を[＃3081](https://github.com/pingcap/tiflow/issues/3081)に設定することにより、Kafkaが過度に大きなメッセージを送信する可能性がある問題を修正し`10M` 。
        -   アップストリームTiDBインスタンスが予期せず終了したときにTiCDCレプリケーションタスクが終了する可能性がある問題を修正します[＃3061](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKVが同じリージョン[＃2386](https://github.com/pingcap/tiflow/issues/2386)に重複したリクエストを送信すると、TiCDCプロセスがパニックになる可能性がある問題を修正します。
        -   複数のTiKVがクラッシュしたとき、または強制的に再起動したときのTiCDCレプリケーションの中断の問題を修正します[＃3288](https://github.com/pingcap/ticdc/issues/3288)
        -   チェンジフィードチェックポイントラグ[＃3010](https://github.com/pingcap/ticdc/issues/3010)の負の値のエラーを修正します
        -   MySQLシンクデッドロック[＃2706](https://github.com/pingcap/tiflow/issues/2706)によって引き起こされる過度に頻繁な警告の問題を修正します
        -   AvroシンクがJSONタイプの列の解析をサポートしていない問題を修正します[＃3624](https://github.com/pingcap/tiflow/issues/3624)
        -   TiKV所有者が再起動したときにTiCDCがTiKVから誤ったスキーマスナップショットを読み取るバグを修正します[＃2603](https://github.com/pingcap/tiflow/issues/2603)
        -   [＃3174](https://github.com/pingcap/ticdc/issues/3174)の処理後のメモリリークの問題を修正
        -   CanalおよびMaxwellプロトコル[＃3676](https://github.com/pingcap/tiflow/issues/3676)で`enable-old-value`の構成アイテムが自動的に`true`に設定されないバグを修正します。
        -   一部のRedHatEnterprise Linuxリリース（6.8や6.9など）で`cdc server`コマンドを実行したときに発生するタイムゾーンエラーを修正します[＃3584](https://github.com/pingcap/tiflow/issues/3584)
        -   Kafkaシンク[＃3431](https://github.com/pingcap/tiflow/issues/3431)の不正確な`txn_batch_size`モニタリングメトリックの問題を修正します
        -   チェンジフィードがない場合に`tikv_cdc_min_resolved_ts_no_change_for_1m`がアラートを出し続ける問題を修正します[＃11017](https://github.com/tikv/tikv/issues/11017)
        -   etcd1のタスクステータスを手動でクリーニングするときに発生するTiCDCパニックの問題を修正し[＃2980](https://github.com/pingcap/tiflow/issues/2980)
        -   ErrGCTTLExceededエラーが発生したときにchangefeedが十分に速く失敗しない問題を修正します[＃3111](https://github.com/pingcap/ticdc/issues/3111)
        -   ストックデータのスキャンに時間がかかりすぎると、TiKVがGCを実行するためにストックデータのスキャンが失敗する可能性がある問題を修正します[＃2470](https://github.com/pingcap/tiflow/issues/2470)
        -   コンテナ環境でのOOMの修正[＃1798](https://github.com/pingcap/ticdc/issues/1798)

    -   バックアップと復元（BR）

        -   バックアップと復元の平均速度が不正確に計算されるバグを修正します[＃1405](https://github.com/pingcap/br/issues/1405)

    -   Dumpling

        -   複合主キーまたは一意キー[＃29386](https://github.com/pingcap/tidb/issues/29386)を使用してテーブルをダンプすると、Dumplingが非常に遅くなるバグを修正します。
