---
title: TiDB 5.0.6 Release Notes
category: Releases
summary: TiDB 5.0.6 は 2021 年 12 月 31 日にリリースされました。このリリースには、TiCDC、TiKV、PD、 TiDB Lightning、 TiFlash、Backup & Restore (BR)、 Dumplingなどのさまざまなツールに対する互換性の変更、改善、バグ修正、更新が含まれています。変更には、エラー処理の強化、パフォーマンスの改善、SQL ステートメントに関連するバグ修正、さまざまなツールのさまざまな最適化が含まれます。
---

# TiDB 5.0.6 リリースノート {#tidb-5-0-6-release-notes}

発売日: 2021年12月31日

TiDB バージョン: 5.0.6

## 互換性の変更 {#compatibility-changes}

-   ツール

    -   ティCDC

        -   `cdc server`コマンドエラーの出力を stdout から stderr [＃3133](https://github.com/pingcap/tiflow/issues/3133)に変更します
        -   Kafkaシンク`max-message-bytes`のデフォルト値を`10M` [＃3081](https://github.com/pingcap/tiflow/issues/3081)に設定する
        -   TiCDC がメッセージを Kafka パーティション間でより均等に分散するように、Kafka シンクのデフォルト値を`partition-num`から 3 に変更します[＃3337](https://github.com/pingcap/ticdc/issues/3337)

## 改善点 {#improvements}

-   ティビ

    -   コプロセッサがロックに遭遇したときに影響を受けるSQL文をデバッグログに表示します。これは問題の診断に役立ちます[＃27718](https://github.com/pingcap/tidb/issues/27718)

-   ティクヴ

    -   検証プロセスを`Apply`スレッドプール[＃11239](https://github.com/tikv/tikv/issues/11239)から`Import`スレッドプールに移動することで、SSTファイルの挿入速度が向上します。
    -   モジュール[＃11374](https://github.com/tikv/tikv/issues/11374)のパフォーマンスの問題を特定するために、 Raftログのガベージコレクションモジュールのメトリックを追加します。
    -   Grafana ダッシュボード[＃11681](https://github.com/tikv/tikv/issues/11681)で、ストレージ関連の珍しいメトリックをいくつか折りたたむ

-   PD

    -   スケジューラ[＃4146](https://github.com/tikv/pd/issues/4146)の終了プロセスを高速化
    -   スケジューラが空のリージョンをスケジュールできるようにし、スケジューラ[＃4497](https://github.com/tikv/pd/issues/4497)の構成を修正することで、スケジューラ`scatter-range-scheduler`のスケジュール結果をより均等にします。
    -   リーダー排除スケジューラが不健全なピアを持つリージョンをスケジュールできるようにサポート[＃4093](https://github.com/tikv/pd/issues/4093)

-   ツール

    -   ティCDC

        -   TiKV リロードのレート制限制御を最適化して、チェンジフィード初期化中の gPRC 輻輳を軽減します[＃3110](https://github.com/pingcap/ticdc/issues/3110)
        -   頻繁な etcd 書き込みが PD サービスに影響を与えないように、EtcdWorker にティック頻度制限を追加します[＃3112](https://github.com/pingcap/ticdc/issues/3112)
        -   Kafkaシンク[＃3352](https://github.com/pingcap/tiflow/issues/3352)の`config.Metadata.Timeout`のデフォルト設定を追加する
        -   デフォルト値の`max-message-bytes`を`10M`に設定して、Kafkaメッセージが送信できない可能性を減らします[＃3081](https://github.com/pingcap/tiflow/issues/3081)
        -   `no owner alert` [＃4054](https://github.com/pingcap/tiflow/issues/4054)含む`buffer sink total row`と`table sink total row`の監視メトリックと[＃1606](https://github.com/pingcap/tiflow/issues/1606)を追加します`mounter row`

    -   バックアップと復元 (BR)

        -   PD 要求エラーまたは TiKV I/O タイムアウト エラーが発生した場合は、 BRタスクを再試行します[＃27787](https://github.com/pingcap/tidb/issues/27787)
        -   復元の堅牢性を向上させる[＃27421](https://github.com/pingcap/tidb/issues/27421)

    -   TiDB Lightning

        -   式インデックスまたは仮想生成列に依存するインデックスを持つテーブルへのデータのインポートをサポート[＃1404](https://github.com/pingcap/br/issues/1404)

## バグの修正 {#bug-fixes}

-   ティビ

    -   楽観的トランザクションの競合によりトランザクションが互いにブロックされる可能性がある問題を修正[＃11148](https://github.com/tikv/tikv/issues/11148)
    -   MPPクエリ[＃1791](https://github.com/pingcap/tics/issues/1791)の誤検知エラーログ`invalid cop task execution summaries length`の問題を修正
    -   DML 文と DDL 文が同時に実行されるときに発生する可能性のあるpanicを修正[＃30940](https://github.com/pingcap/tidb/issues/30940)
    -   グローバルレベルの権限を付与および取り消す操作`grant`および`revoke`を実行するときに発生する`privilege check fail`エラーを修正します[＃29675](https://github.com/pingcap/tidb/issues/29675)
    -   場合によっては`ALTER TABLE.. ADD INDEX`文を実行するときに TiDBpanicが発生する問題を修正[＃27687](https://github.com/pingcap/tidb/issues/27687)
    -   v5.0.4 [＃29252](https://github.com/pingcap/tidb/issues/29252)で`enforce-mpp`設定が有効にならない問題を修正
    -   `ENUM`データ型[＃29357](https://github.com/pingcap/tidb/issues/29357)で`CASE WHEN`関数を使用するときに発生するpanicを修正
    -   ベクトル化された式[＃29244](https://github.com/pingcap/tidb/issues/29244)の`microsecond`関数の誤った結果を修正
    -   `auto analyze`の結果[＃29188](https://github.com/pingcap/tidb/issues/29188)からの不完全なログ情報の問題を修正
    -   ベクトル化された式[＃28643](https://github.com/pingcap/tidb/issues/28643)の関数`hour`の誤った結果を修正
    -   サポートされていない`cast`がTiFlash [＃23907](https://github.com/pingcap/tidb/issues/23907)にプッシュダウンされたときに発生する`tidb_cast to Int32 is not supported`ような予期しないエラーを修正
    -   MPPノードの可用性検出が一部のコーナーケースで機能しないバグを修正[＃3118](https://github.com/pingcap/tics/issues/3118)
    -   `MPP task ID` [＃27952](https://github.com/pingcap/tidb/issues/27952)を割り当てる際の`DATA RACE`問題を修正
    -   空の`dual table` [＃28250](https://github.com/pingcap/tidb/issues/28250)を削除した後のMPPクエリの`INDEX OUT OF RANGE`エラーを修正
    -   無効な日付値を同時に挿入するときに発生する TiDBpanicを修正[＃25393](https://github.com/pingcap/tidb/issues/25393)
    -   MPPモード[＃30980](https://github.com/pingcap/tidb/issues/30980)のクエリの予期しないエラー`can not found column in Schema column`を修正
    -   TiFlashがシャットダウンするときに TiDB がpanicになる可能性がある問題を修正[＃28096](https://github.com/pingcap/tidb/issues/28096)
    -   プランナーが結合順序変更[＃24095](https://github.com/pingcap/tidb/issues/24095)を実行しているときに発生する予期しないエラー`index out of range`を修正しました
    -   `ENUM`型データを制御関数のパラメータとして使用する場合の、制御関数( `IF`や`CASE WHEN`など) の誤った結果を修正[＃23114](https://github.com/pingcap/tidb/issues/23114)
    -   `CONCAT(IFNULL(TIME(3))` [＃29498](https://github.com/pingcap/tidb/issues/29498)の間違った結果を修正
    -   符号なし`BIGINT`引数[#30101](https://github.com/pingcap/tidb/issues/30101)を渡すときに`GREATEST`と`LEAST`の間違った結果を修正
    -   JSON 型の列が`CHAR`型の列[＃29401](https://github.com/pingcap/tidb/issues/29401)に結合すると SQL 操作がキャンセルされる問題を修正しました。
    -   遅延存在チェックと未変更キー最適化の誤った使用によって発生するデータ不整合の問題を修正[＃30410](https://github.com/pingcap/tidb/issues/30410)
    -   トランザクションを使用する場合と使用しない場合でウィンドウ関数が異なる結果を返す可能性がある問題を修正しました[＃29947](https://github.com/pingcap/tidb/issues/29947)
    -   `cast(integer as char) union string`含む SQL 文が間違った結果を返す問題を修正[＃29513](https://github.com/pingcap/tidb/issues/29513)
    -   `Decimal`から`String` [＃29417](https://github.com/pingcap/tidb/issues/29417)へのキャスト時に長さ情報が間違っている問題を修正
    -   SQL文に自然結合[＃25041](https://github.com/pingcap/tidb/issues/25041)が含まれている場合に`Column 'col_name' in field list is ambiguous`エラーが予期せず報告される問題を修正
    -   `GREATEST`関数が`tidb_enable_vectorized_expression`の値が異なるために矛盾した結果を返す問題を修正 ( `on`または`off`に設定) [＃29434](https://github.com/pingcap/tidb/issues/29434)
    -   プランナーが`join`の無効なプランをキャッシュする場合がある問題を修正[＃28087](https://github.com/pingcap/tidb/issues/28087)
    -   SQL 文が結合の結果に基づいて集計結果を評価する場合に、 `index out of range [1] with length 1`エラーが報告される場合がある問題を修正しました[＃1978](https://github.com/pingcap/tics/issues/1978)

-   ティクヴ

    -   TiKVノードがダウンすると解決されたタイムスタンプが[＃11351](https://github.com/tikv/tikv/issues/11351)遅れる問題を修正
    -   Raftクライアント実装[＃9714](https://github.com/tikv/tikv/issues/9714)でバッチメッセージが大きすぎる問題を修正
    -   極端な状況でリージョンのマージ、ConfChange、スナップショットが同時に発生した場合に発生するpanicの問題を修正[＃11475](https://github.com/tikv/tikv/issues/11475)
    -   TiKVが逆テーブルスキャンを実行するときにメモリロックを検出できない問題を修正[＃11440](https://github.com/tikv/tikv/issues/11440)
    -   小数点以下の除算結果がゼロの場合の負の符号の問題を修正[＃29586](https://github.com/pingcap/tidb/issues/29586)
    -   GCタスクの蓄積によりTiKVがOOM（メモリ不足）になる可能性がある問題を修正[＃11410](https://github.com/tikv/tikv/issues/11410)
    -   TiKV メトリック[＃11299](https://github.com/tikv/tikv/issues/11299)でインスタンスごとの gRPC リクエストの平均レイテンシーが不正確になる問題を修正
    -   統計スレッド[＃11195](https://github.com/tikv/tikv/issues/11195)のデータの監視によって発生するメモリリークを修正
    -   ダウンストリームデータベースが見つからない場合に発生する TiCDCpanicの問題を修正[＃11123](https://github.com/tikv/tikv/issues/11123)
    -   TiCDC が輻輳エラー[＃11082](https://github.com/tikv/tikv/issues/11082)によりスキャン再試行を頻繁に追加する問題を修正
    -   チャネルがいっぱいになるとRaft接続が切断される問題を修正[＃11047](https://github.com/tikv/tikv/issues/11047)
    -   TiDB Lightningがデータをインポートする際にファイルが存在しない場合に発生するTiKVpanicの問題を修正[＃10438](https://github.com/tikv/tikv/issues/10438)
    -   TiDBが`Max`関数の`Int64`型が符号付き整数であるかどうかを正しく識別できず、 `Max` / `Min` [＃10158](https://github.com/tikv/tikv/issues/10158)の計算結果が間違ってしまう問題を修正しました`Min`
    -   TiKV がメタデータを正確に変更できないため、ノードがスナップショットを取得した後に TiKV レプリカのノードがダウンする問題を修正しました[＃10225](https://github.com/tikv/tikv/issues/10225)
    -   バックアップスレッドプール[＃10287](https://github.com/tikv/tikv/issues/10287)のリーク問題を修正
    -   不正な文字列を浮動小数点数にキャストする問題を修正[＃23322](https://github.com/pingcap/tidb/issues/23322)

-   PD

    -   TiKVノードが削除された後に発生するpanic問題を修正[＃4344](https://github.com/tikv/pd/issues/4344)
    -   ストア[＃3353](https://github.com/tikv/pd/issues/3353)ダウンによりオペレーターがブロックされる問題を修正
    -   リージョン同期装置[＃3936](https://github.com/tikv/pd/issues/3936)停止によりリーダー選出が遅くなる問題を修正
    -   ダウンしたノードを修復する際にピアの削除速度が制限される問題を修正[＃4090](https://github.com/tikv/pd/issues/4090)
    -   リージョンハートビートが60秒未満の場合にホットスポットキャッシュをクリアできない問題を修正[＃4390](https://github.com/tikv/pd/issues/4390)

-   TiFlash

    -   主キー列をより大きな int データ型に変更した後に発生する可能性のあるデータの不整合を修正します。
    -   `libnsl.so`ライブラリがないため、ARMなどの一部のプラットフォームでTiFlashが起動に失敗する問題を修正しました。
    -   `Store size`メトリックがディスク上の実際のデータ サイズと一致しない問題を修正しました
    -   `Cannot open file`エラーによりTiFlashがクラッシュする問題を修正
    -   MPPクエリが強制終了されたときにTiFlashが時々クラッシュする問題を修正
    -   予期しないエラーを修正`3rd arguments of function substringUTF8 must be constants`
    -   `OR`条件が多すぎるために発生するクエリの失敗を修正
    -   `where <string>`の結果が間違っているバグを修正
    -   TiFlashとTiDB/TiKV間の`CastStringAsDecimal`の不一致な動作を修正
    -   エラー`different types: expected Nullable(Int64), got Int64`によるクエリの失敗を修正
    -   エラー`Unexpected type of column: Nullable(Nothing)`によるクエリの失敗を修正
    -   `DECIMAL`データ型のデータを比較するときにオーバーフローによって発生するクエリの失敗を修正

-   ツール

    -   ティCDC

        -   `force-replicate`が有効になっている場合に、有効なインデックスのない一部のパーティションテーブルが無視される可能性がある問題を修正[＃2834](https://github.com/pingcap/tiflow/issues/2834)
        -   予期しないパラメータを受け取ったときにユーザーパラメータを暗黙的に`cdc cli` 、ユーザー入力パラメータが失われる問題を修正しました[＃2303](https://github.com/pingcap/tiflow/issues/2303)
        -   Kafka メッセージの書き込み中にエラーが発生すると TiCDC 同期タスクが一時停止する可能性がある問題を修正[＃2978](https://github.com/pingcap/tiflow/issues/2978)
        -   一部のタイプの列を Open Protocol 形式[＃2758](https://github.com/pingcap/tiflow/issues/2758)にエンコードするときに発生する可能性のあるpanic問題を修正しました。
        -   デフォルト値の`max-message-bytes`を`10M` [＃3081](https://github.com/pingcap/tiflow/issues/3081)に設定することで、Kafkaが過度に大きなメッセージを送信する可能性がある問題を修正しました。
        -   上流の TiDB インスタンスが予期せず終了すると TiCDC レプリケーション タスクが終了する可能性がある問題を修正[＃3061](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKV が同じリージョン[＃2386](https://github.com/pingcap/tiflow/issues/2386)に重複したリクエストを送信したときに TiCDC プロセスがpanicになる可能性がある問題を修正しました。
        -   複数の TiKV がクラッシュした場合や強制再起動中に TiCDC レプリケーションが中断される問題を修正[＃3288](https://github.com/pingcap/ticdc/issues/3288)
        -   チェンジフィードチェックポイントラグ[＃3010](https://github.com/pingcap/ticdc/issues/3010)負の値エラーを修正
        -   MySQLシンクデッドロック[＃2706](https://github.com/pingcap/tiflow/issues/2706)による警告が頻繁に発生する問題を修正
        -   AvroシンクがJSON型列[＃3624](https://github.com/pingcap/tiflow/issues/3624)の解析をサポートしていない問題を修正
        -   TiKV所有者が再起動したときにTiCDCがTiKVから誤ったスキーマスナップショットを読み取るバグを修正[＃2603](https://github.com/pingcap/tiflow/issues/2603)
        -   DDL [＃3174](https://github.com/pingcap/ticdc/issues/3174)の処理後のメモリリークの問題を修正
        -   Canalプロトコル[＃3676](https://github.com/pingcap/tiflow/issues/3676)で設定項目`enable-old-value`が`true`に自動的に設定されないバグを修正
        -   一部のRed Hat Enterprise Linuxリリース（6.8や6.9など）で`cdc server`コマンドを実行すると発生するタイムゾーンエラーを修正しました[＃3584](https://github.com/pingcap/tiflow/issues/3584)
        -   Kafka シンク[＃3431](https://github.com/pingcap/tiflow/issues/3431)の不正確な`txn_batch_size`監視メトリックの問題を修正しました
        -   `tikv_cdc_min_resolved_ts_no_change_for_1m`チェンジフィードがない場合に警告が継続する問題を修正[＃11017](https://github.com/tikv/tikv/issues/11017)
        -   etcd [＃2980](https://github.com/pingcap/tiflow/issues/2980)でタスク ステータスを手動でクリーンアップするときに発生する TiCDCpanicの問題を修正しました。
        -   ErrGCTTLExceeded エラーが発生したときに changefeed が十分に速く失敗しない問題を修正[＃3111](https://github.com/pingcap/ticdc/issues/3111)
        -   株価データのスキャンに時間がかかりすぎると、TiKV が GC を実行するため株価データのスキャンが失敗する可能性がある問題を修正[＃2470](https://github.com/pingcap/tiflow/issues/2470)
        -   コンテナ環境の OOM を修正[＃1798](https://github.com/pingcap/ticdc/issues/1798)

    -   バックアップと復元 (BR)

        -   バックアップとリストアの平均速度が不正確に計算されるバグを修正[＃1405](https://github.com/pingcap/br/issues/1405)

    -   Dumpling

        -   複合主キーまたは一意キー[＃29386](https://github.com/pingcap/tidb/issues/29386)を持つテーブルをダンプするときにDumpling が非常に遅くなるバグを修正しました。
