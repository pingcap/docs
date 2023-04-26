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
        -   Kafka シンク`max-message-bytes`のデフォルト値を`10M` [#3081](https://github.com/pingcap/tiflow/issues/3081)に設定します
        -   Kafka Sink `partition-num`のデフォルト値を 3 に変更して、TiCDC が Kafka パーティション間でメッセージをより均等に分散するようにします[#3337](https://github.com/pingcap/ticdc/issues/3337)

## 改良点 {#improvements}

-   TiDB

    -   コプロセッサーがロックを検出したときに、影響を受ける SQL ステートメントをデバッグ・ログに表示します。これは、問題の診断に役立ちます[#27718](https://github.com/pingcap/tidb/issues/27718)

-   TiKV

    -   検証プロセスを`Apply`スレッド プール[#11239](https://github.com/tikv/tikv/issues/11239)から`Import`スレッド プールに移動することで、SST ファイルの挿入速度を向上させます。
    -   Raftログのガベージコレクションモジュールにメトリックを追加して、モジュール[#11374](https://github.com/tikv/tikv/issues/11374)のパフォーマンスの問題を特定します。
    -   Grafana ダッシュボード[#11681](https://github.com/tikv/tikv/issues/11681)でいくつかの一般的でないストレージ関連の指標を折りたたむ

-   PD

    -   スケジューラーの終了プロセスを高速化する[#4146](https://github.com/tikv/pd/issues/4146)
    -   スケジューラーが空のリージョンをスケジュールし、スケジューラー[#4497](https://github.com/tikv/pd/issues/4497)の構成を修正できるようにすることで、 `scatter-range-scheduler`スケジューラーのスケジューリング結果をより均一にします。
    -   エビクト リーダー スケジューラが異常なピアを持つリージョンをスケジュールできるようにサポートします[#4093](https://github.com/tikv/pd/issues/4093)

-   ツール

    -   TiCDC

        -   TiKV リロードのレート制限制御を最適化して、変更フィードの初期化中の gPRC の輻輳を軽減します[#3110](https://github.com/pingcap/ticdc/issues/3110)
        -   EtcdWorker にティック頻度制限を追加して、頻繁な etcd 書き込みが PD サービスに影響を与えないようにします[#3112](https://github.com/pingcap/ticdc/issues/3112)
        -   Kafka シンク[#3352](https://github.com/pingcap/tiflow/issues/3352)に`config.Metadata.Timeout`の既定の構成を追加します。
        -   デフォルト値の`max-message-bytes`から`10M`を設定して、Kafka メッセージを送信できない可能性を減らします[#3081](https://github.com/pingcap/tiflow/issues/3081)
        -   `no owner alert` 、 `mounter row` 、 `table sink total row` 、および`buffer sink total row` [#4054](https://github.com/pingcap/tiflow/issues/4054) [#1606](https://github.com/pingcap/tiflow/issues/1606)を含む、Prometheus および Grafana のモニタリング メトリックとアラートをさらに追加します。

    -   バックアップと復元 (BR)

        -   PD 要求エラーまたは TiKV I/O タイムアウト エラー[#27787](https://github.com/pingcap/tidb/issues/27787)が発生したときにBRタスクを再試行します
        -   復元の堅牢性の向上[#27421](https://github.com/pingcap/tidb/issues/27421)

    -   TiDB Lightning

        -   式インデックスまたは仮想生成列に依存するインデックスを持つテーブルへのデータのインポートをサポート[#1404](https://github.com/pingcap/br/issues/1404)

## バグの修正 {#bug-fixes}

-   TiDB

    -   楽観的トランザクションの競合により、トランザクションが相互にブロックされる可能性があるという問題を修正します[#11148](https://github.com/tikv/tikv/issues/11148)
    -   MPP クエリ[#1791](https://github.com/pingcap/tics/issues/1791)の誤検知エラー ログ`invalid cop task execution summaries length`の問題を修正します。
    -   DML ステートメントと DDL ステートメントが同時に実行されたときに発生する可能性があるpanicを修正します[#30940](https://github.com/pingcap/tidb/issues/30940)
    -   `grant`および`revoke`操作を実行してグローバル レベルの権限を付与および取り消すときの`privilege check fail`エラーを修正します[#29675](https://github.com/pingcap/tidb/issues/29675)
    -   場合によっては`ALTER TABLE.. ADD INDEX`ステートメントを実行すると TiDBpanicが発生する問題を修正[#27687](https://github.com/pingcap/tidb/issues/27687)
    -   `enforce-mpp`設定が v5.0.4 で有効にならない問題を修正[#29252](https://github.com/pingcap/tidb/issues/29252)
    -   `ENUM`データ型[#29357](https://github.com/pingcap/tidb/issues/29357)で`CASE WHEN`関数を使用したときのpanicを修正
    -   ベクトル化された式[#29244](https://github.com/pingcap/tidb/issues/29244)の`microsecond`関数の間違った結果を修正
    -   `auto analyze`結果[#29188](https://github.com/pingcap/tidb/issues/29188)の不完全なログ情報の問題を修正
    -   ベクトル化された式[#28643](https://github.com/pingcap/tidb/issues/28643)の`hour`関数の間違った結果を修正
    -   サポートされていない`cast` TiFlash [#23907](https://github.com/pingcap/tidb/issues/23907)に押し下げると`tidb_cast to Int32 is not supported`のような予期しないエラーが発生する問題を修正
    -   一部のまれなケースで MPP ノードの可用性検出が機能しないバグを修正します[#3118](https://github.com/pingcap/tics/issues/3118)
    -   `MPP task ID` [#27952](https://github.com/pingcap/tidb/issues/27952)を割り当てる際の`DATA RACE`問題を修正
    -   空`dual table` [#28250](https://github.com/pingcap/tidb/issues/28250)を削除した後の MPP クエリの`INDEX OUT OF RANGE`エラーを修正
    -   無効な日付値を同時に挿入する場合の TiDBpanicを修正します[#25393](https://github.com/pingcap/tidb/issues/25393)
    -   MPP モード[#30980](https://github.com/pingcap/tidb/issues/30980)でのクエリの予期しない`can not found column in Schema column`エラーを修正
    -   TiFlashのシャットダウン時に TiDB がpanicになる問題を修正[#28096](https://github.com/pingcap/tidb/issues/28096)
    -   プランナーが結合リオーダー[#24095](https://github.com/pingcap/tidb/issues/24095)を行っているときの予期しないエラー`index out of range`を修正します。
    -   制御関数( `IF`や`CASE WHEN`など) のような関数のパラメーターとして`ENUM`型のデータを使用する場合の誤った結果を修正します[#23114](https://github.com/pingcap/tidb/issues/23114)
    -   `CONCAT(IFNULL(TIME(3))` [#29498](https://github.com/pingcap/tidb/issues/29498)の間違った結果を修正
    -   符号なし`BIGINT`引数を渡すときの`GREATEST`と`LEAST`の間違った結果を修正[#30101](https://github.com/pingcap/tidb/issues/30101)
    -   JSON 型の列が`CHAR`型の列を結合すると SQL 操作がキャンセルされる問題を修正します[#29401](https://github.com/pingcap/tidb/issues/29401)
    -   レイジー存在チェックと手付かずのキー最適化の誤った使用によって引き起こされるデータの不整合の問題を修正します[#30410](https://github.com/pingcap/tidb/issues/30410)
    -   トランザクションを使用する場合と使用しない場合で、ウィンドウ関数が異なる結果を返すことがある問題を修正します[#29947](https://github.com/pingcap/tidb/issues/29947)
    -   `cast(integer as char) union string`を含む SQL ステートメントが間違った結果を返す問題を修正します[#29513](https://github.com/pingcap/tidb/issues/29513)
    -   `Decimal`から`String` [#29417](https://github.com/pingcap/tidb/issues/29417)をキャストするとき、長さの情報が間違っている問題を修正
    -   SQL ステートメントに自然結合[#25041](https://github.com/pingcap/tidb/issues/25041)が含まれていると、予期せず`Column 'col_name' in field list is ambiguous`エラーが報告される問題を修正します。
    -   `tidb_enable_vectorized_expression`の異なる値 ( `on`または`off`に設定) が原因で`GREATEST`関数が一貫性のない結果を返す問題を修正します[#29434](https://github.com/pingcap/tidb/issues/29434)
    -   プランナーが場合によっては`join`の無効なプランをキャッシュする可能性がある問題を修正します[#28087](https://github.com/pingcap/tidb/issues/28087)
    -   SQL文でjoinの結果に対して集計結果を評価すると、場合によっては`index out of range [1] with length 1`エラーが報告される問題を修正[#1978](https://github.com/pingcap/tics/issues/1978)

-   TiKV

    -   TiKV ノードがダウンしていると、解決されたタイムスタンプが[#11351](https://github.com/tikv/tikv/issues/11351)遅れる問題を修正します。
    -   Raftクライアント実装[#9714](https://github.com/tikv/tikv/issues/9714)でバッチ メッセージが大きすぎる問題を修正
    -   極端な状況でリージョンのマージ、ConfChange、およびスナップショットが同時に発生したときに発生するpanicの問題を修正します[#11475](https://github.com/tikv/tikv/issues/11475)
    -   TiKV がリバース テーブル スキャンを実行すると、TiKV がメモリロックを検出できない問題を修正します[#11440](https://github.com/tikv/tikv/issues/11440)
    -   10 進数の除算結果がゼロ[#29586](https://github.com/pingcap/tidb/issues/29586)の場合の負号の問題を修正
    -   GC タスクの蓄積により、TiKV が OOM (メモリ不足) になる可能性がある問題を修正します[#11410](https://github.com/tikv/tikv/issues/11410)
    -   インスタンスごとの gRPC リクエストの平均レイテンシーが TiKV メトリクスで不正確である問題を修正します[#11299](https://github.com/tikv/tikv/issues/11299)
    -   統計スレッド[#11195](https://github.com/tikv/tikv/issues/11195)のデータを監視することによって引き起こされるメモリリークを修正します。
    -   ダウンストリーム データベースが見つからない場合に発生する TiCDCpanicの問題を修正します[#11123](https://github.com/tikv/tikv/issues/11123)
    -   Congest エラー[#11082](https://github.com/tikv/tikv/issues/11082)により、TiCDC がスキャンの再試行を頻繁に追加する問題を修正します。
    -   チャネルがいっぱいになるとRaft接続が切断される問題を修正します[#11047](https://github.com/tikv/tikv/issues/11047)
    -   TiDB Lightning がデータをインポートする際にファイルが存在しない場合に TiKVpanicが発生する問題を修正[#10438](https://github.com/tikv/tikv/issues/10438)
    -   TiDB が`Max` / `Min`関数の`Int64`型が符号付き整数かどうかを正しく識別できず、 `Max` / `Min` [#10158](https://github.com/tikv/tikv/issues/10158)という誤った計算結果になる問題を修正
    -   TiKV がメタデータを[#10225](https://github.com/tikv/tikv/issues/10225)に変更できないため、ノードがスナップショットを取得した後に TiKV レプリカのノードがダウンする問題を修正します。
    -   バックアップ スレッド プール[#10287](https://github.com/tikv/tikv/issues/10287)のリークの問題を修正します。
    -   不正な文字列を浮動小数点数にキャストする問題を修正します[#23322](https://github.com/pingcap/tidb/issues/23322)

-   PD

    -   TiKV ノードが削除された後に発生するpanicの問題を修正します[#4344](https://github.com/tikv/pd/issues/4344)
    -   ダウン ストアが原因でオペレーターがブロックされる可能性がある問題を修正します[#3353](https://github.com/tikv/pd/issues/3353)
    -   リージョン syncer [#3936](https://github.com/tikv/pd/issues/3936)のスタックによるリーダー選出の遅さを修正
    -   ダウンしたノードの修復時にピアの削除速度が制限される問題を修正します[#4090](https://github.com/tikv/pd/issues/4090)
    -   リージョンのハートビートが 60 秒未満の場合、ホットスポット キャッシュをクリアできない問題を修正します[#4390](https://github.com/tikv/pd/issues/4390)

-   TiFlash

    -   主キー列をより大きな int データ型に変更した後の潜在的なデータ不整合を修正
    -   ARM などの一部のプラットフォームで、 `libnsl.so`のライブラリが存在しないためにTiFlash が起動しない問題を修正
    -   `Store size`メトリックがディスク上の実際のデータ サイズと一致しない問題を修正します。
    -   `Cannot open file`エラーでTiFlashがクラッシュする問題を修正
    -   MPP クエリが強制終了されたときにTiFlashがときどきクラッシュする問題を修正
    -   予期しないエラーを修正する`3rd arguments of function substringUTF8 must be constants`
    -   過剰な`OR`条件によるクエリの失敗を修正する
    -   `where <string>`の結果がおかしくなるバグを修正
    -   TiFlashと TiDB/TiKV の間で一貫性のない`CastStringAsDecimal`の動作を修正
    -   エラー`different types: expected Nullable(Int64), got Int64`によるクエリの失敗を修正する
    -   エラー`Unexpected type of column: Nullable(Nothing)`によるクエリの失敗を修正する
    -   `DECIMAL`データ型のデータを比較するときのオーバーフローによって引き起こされるクエリの失敗を修正します

-   ツール

    -   TiCDC

        -   `force-replicate`が有効な場合、有効なインデックスのない一部のパーティション テーブルが無視される可能性があるという問題を修正します[#2834](https://github.com/pingcap/tiflow/issues/2834)
        -   `cdc cli`予期しないパラメーターを受け取ったときにユーザー パラメーターが暗黙のうちに切り捨てられ、ユーザー入力パラメーターが失われる問題を修正します[#2303](https://github.com/pingcap/tiflow/issues/2303)
        -   Kafka メッセージの書き込み中にエラーが発生すると、TiCDC 同期タスクが一時停止することがある問題を修正します[#2978](https://github.com/pingcap/tiflow/issues/2978)
        -   一部のタイプの列を Open Protocol フォーマット[#2758](https://github.com/pingcap/tiflow/issues/2758)にエンコードする際に発生する可能性があったpanicの問題を修正
        -   デフォルト値を`max-message-bytes`から`10M` [#3081](https://github.com/pingcap/tiflow/issues/3081)に設定することにより、Kafka が過度に大きなメッセージを送信する可能性がある問題を修正します。
        -   アップストリームの TiDB インスタンスが予期せず終了すると、TiCDC レプリケーション タスクが終了する可能性がある問題を修正します[#3061](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKV が同じリージョン[#2386](https://github.com/pingcap/tiflow/issues/2386)に重複したリクエストを送信すると、TiCDC プロセスがパニックになる可能panicがある問題を修正します。
        -   複数の TiKV がクラッシュしたとき、または強制再起動中に TiCDC レプリケーションが中断する問題を修正します[#3288](https://github.com/pingcap/ticdc/issues/3288)
        -   changefeed チェックポイントラグ[#3010](https://github.com/pingcap/ticdc/issues/3010)の負の値のエラーを修正します。
        -   MySQL シンクのデッドロック[#2706](https://github.com/pingcap/tiflow/issues/2706)が原因で頻繁に警告が表示される問題を修正
        -   Avro シンクが JSON 型の列の解析をサポートしていない問題を修正します[#3624](https://github.com/pingcap/tiflow/issues/3624)
        -   TiKV 所有者が再起動すると、TiCDC が TiKV から誤ったスキーマ スナップショットを読み取るバグを修正します[#2603](https://github.com/pingcap/tiflow/issues/2603)
        -   DDL [#3174](https://github.com/pingcap/ticdc/issues/3174)の処理後のメモリリークの問題を修正します。
        -   Canal および Maxwell プロトコル[#3676](https://github.com/pingcap/tiflow/issues/3676)で`enable-old-value`構成項目が自動的に`true`に設定されないバグを修正
        -   `cdc server`の Red Hat Enterprise Linux リリース (6.8 や 6.9 など) でコマンドを実行するときに発生するタイムゾーン エラーを修正します[#3584](https://github.com/pingcap/tiflow/issues/3584)
        -   Kafka シンク[#3431](https://github.com/pingcap/tiflow/issues/3431)の不正確な`txn_batch_size`モニタリング メトリックの問題を修正します
        -   `tikv_cdc_min_resolved_ts_no_change_for_1m`変更フィードがないときにアラートが鳴り続ける問題を修正[#11017](https://github.com/tikv/tikv/issues/11017)
        -   etcd [#2980](https://github.com/pingcap/tiflow/issues/2980)でタスク ステータスを手動でクリーニングするときに発生する TiCDCpanicの問題を修正します。
        -   ErrGCTTLExceeded エラーが発生したときに changefeed が十分な速さで失敗しないという問題を修正します[#3111](https://github.com/pingcap/ticdc/issues/3111)
        -   株式データのスキャンに時間がかかりすぎると、TiKV が GC を実行するために株式データのスキャンが失敗する可能性がある問題を修正します[#2470](https://github.com/pingcap/tiflow/issues/2470)
        -   コンテナ環境で OOM を修正する[#1798](https://github.com/pingcap/ticdc/issues/1798)

    -   バックアップと復元 (BR)

        -   バックアップとリストアの平均速度が不正確に計算されるバグを修正[#1405](https://github.com/pingcap/br/issues/1405)

    -   Dumpling

        -   複合主キーまたは一意キー[#29386](https://github.com/pingcap/tidb/issues/29386)を持つテーブルをダンプすると、Dumplingが非常に遅くなるバグを修正
