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
    -   v5.1.4以降、TiKVが`storage.enable-ttl = true`に設定されている場合、TiKVのTTL機能は[RawKVモード](https://tikv.org/docs/5.1/concepts/explore-tikv-features/ttl/) [＃27303](https://github.com/pingcap/tidb/issues/27303)のみをサポートしているため、TiDBからの要求は拒否されます。

-   ツール

    -   TiCDC

        -   デフォルト値の`max-message-bytes`を10M [＃4041](https://github.com/pingcap/tiflow/issues/4041)に設定する

## 改善点 {#improvements}

-   TiDB

    -   範囲パーティションテーブル[＃26739](https://github.com/pingcap/tidb/issues/26739)の組み込み式`IN`のパーティションプルーニングをサポート
    -   `IndexJoin`実行時のメモリ使用量の追跡精度を向上[＃28650](https://github.com/pingcap/tidb/issues/28650)

-   TiKV

    -   procファイルシステム（procfs）をv0.12.0 [＃11702](https://github.com/tikv/tikv/issues/11702)に更新する
    -   Raftクライアント[＃11959](https://github.com/tikv/tikv/issues/11959)のエラーログレポートを改善
    -   検証プロセスを`Apply`スレッドプールから`Import`スレッドプールに移動することで、SSTファイルの挿入速度が向上します[＃11239](https://github.com/tikv/tikv/issues/11239)

-   PD

    -   スケジューラ[＃4146](https://github.com/tikv/pd/issues/4146)の終了プロセスを高速化

-   TiFlash

    -   `ADDDATE()`と`DATE_ADD()` TiFlashにプッシュダウンする機能をサポート
    -   `INET6_ATON()`と`INET6_NTOA()` TiFlashにプッシュダウンする機能をサポート
    -   `INET_ATON()`と`INET_NTOA()` TiFlashにプッシュダウンする機能をサポート
    -   DAG リクエスト内の式またはプラン ツリーの最大サポート深度を`100`から`200`に増やします。

-   ツール

    -   TiCDC

        -   チェンジフィードを再開するための指数バックオフメカニズムを追加します[＃3329](https://github.com/pingcap/tiflow/issues/3329)
        -   多数のテーブルを複製する際のレプリケーションのレイテンシーを削減する[＃3900](https://github.com/pingcap/tiflow/issues/3900)
        -   増分スキャン[＃2985](https://github.com/pingcap/tiflow/issues/2985)の残り時間を観察するためのメトリックを追加します
        -   「EventFeed 再試行レート制限」ログの数を減らす[＃4006](https://github.com/pingcap/tiflow/issues/4006)
        -   `no owner alert` `table sink total row`含む`buffer sink total row` PrometheusとGrafana [＃4054](https://github.com/pingcap/tiflow/issues/4054)監視メトリックとアラート[＃1606](https://github.com/pingcap/tiflow/issues/1606)追加します`mounter row`
        -   TiKVリロードのレート制限制御を最適化して、チェンジフィード初期化中のgPRC輻輳を軽減します[＃3110](https://github.com/pingcap/ticdc/issues/3110)
        -   TiKVストアがダウンしたときにKVクライアントが回復するまでの時間を短縮します[＃3191](https://github.com/pingcap/tiflow/issues/3191)

## バグ修正 {#bug-fixes}

-   TiDB

    -   システム変数`tidb_analyze_version` `2` [＃32499](https://github.com/pingcap/tidb/issues/32499)に設定されている場合に発生するメモリリークのバグを修正しました
    -   `MaxDays`と`MaxBackups`設定がスローログ[＃25716](https://github.com/pingcap/tidb/issues/25716)に反映されない問題を修正
    -   `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE`文を実行するとpanic[＃28078](https://github.com/pingcap/tidb/issues/28078)が発生する問題を修正しました
    -   `ENUM`種類の列[＃27831](https://github.com/pingcap/tidb/issues/27831)に対して`JOIN`実行するときに発生する可能性のある誤った結果を修正
    -   INDEX HASH JOINが`send on closed channel`エラーを返す問題を修正しました[＃31129](https://github.com/pingcap/tidb/issues/31129)
    -   [`BatchCommands`](/tidb-configuration-file.md#max-batch-size) APIを使用すると、まれにTiKVへのTiDBリクエストの送信がブロックされる可能性がある問題を修正しました[＃32500](https://github.com/pingcap/tidb/issues/32500)
    -   楽観的トランザクションモード[＃30410](https://github.com/pingcap/tidb/issues/30410)で潜在的なデータインデックスの不整合が発生する問題を修正
    -   トランザクションを使用する場合と使用しない場合でウィンドウ関数が異なる結果を返す可能性がある問題を修正しました[＃29947](https://github.com/pingcap/tidb/issues/29947)
    -   `Decimal`から`String` [＃29417](https://github.com/pingcap/tidb/issues/29417)へのキャスト時に長さ情報が間違っている問題を修正
    -   `tidb_enable_vectorized_expression`ベクトル化式を`off` [＃29434](https://github.com/pingcap/tidb/issues/29434)に設定すると`GREATEST`関数が誤った結果を返す問題を修正しました。
    -   オプティマイザが`join`の無効なプランをキャッシュする可能性がある問題を修正[＃28087](https://github.com/pingcap/tidb/issues/28087)
    -   ベクトル化された式[＃29244](https://github.com/pingcap/tidb/issues/29244) [＃28643](https://github.com/pingcap/tidb/issues/28643)の`microsecond`と`hour`関数の誤った結果を修正
    -   `ALTER TABLE.. ADD INDEX`文を実行する際に TiDBpanicが発生する問題を修正[＃27687](https://github.com/pingcap/tidb/issues/27687)
    -   MPPノードの可用性検出が一部のコーナーケースで機能しないバグを修正[＃3118](https://github.com/pingcap/tics/issues/3118)
    -   `MPP task ID` [＃27952](https://github.com/pingcap/tidb/issues/27952)を割り当てる際の`DATA RACE`問題を修正
    -   空の`dual table` [＃28250](https://github.com/pingcap/tidb/issues/28250)を削除した後のMPPクエリの`INDEX OUT OF RANGE`エラーを修正
    -   MPPクエリ[＃1791](https://github.com/pingcap/tics/issues/1791)の誤検知エラーログ`invalid cop task execution summaries length`の問題を修正
    -   SET GLOBAL tidb_skip_isolation_level_check=1 が新しいセッション設定[＃27897](https://github.com/pingcap/tidb/issues/27897)に影響しない問題を修正しました
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
    -   `resolved_ts` [＃10965](https://github.com/tikv/tikv/issues/10965)で一部のコルーチンがリークする問題を修正
    -   書き込みフローが低い場合に「GC が動作できません」という誤った警告が報告される問題を修正[＃9910](https://github.com/tikv/tikv/issues/9910)
    -   tikv-ctlが正しい地域関連情報を返すことができないバグを修正[＃11393](https://github.com/tikv/tikv/issues/11393)
    -   TiKVノードがダウンすると解決されたタイムスタンプが[＃11351](https://github.com/tikv/tikv/issues/11351)遅れる問題を修正しました
    -   極端な状況でリージョンのマージ、ConfChange、スナップショットが同時に発生した場合に発生するpanicの問題を修正しました[＃11475](https://github.com/tikv/tikv/issues/11475)
    -   TiKVが逆テーブルスキャンを実行するときにメモリロックを検出できない問題を修正しました[＃11440](https://github.com/tikv/tikv/issues/11440)
    -   小数点以下の除算結果がゼロの場合の負の符号の問題を修正しました[＃29586](https://github.com/pingcap/tidb/issues/29586)
    -   統計スレッド[＃11195](https://github.com/tikv/tikv/issues/11195)の監視データによって発生するメモリリークを修正
    -   下流データベースが見つからない場合に発生する TiCDCpanicの問題を修正しました[＃11123](https://github.com/tikv/tikv/issues/11123)
    -   TiCDC が輻輳エラー[＃11082](https://github.com/tikv/tikv/issues/11082)によりスキャンの再試行を頻繁に追加する問題を修正しました
    -   Raftクライアント実装[＃9714](https://github.com/tikv/tikv/issues/9714)でバッチメッセージが大きすぎる問題を修正
    -   Grafanaダッシュボード[＃11681](https://github.com/tikv/tikv/issues/11681)で、ストレージ関連の珍しいメトリックをいくつか折りたたむ

-   PD

    -   リージョンスキャッタラーによって生成されたスケジュールによってピア数が減少する可能性があるバグを修正[＃4565](https://github.com/tikv/pd/issues/4565)
    -   リージョン統計が`flow-round-by-digit` [＃4295](https://github.com/tikv/pd/issues/4295)の影響を受けない問題を修正
    -   リージョン同期が停止したことによるリーダー選出の遅延を修正[＃3936](https://github.com/tikv/pd/issues/3936)
    -   退去リーダースケジューラが不健全なピアを持つ領域をスケジュールできるようにサポート[＃4093](https://github.com/tikv/pd/issues/4093)
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
        -   `cached region`監視メトリックがマイナス[＃4300](https://github.com/pingcap/tiflow/issues/4300)になる問題を修正
        -   `min.insync.replicas` `replication-factor`より小さい場合にレプリケーションを実行できない問題を修正しました[＃3994](https://github.com/pingcap/tiflow/issues/3994)
        -   レプリケーションタスクが削除されたときに発生する可能性のあるpanic問題を修正しました[＃3128](https://github.com/pingcap/tiflow/issues/3128)
        -   不正確なチェックポイント[＃3545](https://github.com/pingcap/tiflow/issues/3545)によって発生する潜在的なデータ損失の問題を修正しました
        -   デッドロックによりレプリケーションタスクが停止する可能性がある問題を修正しました[＃4055](https://github.com/pingcap/tiflow/issues/4055)
        -   DDL文の特別なコメントによりレプリケーションタスクが停止する問題を修正[＃3755](https://github.com/pingcap/tiflow/issues/3755)
        -   EtcdWorker がオーナーとプロセッサ[＃3750](https://github.com/pingcap/tiflow/issues/3750)をハングさせる可能性があるバグを修正しました
        -   クラスタのアップグレード後に`stopped`変更フィードが自動的に再開される問題を修正[＃3473](https://github.com/pingcap/tiflow/issues/3473)
        -   デフォルト値を複製できない問題を修正[＃3793](https://github.com/pingcap/tiflow/issues/3793)
        -   TiCDC のデフォルト値のパディング例外によって発生するデータの不整合を修正[＃3918](https://github.com/pingcap/tiflow/issues/3918) [＃3929](https://github.com/pingcap/tiflow/issues/3929)
        -   PDリーダーがシャットダウンして新しいノード[＃3615](https://github.com/pingcap/tiflow/issues/3615)に転送するときにオーナーがスタックするバグを修正
        -   etcd [＃2980](https://github.com/pingcap/tiflow/issues/2980)でタスクステータスを手動でクリーンアップするときに発生する TiCDCpanicの問題を修正しました
        -   RHELリリース[＃3584](https://github.com/pingcap/tiflow/issues/3584)のタイムゾーンの問題によりサービスを開始できない問題を修正しました
        -   MySQLシンクデッドロック[＃2706](https://github.com/pingcap/tiflow/issues/2706)による警告が頻繁に発生する問題を修正
        -   Canalプロトコル[＃3676](https://github.com/pingcap/tiflow/issues/3676)で設定項目`enable-old-value`が自動的に`true`に設定されないバグを修正
        -   AvroシンクがJSON型列[＃3624](https://github.com/pingcap/tiflow/issues/3624)解析をサポートしていない問題を修正
        -   チェンジフィードチェックポイントラグ[＃3010](https://github.com/pingcap/ticdc/issues/3010)の負の値エラーを修正
        -   コンテナ環境[＃1798](https://github.com/pingcap/tiflow/issues/1798)のOOM問題を修正
        -   複数の TiKV がクラッシュした場合や強制再起動中に TiCDC レプリケーションが中断される問題を修正[＃3288](https://github.com/pingcap/ticdc/issues/3288)
        -   DDL [＃3174](https://github.com/pingcap/ticdc/issues/3174)処理後のメモリリークの問題を修正
        -   ErrGCTTLExceeded エラーが発生したときに changefeed が十分に速く失敗しない問題を修正しました[＃3111](https://github.com/pingcap/ticdc/issues/3111)
        -   上流の TiDB インスタンスが予期せず終了すると、TiCDC レプリケーション タスクが終了する可能性がある問題を修正しました[＃3061](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKVが同じリージョン[＃2386](https://github.com/pingcap/tiflow/issues/2386)に重複したリクエストを送信した場合にTiCDCプロセスがpanic可能性がある問題を修正しました
        -   デフォルト値の`max-message-bytes`を`10M` [＃3081](https://github.com/pingcap/tiflow/issues/3081)に設定することで、Kafkaが過度に大きなメッセージを送信する可能性がある問題を修正しました。
        -   Kafka メッセージの書き込み中にエラーが発生すると TiCDC 同期タスクが一時停止する可能性がある問題を修正[＃2978](https://github.com/pingcap/tiflow/issues/2978)

    -   バックアップと復元 (BR)

        -   復元操作が完了した後にリージョンが不均等に分散される可能性がある問題を修正[＃30425](https://github.com/pingcap/tidb/issues/30425) [＃31034](https://github.com/pingcap/tidb/issues/31034)

    -   TiDBBinlog

        -   CSVファイルのサイズが約256MBで`strict-format`が`true` [＃27763](https://github.com/pingcap/tidb/issues/27763)場合、DBaaSのCSVインポートがInvalidRangeで失敗する問題を修正しました。

    -   TiDB Lightning

        -   S3storageパスが存在しない場合にTiDB Lightningがエラーを報告しない問題を修正[＃28031](https://github.com/pingcap/tidb/issues/28031) [＃30709](https://github.com/pingcap/tidb/issues/30709)
