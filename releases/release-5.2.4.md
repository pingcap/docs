---
title: TiDB 5.2.4 Release Notes
category: Releases
---

# TiDB 5.2.4 リリースノート {#tidb-5-2-4-release-notes}

リリース日：2022年4月26日

TiDB バージョン: 5.2.4

## 互換性の変更 {#compatibility-change-s}

-   TiDB

    -   システム変数[`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510)のデフォルト値を`2`から`1`に変更します[#31748](https://github.com/pingcap/tidb/issues/31748)

-   TiKV

    -   不要なRaftログを圧縮するための時間間隔 (デフォルトでは`"2s"` ) を制御するには[`raft-log-compact-sync-interval`](https://docs.pingcap.com/tidb/v5.2/tikv-configuration-file#raft-log-compact-sync-interval-new-in-v524)を追加します[#11404](https://github.com/tikv/tikv/issues/11404)
    -   デフォルト値の[`raft-log-gc-tick-interval`](/tikv-configuration-file.md#raft-log-gc-tick-interval)を`"10s"`から`"3s"`に変更します[#11404](https://github.com/tikv/tikv/issues/11404)
    -   [`storage.flow-control.enable`](/tikv-configuration-file.md#enable)を`true`に設定すると、 [`storage.flow-control.hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit)の値が[`rocksdb.(defaultcf|writecf|lockcf).hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit-1) [#11424](https://github.com/tikv/tikv/issues/11424)の値を上書きします。

-   ツール

    -   TiDB Lightning

        -   データ インポート[#30018](https://github.com/pingcap/tidb/issues/30018)後に空のリージョンが多すぎるのを避けるために、デフォルト値`regionMaxKeyCount`を 1_440_000 から 1_280_000 に変更します。

## 改善点 {#improvements}

-   TiKV

    -   リーダーシップを CDC オブザーバーに移管して、レイテンシージッター[#12111](https://github.com/tikv/tikv/issues/12111)を削減します。
    -   ロックの解決ステップ[#11993](https://github.com/tikv/tikv/issues/11993)を必要とするリージョンの数を減らすことで、TiCDC の回復時間を短縮します。
    -   proc ファイルシステム (procfs) を v0.12.0 に更新します[#11702](https://github.com/tikv/tikv/issues/11702)
    -   Raftログへの GC を実行するときに書き込みバッチ サイズを増やすことで、ガベージ コレクション (GC) プロセスを高速化します[#11404](https://github.com/tikv/tikv/issues/11404)
    -   検証プロセスを`Apply`スレッド プール[#11239](https://github.com/tikv/tikv/issues/11239)から`Import`スレッド プールに移動することで、SST ファイルの挿入速度が向上しました。

-   ツール

    -   TiCDC

        -   TiCDC が Kafka パーティション間でメッセージをより均等に分散できるように、Kafka Sink のデフォルト値`partition-num`を[#3337](https://github.com/pingcap/tiflow/issues/3337)に変更します。
        -   TiKV ストアがダウンした場合に KV クライアントが回復するまでの時間を短縮します[#3191](https://github.com/pingcap/tiflow/issues/3191)
        -   Grafana [#4891](https://github.com/pingcap/tiflow/issues/4891)に`Lag analyze`パネルを追加する
        -   Kafka プロデューサの構成パラメータを公開して、TiCDC [#4385](https://github.com/pingcap/tiflow/issues/4385)で構成できるようにします。
        -   変更フィードを再開するための指数バックオフ メカニズムを追加します[#3329](https://github.com/pingcap/tiflow/issues/3329)
        -   「EventFeed 再試行速度制限」ログの数を減らす[#4006](https://github.com/pingcap/tiflow/issues/4006)
        -   デフォルト値の`max-message-bytes`を 10M [#4041](https://github.com/pingcap/tiflow/issues/4041)に設定します。
        -   `no owner alert` 、 `mounter row` 、 `table sink total row` 、 `buffer sink total row`などの Prometheus および Grafana モニタリング メトリックとアラートを追加します[#4054](https://github.com/pingcap/tiflow/issues/4054) [#1606](https://github.com/pingcap/tiflow/issues/1606)
        -   Grafana ダッシュボードで複数の Kubernetes クラスターをサポート[#4665](https://github.com/pingcap/tiflow/issues/4665)
        -   キャッチアップ ETA (到着予定時刻) を`changefeed checkpoint`モニタリング指標に追加します[#5232](https://github.com/pingcap/tiflow/issues/5232)

## バグの修正 {#bug-fixes}

-   TiDB

    -   Enum 値[#32428](https://github.com/pingcap/tidb/issues/32428)に対する Nulleq 関数の間違った範囲計算結果を修正しました。
    -   INDEX HASH JOIN が`send on closed channel`エラー[#31129](https://github.com/pingcap/tidb/issues/31129)を返す問題を修正
    -   同時に列の型を変更すると、スキーマとデータの間で不整合が発生する問題を修正します[#31048](https://github.com/pingcap/tidb/issues/31048)
    -   楽観的トランザクション モード[#30410](https://github.com/pingcap/tidb/issues/30410)での潜在的なデータ インデックスの不一致の問題を修正します。
    -   JSON 型の列が`CHAR`型の列[#29401](https://github.com/pingcap/tidb/issues/29401)に結合すると SQL 操作がキャンセルされる問題を修正
    -   トランザクションを使用する場合と使用しない場合に、ウィンドウ関数が異なる結果を返す可能性がある問題を修正します[#29947](https://github.com/pingcap/tidb/issues/29947)
    -   SQL ステートメントに自然結合[#25041](https://github.com/pingcap/tidb/issues/25041)が含まれる場合、予期せず`Column 'col_name' in field list is ambiguous`エラーが報告される問題を修正します。
    -   `Decimal` ～ `String` [#29417](https://github.com/pingcap/tidb/issues/29417)をキャストする際に長さ情報が間違っている問題を修正
    -   `tidb_enable_vectorized_expression`の値が異なるために`GREATEST`関数が一貫性のない結果を返す問題を修正します ( `on`または`off`に設定) [#29434](https://github.com/pingcap/tidb/issues/29434)
    -   `left join` [#31321](https://github.com/pingcap/tidb/issues/31321)を使用して複数のテーブルのデータを削除した場合の誤った結果を修正
    -   TiDB が重複したタスクをTiFlash [#32814](https://github.com/pingcap/tidb/issues/32814)にディスパッチする可能性があるバグを修正
    -   クエリ[#31636](https://github.com/pingcap/tidb/issues/31636)を実行するときの MPP タスク リストが空のエラーを修正しました。
    -   innerWorkerpanic[#31494](https://github.com/pingcap/tidb/issues/31494)によって引き起こされるインデックス結合の間違った結果を修正します。
    -   `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE`ステートメントを実行するとpanic[#28078](https://github.com/pingcap/tidb/issues/28078)が発生する問題を修正
    -   `Order By` [#30271](https://github.com/pingcap/tidb/issues/30271)の最適化による間違ったクエリ結果を修正
    -   `ENUM`型列[#27831](https://github.com/pingcap/tidb/issues/27831)で`JOIN`実行したときに発生する可能性がある間違った結果を修正しました。
    -   `ENUM`データ型[#29357](https://github.com/pingcap/tidb/issues/29357)で`CASE WHEN`関数を使用するときのpanicを修正しました。
    -   ベクトル化された式[#29244](https://github.com/pingcap/tidb/issues/29244)の関数`microsecond`の誤った結果を修正します。
    -   ウィンドウ関数により TiDB がエラーを報告する代わりにpanicを引き起こす問題を修正します[#30326](https://github.com/pingcap/tidb/issues/30326)
    -   特定の場合に Merge Join 演算子が間違った結果を取得する問題を修正します[#33042](https://github.com/pingcap/tidb/issues/33042)
    -   相関サブクエリが定数[#32089](https://github.com/pingcap/tidb/issues/32089)を返すと TiDB が間違った結果を取得する問題を修正
    -   `ENUM`列または`SET`列のエンコーディングが間違っているため、TiDB が間違ったデータを書き込む問題を修正します[#32302](https://github.com/pingcap/tidb/issues/32302)
    -   TiDB [#31638](https://github.com/pingcap/tidb/issues/31638)で新しい照合順序が有効になっている場合、 `ENUM`または`SET`列の`MAX`または`MIN`関数が間違った結果を返す問題を修正します。
    -   IndexHashJoin オペレーターが正常に終了しない問題を修正します[#31062](https://github.com/pingcap/tidb/issues/31062)
    -   テーブルに仮想列[#30965](https://github.com/pingcap/tidb/issues/30965)がある場合、TiDB が間違ったデータを読み取る可能性がある問題を修正
    -   スロークエリログ[#30309](https://github.com/pingcap/tidb/issues/30309)でログレベルの設定が反映されない問題を修正
    -   場合によっては、パーティション化されたテーブルがインデックスを完全に使用してデータをスキャンできない問題を修正します[#33966](https://github.com/pingcap/tidb/issues/33966)
    -   TiDB のバックグラウンド HTTP サービスが正常に終了せず、クラスターが異常な状態になる場合がある問題を修正します[#30571](https://github.com/pingcap/tidb/issues/30571)
    -   TiDB が予期せず認証失敗のログを多数出力する場合がある問題を修正[#29709](https://github.com/pingcap/tidb/issues/29709)
    -   システム変数`max_allowed_packet`が有効にならない問題を修正[#31422](https://github.com/pingcap/tidb/issues/31422)
    -   自動 ID が範囲[#29483](https://github.com/pingcap/tidb/issues/29483)の外にある場合、 `REPLACE`ステートメントが他の行を誤って変更する問題を修正します。
    -   スロークエリログが正常にログ出力できず、メモリを過剰に消費する可能性がある問題を修正[#32656](https://github.com/pingcap/tidb/issues/32656)
    -   NATURAL JOIN の結果に予期しない列が含まれる場合がある問題を修正[#24981](https://github.com/pingcap/tidb/issues/29481)
    -   データ[#29711](https://github.com/pingcap/tidb/issues/29711)のクエリにプレフィックス列インデックスが使用されている場合、1 つのステートメントで`ORDER BY`と`LIMIT`を一緒に使用すると間違った結果が出力される可能性がある問題を修正します。
    -   楽観的トランザクションのリトライ時にDOUBLE型の自動インクリメント列が変更される場合がある問題を修正[#29892](https://github.com/pingcap/tidb/issues/29892)
    -   STR_TO_DATE 関数がマイクロ秒部分の前のゼロを正しく処理できない問題を修正します[#30078](https://github.com/pingcap/tidb/issues/30078)
    -   TiFlash は空の範囲を持つテーブルの読み取りをサポートしていませんが、 TiFlashを使用して空の範囲を持つテーブルをスキャンすると、 TiFlashが間違った結果を取得する問題を修正します[#33083](https://github.com/pingcap/tidb/issues/33083)

-   TiKV

    -   古いメッセージによって TiKV がpanicになるバグを修正[#12023](https://github.com/tikv/tikv/issues/12023)
    -   メモリメトリクス[#12160](https://github.com/tikv/tikv/issues/12160)のオーバーフローによって引き起こされる断続的なパケット損失とメモリ不足 (OOM) の問題を修正します。
    -   TiKV が Ubuntu 18.04 でプロファイリングを実行するときに発生する潜在的なpanicの問題を修正します[#9765](https://github.com/tikv/tikv/issues/9765)
    -   間違った文字列一致[#12329](https://github.com/tikv/tikv/issues/12329)が原因で tikv-ctl が間違った結果を返す問題を修正
    -   レプリカの読み取りが線形化可能性[#12109](https://github.com/tikv/tikv/issues/12109)に違反する可能性があるバグを修正
    -   TiKV が 2 年以上実行されている場合にpanicになる可能性があるバグを修正[#11940](https://github.com/tikv/tikv/issues/11940)
    -   フロー制御が有効で、 `level0_slowdown_trigger`が明示的に設定されている場合の QPS ドロップの問題を修正します[#11424](https://github.com/tikv/tikv/issues/11424)
    -   cgroup コントローラーがマウントされていないときに発生するpanicの問題を修正します[#11569](https://github.com/tikv/tikv/issues/11569)
    -   遅れているリージョンピア[#11526](https://github.com/tikv/tikv/issues/11526)でのリージョンのマージによって発生する可能性のあるメタデータの破損を修正します。
    -   TiKVの動作停止後にResolved TSのレイテンシーが増加する問題を修正[#11351](https://github.com/tikv/tikv/issues/11351)
    -   極端な条件でリージョンのマージ、ConfChange、およびスナップショットが同時に発生したときに発生するpanicの問題を修正します[#11475](https://github.com/tikv/tikv/issues/11475)
    -   tikv-ctl が正しいリージョン関連情報を返せないバグを修正[#11393](https://github.com/tikv/tikv/issues/11393)
    -   10 進数の除算結果が 0 の場合の負号の問題を修正します[#29586](https://github.com/pingcap/tidb/issues/29586)
    -   悲観的トランザクションモードでプリライトリクエストを再試行すると、まれにデータ不整合のリスクが発生する可能性がある問題を修正します[#11187](https://github.com/tikv/tikv/issues/11187)
    -   統計スレッド[#11195](https://github.com/tikv/tikv/issues/11195)のデータ監視によって発生するメモリリークを修正しました。
    -   TiKV メトリクス[#11299](https://github.com/tikv/tikv/issues/11299)でインスタンスごとの gRPC リクエストの平均レイテンシーが不正確である問題を修正します。
    -   ピアのステータスが`Applying` [#11746](https://github.com/tikv/tikv/issues/11746)のときにスナップショット ファイルを削除することによって引き起こされるpanicの問題を修正します。
    -   GC ワーカーがビジー状態[#11903](https://github.com/tikv/tikv/issues/11903)の場合、TiKV が一定範囲のデータを削除できない (内部コマンド`unsafe_destroy_range`が実行されることを意味します) というバグを修正します。
    -   初期化されていないレプリカを削除すると古いレプリカが再作成される可能性がある問題を修正します[#10533](https://github.com/tikv/tikv/issues/10533)
    -   TiKV が逆テーブル スキャンを実行するときに TiKV がメモリロックを検出できない問題を修正します[#11440](https://github.com/tikv/tikv/issues/11440)
    -   コルーチンの実行が速すぎる場合に時折発生するデッドロックの問題を修正します[#11549](https://github.com/tikv/tikv/issues/11549)
    -   ピアを破棄するとレイテンシーが長くなる可能性がある問題を修正[#10210](https://github.com/tikv/tikv/issues/10210)
    -   マージ対象のターゲットリージョンが無効であるため、TiKV がパニックを起こして予期せずピアを破棄する問題を修正します[#12232](https://github.com/tikv/tikv/issues/12232)
    -   リージョン[#12048](https://github.com/tikv/tikv/issues/12048)をマージするときに、ターゲット ピアが初期化されずに破棄されたピアに置き換えられるときに発生する TiKVpanicの問題を修正します。
    -   スナップショットの適用が中止されたときに発生する TiKVpanicの問題を修正します[#11618](https://github.com/tikv/tikv/issues/11618)
    -   オペレーターの実行が失敗した場合、TiKV が送信されるスナップショットの数を正しく計算できないバグを修正[#11341](https://github.com/tikv/tikv/issues/11341)

-   PD

    -   リージョンスキャッタラー スケジューリングで一部のピアが失われる問題を修正します[#4565](https://github.com/tikv/pd/issues/4565)
    -   コールド ホットスポット データがホットスポット統計[#4390](https://github.com/tikv/pd/issues/4390)から削除できない問題を修正します。

-   TiFlash

    -   MPP タスクがスレッドを永久にリークする可能性があるバグを修正[#4238](https://github.com/pingcap/tiflash/issues/4238)
    -   複数値式[#4016](https://github.com/pingcap/tiflash/issues/4016)で`IN`の結果が正しくない問題を修正
    -   日付形式で`'\n'`無効な区切り文字[#4036](https://github.com/pingcap/tiflash/issues/4036)として識別される問題を修正します。
    -   重い読み取りワークロードで列を追加した後の潜在的なクエリ エラーを修正[#3967](https://github.com/pingcap/tiflash/issues/3967)
    -   無効なstorageディレクトリ構成が予期せぬ動作を引き起こすバグを修正[#4093](https://github.com/pingcap/tiflash/issues/4093)
    -   一部の例外が正しく処理されないバグを修正[#4101](https://github.com/pingcap/tiflash/issues/4101)
    -   `STR_TO_DATE()`関数がマイクロ秒[#3557](https://github.com/pingcap/tiflash/issues/3557)を解析する際に先頭のゼロを誤って処理するバグを修正
    -   `INT`から`DECIMAL`にキャストするとオーバーフローが発生する可能性がある問題を修正[#3920](https://github.com/pingcap/tiflash/issues/3920)
    -   `DATETIME`から`DECIMAL` [#4151](https://github.com/pingcap/tiflash/issues/4151)をキャストするときに発生する間違った結果を修正
    -   `FLOAT` ～ `DECIMAL` [#3998](https://github.com/pingcap/tiflash/issues/3998)キャスト時に発生するオーバーフローを修正
    -   TiFlashと TiDB または TiKV [#3475](https://github.com/pingcap/tiflash/issues/3475)で`CastStringAsReal`動作が矛盾する問題を修正
    -   TiFlashと TiDB または TiKV [#3619](https://github.com/pingcap/tiflash/issues/3619)で`CastStringAsDecimal`動作が矛盾する問題を修正
    -   TiFlashの再起動後に`EstablishMPPConnection`エラーが返されることがある問題を修正[#3615](https://github.com/pingcap/tiflash/issues/3615)
    -   TiFlashレプリカの数を 0 [#3659](https://github.com/pingcap/tiflash/issues/3659)に設定した後、古いデータを再利用できない問題を修正
    -   主キーが`handle` [#3569](https://github.com/pingcap/tiflash/issues/3569)の主キー列を拡張するときに発生する可能性のあるデータの不整合を修正しました。
    -   SQL ステートメントに非常に長いネストされた式が含まれている場合に発生する可能性のある解析エラーを修正します[#3354](https://github.com/pingcap/tiflash/issues/3354)
    -   クエリに`where <string>`句[#3447](https://github.com/pingcap/tiflash/issues/3447)が含まれる場合に発生する可能性のある間違った結果を修正
    -   `new_collations_enabled_on_first_bootstrap`有効になっている場合に発生する可能性のある間違った結果を修正[#3388](https://github.com/pingcap/tiflash/issues/3388) 、 [#3391](https://github.com/pingcap/tiflash/issues/3391)
    -   TLS が有効になっているときに発生するpanicの問題を修正します[#4196](https://github.com/pingcap/tiflash/issues/4196)
    -   メモリ制限が有効になっているときに発生するpanicの問題を修正します[#3902](https://github.com/pingcap/tiflash/issues/3902)
    -   MPP クエリが停止するとTiFlashが時折クラッシュする問題を修正[#3401](https://github.com/pingcap/tiflash/issues/3401)
    -   `Unexpected type of column: Nullable(Nothing)` [#3351](https://github.com/pingcap/tiflash/issues/3351)の予期しないエラーを修正
    -   遅れているリージョンピア[#4437](https://github.com/pingcap/tiflash/issues/4437)でのリージョンのマージによって発生する可能性のあるメタデータの破損を修正します。
    -   `JOIN`を含むクエリでエラーが発生した場合にハングする可能性がある問題を修正[#4195](https://github.com/pingcap/tiflash/issues/4195)
    -   不正な実行プランにより、MPP クエリに対して誤った結果が返される可能性がある問題を修正[#3389](https://github.com/pingcap/tiflash/issues/3389)

-   ツール

    -   バックアップと復元 (BR)

        -   BR がRawKV [#32607](https://github.com/pingcap/tidb/issues/32607)のバックアップに失敗する問題を修正

    -   TiCDC

        -   デフォルト値を複製できない問題を修正[#3793](https://github.com/pingcap/tiflow/issues/3793)
        -   場合によってはシーケンスが不正に複製されるバグを修正[#4563](https://github.com/pingcap/tiflow/issues/4552)
        -   PDリーダーがキルされた場合にTiCDCノードが異常終了するバグを修正[#4248](https://github.com/pingcap/tiflow/issues/4248)
        -   `batch-replace-enable`が無効になっている場合、MySQL シンクが重複した`replace` SQL ステートメントを生成するバグを修正[#4501](https://github.com/pingcap/tiflow/issues/4501)
        -   デフォルトの列値[#3929](https://github.com/pingcap/tiflow/issues/3929)を出力するときに発生するpanicとデータの不整合の問題を修正します。
        -   `mq sink write row`監視データがない問題を修正[#3431](https://github.com/pingcap/tiflow/issues/3431)
        -   `min.insync.replicas`が`replication-factor` [#3994](https://github.com/pingcap/tiflow/issues/3994)より小さい場合にレプリケーションが実行できない問題を修正
        -   レプリケーション タスクが削除されたときに発生する潜在的なpanicの問題を修正します[#3128](https://github.com/pingcap/tiflow/issues/3128)
        -   必要なプロセッサ情報が存在しない場合にHTTP APIがパニックするバグを修正[#3840](https://github.com/pingcap/tiflow/issues/3840)
        -   不正確なチェックポイント[#3545](https://github.com/pingcap/tiflow/issues/3545)によって引き起こされる潜在的なデータ損失の問題を修正します。
        -   デッドロックによりレプリケーション タスクが停止するという潜在的な問題を修正します[#4055](https://github.com/pingcap/tiflow/issues/4055)
        -   etcd [#2980](https://github.com/pingcap/tiflow/issues/2980)でタスクステータスを手動でクリーンアップするときに発生する TiCDCpanicの問題を修正します。
        -   DDL ステートメント内の特別なコメントによりレプリケーション タスクが停止する問題を修正します[#3755](https://github.com/pingcap/tiflow/issues/3755)
        -   `config.Metadata.Timeout` [#3352](https://github.com/pingcap/tiflow/issues/3352)の誤った構成によって引き起こされるレプリケーション停止の問題を修正します。
        -   RHEL リリース[#3584](https://github.com/pingcap/tiflow/issues/3584)のタイムゾーンの問題によりサービスを開始できない問題を修正
        -   `stopped`クラスターのアップグレード後に変更フィードが自動的に再開される問題を修正[#3473](https://github.com/pingcap/tiflow/issues/3473)
        -   MySQL シンクのデッドロックによって引き起こされる過度に頻繁な警告の問題を修正します[#2706](https://github.com/pingcap/tiflow/issues/2706)
        -   CanalおよびMaxwellプロトコル[#3676](https://github.com/pingcap/tiflow/issues/3676)において、 `enable-old-value`設定項目が自動的に`true`に設定されないバグを修正
        -   Avro シンクが JSON 型列の解析をサポートしていない問題を修正します[#3624](https://github.com/pingcap/tiflow/issues/3624)
        -   チェンジフィードチェックポイントラグ[#3010](https://github.com/pingcap/tiflow/issues/3010)の負の値エラーを修正
        -   コンテナ環境の OOM 問題を修正する[#1798](https://github.com/pingcap/tiflow/issues/1798)
        -   DDL 処理後のメモリリーク問題を修正[#3174](https://github.com/pingcap/tiflow/issues/3174)
        -   同じノード[#4464](https://github.com/pingcap/tiflow/issues/4464)でテーブルが繰り返しスケジュールされると、変更フィードがスタックする問題を修正します。
        -   PDノードが異常[#4778](https://github.com/pingcap/tiflow/issues/4778)の場合、オープンAPIによるステータス問い合わせがブロックされる場合があるバグを修正
        -   所有者の変更によって引き起こされた誤ったメトリクスを修正する[#4774](https://github.com/pingcap/tiflow/issues/4774)
        -   Unified Sorter [#4447](https://github.com/pingcap/tiflow/issues/4447)によって使用されるワーカープールの安定性の問題を修正しました。
        -   `cached region`監視メトリクスがマイナス[#4300](https://github.com/pingcap/tiflow/issues/4300)になる問題を修正

    -   TiDB Lightning

        -   TiDB Lightning にテーブル`mysql.tidb`へのアクセス権限がない場合にインポート結果が正しくない問題を[#31088](https://github.com/pingcap/tidb/issues/31088)
        -   チェックサム エラー「GC ライフタイムがトランザクション期間よりも短い」 [#32733](https://github.com/pingcap/tidb/issues/32733)を修正
        -   一部のインポートタスクにソースファイルが含まれていない場合、 TiDB Lightning がメタデータスキーマを削除できないことがあるバグを修正[#28144](https://github.com/pingcap/tidb/issues/28144)
        -   S3storageパスが存在しない場合にTiDB Lightning がエラーを報告しない問題を修正[#28031](https://github.com/pingcap/tidb/issues/28031) [#30709](https://github.com/pingcap/tidb/issues/30709)
        -   GCS [#30377](https://github.com/pingcap/tidb/issues/30377)で 1000 を超えるキーを反復するときに発生するエラーを修正
