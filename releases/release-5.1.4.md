---
title: TiDB 5.1.4 Release Notes
---

# TiDB 5.1.4 リリースノート {#tidb-5-1-4-release-notes}

リリース日：2022年2月22日

TiDB バージョン: 5.1.4

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   システム変数[<a href="/system-variables.md#tidb_analyze_version-new-in-v510">`tidb_analyze_version`</a>](/system-variables.md#tidb_analyze_version-new-in-v510)のデフォルト値を`2`から`1`に変更します[<a href="https://github.com/pingcap/tidb/issues/31748">#31748</a>](https://github.com/pingcap/tidb/issues/31748)
    -   v5.1.4 以降、TiKV が`storage.enable-ttl = true`で構成されている場合、TiKV の TTL 機能は[<a href="https://tikv.org/docs/5.1/concepts/explore-tikv-features/ttl/">RawKVモード</a>](https://tikv.org/docs/5.1/concepts/explore-tikv-features/ttl/) [<a href="https://github.com/pingcap/tidb/issues/27303">#27303</a>](https://github.com/pingcap/tidb/issues/27303)のみをサポートしているため、TiDB からのリクエストは拒否されます。

-   ツール

    -   TiCDC

        -   デフォルト値の`max-message-bytes`を 10M [<a href="https://github.com/pingcap/tiflow/issues/4041">#4041</a>](https://github.com/pingcap/tiflow/issues/4041)に設定します。

## 改善点 {#improvements}

-   TiDB

    -   範囲パーティション テーブル[<a href="https://github.com/pingcap/tidb/issues/26739">#26739</a>](https://github.com/pingcap/tidb/issues/26739)の組み込み`IN`式のパーティション プルーニングをサポートします。
    -   `IndexJoin`の実行時のメモリ使用量の追跡の精度を向上させる[<a href="https://github.com/pingcap/tidb/issues/28650">#28650</a>](https://github.com/pingcap/tidb/issues/28650)

-   TiKV

    -   proc ファイルシステム (procfs) を v0.12.0 に更新します[<a href="https://github.com/tikv/tikv/issues/11702">#11702</a>](https://github.com/tikv/tikv/issues/11702)
    -   Raftクライアント[<a href="https://github.com/tikv/tikv/issues/11959">#11959</a>](https://github.com/tikv/tikv/issues/11959)のエラーログレポートを改善しました。
    -   検証プロセスを`Apply`スレッド プール[<a href="https://github.com/tikv/tikv/issues/11239">#11239</a>](https://github.com/tikv/tikv/issues/11239)から`Import`スレッド プールに移動することで、SST ファイルの挿入速度が向上しました。

-   PD

    -   スケジューラの終了プロセスを高速化[<a href="https://github.com/tikv/pd/issues/4146">#4146</a>](https://github.com/tikv/pd/issues/4146)

-   TiFlash

    -   `ADDDATE()`と`DATE_ADD()`をTiFlashにプッシュダウンするサポート
    -   `INET6_ATON()`と`INET6_NTOA()`をTiFlashにプッシュダウンするサポート
    -   `INET_ATON()`と`INET_NTOA()`をTiFlashにプッシュダウンするサポート
    -   DAG リクエスト内の式またはプラン ツリーでサポートされる最大の深さを`100`から`200`に増やします。

-   ツール

    -   TiCDC

        -   変更フィードを再開するための指数バックオフ メカニズムを追加します。 [<a href="https://github.com/pingcap/tiflow/issues/3329">#3329</a>](https://github.com/pingcap/tiflow/issues/3329)
        -   多数のテーブルをレプリケートする場合のレプリケーションのレイテンシーを短縮します[<a href="https://github.com/pingcap/tiflow/issues/3900">#3900</a>](https://github.com/pingcap/tiflow/issues/3900)
        -   インクリメンタル スキャン[<a href="https://github.com/pingcap/tiflow/issues/2985">#2985</a>](https://github.com/pingcap/tiflow/issues/2985)の残り時間を監視するためのメトリクスを追加します。
        -   「EventFeed 再試行速度制限」ログの数を減らす[<a href="https://github.com/pingcap/tiflow/issues/4006">#4006</a>](https://github.com/pingcap/tiflow/issues/4006)
        -   `no owner alert` 、 `mounter row` 、 `table sink total row` 、 `buffer sink total row`などの Prometheus および Grafana モニタリング メトリックとアラートを追加します[<a href="https://github.com/pingcap/tiflow/issues/4054">#4054</a>](https://github.com/pingcap/tiflow/issues/4054) [<a href="https://github.com/pingcap/tiflow/issues/1606">#1606</a>](https://github.com/pingcap/tiflow/issues/1606)
        -   TiKV リロードのレート制限制御を最適化し、チェンジフィードの初期化中の gPRC の輻輳を軽減します[<a href="https://github.com/pingcap/ticdc/issues/3110">#3110</a>](https://github.com/pingcap/ticdc/issues/3110)
        -   TiKV ストアがダウンした場合に KV クライアントが回復するまでの時間を短縮します[<a href="https://github.com/pingcap/tiflow/issues/3191">#3191</a>](https://github.com/pingcap/tiflow/issues/3191)

## バグの修正 {#bug-fixes}

-   TiDB

    -   システム変数`tidb_analyze_version`が`2` [<a href="https://github.com/pingcap/tidb/issues/32499">#32499</a>](https://github.com/pingcap/tidb/issues/32499)に設定されている場合に発生するメモリリークのバグを修正
    -   `MaxDays`と`MaxBackups`設定がスロー ログ[<a href="https://github.com/pingcap/tidb/issues/25716">#25716</a>](https://github.com/pingcap/tidb/issues/25716)に反映されない問題を修正
    -   `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE`ステートメントを実行するとpanic[<a href="https://github.com/pingcap/tidb/issues/28078">#28078</a>](https://github.com/pingcap/tidb/issues/28078)が発生する問題を修正
    -   `ENUM`型列[<a href="https://github.com/pingcap/tidb/issues/27831">#27831</a>](https://github.com/pingcap/tidb/issues/27831)で`JOIN`実行したときに発生する可能性がある間違った結果を修正しました。
    -   INDEX HASH JOIN が`send on closed channel`エラー[<a href="https://github.com/pingcap/tidb/issues/31129">#31129</a>](https://github.com/pingcap/tidb/issues/31129)を返す問題を修正
    -   [<a href="/tidb-configuration-file.md#max-batch-size">`BatchCommands`</a>](/tidb-configuration-file.md#max-batch-size) API を使用すると、まれに TiKV への TiDB リクエストの送信がブロックされる可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/32500">#32500</a>](https://github.com/pingcap/tidb/issues/32500)
    -   楽観的トランザクション モード[<a href="https://github.com/pingcap/tidb/issues/30410">#30410</a>](https://github.com/pingcap/tidb/issues/30410)での潜在的なデータ インデックスの不一致の問題を修正します。
    -   トランザクションを使用する場合と使用しない場合に、ウィンドウ関数が異なる結果を返す可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/29947">#29947</a>](https://github.com/pingcap/tidb/issues/29947)
    -   `Decimal` ～ `String` [<a href="https://github.com/pingcap/tidb/issues/29417">#29417</a>](https://github.com/pingcap/tidb/issues/29417)をキャストする際に長さ情報が間違っている問題を修正
    -   `tidb_enable_vectorized_expression`ベクトル化式を`off` [<a href="https://github.com/pingcap/tidb/issues/29434">#29434</a>](https://github.com/pingcap/tidb/issues/29434)に設定すると、 `GREATEST`関数が誤った結果を返す問題を修正します。
    -   場合によってはオプティマイザが`join`の無効なプランをキャッシュする可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/28087">#28087</a>](https://github.com/pingcap/tidb/issues/28087)
    -   ベクトル化された式の`microsecond`および`hour`関数の誤った結果を修正[<a href="https://github.com/pingcap/tidb/issues/29244">#29244</a>](https://github.com/pingcap/tidb/issues/29244) [<a href="https://github.com/pingcap/tidb/issues/28643">#28643</a>](https://github.com/pingcap/tidb/issues/28643)
    -   場合によっては`ALTER TABLE.. ADD INDEX`ステートメント実行時の TiDBpanicを修正[<a href="https://github.com/pingcap/tidb/issues/27687">#27687</a>](https://github.com/pingcap/tidb/issues/27687)
    -   MPP ノードの可用性検出が一部の特殊なケースで機能しないバグを修正[<a href="https://github.com/pingcap/tics/issues/3118">#3118</a>](https://github.com/pingcap/tics/issues/3118)
    -   `MPP task ID` [<a href="https://github.com/pingcap/tidb/issues/27952">#27952</a>](https://github.com/pingcap/tidb/issues/27952)を割り当てるときの`DATA RACE`問題を修正
    -   空`dual table` [<a href="https://github.com/pingcap/tidb/issues/28250">#28250</a>](https://github.com/pingcap/tidb/issues/28250)を削除した後の MPP クエリの`INDEX OUT OF RANGE`エラーを修正
    -   MPP クエリ[<a href="https://github.com/pingcap/tics/issues/1791">#1791</a>](https://github.com/pingcap/tics/issues/1791)の誤検知エラー ログ`invalid cop task execution summaries length`の問題を修正します。
    -   SET GLOBAL tidb_skip_isolation_level_check=1 が新しいセッション設定に影響を与えないという問題を修正[<a href="https://github.com/pingcap/tidb/issues/27897">#27897</a>](https://github.com/pingcap/tidb/issues/27897)
    -   `tiup bench`を長時間実行すると発生する`index out of range`問題を修正[<a href="https://github.com/pingcap/tidb/issues/26832">#26832</a>](https://github.com/pingcap/tidb/issues/26832)

-   TiKV

    -   GC ワーカーがビジー状態の場合、TiKV がデータ範囲を削除できない ( `unsafe_destroy_range`は実行できない) バグを修正[<a href="https://github.com/tikv/tikv/issues/11903">#11903</a>](https://github.com/tikv/tikv/issues/11903)
    -   ピアを破棄するとレイテンシーが長くなる可能性がある問題を修正[<a href="https://github.com/tikv/tikv/issues/10210">#10210</a>](https://github.com/tikv/tikv/issues/10210)
    -   `any_value`領域が空の場合に関数が間違った結果を返すバグを修正[<a href="https://github.com/tikv/tikv/issues/11735">#11735</a>](https://github.com/tikv/tikv/issues/11735)
    -   初期化されていないレプリカを削除すると古いレプリカが再作成される可能性がある問題を修正します[<a href="https://github.com/tikv/tikv/issues/10533">#10533</a>](https://github.com/tikv/tikv/issues/10533)
    -   新しい選択が完了した後に`Prepare Merge`がトリガーされたが、分離されたピアに通知されなかった場合のメタデータ破損の問題を修正します[<a href="https://github.com/tikv/tikv/issues/11526">#11526</a>](https://github.com/tikv/tikv/issues/11526)
    -   コルーチンの実行が速すぎる場合に時折発生するデッドロックの問題を修正します[<a href="https://github.com/tikv/tikv/issues/11549">#11549</a>](https://github.com/tikv/tikv/issues/11549)
    -   フレーム グラフ[<a href="https://github.com/tikv/tikv/issues/11108">#11108</a>](https://github.com/tikv/tikv/issues/11108)をプロファイリングする際の潜在的なデッドロックとメモリリークの問題を修正します。
    -   悲観的トランザクションで事前書き込みリクエストを再試行するときに発生するまれなデータの不整合の問題を修正します[<a href="https://github.com/tikv/tikv/issues/11187">#11187</a>](https://github.com/tikv/tikv/issues/11187)
    -   設定`resource-metering.enabled`が動作しないバグを修正[<a href="https://github.com/tikv/tikv/issues/11235">#11235</a>](https://github.com/tikv/tikv/issues/11235)
    -   `resolved_ts` [<a href="https://github.com/tikv/tikv/issues/10965">#10965</a>](https://github.com/tikv/tikv/issues/10965)で一部のコルーチンがリークする問題を修正
    -   書き込みフローが低い場合に誤った「GC が機能しません」アラートが報告される問題を修正[<a href="https://github.com/tikv/tikv/issues/9910">#9910</a>](https://github.com/tikv/tikv/issues/9910)
    -   tikv-ctl が正しいリージョン関連情報を返せないバグを修正[<a href="https://github.com/tikv/tikv/issues/11393">#11393</a>](https://github.com/tikv/tikv/issues/11393)
    -   TiKV ノードがダウンすると解決されたタイムスタンプが[<a href="https://github.com/tikv/tikv/issues/11351">#11351</a>](https://github.com/tikv/tikv/issues/11351)遅れる問題を修正
    -   極端な条件でリージョンのマージ、ConfChange、およびスナップショットが同時に発生したときに発生するpanicの問題を修正します[<a href="https://github.com/tikv/tikv/issues/11475">#11475</a>](https://github.com/tikv/tikv/issues/11475)
    -   TiKV が逆テーブル スキャンを実行するときに TiKV がメモリロックを検出できない問題を修正します[<a href="https://github.com/tikv/tikv/issues/11440">#11440</a>](https://github.com/tikv/tikv/issues/11440)
    -   10 進数の除算結果が 0 の場合の負号の問題を修正します[<a href="https://github.com/pingcap/tidb/issues/29586">#29586</a>](https://github.com/pingcap/tidb/issues/29586)
    -   統計スレッド[<a href="https://github.com/tikv/tikv/issues/11195">#11195</a>](https://github.com/tikv/tikv/issues/11195)の監視データによって引き起こされるメモリリークを修正
    -   ダウンストリーム データベースが見つからない場合に発生する TiCDCpanicの問題を修正します[<a href="https://github.com/tikv/tikv/issues/11123">#11123</a>](https://github.com/tikv/tikv/issues/11123)
    -   TiCDC が輻輳エラー[<a href="https://github.com/tikv/tikv/issues/11082">#11082</a>](https://github.com/tikv/tikv/issues/11082)によりスキャンの再試行を頻繁に追加する問題を修正します。
    -   Raftクライアント実装[<a href="https://github.com/tikv/tikv/issues/9714">#9714</a>](https://github.com/tikv/tikv/issues/9714)でバッチメッセージが大きすぎる問題を修正
    -   Grafana ダッシュボードでいくつかの一般的ではないストレージ関連のメトリクスを折りたたむ[<a href="https://github.com/tikv/tikv/issues/11681">#11681</a>](https://github.com/tikv/tikv/issues/11681)

-   PD

    -   リージョンスキャッタラーが生成するスケジュールによりピア数が減少する場合があるバグを修正[<a href="https://github.com/tikv/pd/issues/4565">#4565</a>](https://github.com/tikv/pd/issues/4565)
    -   リージョン統計が`flow-round-by-digit` [<a href="https://github.com/tikv/pd/issues/4295">#4295</a>](https://github.com/tikv/pd/issues/4295)の影響を受けない問題を修正
    -   リージョン同期器[<a href="https://github.com/tikv/pd/issues/3936">#3936</a>](https://github.com/tikv/pd/issues/3936)のスタックによって引き起こされるリーダー選出の遅さを修正
    -   エビクト リーダー スケジューラが異常なピアのあるリージョンをスケジュールできることのサポート[<a href="https://github.com/tikv/pd/issues/4093">#4093</a>](https://github.com/tikv/pd/issues/4093)
    -   コールド ホットスポット データがホットスポット統計[<a href="https://github.com/tikv/pd/issues/4390">#4390</a>](https://github.com/tikv/pd/issues/4390)から削除できない問題を修正します。
    -   TiKV ノードが削除された後に発生するpanicの問題を修正します[<a href="https://github.com/tikv/pd/issues/4344">#4344</a>](https://github.com/tikv/pd/issues/4344)
    -   ターゲット ストアがダウンしているため、スケジューリング オペレーターがフェイル ファストできない問題を修正します[<a href="https://github.com/tikv/pd/issues/3353">#3353</a>](https://github.com/tikv/pd/issues/3353)

-   TiFlash

    -   `str_to_date()`関数がマイクロ秒の解析時に先頭のゼロを誤って処理する問題を修正
    -   メモリ制限が有効になっている場合のTiFlashクラッシュ問題を修正
    -   入力時刻が 1970-01-01 00:00:01 UTC より前の場合、 `unix_timestamp`の動作が TiDB または MySQL の動作と一致しない問題を修正
    -   主キーがハンドルである場合に主キー列の幅を広げることによって引き起こされる潜在的なデータの不整合を修正
    -   オーバーフローのバグと、 `DECIMAL`データ型のデータを比較するときに`Can't compare`エラーが報告される問題を修正しました。
    -   `3rd arguments of function substringUTF8 must be constants.`の予期しないエラーを修正
    -   `nsl`ライブラリがないプラットフォームでTiFlash が起動できない問題を修正
    -   データを`DECIMAL`データ型にキャストするときのオーバーフローのバグを修正
    -   TiFlashと TiDB/TiKV で`castStringAsReal`動作が矛盾する問題を修正
    -   TiFlashの再起動後に`EstablishMPPConnection`エラーが返される場合がある問題を修正
    -   TiFlashレプリカの数を 0 に設定した後、古いデータを再利用できない問題を修正
    -   TiFlashと TiDB/TiKV で`CastStringAsDecimal`動作が矛盾する問題を修正
    -   `where <string>`句を含むクエリが間違った結果を返す問題を修正
    -   MPP クエリが停止するとTiFlash がpanicになる問題を修正
    -   `Unexpected type of column: Nullable(Nothing)`の予期しないエラーを修正

-   ツール

    -   TiCDC

        -   `batch-replace-enable`が無効になっている場合、MySQL シンクが重複した`replace` SQL ステートメントを生成するバグを修正[<a href="https://github.com/pingcap/tiflow/issues/4501">#4501</a>](https://github.com/pingcap/tiflow/issues/4501)
        -   `cached region`監視メトリクスがマイナス[<a href="https://github.com/pingcap/tiflow/issues/4300">#4300</a>](https://github.com/pingcap/tiflow/issues/4300)になる問題を修正
        -   `min.insync.replicas`が`replication-factor` [<a href="https://github.com/pingcap/tiflow/issues/3994">#3994</a>](https://github.com/pingcap/tiflow/issues/3994)より小さい場合にレプリケーションが実行できない問題を修正
        -   レプリケーション タスクが削除されたときに発生する潜在的なpanicの問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/3128">#3128</a>](https://github.com/pingcap/tiflow/issues/3128)
        -   不正確なチェックポイント[<a href="https://github.com/pingcap/tiflow/issues/3545">#3545</a>](https://github.com/pingcap/tiflow/issues/3545)によって引き起こされる潜在的なデータ損失の問題を修正します。
        -   デッドロックによりレプリケーション タスクが停止するという潜在的な問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/4055">#4055</a>](https://github.com/pingcap/tiflow/issues/4055)
        -   DDL ステートメント内の特別なコメントによりレプリケーション タスクが停止する問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/3755">#3755</a>](https://github.com/pingcap/tiflow/issues/3755)
        -   EtcdWorker がオーナーとプロセッサ[<a href="https://github.com/pingcap/tiflow/issues/3750">#3750</a>](https://github.com/pingcap/tiflow/issues/3750)をハングさせる可能性があるバグを修正
        -   `stopped`クラスターのアップグレード後に変更フィードが自動的に再開される問題を修正[<a href="https://github.com/pingcap/tiflow/issues/3473">#3473</a>](https://github.com/pingcap/tiflow/issues/3473)
        -   デフォルト値を複製できない問題を修正[<a href="https://github.com/pingcap/tiflow/issues/3793">#3793</a>](https://github.com/pingcap/tiflow/issues/3793)
        -   TiCDC デフォルト値パディング例外によって引き起こされるデータの不整合を修正[<a href="https://github.com/pingcap/tiflow/issues/3918">#3918</a>](https://github.com/pingcap/tiflow/issues/3918) [<a href="https://github.com/pingcap/tiflow/issues/3929">#3929</a>](https://github.com/pingcap/tiflow/issues/3929)
        -   PDリーダーがシャットダウンして新しいノード[<a href="https://github.com/pingcap/tiflow/issues/3615">#3615</a>](https://github.com/pingcap/tiflow/issues/3615)に転送するとオーナーがスタックするバグを修正
        -   etcd [<a href="https://github.com/pingcap/tiflow/issues/2980">#2980</a>](https://github.com/pingcap/tiflow/issues/2980)でタスクステータスを手動でクリーンアップするときに発生する TiCDCpanicの問題を修正します。
        -   RHEL リリース[<a href="https://github.com/pingcap/tiflow/issues/3584">#3584</a>](https://github.com/pingcap/tiflow/issues/3584)のタイムゾーンの問題によりサービスを開始できない問題を修正
        -   MySQL シンクのデッドロックによって引き起こされる過度に頻繁な警告の問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/2706">#2706</a>](https://github.com/pingcap/tiflow/issues/2706)
        -   Canal および Maxwell プロトコル[<a href="https://github.com/pingcap/tiflow/issues/3676">#3676</a>](https://github.com/pingcap/tiflow/issues/3676)で`enable-old-value`設定項目が自動的に`true`に設定されないバグを修正
        -   Avro シンクが JSON 型列の解析をサポートしていない問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/3624">#3624</a>](https://github.com/pingcap/tiflow/issues/3624)
        -   チェンジフィードチェックポイントラグ[<a href="https://github.com/pingcap/ticdc/issues/3010">#3010</a>](https://github.com/pingcap/ticdc/issues/3010)の負の値エラーを修正
        -   コンテナ環境の OOM 問題を修正する[<a href="https://github.com/pingcap/tiflow/issues/1798">#1798</a>](https://github.com/pingcap/tiflow/issues/1798)
        -   複数の TiKV がクラッシュしたとき、または強制再起動中に TiCDC レプリケーションが中断される問題を修正します[<a href="https://github.com/pingcap/ticdc/issues/3288">#3288</a>](https://github.com/pingcap/ticdc/issues/3288)
        -   DDL 処理後のメモリリーク問題を修正[<a href="https://github.com/pingcap/ticdc/issues/3174">#3174</a>](https://github.com/pingcap/ticdc/issues/3174)
        -   ErrGCTTLExceeded エラーが発生したときに変更フィードが十分な速度で失敗しない問題を修正します[<a href="https://github.com/pingcap/ticdc/issues/3111">#3111</a>](https://github.com/pingcap/ticdc/issues/3111)
        -   上流の TiDB インスタンスが予期せず終了すると、TiCDC レプリケーション タスクが終了する可能性がある問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/3061">#3061</a>](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKV が同じリージョン[<a href="https://github.com/pingcap/tiflow/issues/2386">#2386</a>](https://github.com/pingcap/tiflow/issues/2386)に重複したリクエストを送信すると、TiCDC プロセスがパニックになる可能panicがある問題を修正
        -   デフォルト値の`max-message-bytes` ～ `10M` [<a href="https://github.com/pingcap/tiflow/issues/3081">#3081</a>](https://github.com/pingcap/tiflow/issues/3081)設定することで、Kafka が過度に大きなメッセージを送信する可能性がある問題を修正します。
        -   Kafka メッセージの書き込み中にエラーが発生したときに TiCDC 同期タスクが一時停止することがある問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/2978">#2978</a>](https://github.com/pingcap/tiflow/issues/2978)

    -   バックアップと復元 (BR)

        -   復元操作の完了後にリージョンが不均一に分散される可能性がある潜在的な問題を修正します[<a href="https://github.com/pingcap/tidb/issues/30425">#30425</a>](https://github.com/pingcap/tidb/issues/30425) [<a href="https://github.com/pingcap/tidb/issues/31034">#31034</a>](https://github.com/pingcap/tidb/issues/31034)

    -   TiDBBinlog

        -   CSV ファイルのサイズが約 256MB で`strict-format`が`true` [<a href="https://github.com/pingcap/tidb/issues/27763">#27763</a>](https://github.com/pingcap/tidb/issues/27763)の場合、DBaaS による CSV インポートが InvalidRange で失敗する問題を修正

    -   TiDB Lightning

        -   S3storageパスが存在しない場合にTiDB Lightning がエラーを報告しない問題を修正[<a href="https://github.com/pingcap/tidb/issues/28031">#28031</a>](https://github.com/pingcap/tidb/issues/28031) [<a href="https://github.com/pingcap/tidb/issues/30709">#30709</a>](https://github.com/pingcap/tidb/issues/30709)
