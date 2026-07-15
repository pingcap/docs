---
title: TiDB 5.1.4 Release Notes
summary: "TiDB 5.1.4 リリースノート: 互換性の変更には、システム変数のデフォルト値の変更が含まれます。パーティションプルーニング、メモリ使用量の追跡、SST ファイルの挿入速度が向上しました。バグ修正により、メモリリーク、構成の問題、および誤ったクエリ結果が修正されました。TiCDC やTiFlashなどのツールにも、さまざまな修正と改善が加えられました。"
---

# TiDB 5.1.4 リリースノート {#tidb-5-1-4-release-notes}

リリース日：2022年2月22日

TiDB バージョン: 5.1.4

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   システム変数[`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510)のデフォルト値を`2`から`1`に変更します[＃31748](https://github.com/pingcap/tidb/issues/31748)
    -   v5.1.4以降、TiKVが`storage.enable-ttl = true`に設定されている場合、TiKVのTTL機能は[RawKVモード](https://tikv.org/docs/5.1/concepts/explore-tikv-features/ttl/) のみをサポートしているため、TiDBからの要求は拒否されます。 [＃27303](https://github.com/pingcap/tidb/issues/27303)

-   ツール

    -   TiCDC

        -   デフォルト値の`max-message-bytes`を10M に設定する [＃4041](https://github.com/pingcap/tiflow/issues/4041)

## 改善点 {#improvements}

-   TiDB

    -   範囲パーティションテーブルの組み込み式`IN`のパーティションプルーニングをサポート [＃26739](https://github.com/pingcap/tidb/issues/26739)
    -   `IndexJoin`実行時のメモリ使用量の追跡精度を向上[＃28650](https://github.com/pingcap/tidb/issues/28650)

-   TiKV

    -   procファイルシステム（procfs）をv0.12.0 に更新する [＃11702](https://github.com/tikv/tikv/issues/11702)
    -   Raftクライアントのエラーログレポートを改善 [＃11959](https://github.com/tikv/tikv/issues/11959)
    -   検証プロセスを`Apply`スレッドプールから`Import`スレッドプールに移動することで、SSTファイルの挿入速度が向上します[＃11239](https://github.com/tikv/tikv/issues/11239)

-   PD

    -   スケジューラの終了プロセスを高速化 [＃4146](https://github.com/tikv/pd/issues/4146)

-   TiFlash

    -   `ADDDATE()`と`DATE_ADD()` TiFlashにプッシュダウンする機能をサポート
    -   `INET6_ATON()`と`INET6_NTOA()` TiFlashにプッシュダウンする機能をサポート
    -   `INET_ATON()`と`INET_NTOA()` TiFlashにプッシュダウンする機能をサポート
    -   DAG リクエスト内の式またはプラン ツリーの最大サポート深度を`100`から`200`に増やします。

-   ツール

    -   TiCDC

        -   チェンジフィードを再開するための指数バックオフメカニズムを追加します[＃3329](https://github.com/pingcap/tiflow/issues/3329)
        -   多数のテーブルを複製する際のレプリケーションのレイテンシーを削減する[＃3900](https://github.com/pingcap/tiflow/issues/3900)
        -   増分スキャンの残り時間を観察するためのメトリックを追加します [＃2985](https://github.com/pingcap/tiflow/issues/2985)
        -   「EventFeed 再試行レート制限」ログの数を減らす[＃4006](https://github.com/pingcap/tiflow/issues/4006)
        -   `no owner alert` `table sink total row`含む`buffer sink total row` PrometheusとGrafana 監視メトリックとアラート追加します`mounter row` [＃4054](https://github.com/pingcap/tiflow/issues/4054) [＃1606](https://github.com/pingcap/tiflow/issues/1606)
        -   TiKVリロードのレート制限制御を最適化して、チェンジフィード初期化中のgPRC輻輳を軽減します[＃3110](https://github.com/pingcap/ticdc/issues/3110)
        -   TiKVストアがダウンしたときにKVクライアントが回復するまでの時間を短縮します[＃3191](https://github.com/pingcap/tiflow/issues/3191)

## バグ修正 {#bug-fixes}

-   TiDB

    -   システム変数`tidb_analyze_version` `2` に設定されている場合に発生するメモリリークのバグを修正しました [＃32499](https://github.com/pingcap/tidb/issues/32499)
    -   `MaxDays`と`MaxBackups`設定がスローログに反映されない問題を修正 [＃25716](https://github.com/pingcap/tidb/issues/25716)
    -   `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE`文を実行するとpanicが発生する問題を修正しました [＃28078](https://github.com/pingcap/tidb/issues/28078)
    -   `ENUM`種類の列に対して`JOIN`実行するときに発生する可能性のある誤った結果を修正 [＃27831](https://github.com/pingcap/tidb/issues/27831)
    -   INDEX HASH JOINが`send on closed channel`エラーを返す問題を修正しました[＃31129](https://github.com/pingcap/tidb/issues/31129)
    -   [`BatchCommands`](/tidb-configuration-file.md#max-batch-size) APIを使用すると、まれにTiKVへのTiDBリクエストの送信がブロックされる可能性がある問題を修正しました[＃32500](https://github.com/pingcap/tidb/issues/32500)
    -   楽観的トランザクションモードで潜在的なデータインデックスの不整合が発生する問題を修正 [＃30410](https://github.com/pingcap/tidb/issues/30410)
    -   トランザクションを使用する場合と使用しない場合でウィンドウ関数が異なる結果を返す可能性がある問題を修正しました[＃29947](https://github.com/pingcap/tidb/issues/29947)
    -   `Decimal`から`String` へのキャスト時に長さ情報が間違っている問題を修正 [＃29417](https://github.com/pingcap/tidb/issues/29417)
    -   `tidb_enable_vectorized_expression`ベクトル化式を`off` に設定すると`GREATEST`関数が誤った結果を返す問題を修正しました。 [＃29434](https://github.com/pingcap/tidb/issues/29434)
    -   オプティマイザが`join`の無効なプランをキャッシュする可能性がある問題を修正[＃28087](https://github.com/pingcap/tidb/issues/28087)
    -   ベクトル化された式 の`microsecond`と`hour`関数の誤った結果を修正 [＃28643](https://github.com/pingcap/tidb/issues/28643) [＃29244](https://github.com/pingcap/tidb/issues/29244)
    -   `ALTER TABLE.. ADD INDEX`文を実行する際に TiDBpanicが発生する問題を修正[＃27687](https://github.com/pingcap/tidb/issues/27687)
    -   MPPノードの可用性検出が一部のコーナーケースで機能しないバグを修正[＃3118](https://github.com/pingcap/tics/issues/3118)
    -   `MPP task ID` を割り当てる際の`DATA RACE`問題を修正 [＃27952](https://github.com/pingcap/tidb/issues/27952)
    -   空の`dual table` を削除した後のMPPクエリの`INDEX OUT OF RANGE`エラーを修正 [＃28250](https://github.com/pingcap/tidb/issues/28250)
    -   MPPクエリの誤検知エラーログ`invalid cop task execution summaries length`の問題を修正 [＃1791](https://github.com/pingcap/tics/issues/1791)
    -   SET GLOBAL tidb_skip_isolation_level_check=1 が新しいセッション設定に影響しない問題を修正しました [＃27897](https://github.com/pingcap/tidb/issues/27897)
    -   `tiup bench`長時間実行した場合に発生する`index out of range`問題を修正[＃26832](https://github.com/pingcap/tidb/issues/26832)

-   TiKV

    -   GCワーカーがビジー状態のときにTiKVがデータ範囲を削除できない（ `unsafe_destroy_range`実行できない）というバグを修正[＃11903](https://github.com/tikv/tikv/issues/11903)
    -   ピアを破棄するとレイテンシーが大きくなる可能性がある問題を修正[＃10210](https://github.com/tikv/tikv/issues/10210)
    -   領域が空の場合に関数`any_value`が誤った結果を返すバグを修正しました[＃11735](https://github.com/tikv/tikv/issues/11735)
    -   初期化されていないレプリカを削除すると古いレプリカが再作成される可能性がある問題を修正[＃10533](https://github.com/tikv/tikv/issues/10533)
    -   新しい選出が終了した後に`Prepare Merge`トリガーされたが、分離されたピアに通知されない場合のメタデータ破損の問題を修正しました[＃11526](https://github.com/tikv/tikv/issues/11526)
    -   コルーチンの実行速度が速すぎる場合に時々発生するデッドロックの問題を修正しました[＃11549](https://github.com/tikv/tikv/issues/11549)
    -   フレームグラフのプロファイリング時に発生する可能性のあるデッドロックとメモリリークの問題を修正[＃11108](https://github.com/tikv/tikv/issues/11108)
    -   悲観的トランザクションで事前書き込み要求を再試行するときにまれに発生するデータの不整合の問題を修正[＃11187](https://github.com/tikv/tikv/issues/11187)
    -   設定`resource-metering.enabled`が動作しないバグを修正[＃11235](https://github.com/tikv/tikv/issues/11235)
    -   `resolved_ts` で一部のコルーチンがリークする問題を修正 [＃10965](https://github.com/tikv/tikv/issues/10965)
    -   書き込みフローが低い場合に「GC が動作できません」という誤った警告が報告される問題を修正[＃9910](https://github.com/tikv/tikv/issues/9910)
    -   tikv-ctlが正しいリージョン関連情報を返すことができないバグを修正[＃11393](https://github.com/tikv/tikv/issues/11393)
    -   TiKVノードがダウンすると解決されたタイムスタンプが遅れる問題を修正しました [＃11351](https://github.com/tikv/tikv/issues/11351)
    -   極端な状況でリージョンのマージ、ConfChange、スナップショットが同時に発生した場合に発生するpanicの問題を修正しました[＃11475](https://github.com/tikv/tikv/issues/11475)
    -   TiKVが逆テーブルスキャンを実行するときにメモリロックを検出できない問題を修正しました[＃11440](https://github.com/tikv/tikv/issues/11440)
    -   小数点以下の除算結果がゼロの場合の負の符号の問題を修正しました[＃29586](https://github.com/pingcap/tidb/issues/29586)
    -   統計スレッドの監視データによって発生するメモリリークを修正 [＃11195](https://github.com/tikv/tikv/issues/11195)
    -   下流データベースが見つからない場合に発生する TiCDCpanicの問題を修正しました[＃11123](https://github.com/tikv/tikv/issues/11123)
    -   TiCDC が輻輳エラーによりスキャンの再試行を頻繁に追加する問題を修正しました [＃11082](https://github.com/tikv/tikv/issues/11082)
    -   Raftクライアント実装でバッチメッセージが大きすぎる問題を修正 [＃9714](https://github.com/tikv/tikv/issues/9714)
    -   Grafanaダッシュボードで、ストレージ関連の珍しいメトリックをいくつか折りたたむ [＃11681](https://github.com/tikv/tikv/issues/11681)

-   PD

    -   リージョンスキャッタラーによって生成されたスケジュールによってピア数が減少する可能性があるバグを修正[＃4565](https://github.com/tikv/pd/issues/4565)
    -   リージョン統計が`flow-round-by-digit` の影響を受けない問題を修正 [＃4295](https://github.com/tikv/pd/issues/4295)
    -   リージョン同期が停止したことによるリーダー選出の遅延を修正[＃3936](https://github.com/tikv/pd/issues/3936)
    -   退去リーダースケジューラが不健全なピアを持つリージョンをスケジュールできるようにサポート[＃4093](https://github.com/tikv/pd/issues/4093)
    -   ホットスポット統計からコールドホットスポットデータを削除できない問題を修正[＃4390](https://github.com/tikv/pd/issues/4390)
    -   TiKVノードが削除された後に発生するpanic問題を修正[＃4344](https://github.com/tikv/pd/issues/4344)
    -   ターゲットストアがダウンしているため、スケジューリングオペレータがフェイルファストを実行できない問題を修正しました[＃3353](https://github.com/tikv/pd/issues/3353)

-   TiFlash

    -   `str_to_date()`関数がマイクロ秒を解析する際に先頭のゼロを誤って処理する問題を修正しました
    -   メモリ制限が有効になっているときにTiFlash がクラッシュする問題を修正しました
    -   入力時間が1970-01-01 00:00:01 UTCより前の場合、 `unix_timestamp`の動作がTiDBまたはMySQLの動作と一致しない問題を修正しました。
    -   主キーがハンドルされているときに主キー列を拡張することによって発生する可能性のあるデータの不整合を修正しました。
    -   オーバーフローバグと、 `DECIMAL`データ型でデータを比較するときに`Can't compare`エラーを報告する問題を修正しました。
    -   `3rd arguments of function substringUTF8 must be constants.`の予期しないエラーを修正
    -   `nsl`ライブラリのないプラットフォームでTiFlashが起動しない問題を修正しました
    -   データを`DECIMAL`データ型にキャストする際のオーバーフローバグを修正
    -   `castStringAsReal` TiFlashとTiDB/TiKVの動作が一致しない問題を修正
    -   TiFlash が再起動後に`EstablishMPPConnection`エラーを返す可能性がある問題を修正しました
    -   TiFlashレプリカの数を 0 に設定した後に古いデータを再利用できない問題を修正しました
    -   `CastStringAsDecimal` TiFlashとTiDB/TiKVの動作が一致しない問題を修正
    -   `where <string>`句を含むクエリが間違った結果を返す問題を修正しました
    -   MPPクエリが停止したときにTiFlashがpanicになる可能性がある問題を修正しました
    -   `Unexpected type of column: Nullable(Nothing)`の予期しないエラーを修正

-   ツール

    -   TiCDC

        -   `batch-replace-enable`無効になっている場合、MySQLシンクが重複した`replace` SQL文を生成するバグを修正[＃4501](https://github.com/pingcap/tiflow/issues/4501)
        -   `cached region`監視メトリックがマイナスになる問題を修正 [＃4300](https://github.com/pingcap/tiflow/issues/4300)
        -   `min.insync.replicas` `replication-factor`より小さい場合にレプリケーションを実行できない問題を修正しました[＃3994](https://github.com/pingcap/tiflow/issues/3994)
        -   レプリケーションタスクが削除されたときに発生する可能性のあるpanic問題を修正しました[＃3128](https://github.com/pingcap/tiflow/issues/3128)
        -   不正確なチェックポイントによって発生する潜在的なデータ損失の問題を修正しました [＃3545](https://github.com/pingcap/tiflow/issues/3545)
        -   デッドロックによりレプリケーションタスクが停止する可能性がある問題を修正しました[＃4055](https://github.com/pingcap/tiflow/issues/4055)
        -   DDL文の特別なコメントによりレプリケーションタスクが停止する問題を修正[＃3755](https://github.com/pingcap/tiflow/issues/3755)
        -   EtcdWorker がオーナーとプロセッサをハングさせる可能性があるバグを修正しました [＃3750](https://github.com/pingcap/tiflow/issues/3750)
        -   クラスタのアップグレード後に`stopped`変更フィードが自動的に再開される問題を修正[＃3473](https://github.com/pingcap/tiflow/issues/3473)
        -   デフォルト値を複製できない問題を修正[＃3793](https://github.com/pingcap/tiflow/issues/3793)
        -   TiCDC のデフォルト値のパディング例外によって発生するデータの不整合を修正[＃3918](https://github.com/pingcap/tiflow/issues/3918) [＃3929](https://github.com/pingcap/tiflow/issues/3929)
        -   PDリーダーがシャットダウンして新しいノードに転送するときにオーナーがスタックするバグを修正 [＃3615](https://github.com/pingcap/tiflow/issues/3615)
        -   etcd [＃2980](https://github.com/pingcap/tiflow/issues/2980)でタスクステータスを手動でクリーンアップするときに発生する TiCDCpanicの問題を修正しました
        -   RHELリリースのタイムゾーンの問題によりサービスを開始できない問題を修正しました [＃3584](https://github.com/pingcap/tiflow/issues/3584)
        -   MySQLシンクデッドロックによる警告が頻繁に発生する問題を修正 [＃2706](https://github.com/pingcap/tiflow/issues/2706)
        -   Canalプロトコルで設定項目`enable-old-value`が自動的に`true`に設定されないバグを修正 [＃3676](https://github.com/pingcap/tiflow/issues/3676)
        -   AvroシンクがJSON型列解析をサポートしていない問題を修正 [＃3624](https://github.com/pingcap/tiflow/issues/3624)
        -   チェンジフィードチェックポイントラグの負の値エラーを修正 [＃3010](https://github.com/pingcap/ticdc/issues/3010)
        -   コンテナ環境のOOM問題を修正 [＃1798](https://github.com/pingcap/tiflow/issues/1798)
        -   複数の TiKV がクラッシュした場合や強制再起動中に TiCDC レプリケーションが中断される問題を修正[＃3288](https://github.com/pingcap/ticdc/issues/3288)
        -   DDL 処理後のメモリリークの問題を修正 [＃3174](https://github.com/pingcap/ticdc/issues/3174)
        -   ErrGCTTLExceeded エラーが発生したときに changefeed が十分に速く失敗しない問題を修正しました[＃3111](https://github.com/pingcap/ticdc/issues/3111)
        -   上流の TiDB インスタンスが予期せず終了すると、TiCDC レプリケーション タスクが終了する可能性がある問題を修正しました[＃3061](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKVが同じリージョンに重複したリクエストを送信した場合にTiCDCプロセスがpanic可能性がある問題を修正しました [＃2386](https://github.com/pingcap/tiflow/issues/2386)
        -   デフォルト値の`max-message-bytes`を`10M` に設定することで、Kafkaが過度に大きなメッセージを送信する可能性がある問題を修正しました。 [＃3081](https://github.com/pingcap/tiflow/issues/3081)
        -   Kafka メッセージの書き込み中にエラーが発生すると TiCDC 同期タスクが一時停止する可能性がある問題を修正[＃2978](https://github.com/pingcap/tiflow/issues/2978)

    -   Backup & Restore (BR)

        -   復元操作が完了した後にリージョンが不均等に分散される可能性がある問題を修正[＃30425](https://github.com/pingcap/tidb/issues/30425) [＃31034](https://github.com/pingcap/tidb/issues/31034)

    -   TiDB Binlog

        -   CSVファイルのサイズが約256MBで`strict-format`が`true` 場合、DBaaSのCSVインポートがInvalidRangeで失敗する問題を修正しました。 [＃27763](https://github.com/pingcap/tidb/issues/27763)

    -   TiDB Lightning

        -   S3ストレージパスが存在しない場合にTiDB Lightningがエラーを報告しない問題を修正[＃28031](https://github.com/pingcap/tidb/issues/28031) [＃30709](https://github.com/pingcap/tidb/issues/30709)
