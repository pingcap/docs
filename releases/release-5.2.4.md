---
title: TiDB 5.2.4 Release Notes
category: Releases
---

# TiDB5.2.4リリースノート {#tidb-5-2-4-release-notes}

発売日：2022年4月26日

TiDBバージョン：5.2.4

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   システム変数[`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510)のデフォルト値を`2`から[＃31748](https://github.com/pingcap/tidb/issues/31748)に変更し`1` 。

-   TiKV

    -   [`raft-log-compact-sync-interval`](https://docs.pingcap.com/tidb/v5.2/tikv-configuration-file#raft-log-compact-sync-interval-new-in-v524)を追加して時間間隔（デフォルトでは`"2s"` ）を制御し、不要なRaftログを圧縮します[＃11404](https://github.com/tikv/tikv/issues/11404)
    -   デフォルト値の[`raft-log-gc-tick-interval`](/tikv-configuration-file.md#raft-log-gc-tick-interval)を`"10s"`から[＃11404](https://github.com/tikv/tikv/issues/11404)に変更し`"3s"` 。
    -   [`storage.flow-control.enable`](/tikv-configuration-file.md#enable)が`true`に設定されている場合、 [`storage.flow-control.hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit)の値は[＃11424](https://github.com/tikv/tikv/issues/11424)の値を上書きし[`rocksdb.(defaultcf|writecf|lockcf).hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit-1) 。

-   ツール

    -   TiDB Lightning

        -   データのインポート後に空のリージョンが多すぎないように、デフォルト値の`regionMaxKeyCount`を1_440_000から1_280_000に変更します[＃30018](https://github.com/pingcap/tidb/issues/30018)

## 改善 {#improvements}

-   TiKV

    -   リーダーシップをCDCオブザーバーに移し、レイテンシーのジッターを減らします[＃12111](https://github.com/tikv/tikv/issues/12111)
    -   ロックの解決ステップ[＃11993](https://github.com/tikv/tikv/issues/11993)を必要とするリージョンの数を減らすことにより、TiCDCの回復時間を短縮します。
    -   procファイルシステム（procfs）をv0.12.0に更新します[＃11702](https://github.com/tikv/tikv/issues/11702)
    -   GC to Raftログを実行するときに書き込みバッチサイズを増やすことにより、ガベージコレクション（GC）プロセスを高速化します[＃11404](https://github.com/tikv/tikv/issues/11404)
    -   検証プロセスを`Apply`スレッドプールから`Import`スレッドプールに移動して、SSTファイルの挿入速度を上げます[＃11239](https://github.com/tikv/tikv/issues/11239)

-   ツール

    -   TiCDC

        -   Kafka Sink `partition-num`のデフォルト値を3に変更して、TiCDCがKafkaパーティション間でメッセージをより均等に分散するようにします[＃3337](https://github.com/pingcap/tiflow/issues/3337)
        -   TiKVストアがダウンしたときにKVクライアントが回復する時間を短縮する[＃3191](https://github.com/pingcap/tiflow/issues/3191)
        -   Grafana3に`Lag analyze`のパネルを追加し[＃4891](https://github.com/pingcap/tiflow/issues/4891)
        -   Kafkaプロデューサーの構成パラメーターを公開して、 [＃4385](https://github.com/pingcap/tiflow/issues/4385)で構成可能にします。
        -   チェンジフィードを再開するための指数バックオフメカニズムを追加する[＃3329](https://github.com/pingcap/tiflow/issues/3329)
        -   「EventFeed再試行率制限」ログの数を減らす[＃4006](https://github.com/pingcap/tiflow/issues/4006)
        -   デフォルト値の`max-message-bytes`を設定します[＃4041](https://github.com/pingcap/tiflow/issues/4041)
        -   `no owner alert` `buffer sink total row` [＃4054](https://github.com/pingcap/tiflow/issues/4054)など、 [＃1606](https://github.com/pingcap/tiflow/issues/1606)と`mounter row`の監視メトリックとアラートをさらに追加し`table sink total row`
        -   Grafanaダッシュボードで複数のKubernetesクラスターをサポートする[＃4665](https://github.com/pingcap/tiflow/issues/4665)
        -   キャッチアップETA（到着予定時刻）を`changefeed checkpoint`の監視メトリックに追加します[＃5232](https://github.com/pingcap/tiflow/issues/5232)

## バグの修正 {#bug-fixes}

-   TiDB

    -   列挙値[＃32428](https://github.com/pingcap/tidb/issues/32428)のNulleq関数の誤った範囲計算結果を修正しました
    -   INDEXHASHJOINが`send on closed channel`エラー[＃31129](https://github.com/pingcap/tidb/issues/31129)を返す問題を修正します
    -   列タイプを同時に変更すると、スキーマとデータの間に不整合が生じる問題を修正します[＃31048](https://github.com/pingcap/tidb/issues/31048)
    -   楽観的なトランザクションモード[＃30410](https://github.com/pingcap/tidb/issues/30410)での潜在的なデータインデックスの不整合の問題を修正します
    -   JSON型の列が`CHAR`型の列に結合するとSQL操作がキャンセルされる問題を修正します[＃29401](https://github.com/pingcap/tidb/issues/29401)
    -   トランザクションを使用するかどうかにかかわらず、ウィンドウ関数が異なる結果を返す可能性がある問題を修正します[＃29947](https://github.com/pingcap/tidb/issues/29947)
    -   SQLステートメントに自然結合[＃25041](https://github.com/pingcap/tidb/issues/25041)が含まれている場合に`Column 'col_name' in field list is ambiguous`エラーが予期せず報告される問題を修正します
    -   `Decimal`から[＃29417](https://github.com/pingcap/tidb/issues/29417)をキャストするときに長さ情報が間違っている問題を修正し`String`
    -   `tidb_enable_vectorized_expression`の値が異なるために`GREATEST`関数が一貫性のない結果を返す問題を修正します（ `on`または`off`に設定） [＃29434](https://github.com/pingcap/tidb/issues/29434)
    -   `left join`を使用して複数のテーブルのデータを削除した誤った結果を[＃31321](https://github.com/pingcap/tidb/issues/31321)
    -   TiDBが重複タスクをTiFlash1にディスパッチする可能性があるバグを修正し[＃32814](https://github.com/pingcap/tidb/issues/32814)
    -   クエリ実行時のMPPタスクリストの空のエラーを修正[＃31636](https://github.com/pingcap/tidb/issues/31636)
    -   innerWorkerパニックによって引き起こされるインデックス結合の誤った結果を修正します[＃31494](https://github.com/pingcap/tidb/issues/31494)
    -   `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE`ステートメントを実行するとパニックになる問題を修正します[＃28078](https://github.com/pingcap/tidb/issues/28078)
    -   `Order By`の最適化による誤ったクエリ結果を[＃30271](https://github.com/pingcap/tidb/issues/30271)
    -   `ENUM`のタイプの列で`JOIN`を実行するときに発生する可能性のある間違った結果を修正します[＃27831](https://github.com/pingcap/tidb/issues/27831)
    -   `ENUM`データ型[＃29357](https://github.com/pingcap/tidb/issues/29357)で`CASE WHEN`関数を使用するときのパニックを修正します
    -   ベクトル化された式[＃29244](https://github.com/pingcap/tidb/issues/29244)の`microsecond`関数の誤った結果を修正します
    -   ウィンドウ関数がエラーを報告する代わりにTiDBをパニックにする問題を修正します[＃30326](https://github.com/pingcap/tidb/issues/30326)
    -   マージ結合演算子が特定の場合に間違った結果を得る問題を修正します[＃33042](https://github.com/pingcap/tidb/issues/33042)
    -   相関サブクエリが定数[＃32089](https://github.com/pingcap/tidb/issues/32089)を返すときにTiDBが間違った結果を取得する問題を修正します
    -   `ENUM`列または`SET`列のエンコードが間違っているためにTiDBが間違ったデータを書き込む問題を修正します[＃32302](https://github.com/pingcap/tidb/issues/32302)
    -   TiDB [＃31638](https://github.com/pingcap/tidb/issues/31638)で新しい照合順序が有効になっている場合、 `ENUM`列または`SET`列の`MAX`または`MIN`関数が間違った結果を返す問題を修正します。
    -   IndexHashJoinオペレーターが正常に終了しない問題を修正します[＃31062](https://github.com/pingcap/tidb/issues/31062)
    -   テーブルに仮想列[＃30965](https://github.com/pingcap/tidb/issues/30965)がある場合にTiDBが誤ったデータを読み取る可能性がある問題を修正します
    -   ログレベルの設定が遅いクエリログ[＃30309](https://github.com/pingcap/tidb/issues/30309)で有効にならない問題を修正します
    -   パーティション化されたテーブルがインデックスを完全に使用してデータをスキャンできない場合がある問題を修正します[＃33966](https://github.com/pingcap/tidb/issues/33966)
    -   TiDBのバックグラウンドHTTPサービスが正常に終了せず、クラスタが異常な状態になる可能性がある問題を修正します[＃30571](https://github.com/pingcap/tidb/issues/30571)
    -   TiDBが失敗した認証の多くのログを予期せず出力する可能性がある問題を修正します[＃29709](https://github.com/pingcap/tidb/issues/29709)
    -   システム変数`max_allowed_packet`が有効にならない問題を修正します[＃31422](https://github.com/pingcap/tidb/issues/31422)
    -   自動IDが範囲[＃29483](https://github.com/pingcap/tidb/issues/29483)から外れると、 `REPLACE`ステートメントが他の行を誤って変更する問題を修正します。
    -   遅いクエリログがログを正常に出力できず、メモリを過剰に消費する可能性があるという問題を修正します[＃32656](https://github.com/pingcap/tidb/issues/32656)
    -   NATURALJOINの結果に予期しない列が含まれる可能性がある問題を修正します[＃24981](https://github.com/pingcap/tidb/issues/29481)
    -   1つのステートメントで`ORDER BY`と`LIMIT`を一緒に使用すると、データのクエリにプレフィックス列インデックスが使用されている場合に誤った結果が出力される可能性がある問題を修正します[＃29711](https://github.com/pingcap/tidb/issues/29711)
    -   楽観的なトランザクションが再試行すると、DOUBLEタイプの自動インクリメント列が変更される可能性がある問題を修正します[＃29892](https://github.com/pingcap/tidb/issues/29892)
    -   STR_TO_DATE関数がマイクロ秒部分の先行ゼロを正しく処理できない問題を修正します[＃30078](https://github.com/pingcap/tidb/issues/30078)
    -   TiFlashはまだ空の範囲のテーブルの読み取りをサポートしていませんが、TiFlashを使用して空の範囲のテーブルをスキャンするとTiDBが間違った結果を取得する問題を修正します[＃33083](https://github.com/pingcap/tidb/issues/33083)

-   TiKV

    -   古いメッセージが原因でTiKVがパニックになるバグを修正します[＃12023](https://github.com/tikv/tikv/issues/12023)
    -   メモリメトリックのオーバーフローによって引き起こされる断続的なパケット損失とメモリ不足（OOM）の問題を修正します[＃12160](https://github.com/tikv/tikv/issues/12160)
    -   TiKVが[＃9765](https://github.com/tikv/tikv/issues/9765)でプロファイリングを実行するときに発生する可能性のあるパニックの問題を修正します。
    -   文字列の一致が正しくないためにtikv-ctlが誤った結果を返す問題を修正します[＃12329](https://github.com/tikv/tikv/issues/12329)
    -   レプリカの読み取りが線形化可能性に違反する可能性があるバグを修正します[＃12109](https://github.com/tikv/tikv/issues/12109)
    -   TiKVが2年以上実行されている場合にパニックになる可能性があるバグを修正します[＃11940](https://github.com/tikv/tikv/issues/11940)
    -   フロー制御が有効で、 `level0_slowdown_trigger`が明示的に設定されている場合のQPSドロップの問題を修正します[＃11424](https://github.com/tikv/tikv/issues/11424)
    -   cgroupコントローラーがマウントされていないときに発生するパニックの問題を修正します[＃11569](https://github.com/tikv/tikv/issues/11569)
    -   遅れているリージョンピア[＃11526](https://github.com/tikv/tikv/issues/11526)でのリージョンマージによって引き起こされる可能性のあるメタデータの破損を修正します
    -   TiKVの動作が停止した後、解決されたTSの遅延が増加する問題を修正します[＃11351](https://github.com/tikv/tikv/issues/11351)
    -   リージョンマージ、ConfChange、およびスナップショットが極端な条件で同時に発生するときに発生するパニックの問題を修正します[＃11475](https://github.com/tikv/tikv/issues/11475)
    -   tikv-ctlが正しいリージョン関連情報を返さないバグを修正します[＃11393](https://github.com/tikv/tikv/issues/11393)
    -   10進数の除算結果がゼロの場合の負の符号の問題を修正します[＃29586](https://github.com/pingcap/tidb/issues/29586)
    -   悲観的なトランザクションモードで事前書き込み要求を再試行すると、まれにデータの不整合のリスクが発生する可能性があるという問題を修正します[＃11187](https://github.com/tikv/tikv/issues/11187)
    -   統計スレッド[＃11195](https://github.com/tikv/tikv/issues/11195)の監視データによって引き起こされるメモリリークを修正します
    -   インスタンスごとのgRPCリクエストの平均レイテンシがTiKVメトリクス[＃11299](https://github.com/tikv/tikv/issues/11299)で不正確であるという問題を修正します
    -   ピアステータスが`Applying`のときにスナップショットファイルを削除することによって引き起こされるパニックの問題を修正し[＃11746](https://github.com/tikv/tikv/issues/11746)
    -   GCワーカーがビジー状態のときにTiKVがデータの範囲を削除できない（つまり、内部コマンド`unsafe_destroy_range`が実行される）バグを修正します[＃11903](https://github.com/tikv/tikv/issues/11903)
    -   初期化されていないレプリカを削除すると、古いレプリカが再作成される可能性がある問題を修正します[＃10533](https://github.com/tikv/tikv/issues/10533)
    -   TiKVが逆テーブルスキャンを実行すると、TiKVがメモリロックを検出できない問題を修正します[＃11440](https://github.com/tikv/tikv/issues/11440)
    -   コルーチンの実行速度が速すぎる場合に時々発生するデッドロックの問題を修正します[＃11549](https://github.com/tikv/tikv/issues/11549)
    -   ピアを破棄すると待ち時間が長くなる可能性があるという問題を修正します[＃10210](https://github.com/tikv/tikv/issues/10210)
    -   マージされるターゲットリージョンが無効であるためにTiKVがパニックになり、ピアを予期せず破壊する問題を修正します[＃12232](https://github.com/tikv/tikv/issues/12232)
    -   ターゲットピアがリージョン[＃12048](https://github.com/tikv/tikv/issues/12048)のマージ時に初期化されずに破棄されたピアに置き換えられたときに発生するTiKVパニックの問題を修正します。
    -   スナップショットの適用が中止されたときに発生するTiKVパニックの問題を修正します[＃11618](https://github.com/tikv/tikv/issues/11618)
    -   オペレーターの実行が失敗したときにTiKVが送信されるスナップショットの数を正しく計算できないバグを修正します[＃11341](https://github.com/tikv/tikv/issues/11341)

-   PD

    -   リージョンスキャッタースケジューリングが一部のピアを失った問題を修正します[＃4565](https://github.com/tikv/pd/issues/4565)
    -   コールドホットスポットデータをホットスポット統計から削除できない問題を修正します[＃4390](https://github.com/tikv/pd/issues/4390)

-   TiFlash

    -   MPPタスクがスレッドを永久にリークする可能性があるバグを修正します[＃4238](https://github.com/pingcap/tiflash/issues/4238)
    -   複数値式[＃4016](https://github.com/pingcap/tiflash/issues/4016)で`IN`の結果が正しくない問題を修正します
    -   日付形式が`'\n'`を無効な区切り文字[＃4036](https://github.com/pingcap/tiflash/issues/4036)として識別する問題を修正します
    -   読み取りワークロードが重い場合に列を追加した後の潜在的なクエリエラーを修正する[＃3967](https://github.com/pingcap/tiflash/issues/3967)
    -   無効なストレージディレクトリ構成が予期しない動作につながるバグを修正します[＃4093](https://github.com/pingcap/tiflash/issues/4093)
    -   一部の例外が適切に処理されないというバグを修正します[＃4101](https://github.com/pingcap/tiflash/issues/4101)
    -   マイクロ秒[＃3557](https://github.com/pingcap/tiflash/issues/3557)を解析するときに、 `STR_TO_DATE()`関数が先行ゼロを誤って処理するバグを修正します。
    -   `INT`から`DECIMAL`をキャストするとオーバーフロー[＃3920](https://github.com/pingcap/tiflash/issues/3920)が発生する可能性がある問題を修正します
    -   `DATETIME`から[＃4151](https://github.com/pingcap/tiflash/issues/4151)をキャストするときに発生する間違った結果を修正し`DECIMAL`
    -   `FLOAT`から[＃3998](https://github.com/pingcap/tiflash/issues/3998)をキャストするときに発生するオーバーフローを修正し`DECIMAL`
    -   `CastStringAsReal`の動作がTiFlashとTiDBまたはTiKV3で一貫していない問題を修正し[＃3475](https://github.com/pingcap/tiflash/issues/3475)
    -   `CastStringAsDecimal`の動作がTiFlashとTiDBまたはTiKV3で一貫していない問題を修正し[＃3619](https://github.com/pingcap/tiflash/issues/3619)
    -   TiFlashが再起動後に`EstablishMPPConnection`エラーを返す可能性がある問題を修正します[＃3615](https://github.com/pingcap/tiflash/issues/3615)
    -   TiFlashレプリカの数を[＃3659](https://github.com/pingcap/tiflash/issues/3659)に設定した後、廃止されたデータを再利用できない問題を修正します。
    -   主キーが`handle`である場合に、主キー列を広げるときに発生する可能性のあるデータの不整合を修正し[＃3569](https://github.com/pingcap/tiflash/issues/3569) 。
    -   SQLステートメントに非常に長いネストされた式が含まれている場合に発生する可能性のある解析エラーを修正します[＃3354](https://github.com/pingcap/tiflash/issues/3354)
    -   クエリに`where <string>`句[＃3447](https://github.com/pingcap/tiflash/issues/3447)が含まれている場合に発生する可能性のある誤った結果を修正
    -   `new_collations_enabled_on_first_bootstrap`が有効になっているときに発生する可能性のある誤った結果を修正し[＃3391](https://github.com/pingcap/tiflash/issues/3391) [＃3388](https://github.com/pingcap/tiflash/issues/3388)
    -   TLSが有効になっているときに発生するパニックの問題を修正します[＃4196](https://github.com/pingcap/tiflash/issues/4196)
    -   メモリ制限が有効になっているときに発生するパニックの問題を修正します[＃3902](https://github.com/pingcap/tiflash/issues/3902)
    -   MPPクエリが停止したときにTiFlashがときどきクラッシュする問題を修正します[＃3401](https://github.com/pingcap/tiflash/issues/3401)
    -   [＃3351](https://github.com/pingcap/tiflash/issues/3351)の予期しないエラーを修正し`Unexpected type of column: Nullable(Nothing)`
    -   遅れているリージョンピア[＃4437](https://github.com/pingcap/tiflash/issues/4437)でのリージョンマージによって引き起こされる可能性のあるメタデータの破損を修正します
    -   エラーが発生した場合に`JOIN`を含むクエリがハングする可能性がある問題を修正します[＃4195](https://github.com/pingcap/tiflash/issues/4195)
    -   誤った実行プランが原因でMPPクエリに対して返される可能性のある誤った結果を修正する[＃3389](https://github.com/pingcap/tiflash/issues/3389)

-   ツール

    -   バックアップと復元（BR）

        -   BRがRawKV1のバックアップに失敗する問題を修正し[＃32607](https://github.com/pingcap/tidb/issues/32607)

    -   TiCDC

        -   デフォルト値を複製できない問題を修正します[＃3793](https://github.com/pingcap/tiflow/issues/3793)
        -   シーケンスが誤って複製される場合があるバグを修正します[＃4563](https://github.com/pingcap/tiflow/issues/4552)
        -   PDリーダーが殺されたときにTiCDCノードが異常終了するバグを修正します[＃4248](https://github.com/pingcap/tiflow/issues/4248)
        -   `batch-replace-enable`が無効になっている場合にMySQLシンクが重複した`replace`のSQLステートメントを生成するバグを修正します[＃4501](https://github.com/pingcap/tiflow/issues/4501)
        -   デフォルトの列値[＃3929](https://github.com/pingcap/tiflow/issues/3929)を出力するときに発生するパニックとデータの不整合の問題を修正します
        -   `mq sink write row`に監視データがないという問題を修正します[＃3431](https://github.com/pingcap/tiflow/issues/3431)
        -   `min.insync.replicas`が[＃3994](https://github.com/pingcap/tiflow/issues/3994)より小さい場合、レプリケーションを実行できない問題を修正し`replication-factor` 。
        -   レプリケーションタスクが削除されたときに発生する可能性のあるパニックの問題を修正する[＃3128](https://github.com/pingcap/tiflow/issues/3128)
        -   必要なプロセッサ情報が存在しない場合にHTTPAPIがパニックになるバグを修正します[＃3840](https://github.com/pingcap/tiflow/issues/3840)
        -   不正確なチェックポイント[＃3545](https://github.com/pingcap/tiflow/issues/3545)によって引き起こされる潜在的なデータ損失の問題を修正します
        -   デッドロックによってレプリケーションタスクがスタックするという潜在的な問題を修正します[＃4055](https://github.com/pingcap/tiflow/issues/4055)
        -   etcd1のタスクステータスを手動でクリーニングするときに発生するTiCDCパニックの問題を修正し[＃2980](https://github.com/pingcap/tiflow/issues/2980)
        -   DDLステートメントの特別なコメントによってレプリケーションタスクが停止する問題を修正します[＃3755](https://github.com/pingcap/tiflow/issues/3755)
        -   `config.Metadata.Timeout`の誤った構成によって引き起こされるレプリケーション停止の問題を修正し[＃3352](https://github.com/pingcap/tiflow/issues/3352) 。
        -   RHELリリース[＃3584](https://github.com/pingcap/tiflow/issues/3584)のタイムゾーンの問題が原因でサービスを開始できない問題を修正します
        -   クラスタのアップグレード後に`stopped`つのチェンジフィードが自動的に再開する問題を修正します[＃3473](https://github.com/pingcap/tiflow/issues/3473)
        -   MySQLシンクデッドロック[＃2706](https://github.com/pingcap/tiflow/issues/2706)によって引き起こされる過度に頻繁な警告の問題を修正します
        -   CanalおよびMaxwellプロトコル[＃3676](https://github.com/pingcap/tiflow/issues/3676)で`enable-old-value`の構成アイテムが自動的に`true`に設定されないバグを修正します。
        -   AvroシンクがJSONタイプの列の解析をサポートしていない問題を修正します[＃3624](https://github.com/pingcap/tiflow/issues/3624)
        -   チェンジフィードチェックポイントラグ[＃3010](https://github.com/pingcap/tiflow/issues/3010)の負の値のエラーを修正します
        -   コンテナ環境でのOOMの問題を修正する[＃1798](https://github.com/pingcap/tiflow/issues/1798)
        -   [＃3174](https://github.com/pingcap/tiflow/issues/3174)の処理後のメモリリークの問題を修正
        -   テーブルが同じノードで繰り返しスケジュールされている場合にchangefeedがスタックする問題を修正します[＃4464](https://github.com/pingcap/tiflow/issues/4464)
        -   PDノードが異常な場合にオープンAPIを介したステータスのクエリがブロックされる可能性があるバグを修正します[＃4778](https://github.com/pingcap/tiflow/issues/4778)
        -   所有者の変更によって引き起こされた誤ったメトリックを修正する[＃4774](https://github.com/pingcap/tiflow/issues/4774)
        -   UnifiedSorter1で使用されるworkerpoolの安定性の問題を修正し[＃4447](https://github.com/pingcap/tiflow/issues/4447)
        -   `cached region`モニタリングメトリックが負の[＃4300](https://github.com/pingcap/tiflow/issues/4300)である問題を修正します

    -   TiDB Lightning

        -   TiDBLightningに`mysql.tidb`テーブル[＃31088](https://github.com/pingcap/tidb/issues/31088)にアクセスする権限がない場合に発生する誤ったインポート結果の問題を修正します。
        -   チェックサムエラー「GCの有効期間がトランザクション期間より短い」を修正[＃32733](https://github.com/pingcap/tidb/issues/32733)
        -   一部のインポートタスクにソースファイルが含まれていない場合にTiDBLightningがメタデータスキーマを削除しない可能性があるバグを修正します[＃28144](https://github.com/pingcap/tidb/issues/28144)
        -   S3ストレージパスが存在しない場合にTiDBLightningがエラーを報告しない問題を修正し[＃30709](https://github.com/pingcap/tidb/issues/30709) [＃28031](https://github.com/pingcap/tidb/issues/28031)
        -   GCS1で1000を超えるキーを反復処理するときに発生するエラーを修正し[＃30377](https://github.com/pingcap/tidb/issues/30377)
