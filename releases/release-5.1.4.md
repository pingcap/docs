---
title: TiDB 5.1.4 Release Notes
---

# TiDB5.1.4リリースノート {#tidb-5-1-4-release-notes}

発売日：2022年2月22日

TiDBバージョン：5.1.4

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   システム変数[`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510)のデフォルト値を`2`から[＃31748](https://github.com/pingcap/tidb/issues/31748)に変更し`1` 。
    -   v5.1.4以降、TiKVが`storage.enable-ttl = true`で構成されている場合、TiKVのTTL機能は[RawKVモード](https://tikv.org/docs/5.1/concepts/explore-tikv-features/ttl/) [＃27303](https://github.com/pingcap/tidb/issues/27303)のみをサポートするため、TiDBからの要求は拒否されます。

-   ツール

    -   TiCDC

        -   デフォルト値の`max-message-bytes`を設定します[＃4041](https://github.com/pingcap/tiflow/issues/4041)

## 改善 {#improvements}

-   TiDB

    -   Rangeパーティションテーブル[＃26739](https://github.com/pingcap/tidb/issues/26739)の組み込み`IN`式のパーティションプルーニングをサポートします。
    -   `IndexJoin`が実行されたときのメモリ使用量の追跡の精度を向上させます[＃28650](https://github.com/pingcap/tidb/issues/28650)

-   TiKV

    -   procファイルシステム（procfs）をv0.12.0に更新します[＃11702](https://github.com/tikv/tikv/issues/11702)
    -   Raftクライアントのエラーログレポートを改善する[＃11959](https://github.com/tikv/tikv/issues/11959)
    -   検証プロセスを`Apply`スレッドプールから`Import`スレッドプールに移動して、SSTファイルの挿入速度を上げます[＃11239](https://github.com/tikv/tikv/issues/11239)

-   PD

    -   スケジューラーの終了プロセスを高速化する[＃4146](https://github.com/tikv/pd/issues/4146)

-   TiFlash

    -   `ADDDATE()`と`DATE_ADD()`をTiFlashにプッシュダウンすることをサポート
    -   `INET6_ATON()`と`INET6_NTOA()`をTiFlashにプッシュダウンすることをサポート
    -   `INET_ATON()`と`INET_NTOA()`をTiFlashにプッシュダウンすることをサポート
    -   DAGリクエストでサポートされる式またはプランツリーの最大深度を`100`から`200`に増やします。

-   ツール

    -   TiCDC

        -   チェンジフィードを再開するための指数バックオフメカニズムを追加します。 [＃3329](https://github.com/pingcap/tiflow/issues/3329)
        -   多くのテーブルを複製するときの複製待ち時間を短縮する[＃3900](https://github.com/pingcap/tiflow/issues/3900)
        -   インクリメンタルスキャンの残り時間を監視するためのメトリックを追加する[＃2985](https://github.com/pingcap/tiflow/issues/2985)
        -   「EventFeed再試行率制限」ログの数を減らす[＃4006](https://github.com/pingcap/tiflow/issues/4006)
        -   `no owner alert` `buffer sink total row` [＃4054](https://github.com/pingcap/tiflow/issues/4054)など、 [＃1606](https://github.com/pingcap/tiflow/issues/1606)と`mounter row`の監視メトリックとアラートをさらに追加し`table sink total row`
        -   TiKVリロードのレート制限制御を最適化して、チェンジフィード初期化中のgPRC輻輳を低減します[＃3110](https://github.com/pingcap/ticdc/issues/3110)
        -   TiKVストアがダウンしたときにKVクライアントが回復する時間を短縮する[＃3191](https://github.com/pingcap/tiflow/issues/3191)

## バグの修正 {#bug-fixes}

-   TiDB

    -   システム変数`tidb_analyze_version`が[＃32499](https://github.com/pingcap/tidb/issues/32499)に設定されているときに発生するメモリリークのバグを修正し`2` 。
    -   `MaxDays`と`MaxBackups`の構成が遅いログ[＃25716](https://github.com/pingcap/tidb/issues/25716)に対して有効にならない問題を修正します
    -   `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE`ステートメントを実行するとパニックになる問題を修正します[＃28078](https://github.com/pingcap/tidb/issues/28078)
    -   `ENUM`のタイプの列で`JOIN`を実行するときに発生する可能性のある間違った結果を修正します[＃27831](https://github.com/pingcap/tidb/issues/27831)
    -   INDEXHASHJOINが`send on closed channel`エラー[＃31129](https://github.com/pingcap/tidb/issues/31129)を返す問題を修正します
    -   [`BatchCommands`](/tidb-configuration-file.md#max-batch-size) APIを使用すると、まれにTiKVへのTiDBリクエストの送信がブロックされる可能性がある問題を修正します[＃32500](https://github.com/pingcap/tidb/issues/32500)
    -   楽観的なトランザクションモード[＃30410](https://github.com/pingcap/tidb/issues/30410)での潜在的なデータインデックスの不整合の問題を修正します
    -   トランザクションを使用するかどうかにかかわらず、ウィンドウ関数が異なる結果を返す可能性がある問題を修正します[＃29947](https://github.com/pingcap/tidb/issues/29947)
    -   `Decimal`から[＃29417](https://github.com/pingcap/tidb/issues/29417)をキャストするときに長さ情報が間違っている問題を修正し`String`
    -   `tidb_enable_vectorized_expression`ベクトル化された式を[＃29434](https://github.com/pingcap/tidb/issues/29434)に設定すると、 `GREATEST`関数が誤った結果を返す問題を修正し`off` 。
    -   オプティマイザーが`join` 、場合によっては[＃28087](https://github.com/pingcap/tidb/issues/28087)の無効なプランをキャッシュする可能性がある問題を修正します
    -   ベクトル化された式の`microsecond`および`hour`関数の[＃28643](https://github.com/pingcap/tidb/issues/28643)た結果を修正する[＃29244](https://github.com/pingcap/tidb/issues/29244)
    -   場合によっては`ALTER TABLE.. ADD INDEX`ステートメントを実行するときのTiDBパニックを修正します[＃27687](https://github.com/pingcap/tidb/issues/27687)
    -   一部のコーナーケースでMPPノードの可用性検出が機能しないバグを修正します[＃3118](https://github.com/pingcap/tics/issues/3118)
    -   35を割り当てるときの`DATA RACE` [＃27952](https://github.com/pingcap/tidb/issues/27952)問題を修正し`MPP task ID`
    -   空の[＃28250](https://github.com/pingcap/tidb/issues/28250)を削除した後のMPPクエリの`INDEX OUT OF RANGE`エラーを修正し`dual table`
    -   MPPクエリ[＃1791](https://github.com/pingcap/tics/issues/1791)の誤検知エラーログ`invalid cop task execution summaries length`の問題を修正します
    -   SET GLOBAL tidb_skip_isolation_level_check=1が新しいセッション設定に影響を与えない問題を修正します[＃27897](https://github.com/pingcap/tidb/issues/27897)

-   TiKV

    -   GCワーカーがビジー状態のときにTiKVがデータの範囲を削除できない（ `unsafe_destroy_range`は実行できない）バグを修正します[＃11903](https://github.com/tikv/tikv/issues/11903)
    -   ピアを破棄すると待ち時間が長くなる可能性があるという問題を修正します[＃10210](https://github.com/tikv/tikv/issues/10210)
    -   領域が空の場合に`any_value`関数が間違った結果を返すバグを修正します[＃11735](https://github.com/tikv/tikv/issues/11735)
    -   初期化されていないレプリカを削除すると、古いレプリカが再作成される可能性がある問題を修正します[＃10533](https://github.com/tikv/tikv/issues/10533)
    -   新しい選択が終了した後に`Prepare Merge`がトリガーされたが、分離されたピアに通知されない場合のメタデータ破損の問題を修正します[＃11526](https://github.com/tikv/tikv/issues/11526)
    -   コルーチンの実行速度が速すぎる場合に時々発生するデッドロックの問題を修正します[＃11549](https://github.com/tikv/tikv/issues/11549)
    -   フレームグラフをプロファイリングするときに発生する可能性のあるデッドロックとメモリリークの問題を修正する[＃11108](https://github.com/tikv/tikv/issues/11108)
    -   悲観的なトランザクションで事前書き込み要求を再試行するときのまれなデータの不整合の問題を修正します[＃11187](https://github.com/tikv/tikv/issues/11187)
    -   構成`resource-metering.enabled`が機能しないバグを修正します[＃11235](https://github.com/tikv/tikv/issues/11235)
    -   一部のコルーチンが[＃10965](https://github.com/tikv/tikv/issues/10965)でリークする問題を修正し`resolved_ts`
    -   書き込みフローが少ない場合に誤った「GCが機能しない」アラートを報告する問題を修正します[＃9910](https://github.com/tikv/tikv/issues/9910)
    -   tikv-ctlが正しいリージョン関連情報を返さないバグを修正します[＃11393](https://github.com/tikv/tikv/issues/11393)
    -   TiKVノードがダウンすると、解決されたタイムスタンプが[＃11351](https://github.com/tikv/tikv/issues/11351)遅れる問題を修正します。
    -   リージョンマージ、ConfChange、およびスナップショットが極端な条件で同時に発生するときに発生するパニックの問題を修正します[＃11475](https://github.com/tikv/tikv/issues/11475)
    -   TiKVが逆テーブルスキャンを実行すると、TiKVがメモリロックを検出できない問題を修正します[＃11440](https://github.com/tikv/tikv/issues/11440)
    -   10進数の除算結果がゼロの場合の負の符号の問題を修正します[＃29586](https://github.com/pingcap/tidb/issues/29586)
    -   統計スレッド[＃11195](https://github.com/tikv/tikv/issues/11195)の監視データによって引き起こされるメモリリークを修正します
    -   ダウンストリームデータベースが欠落しているときに発生するTiCDCパニックの問題を修正します[＃11123](https://github.com/tikv/tikv/issues/11123)
    -   輻輳エラー[＃11082](https://github.com/tikv/tikv/issues/11082)が原因でTiCDCがスキャンの再試行を頻繁に追加する問題を修正します
    -   Raftクライアントの実装でバッチメッセージが大きすぎるという問題を修正します[＃9714](https://github.com/tikv/tikv/issues/9714)
    -   Grafanaダッシュボード[＃11681](https://github.com/tikv/tikv/issues/11681)でいくつかの一般的でないストレージ関連のメトリックを折りたたむ

-   PD

    -   リージョンスキャッターによって生成されたスケジュールによってピアの数が減少する可能性があるバグを修正します[＃4565](https://github.com/tikv/pd/issues/4565)
    -   リージョン統計が[＃4295](https://github.com/tikv/pd/issues/4295)の影響を受けない問題を修正し`flow-round-by-digit`
    -   スタックしたリージョンシンカー[＃3936](https://github.com/tikv/pd/issues/3936)によって引き起こされる遅いリーダー選出を修正
    -   エビクトリーダースケジューラが異常なピアのあるリージョンをスケジュールできることをサポートする[＃4093](https://github.com/tikv/pd/issues/4093)
    -   コールドホットスポットデータをホットスポット統計から削除できない問題を修正します[＃4390](https://github.com/tikv/pd/issues/4390)
    -   TiKVノードが削除された後に発生するパニックの問題を修正します[＃4344](https://github.com/tikv/pd/issues/4344)
    -   ターゲットストアがダウンしているためにスケジューリングオペレーターが迅速に失敗できない問題を修正します[＃3353](https://github.com/tikv/pd/issues/3353)

-   TiFlash

    -   マイクロ秒を解析するときに`str_to_date()`関数が先行ゼロを誤って処理する問題を修正します
    -   メモリ制限が有効になっている場合のTiFlashクラッシュの問題を修正します
    -   入力時刻が1970-01-0100:00:01UTCより前の場合、 `unix_timestamp`の動作がTiDBまたはMySQLの動作と矛盾する問題を修正します。
    -   主キーがハンドルであるときに主キー列を広げることによって引き起こされる潜在的なデータの不整合を修正します
    -   `DECIMAL`のデータ型のデータを比較するときにオーバーフローのバグと`Can't compare`のエラーを報告する問題を修正します
    -   `3rd arguments of function substringUTF8 must be constants.`の予期しないエラーを修正します
    -   `nsl`のライブラリがないプラットフォームでTiFlashを起動できない問題を修正します
    -   データを`DECIMAL`データ型にキャストするときのオーバーフローのバグを修正しました
    -   `castStringAsReal`の動作がTiFlashとTiDB/TiKVで一貫していない問題を修正します
    -   再起動後にTiFlashが`EstablishMPPConnection`エラーを返す可能性がある問題を修正します
    -   TiFlashレプリカの数を0に設定した後、廃止されたデータを再利用できない問題を修正します
    -   `CastStringAsDecimal`の動作がTiFlashとTiDB/TiKVで一貫していない問題を修正します
    -   `where <string>`句を使用したクエリが間違った結果を返す問題を修正します
    -   MPPクエリが停止したときにTiFlashがパニックになる可能性がある問題を修正します
    -   `Unexpected type of column: Nullable(Nothing)`の予期しないエラーを修正します

-   ツール

    -   TiCDC

        -   `batch-replace-enable`が無効になっている場合にMySQLシンクが重複した`replace`のSQLステートメントを生成するバグを修正します[＃4501](https://github.com/pingcap/tiflow/issues/4501)
        -   `cached region`モニタリングメトリックが負の[＃4300](https://github.com/pingcap/tiflow/issues/4300)である問題を修正します
        -   `min.insync.replicas`が[＃3994](https://github.com/pingcap/tiflow/issues/3994)より小さい場合、レプリケーションを実行できない問題を修正し`replication-factor` 。
        -   レプリケーションタスクが削除されたときに発生する可能性のあるパニックの問題を修正する[＃3128](https://github.com/pingcap/tiflow/issues/3128)
        -   不正確なチェックポイント[＃3545](https://github.com/pingcap/tiflow/issues/3545)によって引き起こされる潜在的なデータ損失の問題を修正します
        -   デッドロックによってレプリケーションタスクがスタックするという潜在的な問題を修正します[＃4055](https://github.com/pingcap/tiflow/issues/4055)
        -   DDLステートメントの特別なコメントによってレプリケーションタスクが停止する問題を修正します[＃3755](https://github.com/pingcap/tiflow/issues/3755)
        -   EtcdWorkerが所有者とプロセッサをハングさせる可能性があるバグを修正します[＃3750](https://github.com/pingcap/tiflow/issues/3750)
        -   クラスタのアップグレード後に`stopped`つのチェンジフィードが自動的に再開する問題を修正します[＃3473](https://github.com/pingcap/tiflow/issues/3473)
        -   デフォルト値を複製できない問題を修正します[＃3793](https://github.com/pingcap/tiflow/issues/3793)
        -   TiCDCのデフォルト値のパディング例外によって引き起こされるデータの不整合を修正し[＃3929](https://github.com/pingcap/tiflow/issues/3929) [＃3918](https://github.com/pingcap/tiflow/issues/3918)
        -   PDリーダーがシャットダウンして新しいノードに転送したときに所有者がスタックするバグを修正します[＃3615](https://github.com/pingcap/tiflow/issues/3615)
        -   etcd1のタスクステータスを手動でクリーニングするときに発生するTiCDCパニックの問題を修正し[＃2980](https://github.com/pingcap/tiflow/issues/2980)
        -   RHELリリース[＃3584](https://github.com/pingcap/tiflow/issues/3584)のタイムゾーンの問題が原因でサービスを開始できない問題を修正します
        -   MySQLシンクデッドロック[＃2706](https://github.com/pingcap/tiflow/issues/2706)によって引き起こされる過度に頻繁な警告の問題を修正します
        -   CanalおよびMaxwellプロトコル[＃3676](https://github.com/pingcap/tiflow/issues/3676)で`enable-old-value`の構成アイテムが自動的に`true`に設定されないバグを修正します。
        -   AvroシンクがJSONタイプの列の解析をサポートしていない問題を修正します[＃3624](https://github.com/pingcap/tiflow/issues/3624)
        -   チェンジフィードチェックポイントラグ[＃3010](https://github.com/pingcap/ticdc/issues/3010)の負の値のエラーを修正します
        -   コンテナ環境でのOOMの問題を修正する[＃1798](https://github.com/pingcap/tiflow/issues/1798)
        -   複数のTiKVがクラッシュしたとき、または強制的に再起動したときのTiCDCレプリケーションの中断の問題を修正します[＃3288](https://github.com/pingcap/ticdc/issues/3288)
        -   [＃3174](https://github.com/pingcap/ticdc/issues/3174)の処理後のメモリリークの問題を修正
        -   ErrGCTTLExceededエラーが発生したときにchangefeedが十分に速く失敗しない問題を修正します[＃3111](https://github.com/pingcap/ticdc/issues/3111)
        -   アップストリームTiDBインスタンスが予期せず終了したときにTiCDCレプリケーションタスクが終了する可能性がある問題を修正します[＃3061](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKVが同じリージョン[＃2386](https://github.com/pingcap/tiflow/issues/2386)に重複したリクエストを送信すると、TiCDCプロセスがパニックになる可能性がある問題を修正します。
        -   デフォルト値の`max-message-bytes`を[＃3081](https://github.com/pingcap/tiflow/issues/3081)に設定することにより、Kafkaが過度に大きなメッセージを送信する可能性がある問題を修正し`10M` 。
        -   Kafkaメッセージの書き込み中にエラーが発生したときにTiCDC同期タスクが一時停止する可能性がある問題を修正します[＃2978](https://github.com/pingcap/tiflow/issues/2978)

    -   バックアップと復元（BR）

        -   復元操作の終了後にリージョンが不均一に分散される可能性があるという潜在的な問題を修正し[＃31034](https://github.com/pingcap/tidb/issues/31034) [＃30425](https://github.com/pingcap/tidb/issues/30425)

    -   TiDB Binlog

        -   CSVファイルのサイズが約256MBで、 `strict-format`が`true` [＃27763](https://github.com/pingcap/tidb/issues/27763)の場合、CSVのインポートがInvalidRangeで失敗する問題を修正します。

    -   TiDB Lightning

        -   S3ストレージパスが存在しない場合にTiDBLightningがエラーを報告しない問題を修正し[＃30709](https://github.com/pingcap/tidb/issues/30709) [＃28031](https://github.com/pingcap/tidb/issues/28031)
