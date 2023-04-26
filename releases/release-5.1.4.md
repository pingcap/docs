---
title: TiDB 5.1.4 Release Notes
---

# TiDB 5.1.4 リリースノート {#tidb-5-1-4-release-notes}

リリース日：2022年2月22日

TiDB バージョン: 5.1.4

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   システム変数[`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510)のデフォルト値を`2`から`1` [#31748](https://github.com/pingcap/tidb/issues/31748)に変更します。
    -   v5.1.4 以降、TiKV が`storage.enable-ttl = true`で構成されている場合、TiKV の TTL 機能は[RawKV モード](https://tikv.org/docs/5.1/concepts/explore-tikv-features/ttl/) [#27303](https://github.com/pingcap/tidb/issues/27303)のみをサポートするため、TiDB からのリクエストは拒否されます。

-   ツール

    -   TiCDC

        -   デフォルト値の`max-message-bytes`を 10M に設定[#4041](https://github.com/pingcap/tiflow/issues/4041)

## 改良点 {#improvements}

-   TiDB

    -   範囲パーティション テーブル[#26739](https://github.com/pingcap/tidb/issues/26739)の組み込み`IN`式のパーティション プルーニングをサポートします。
    -   `IndexJoin`実行時のメモリ使用量のトラッキング精度を向上[#28650](https://github.com/pingcap/tidb/issues/28650)

-   TiKV

    -   proc ファイルシステム (procfs) を v0.12.0 に更新します[#11702](https://github.com/tikv/tikv/issues/11702)
    -   Raftクライアント[#11959](https://github.com/tikv/tikv/issues/11959)のエラー ログ レポートを改善する
    -   検証プロセスを`Apply`スレッド プール[#11239](https://github.com/tikv/tikv/issues/11239)から`Import`スレッド プールに移動することで、SST ファイルの挿入速度を向上させます。

-   PD

    -   スケジューラーの終了プロセスを高速化する[#4146](https://github.com/tikv/pd/issues/4146)

-   TiFlash

    -   `ADDDATE()`と`DATE_ADD()`のTiFlashへのプッシュ ダウンをサポート
    -   `INET6_ATON()`と`INET6_NTOA()`のTiFlashへのプッシュ ダウンをサポート
    -   `INET_ATON()`と`INET_NTOA()`のTiFlashへのプッシュ ダウンをサポート
    -   DAG リクエストでサポートされる式またはプラン ツリーの最大深度を`100`から`200`に増やします

-   ツール

    -   TiCDC

        -   変更フィードを再開するための指数バックオフ メカニズムを追加します。 [#3329](https://github.com/pingcap/tiflow/issues/3329)
        -   多数のテーブルをレプリケートする場合のレプリケーションレイテンシーを削減する[#3900](https://github.com/pingcap/tiflow/issues/3900)
        -   インクリメンタル スキャン[#2985](https://github.com/pingcap/tiflow/issues/2985)の残り時間を監視するためのメトリックを追加します。
        -   「EventFeed retry rate limited」ログのカウントを減らします[#4006](https://github.com/pingcap/tiflow/issues/4006)
        -   `no owner alert` 、 `mounter row` 、 `table sink total row` 、および`buffer sink total row` [#4054](https://github.com/pingcap/tiflow/issues/4054) [#1606](https://github.com/pingcap/tiflow/issues/1606)を含む、Prometheus および Grafana のモニタリング メトリックとアラートをさらに追加します。
        -   TiKV リロードのレート制限制御を最適化して、変更フィードの初期化中の gPRC の輻輳を軽減します[#3110](https://github.com/pingcap/ticdc/issues/3110)
        -   TiKV ストアがダウンしたときに KV クライアントが回復するまでの時間を短縮する[#3191](https://github.com/pingcap/tiflow/issues/3191)

## バグの修正 {#bug-fixes}

-   TiDB

    -   システム変数`tidb_analyze_version`が`2` [#32499](https://github.com/pingcap/tidb/issues/32499)に設定されている場合に発生するメモリリークのバグを修正します。
    -   スローログ[#25716](https://github.com/pingcap/tidb/issues/25716)で`MaxDays`と`MaxBackups`の構成が有効にならない問題を修正
    -   `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE`ステートメントを実行するとpanic[#28078](https://github.com/pingcap/tidb/issues/28078)が発生する問題を修正します。
    -   `JOIN` on `ENUM`型の列[#27831](https://github.com/pingcap/tidb/issues/27831)を実行したときに発生する可能性のある間違った結果を修正します。
    -   INDEX HASH JOIN が`send on closed channel`エラー[#31129](https://github.com/pingcap/tidb/issues/31129)を返す問題を修正
    -   [`BatchCommands`](/tidb-configuration-file.md#max-batch-size) API を使用すると、まれに TiKV への TiDB リクエストの送信がブロックされる可能性があるという問題を修正します[#32500](https://github.com/pingcap/tidb/issues/32500)
    -   楽観的トランザクション モード[#30410](https://github.com/pingcap/tidb/issues/30410)での潜在的なデータ インデックスの不整合の問題を修正します。
    -   トランザクションを使用する場合と使用しない場合で、ウィンドウ関数が異なる結果を返すことがある問題を修正します[#29947](https://github.com/pingcap/tidb/issues/29947)
    -   `Decimal`から`String` [#29417](https://github.com/pingcap/tidb/issues/29417)をキャストするとき、長さの情報が間違っている問題を修正
    -   `tidb_enable_vectorized_expression`ベクトル化された式を`off` [#29434](https://github.com/pingcap/tidb/issues/29434)に設定すると、 `GREATEST`関数が誤った結果を返す問題を修正します。
    -   場合によってはオプティマイザーが`join`の無効なプランをキャッシュする可能性がある問題を修正します[#28087](https://github.com/pingcap/tidb/issues/28087)
    -   ベクトル化された式の`microsecond`および`hour`関数の誤った結果を修正する[#29244](https://github.com/pingcap/tidb/issues/29244) [#28643](https://github.com/pingcap/tidb/issues/28643)
    -   場合によっては`ALTER TABLE.. ADD INDEX`ステートメントを実行すると TiDBpanicが発生する問題を修正[#27687](https://github.com/pingcap/tidb/issues/27687)
    -   一部のまれなケースで MPP ノードの可用性検出が機能しないバグを修正します[#3118](https://github.com/pingcap/tics/issues/3118)
    -   `MPP task ID` [#27952](https://github.com/pingcap/tidb/issues/27952)を割り当てる際の`DATA RACE`問題を修正
    -   空`dual table` [#28250](https://github.com/pingcap/tidb/issues/28250)を削除した後の MPP クエリの`INDEX OUT OF RANGE`エラーを修正
    -   MPP クエリ[#1791](https://github.com/pingcap/tics/issues/1791)の誤検知エラー ログ`invalid cop task execution summaries length`の問題を修正します。
    -   SET GLOBAL tidb_skip_isolation_level_check=1 が新しいセッション設定に影響しない問題を修正[#27897](https://github.com/pingcap/tidb/issues/27897)
    -   `index out of range` `tiup bench`長時間実行すると発生する問題を修正[#26832](https://github.com/pingcap/tidb/issues/26832)

-   TiKV

    -   TiKV が GC ワーカがビジー状態の場合、データの範囲を削除できない ( `unsafe_destroy_range`を実行できない) バグを修正[#11903](https://github.com/tikv/tikv/issues/11903)
    -   ピアを破棄すると高レイテンシーが発生する可能性がある問題を修正します[#10210](https://github.com/tikv/tikv/issues/10210)
    -   領域が空の場合に`any_value`関数が間違った結果を返すバグを修正[#11735](https://github.com/tikv/tikv/issues/11735)
    -   初期化されていないレプリカを削除すると、古いレプリカが再作成される可能性があるという問題を修正します[#10533](https://github.com/tikv/tikv/issues/10533)
    -   新しい選択が終了した後に`Prepare Merge`がトリガーされたが、隔離されたピアに通知されていない場合のメタデータの破損の問題を修正します[#11526](https://github.com/tikv/tikv/issues/11526)
    -   コルーチンの実行速度が速すぎる場合に時々発生するデッドロックの問題を修正します[#11549](https://github.com/tikv/tikv/issues/11549)
    -   フレーム グラフをプロファイリングする際の潜在的なデッドロックとメモリリークの問題を修正します[#11108](https://github.com/tikv/tikv/issues/11108)
    -   悲観的トランザクションで事前書き込み要求を再試行するときにまれに発生するデータの不整合の問題を修正します[#11187](https://github.com/tikv/tikv/issues/11187)
    -   設定`resource-metering.enabled`が動かない不具合を修正[#11235](https://github.com/tikv/tikv/issues/11235)
    -   `resolved_ts` [#10965](https://github.com/tikv/tikv/issues/10965)で一部のコルーチンがリークする問題を修正
    -   低い書き込みフロー[#9910](https://github.com/tikv/tikv/issues/9910)で誤った「GC can not work」アラートが報告される問題を修正
    -   tikv-ctl が正しいリージョン関連の情報を返せないバグを修正[#11393](https://github.com/tikv/tikv/issues/11393)
    -   TiKV ノードがダウンしていると、解決されたタイムスタンプが[#11351](https://github.com/tikv/tikv/issues/11351)遅れる問題を修正します。
    -   極端な状況でリージョンのマージ、ConfChange、およびスナップショットが同時に発生したときに発生するpanicの問題を修正します[#11475](https://github.com/tikv/tikv/issues/11475)
    -   TiKV がリバース テーブル スキャンを実行すると、TiKV がメモリロックを検出できない問題を修正します[#11440](https://github.com/tikv/tikv/issues/11440)
    -   10 進数の除算結果がゼロ[#29586](https://github.com/pingcap/tidb/issues/29586)の場合の負号の問題を修正
    -   統計スレッド[#11195](https://github.com/tikv/tikv/issues/11195)の監視データによって引き起こされるメモリリークを修正します。
    -   ダウンストリーム データベースが見つからない場合に発生する TiCDCpanicの問題を修正します[#11123](https://github.com/tikv/tikv/issues/11123)
    -   Congest エラー[#11082](https://github.com/tikv/tikv/issues/11082)により、TiCDC がスキャンの再試行を頻繁に追加する問題を修正します。
    -   Raftクライアント実装[#9714](https://github.com/tikv/tikv/issues/9714)でバッチ メッセージが大きすぎる問題を修正
    -   Grafana ダッシュボード[#11681](https://github.com/tikv/tikv/issues/11681)でいくつかの一般的でないストレージ関連の指標を折りたたむ

-   PD

    -   リージョンスキャッタによって生成されたスケジュールがピアの数を減らす可能性があるバグを修正します[#4565](https://github.com/tikv/pd/issues/4565)
    -   リージョン統計が`flow-round-by-digit` [#4295](https://github.com/tikv/pd/issues/4295)の影響を受けない問題を修正
    -   リージョン シンサー[#3936](https://github.com/tikv/pd/issues/3936)のスタックによるリーダー選出の遅さを修正
    -   エビクト リーダー スケジューラが異常なピアを含むリージョンをスケジュールできるようにするサポート[#4093](https://github.com/tikv/pd/issues/4093)
    -   コールド ホットスポット データがホットスポット統計から削除できない問題を修正します[#4390](https://github.com/tikv/pd/issues/4390)
    -   TiKV ノードが削除された後に発生するpanicの問題を修正します[#4344](https://github.com/tikv/pd/issues/4344)
    -   ターゲットストアがダウンしているため、スケジューリングオペレーターが高速に失敗できない問題を修正します[#3353](https://github.com/tikv/pd/issues/3353)

-   TiFlash

    -   マイクロ秒を解析するときに`str_to_date()`関数が先頭のゼロを正しく処理しないという問題を修正します
    -   メモリ制限が有効な場合のTiFlashクラッシュの問題を修正
    -   入力時刻が 1970-01-01 00:00:01 UTC より前の場合、 `unix_timestamp`の動作が TiDB や MySQL の動作と一致しない問題を修正
    -   主キーがハンドルの場合に主キー列を拡張することによって発生する潜在的なデータの不整合を修正します
    -   オーバーフローのバグと、 `DECIMAL`のデータ型のデータを比較するときに`Can't compare`エラーが報告される問題を修正します。
    -   `3rd arguments of function substringUTF8 must be constants.`の予期しないエラーを修正します
    -   ライブラリが`nsl`つないプラットフォームでTiFlash が起動しない問題を修正
    -   データを`DECIMAL`データ型にキャストする際のオーバーフロー バグを修正
    -   `castStringAsReal`動作がTiFlashと TiDB/TiKV で一致しない問題を修正
    -   再起動後にTiFlash が`EstablishMPPConnection`エラーを返すことがある問題を修正
    -   TiFlashレプリカの数を 0 に設定した後、古いデータを再利用できないという問題を修正します。
    -   `CastStringAsDecimal`動作がTiFlashと TiDB/TiKV で一致しない問題を修正
    -   `where <string>`句を含むクエリが間違った結果を返す問題を修正
    -   MPP クエリが停止したときにTiFlash がpanicになる問題を修正
    -   `Unexpected type of column: Nullable(Nothing)`の予期しないエラーを修正します

-   ツール

    -   TiCDC

        -   `batch-replace-enable`が無効になっている場合、MySQL シンクが重複した`replace` SQL ステートメントを生成するバグを修正します[#4501](https://github.com/pingcap/tiflow/issues/4501)
        -   `cached region`モニタリング指標がマイナス[#4300](https://github.com/pingcap/tiflow/issues/4300)になる問題を修正
        -   `min.insync.replicas`が`replication-factor` [#3994](https://github.com/pingcap/tiflow/issues/3994)より小さい場合にレプリケーションが実行できない問題を修正
        -   レプリケーション タスクが削除されたときに発生する潜在的なpanicの問題を修正します[#3128](https://github.com/pingcap/tiflow/issues/3128)
        -   不正確なチェックポイント[#3545](https://github.com/pingcap/tiflow/issues/3545)によって引き起こされる潜在的なデータ損失の問題を修正します。
        -   デッドロックが原因でレプリケーション タスクがスタックする潜在的な問題を修正します[#4055](https://github.com/pingcap/tiflow/issues/4055)
        -   DDL ステートメントの特殊なコメントによってレプリケーション タスクが停止する問題を修正します[#3755](https://github.com/pingcap/tiflow/issues/3755)
        -   EtcdWorker が所有者とプロセッサをハングさせる可能性があるバグを修正します[#3750](https://github.com/pingcap/tiflow/issues/3750)
        -   `stopped`クラスターのアップグレード後に変更フィードが自動的に再開される問題を修正します[#3473](https://github.com/pingcap/tiflow/issues/3473)
        -   デフォルト値をレプリケートできない問題を修正[#3793](https://github.com/pingcap/tiflow/issues/3793)
        -   TiCDC のデフォルト値のパディング例外によって引き起こされるデータの不一致を修正します[#3918](https://github.com/pingcap/tiflow/issues/3918) [#3929](https://github.com/pingcap/tiflow/issues/3929)
        -   PD リーダーがシャットダウンして新しいノードに転送すると、所有者がスタックするバグを修正します[#3615](https://github.com/pingcap/tiflow/issues/3615)
        -   etcd [#2980](https://github.com/pingcap/tiflow/issues/2980)でタスク ステータスを手動でクリーニングするときに発生する TiCDCpanicの問題を修正します。
        -   RHEL リリース[#3584](https://github.com/pingcap/tiflow/issues/3584)でタイムゾーンの問題が原因でサービスを開始できない問題を修正
        -   MySQL シンクのデッドロック[#2706](https://github.com/pingcap/tiflow/issues/2706)が原因で頻繁に警告が表示される問題を修正
        -   Canal および Maxwell プロトコル[#3676](https://github.com/pingcap/tiflow/issues/3676)で`enable-old-value`構成項目が自動的に`true`に設定されないバグを修正
        -   Avro シンクが JSON 型の列の解析をサポートしていない問題を修正します[#3624](https://github.com/pingcap/tiflow/issues/3624)
        -   changefeed チェックポイントラグ[#3010](https://github.com/pingcap/ticdc/issues/3010)の負の値のエラーを修正します。
        -   コンテナー環境での OOM の問題を修正する[#1798](https://github.com/pingcap/tiflow/issues/1798)
        -   複数の TiKV がクラッシュしたとき、または強制再起動中に TiCDC レプリケーションが中断する問題を修正します[#3288](https://github.com/pingcap/ticdc/issues/3288)
        -   DDL [#3174](https://github.com/pingcap/ticdc/issues/3174)の処理後のメモリリークの問題を修正します。
        -   ErrGCTTLExceeded エラーが発生したときに changefeed が十分な速さで失敗しないという問題を修正します[#3111](https://github.com/pingcap/ticdc/issues/3111)
        -   アップストリームの TiDB インスタンスが予期せず終了すると、TiCDC レプリケーション タスクが終了する可能性がある問題を修正します[#3061](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKV が同じリージョン[#2386](https://github.com/pingcap/tiflow/issues/2386)に重複したリクエストを送信すると、TiCDC プロセスがパニックになる可能panicがある問題を修正します。
        -   デフォルト値を`max-message-bytes`から`10M` [#3081](https://github.com/pingcap/tiflow/issues/3081)に設定することにより、Kafka が過度に大きなメッセージを送信する可能性がある問題を修正します。
        -   Kafka メッセージの書き込み中にエラーが発生すると、TiCDC 同期タスクが一時停止することがある問題を修正します[#2978](https://github.com/pingcap/tiflow/issues/2978)

    -   バックアップと復元 (BR)

        -   復元操作の完了後にリージョンが不均一に分散される可能性があるという潜在的な問題を修正します[#30425](https://github.com/pingcap/tidb/issues/30425) [#31034](https://github.com/pingcap/tidb/issues/31034)

    -   TiDBBinlog

        -   CSV ファイルのサイズが約 256MB で`strict-format`が`true` [#27763](https://github.com/pingcap/tidb/issues/27763)の場合、DBaaS の CSV インポートが InvalidRange で失敗する問題を修正します。

    -   TiDB Lightning

        -   S3storageパスが存在しない場合にTiDB Lightning がエラーを報告しない問題を修正[#28031](https://github.com/pingcap/tidb/issues/28031) [#30709](https://github.com/pingcap/tidb/issues/30709)
