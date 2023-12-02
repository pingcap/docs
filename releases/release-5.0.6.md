---
title: TiDB 5.0.6 Release Notes
category: Releases
---

# TiDB 5.0.6 リリースノート {#tidb-5-0-6-release-notes}

発売日：2021年12月31日

TiDB バージョン: 5.0.6

## 互換性の変更 {#compatibility-changes}

-   ツール

    -   TiCDC

        -   `cdc server`コマンド エラーの出力を stdout から stderr [#3133](https://github.com/pingcap/tiflow/issues/3133)に変更します。
        -   Kafka シンクのデフォルト値を`max-message-bytes` ～ `10M` [#3081](https://github.com/pingcap/tiflow/issues/3081)に設定します。
        -   TiCDC が Kafka パーティション間でメッセージをより均等に分散できるように、Kafka Sink のデフォルト値`partition-num`を[#3337](https://github.com/pingcap/ticdc/issues/3337)に変更します。

## 改善点 {#improvements}

-   TiDB

    -   コプロセッサーがロックを検出したときに、影響を受ける SQL ステートメントをデバッグ ログに表示します。これは、問題の診断に役立ちます[#27718](https://github.com/pingcap/tidb/issues/27718)

-   TiKV

    -   検証プロセスを`Apply`スレッド プール[#11239](https://github.com/tikv/tikv/issues/11239)から`Import`スレッド プールに移動することで、SST ファイルの挿入速度が向上しました。
    -   Raftログのガベージコレクションモジュールにメトリクスを追加して、モジュール[#11374](https://github.com/tikv/tikv/issues/11374)のパフォーマンスの問題を特定します。
    -   Grafana ダッシュボードでいくつかの一般的ではないストレージ関連のメトリクスを折りたたむ[#11681](https://github.com/tikv/tikv/issues/11681)

-   PD

    -   スケジューラの終了プロセスを高速化[#4146](https://github.com/tikv/pd/issues/4146)
    -   スケジューラ`scatter-range-scheduler`が空のリージョンをスケジュールし、スケジューラ[#4497](https://github.com/tikv/pd/issues/4497)の構成を修正できるようにすることで、スケジューラ 1 のスケジューリング結果をより均一にします。
    -   エビクト リーダー スケジューラが異常なピアのあるリージョンをスケジュールできることのサポート[#4093](https://github.com/tikv/pd/issues/4093)

-   ツール

    -   TiCDC

        -   TiKV リロードのレート制限制御を最適化し、チェンジフィードの初期化中の gPRC の輻輳を軽減します[#3110](https://github.com/pingcap/ticdc/issues/3110)
        -   頻繁な etcd 書き込みが PD サービスに影響を与えるのを防ぐために、EtcdWorker にティック頻度制限を追加します[#3112](https://github.com/pingcap/ticdc/issues/3112)
        -   Kafka シンク[#3352](https://github.com/pingcap/tiflow/issues/3352)に`config.Metadata.Timeout`のデフォルト構成を追加します。
        -   Kafka メッセージが送信できない可能性を減らすには、デフォルト値の`max-message-bytes`を`10M`に設定します[#3081](https://github.com/pingcap/tiflow/issues/3081)
        -   `no owner alert` 、 `mounter row` 、 `table sink total row` 、 `buffer sink total row`などの Prometheus および Grafana モニタリング メトリックとアラートを追加します[#4054](https://github.com/pingcap/tiflow/issues/4054) [#1606](https://github.com/pingcap/tiflow/issues/1606)

    -   バックアップと復元 (BR)

        -   PD リクエスト エラーまたは TiKV I/O タイムアウト エラー[#27787](https://github.com/pingcap/tidb/issues/27787)が発生した場合にBRタスクを再試行します。
        -   復元の堅牢性の向上[#27421](https://github.com/pingcap/tidb/issues/27421)

    -   TiDB Lightning

        -   式インデックスまたは仮想生成列に依存するインデックスを持つテーブルへのデータのインポートをサポートします[#1404](https://github.com/pingcap/br/issues/1404)

## バグの修正 {#bug-fixes}

-   TiDB

    -   楽観的トランザクションの競合によってトランザクションが互いにブロックされる可能性がある問題を修正します[#11148](https://github.com/tikv/tikv/issues/11148)
    -   MPP クエリ[#1791](https://github.com/pingcap/tics/issues/1791)の誤検知エラー ログ`invalid cop task execution summaries length`の問題を修正します。
    -   DML ステートメントと DDL ステートメントが同時に実行されるときに発生する可能性があるpanicを修正します[#30940](https://github.com/pingcap/tidb/issues/30940)
    -   グローバル レベルの権限を付与および取り消すための`grant`および`revoke`操作を実行するときの`privilege check fail`エラーを修正します[#29675](https://github.com/pingcap/tidb/issues/29675)
    -   場合によっては`ALTER TABLE.. ADD INDEX`ステートメント実行時の TiDBpanicを修正[#27687](https://github.com/pingcap/tidb/issues/27687)
    -   `enforce-mpp`設定が v5.0.4 で有効にならない問題を修正[#29252](https://github.com/pingcap/tidb/issues/29252)
    -   `ENUM`データ型[#29357](https://github.com/pingcap/tidb/issues/29357)で`CASE WHEN`関数を使用するときのpanicを修正しました。
    -   ベクトル化された式[#29244](https://github.com/pingcap/tidb/issues/29244)の関数`microsecond`の誤った結果を修正します。
    -   `auto analyze`結果[#29188](https://github.com/pingcap/tidb/issues/29188)のログ情報が不完全である問題を修正
    -   ベクトル化された式[#28643](https://github.com/pingcap/tidb/issues/28643)の関数`hour`の誤った結果を修正しました。
    -   サポートされていない`cast`がTiFlash [#23907](https://github.com/pingcap/tidb/issues/23907)にプッシュダウンされた場合の`tidb_cast to Int32 is not supported`のような予期しないエラーを修正
    -   MPP ノードの可用性検出が一部の特殊なケースで機能しないバグを修正[#3118](https://github.com/pingcap/tics/issues/3118)
    -   `MPP task ID` [#27952](https://github.com/pingcap/tidb/issues/27952)を割り当てるときの`DATA RACE`問題を修正
    -   空`dual table` [#28250](https://github.com/pingcap/tidb/issues/28250)を削除した後の MPP クエリの`INDEX OUT OF RANGE`エラーを修正
    -   無効な日付値を同時に挿入した場合の TiDBpanicを修正[#25393](https://github.com/pingcap/tidb/issues/25393)
    -   MPP モード[#30980](https://github.com/pingcap/tidb/issues/30980)でのクエリの予期しない`can not found column in Schema column`エラーを修正しました。
    -   TiFlashのシャットダウン時に TiDB がpanicになる問題を修正[#28096](https://github.com/pingcap/tidb/issues/28096)
    -   プランナーが結合再順序[#24095](https://github.com/pingcap/tidb/issues/24095)を実行しているときの予期しない`index out of range`エラーを修正しました。
    -   制御関数（ `IF`や`CASE WHEN`など）の関数として`ENUM`種類のデータを使用した場合の誤った結果を修正[#23114](https://github.com/pingcap/tidb/issues/23114)
    -   `CONCAT(IFNULL(TIME(3))` [#29498](https://github.com/pingcap/tidb/issues/29498)の間違った結果を修正します
    -   符号なし`BIGINT`引数[#30101](https://github.com/pingcap/tidb/issues/30101)を渡すときの`GREATEST`と`LEAST`の間違った結果を修正
    -   JSON 型の列が`CHAR`型の列[#29401](https://github.com/pingcap/tidb/issues/29401)に結合すると SQL 操作がキャンセルされる問題を修正
    -   遅延存在チェックとアンタッチドキー最適化の誤った使用によって引き起こされるデータの不整合の問題を修正します[#30410](https://github.com/pingcap/tidb/issues/30410)
    -   トランザクションを使用する場合と使用しない場合に、ウィンドウ関数が異なる結果を返す可能性がある問題を修正します[#29947](https://github.com/pingcap/tidb/issues/29947)
    -   `cast(integer as char) union string`を含む SQL ステートメントが間違った結果を返す問題を修正します[#29513](https://github.com/pingcap/tidb/issues/29513)
    -   `Decimal` ～ `String` [#29417](https://github.com/pingcap/tidb/issues/29417)をキャストする際に長さ情報が間違っている問題を修正
    -   SQL ステートメントに自然結合[#25041](https://github.com/pingcap/tidb/issues/25041)が含まれる場合、予期せず`Column 'col_name' in field list is ambiguous`エラーが報告される問題を修正します。
    -   `tidb_enable_vectorized_expression`の値が異なるために`GREATEST`関数が一貫性のない結果を返す問題を修正します ( `on`または`off`に設定) [#29434](https://github.com/pingcap/tidb/issues/29434)
    -   場合によってはプランナーが`join`の無効なプランをキャッシュする可能性がある問題を修正します[#28087](https://github.com/pingcap/tidb/issues/28087)
    -   SQL文で結合結果の集計結果を評価すると、場合によっては`index out of range [1] with length 1`エラーが報告される問題を修正[#1978](https://github.com/pingcap/tics/issues/1978)

-   TiKV

    -   TiKV ノードがダウンすると解決されたタイムスタンプが[#11351](https://github.com/tikv/tikv/issues/11351)遅れる問題を修正
    -   Raftクライアント実装[#9714](https://github.com/tikv/tikv/issues/9714)でバッチメッセージが大きすぎる問題を修正
    -   極端な条件でリージョンのマージ、ConfChange、およびスナップショットが同時に発生したときに発生するpanicの問題を修正します[#11475](https://github.com/tikv/tikv/issues/11475)
    -   TiKV が逆テーブル スキャンを実行するときに TiKV がメモリロックを検出できない問題を修正します[#11440](https://github.com/tikv/tikv/issues/11440)
    -   10 進数の除算結果が 0 の場合の負号の問題を修正します[#29586](https://github.com/pingcap/tidb/issues/29586)
    -   GC タスクの蓄積によって TiKV が OOM (メモリ不足) になる可能性がある問題を修正します[#11410](https://github.com/tikv/tikv/issues/11410)
    -   TiKV メトリクス[#11299](https://github.com/tikv/tikv/issues/11299)でインスタンスごとの gRPC リクエストの平均レイテンシーが不正確である問題を修正します。
    -   統計スレッド[#11195](https://github.com/tikv/tikv/issues/11195)のデータ監視によって発生するメモリリークを修正しました。
    -   ダウンストリーム データベースが見つからない場合に発生する TiCDCpanicの問題を修正します[#11123](https://github.com/tikv/tikv/issues/11123)
    -   TiCDC が輻輳エラー[#11082](https://github.com/tikv/tikv/issues/11082)によりスキャンの再試行を頻繁に追加する問題を修正します。
    -   チャンネルがいっぱいの場合、 Raft接続が切断される問題を修正[#11047](https://github.com/tikv/tikv/issues/11047)
    -   TiDB Lightning がデータをインポートするときにファイルが存在しない場合に発生する TiKVpanicの問題を修正します[#10438](https://github.com/tikv/tikv/issues/10438)
    -   TiDB が`Max` / `Min`関数の`Int64`型が符号付き整数であるかどうかを正しく識別できず、 `Max` / `Min`という間違った計算結果が発生する問題を修正[#10158](https://github.com/tikv/tikv/issues/10158)
    -   TiKV がメタデータを正確に変更できないため、ノードがスナップショットを取得した後に TiKV レプリカのノードがダウンする問題を修正します[#10225](https://github.com/tikv/tikv/issues/10225)
    -   バックアップ スレッド プール[#10287](https://github.com/tikv/tikv/issues/10287)のリーク問題を修正
    -   不正な文字列を浮動小数点数にキャストする問題を修正します[#23322](https://github.com/pingcap/tidb/issues/23322)

-   PD

    -   TiKV ノードが削除された後に発生するpanicの問題を修正します[#4344](https://github.com/tikv/pd/issues/4344)
    -   ダウンストア[#3353](https://github.com/tikv/pd/issues/3353)が原因でオペレーターがブロックされる可能性がある問題を修正
    -   リージョン装置[#3936](https://github.com/tikv/pd/issues/3936)のスタックによって引き起こされるリーダー選出の遅さを修正
    -   ダウンしたノードを修復するときにピアの削除速度が制限される問題を修正します[#4090](https://github.com/tikv/pd/issues/4090)
    -   リージョンのハートビートが 60 秒未満の場合にホットスポット キャッシュをクリアできない問題を修正します[#4390](https://github.com/tikv/pd/issues/4390)

-   TiFlash

    -   主キー列をより大きな int データ型に変更した後の潜在的なデータの不整合を修正
    -   `libnsl.so`ライブラリがないため、ARM などの一部のプラットフォームでTiFlashが起動できない問題を修正
    -   `Store size`メトリックがディスク上の実際のデータ サイズと一致しない問題を修正
    -   `Cannot open file`エラーによりTiFlashがクラッシュする問題を修正
    -   MPP クエリが強制終了されたときにTiFlashが時折クラッシュする問題を修正
    -   予期しないエラーを修正する`3rd arguments of function substringUTF8 must be constants`
    -   過剰な`OR`条件によって引き起こされるクエリの失敗を修正
    -   `where <string>`の結果が間違っているバグを修正
    -   TiFlashと TiDB/TiKV の間の`CastStringAsDecimal`の一貫性のない動作を修正
    -   エラー`different types: expected Nullable(Int64), got Int64`によるクエリの失敗を修正
    -   エラー`Unexpected type of column: Nullable(Nothing)`によるクエリの失敗を修正
    -   `DECIMAL`データ型のデータを比較するときにオーバーフローが原因で発生するクエリのエラーを修正

-   ツール

    -   TiCDC

        -   `force-replicate`が有効な場合、有効なインデックスのない一部のパーティション テーブルが無視される可能性がある問題を修正します[#2834](https://github.com/pingcap/tiflow/issues/2834)
        -   予期しないパラメータを受信したときにユーザー パラメータが`cdc cli`に切り捨てられ、ユーザー入力パラメータが失われる問題を修正します[#2303](https://github.com/pingcap/tiflow/issues/2303)
        -   Kafka メッセージの書き込み中にエラーが発生したときに TiCDC 同期タスクが一時停止することがある問題を修正します[#2978](https://github.com/pingcap/tiflow/issues/2978)
        -   一部の種類の列をオープン プロトコル形式[#2758](https://github.com/pingcap/tiflow/issues/2758)にエンコードするときに発生する可能性のpanicの問題を修正しました。
        -   デフォルト値の`max-message-bytes` ～ `10M` [#3081](https://github.com/pingcap/tiflow/issues/3081)設定することで、Kafka が過度に大きなメッセージを送信する可能性がある問題を修正します。
        -   上流の TiDB インスタンスが予期せず終了すると、TiCDC レプリケーション タスクが終了する可能性がある問題を修正します[#3061](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKV が同じリージョン[#2386](https://github.com/pingcap/tiflow/issues/2386)に重複したリクエストを送信すると、TiCDC プロセスがパニックになる可能panicがある問題を修正
        -   複数の TiKV がクラッシュしたとき、または強制再起動中に TiCDC レプリケーションが中断される問題を修正します[#3288](https://github.com/pingcap/ticdc/issues/3288)
        -   チェンジフィードチェックポイントラグ[#3010](https://github.com/pingcap/ticdc/issues/3010)の負の値エラーを修正
        -   MySQL シンクのデッドロックによって引き起こされる過度に頻繁な警告の問題を修正します[#2706](https://github.com/pingcap/tiflow/issues/2706)
        -   Avro シンクが JSON 型列の解析をサポートしていない問題を修正します[#3624](https://github.com/pingcap/tiflow/issues/3624)
        -   TiKV 所有者が再起動したときに、TiCDC が TiKV から誤ったスキーマ スナップショットを読み取るバグを修正[#2603](https://github.com/pingcap/tiflow/issues/2603)
        -   DDL 処理後のメモリリーク問題を修正[#3174](https://github.com/pingcap/ticdc/issues/3174)
        -   Canal および Maxwell プロトコル[#3676](https://github.com/pingcap/tiflow/issues/3676)で`enable-old-value`設定項目が自動的に`true`に設定されないバグを修正
        -   `cdc server`コマンドが一部の Red Hat Enterprise Linux リリース (6.8 や 6.9 など) で実行されるときに発生するタイムゾーン エラーを修正します[#3584](https://github.com/pingcap/tiflow/issues/3584)
        -   Kafka シンク[#3431](https://github.com/pingcap/tiflow/issues/3431)の不正確な`txn_batch_size`監視メトリクスの問題を修正
        -   変更フィード[#11017](https://github.com/tikv/tikv/issues/11017)がないときに`tikv_cdc_min_resolved_ts_no_change_for_1m`がアラートを出し続ける問題を修正します。
        -   etcd [#2980](https://github.com/pingcap/tiflow/issues/2980)でタスクステータスを手動でクリーンアップするときに発生する TiCDCpanicの問題を修正します。
        -   ErrGCTTLExceeded エラーが発生したときに変更フィードが十分な速度で失敗しない問題を修正します[#3111](https://github.com/pingcap/ticdc/issues/3111)
        -   ストック データのスキャンに時間がかかりすぎる場合、TiKV が GC を実行するためにストック データのスキャンが失敗する可能性がある問題を修正します[#2470](https://github.com/pingcap/tiflow/issues/2470)
        -   コンテナ環境での OOM の修正[#1798](https://github.com/pingcap/ticdc/issues/1798)

    -   バックアップと復元 (BR)

        -   バックアップおよびリストア[#1405](https://github.com/pingcap/br/issues/1405)の平均速度が不正確に計算されるバグを修正

    -   Dumpling

        -   複合主キーまたは一意キーを持つテーブルをダンプするとDumplingが非常に遅くなるバグを修正[#29386](https://github.com/pingcap/tidb/issues/29386)
