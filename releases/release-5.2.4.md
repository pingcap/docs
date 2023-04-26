---
title: TiDB 5.2.4 Release Notes
category: Releases
---

# TiDB 5.2.4 リリースノート {#tidb-5-2-4-release-notes}

リリース日：2022年4月26日

TiDB バージョン: 5.2.4

## 互換性の変更 {#compatibility-change-s}

-   TiDB

    -   システム変数[`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510)のデフォルト値を`2`から`1` [#31748](https://github.com/pingcap/tidb/issues/31748)に変更します。

-   TiKV

    -   時間間隔を制御するために[`raft-log-compact-sync-interval`](https://docs.pingcap.com/tidb/v5.2/tikv-configuration-file#raft-log-compact-sync-interval-new-in-v524)を追加します (デフォルトでは`"2s"` ) 不要なRaftログを圧縮します[#11404](https://github.com/tikv/tikv/issues/11404)
    -   デフォルト値の[`raft-log-gc-tick-interval`](/tikv-configuration-file.md#raft-log-gc-tick-interval)を`"10s"`から`"3s"` [#11404](https://github.com/tikv/tikv/issues/11404)に変更します。
    -   [`storage.flow-control.enable`](/tikv-configuration-file.md#enable)を`true`に設定すると、 [`storage.flow-control.hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit)の値が[`rocksdb.(defaultcf|writecf|lockcf).hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit-1) [#11424](https://github.com/tikv/tikv/issues/11424)の値を上書きします。

-   ツール

    -   TiDB Lightning

        -   デフォルト値の`regionMaxKeyCount` 1_440_000 から 1_280_000 に変更して、データのインポート後に空のリージョンが多くなりすぎないようにします[#30018](https://github.com/pingcap/tidb/issues/30018)

## 改良点 {#improvements}

-   TiKV

    -   リーダーシップを CDC オブザーバーに移管し、レイテンシーのジッターを減らします[#12111](https://github.com/tikv/tikv/issues/12111)
    -   ロックの解決ステップ[#11993](https://github.com/tikv/tikv/issues/11993)を必要とするリージョンの数を減らすことで、TiCDC の回復時間を短縮します。
    -   proc ファイルシステム (procfs) を v0.12.0 に更新します[#11702](https://github.com/tikv/tikv/issues/11702)
    -   ガベージ コレクション (GC) プロセスを高速化するには、GC をRaftログに実行するときに書き込みバッチ サイズを増やします[#11404](https://github.com/tikv/tikv/issues/11404)
    -   検証プロセスを`Apply`スレッド プール[#11239](https://github.com/tikv/tikv/issues/11239)から`Import`スレッド プールに移動することで、SST ファイルの挿入速度を向上させます。

-   ツール

    -   TiCDC

        -   Kafka Sink `partition-num`のデフォルト値を 3 に変更して、TiCDC が Kafka パーティション間でメッセージをより均等に分散するようにします[#3337](https://github.com/pingcap/tiflow/issues/3337)
        -   TiKV ストアがダウンしたときに KV クライアントが回復するまでの時間を短縮する[#3191](https://github.com/pingcap/tiflow/issues/3191)
        -   Grafana [#4891](https://github.com/pingcap/tiflow/issues/4891)に`Lag analyze`パネルを追加する
        -   Kafka プロデューサーの構成パラメーターを公開して、TiCDC [#4385](https://github.com/pingcap/tiflow/issues/4385)で構成可能にする
        -   changefeed [#3329](https://github.com/pingcap/tiflow/issues/3329)を再開するための指数バックオフ メカニズムを追加します。
        -   「EventFeed retry rate limited」ログのカウントを減らします[#4006](https://github.com/pingcap/tiflow/issues/4006)
        -   デフォルト値の`max-message-bytes`を 10M に設定[#4041](https://github.com/pingcap/tiflow/issues/4041)
        -   `no owner alert` 、 `mounter row` 、 `table sink total row` 、および`buffer sink total row` [#4054](https://github.com/pingcap/tiflow/issues/4054) [#1606](https://github.com/pingcap/tiflow/issues/1606)を含む、Prometheus および Grafana のモニタリング メトリックとアラートをさらに追加します。
        -   Grafana ダッシュボードで複数の Kubernetes クラスターをサポートする[#4665](https://github.com/pingcap/tiflow/issues/4665)
        -   キャッチアップ ETA (到着予定時刻) を`changefeed checkpoint`モニタリング メトリック[#5232](https://github.com/pingcap/tiflow/issues/5232)に追加します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   Enum 値[#32428](https://github.com/pingcap/tidb/issues/32428)の Nulleq 関数の誤った範囲計算結果を修正
    -   INDEX HASH JOIN が`send on closed channel`エラー[#31129](https://github.com/pingcap/tidb/issues/31129)を返す問題を修正
    -   列の型を同時に変更すると、スキーマとデータの間で不整合が発生する問題を修正します[#31048](https://github.com/pingcap/tidb/issues/31048)
    -   楽観的トランザクション モード[#30410](https://github.com/pingcap/tidb/issues/30410)での潜在的なデータ インデックスの不整合の問題を修正します。
    -   JSON 型の列が`CHAR`型の列を結合すると SQL 操作がキャンセルされる問題を修正します[#29401](https://github.com/pingcap/tidb/issues/29401)
    -   トランザクションを使用する場合と使用しない場合で、ウィンドウ関数が異なる結果を返すことがある問題を修正します[#29947](https://github.com/pingcap/tidb/issues/29947)
    -   SQL ステートメントに自然結合[#25041](https://github.com/pingcap/tidb/issues/25041)が含まれていると、予期せず`Column 'col_name' in field list is ambiguous`エラーが報告される問題を修正します。
    -   `Decimal`から`String` [#29417](https://github.com/pingcap/tidb/issues/29417)をキャストするとき、長さの情報が間違っている問題を修正
    -   `tidb_enable_vectorized_expression`の異なる値 ( `on`または`off`に設定) が原因で`GREATEST`関数が一貫性のない結果を返す問題を修正します[#29434](https://github.com/pingcap/tidb/issues/29434)
    -   `left join` [#31321](https://github.com/pingcap/tidb/issues/31321)を使用して複数のテーブルのデータを削除したときの誤った結果を修正
    -   TiDB が重複したタスクをTiFlash [#32814](https://github.com/pingcap/tidb/issues/32814)にディスパッチする可能性があるバグを修正
    -   クエリ実行時の MPP タスク リストの空エラーを修正します[#31636](https://github.com/pingcap/tidb/issues/31636)
    -   innerWorkerpanic[#31494](https://github.com/pingcap/tidb/issues/31494)によって引き起こされたインデックス結合の誤った結果を修正
    -   `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE`ステートメントを実行するとpanic[#28078](https://github.com/pingcap/tidb/issues/28078)が発生する問題を修正します。
    -   `Order By` [#30271](https://github.com/pingcap/tidb/issues/30271)の最適化による間違ったクエリ結果を修正
    -   `JOIN` on `ENUM`型の列[#27831](https://github.com/pingcap/tidb/issues/27831)を実行したときに発生する可能性のある間違った結果を修正します。
    -   `ENUM`データ型[#29357](https://github.com/pingcap/tidb/issues/29357)で`CASE WHEN`関数を使用したときのpanicを修正
    -   ベクトル化された式[#29244](https://github.com/pingcap/tidb/issues/29244)の`microsecond`関数の間違った結果を修正
    -   ウィンドウ関数が原因で TiDB がエラーを報告する代わりにpanicになる問題を修正します[#30326](https://github.com/pingcap/tidb/issues/30326)
    -   Merge Join 演算子が特定のケースで間違った結果を取得する問題を修正します[#33042](https://github.com/pingcap/tidb/issues/33042)
    -   相関サブクエリが定数[#32089](https://github.com/pingcap/tidb/issues/32089)を返すと、TiDB が間違った結果を取得する問題を修正します。
    -   `ENUM`列または`SET`列のエンコーディングが間違っているため、TiDB が間違ったデータを書き込む問題を修正します[#32302](https://github.com/pingcap/tidb/issues/32302)
    -   TiDB [#31638](https://github.com/pingcap/tidb/issues/31638)で新しい照合順序が有効になっている場合、 `ENUM`または`SET`列の`MAX`または`MIN`関数が間違った結果を返す問題を修正します。
    -   IndexHashJoin オペレーターが正常に終了しない問題を修正します[#31062](https://github.com/pingcap/tidb/issues/31062)
    -   テーブルに仮想列[#30965](https://github.com/pingcap/tidb/issues/30965)がある場合、TiDB が間違ったデータを読み取る可能性がある問題を修正します。
    -   スロークエリログ[#30309](https://github.com/pingcap/tidb/issues/30309)でログレベルの設定が反映されない問題を修正
    -   場合によっては、分割されたテーブルがインデックスを完全に使用してデータをスキャンできないという問題を修正します[#33966](https://github.com/pingcap/tidb/issues/33966)
    -   TiDB のバックグラウンド HTTP サービスが正常に終了せず、クラスターが異常な状態になることがある問題を修正します[#30571](https://github.com/pingcap/tidb/issues/30571)
    -   TiDB が予期せず多くの認証失敗のログを出力する可能性がある問題を修正します[#29709](https://github.com/pingcap/tidb/issues/29709)
    -   システム変数`max_allowed_packet`が有効にならない問題を修正[#31422](https://github.com/pingcap/tidb/issues/31422)
    -   自動 ID が範囲外の場合に`REPLACE`ステートメントが他の行を誤って変更する問題を修正します[#29483](https://github.com/pingcap/tidb/issues/29483)
    -   スロークエリログがログを正常に出力できず、メモリを消費しすぎる可能性がある問題を修正[#32656](https://github.com/pingcap/tidb/issues/32656)
    -   NATURAL JOIN の結果に予期しない列が含まれる可能性がある問題を修正します[#24981](https://github.com/pingcap/tidb/issues/29481)
    -   データ[#29711](https://github.com/pingcap/tidb/issues/29711)のクエリにプレフィックス列インデックスが使用されている場合、1 つのステートメントで`ORDER BY`と`LIMIT`を一緒に使用すると間違った結果が出力される可能性があるという問題を修正します。
    -   楽観的トランザクションが[#29892](https://github.com/pingcap/tidb/issues/29892)をリトライすると、DOUBLE 型の自動インクリメント カラムが変更される可能性がある問題を修正します。
    -   STR_TO_DATE 関数がマイクロ秒部分の前のゼロを正しく処理できない問題を修正します[#30078](https://github.com/pingcap/tidb/issues/30078)
    -   TiFlashを使用して空の範囲を持つテーブルをスキャンすると、TiDB が間違った結果を取得する問題を修正しますが、 TiFlash はまだ空の範囲を持つテーブルの読み取りをサポートしていません[#33083](https://github.com/pingcap/tidb/issues/33083)

-   TiKV

    -   古いメッセージが原因で TiKV がpanicになるバグを修正[#12023](https://github.com/tikv/tikv/issues/12023)
    -   メモリメトリック[#12160](https://github.com/tikv/tikv/issues/12160)のオーバーフローが原因で発生する断続的なパケット損失とメモリ不足 (OOM) の問題を修正します。
    -   TiKV が Ubuntu [#9765](https://github.com/tikv/tikv/issues/9765)でプロファイリングを実行するときに発生する潜在的なpanicの問題を修正します。
    -   間違った文字列の一致が原因で tikv-ctl が間違った結果を返す問題を修正します[#12329](https://github.com/tikv/tikv/issues/12329)
    -   レプリカの読み取りが線形化可能性に違反する可能性があるバグを修正します[#12109](https://github.com/tikv/tikv/issues/12109)
    -   TiKVが2年以上稼働しているとpanicになることがあるバグを修正[#11940](https://github.com/tikv/tikv/issues/11940)
    -   フロー制御が有効で、 `level0_slowdown_trigger`が明示的に設定され[#11424](https://github.com/tikv/tikv/issues/11424)いる場合の QPS ドロップの問題を修正します。
    -   cgroup コントローラーがマウントされていない場合に発生するpanicの問題を修正します[#11569](https://github.com/tikv/tikv/issues/11569)
    -   遅れているリージョンピア[#11526](https://github.com/tikv/tikv/issues/11526)でのリージョンマージによって発生する可能性のあるメタデータの破損を修正します。
    -   TiKVの動作停止後、Resolved TSのレイテンシーが増加する問題を修正[#11351](https://github.com/tikv/tikv/issues/11351)
    -   極端な状況でリージョンのマージ、ConfChange、およびスナップショットが同時に発生したときに発生するpanicの問題を修正します[#11475](https://github.com/tikv/tikv/issues/11475)
    -   tikv-ctl が正しいリージョン関連の情報を返せないバグを修正[#11393](https://github.com/tikv/tikv/issues/11393)
    -   10 進数の除算結果がゼロ[#29586](https://github.com/pingcap/tidb/issues/29586)の場合の負号の問題を修正
    -   悲観的トランザクション モードでプリライト リクエストを再試行すると、まれにデータの不整合が発生する可能性がある問題を修正します[#11187](https://github.com/tikv/tikv/issues/11187)
    -   統計スレッド[#11195](https://github.com/tikv/tikv/issues/11195)のデータを監視することによって引き起こされるメモリリークを修正します。
    -   インスタンスごとの gRPC リクエストの平均レイテンシーが TiKV メトリクスで不正確である問題を修正します[#11299](https://github.com/tikv/tikv/issues/11299)
    -   ピア ステータスが`Applying` [#11746](https://github.com/tikv/tikv/issues/11746)のときにスナップショット ファイルを削除すると発生するpanicの問題を修正します。
    -   GC ワーカーがビジー状態の場合、TiKV がデータの範囲を削除できない (つまり、内部コマンド`unsafe_destroy_range`が実行される) バグを修正します[#11903](https://github.com/tikv/tikv/issues/11903)
    -   初期化されていないレプリカを削除すると、古いレプリカが再作成される可能性があるという問題を修正します[#10533](https://github.com/tikv/tikv/issues/10533)
    -   TiKV がリバース テーブル スキャンを実行すると、TiKV がメモリロックを検出できない問題を修正します[#11440](https://github.com/tikv/tikv/issues/11440)
    -   コルーチンの実行速度が速すぎる場合に時々発生するデッドロックの問題を修正します[#11549](https://github.com/tikv/tikv/issues/11549)
    -   ピアを破棄すると高レイテンシーが発生する可能性がある問題を修正します[#10210](https://github.com/tikv/tikv/issues/10210)
    -   マージする対象のリージョンが無効であるため、TiKV が予期せずパニックになり、ピアを破棄する問題を修正します[#12232](https://github.com/tikv/tikv/issues/12232)
    -   リージョン[#12048](https://github.com/tikv/tikv/issues/12048)のマージ時にターゲット ピアが初期化されずに破棄されたピアに置き換えられると発生する TiKVpanicの問題を修正します。
    -   スナップショットの適用が中止されたときに発生する TiKVpanicの問題を修正します[#11618](https://github.com/tikv/tikv/issues/11618)
    -   オペレーターの実行が失敗したときに、TiKV が送信されているスナップショットの数を正しく計算できないというバグを修正します[#11341](https://github.com/tikv/tikv/issues/11341)

-   PD

    -   リージョン scatterer スケジューリングで一部のピアが失われる問題を修正します[#4565](https://github.com/tikv/pd/issues/4565)
    -   コールド ホットスポット データがホットスポット統計から削除できない問題を修正します[#4390](https://github.com/tikv/pd/issues/4390)

-   TiFlash

    -   MPP タスクがスレッドを永久にリークする可能性があるバグを修正します[#4238](https://github.com/pingcap/tiflash/issues/4238)
    -   多値式で`IN`の結果が正しくない問題を修正[#4016](https://github.com/pingcap/tiflash/issues/4016)
    -   日付形式が`'\n'`を無効な区切り文字として識別する問題を修正します[#4036](https://github.com/pingcap/tiflash/issues/4036)
    -   重い読み取りワークロードの下で列を追加した後の潜在的なクエリ エラーを修正します[#3967](https://github.com/pingcap/tiflash/issues/3967)
    -   無効なstorageディレクトリ構成が予期しない動作を引き起こすバグを修正します[#4093](https://github.com/pingcap/tiflash/issues/4093)
    -   一部の例外が適切に処理されないバグを修正[#4101](https://github.com/pingcap/tiflash/issues/4101)
    -   `STR_TO_DATE()`関数がマイクロ秒の解析時に先頭のゼロを正しく処理しないというバグを修正します[#3557](https://github.com/pingcap/tiflash/issues/3557)
    -   `INT`から`DECIMAL`をキャストするとオーバーフロー[#3920](https://github.com/pingcap/tiflash/issues/3920)が発生する可能性がある問題を修正
    -   `DATETIME`から`DECIMAL` [#4151](https://github.com/pingcap/tiflash/issues/4151)をキャストしたときに発生する誤った結果を修正します
    -   `FLOAT`から`DECIMAL` [#3998](https://github.com/pingcap/tiflash/issues/3998)へのキャスト時に発生するオーバーフローを修正
    -   `CastStringAsReal`動作がTiFlashと TiDB または TiKV [#3475](https://github.com/pingcap/tiflash/issues/3475)で一貫していない問題を修正
    -   `CastStringAsDecimal`動作がTiFlashと TiDB または TiKV [#3619](https://github.com/pingcap/tiflash/issues/3619)で一貫していない問題を修正
    -   TiFlash が再起動後に`EstablishMPPConnection`エラーを返す場合がある問題を修正[#3615](https://github.com/pingcap/tiflash/issues/3615)
    -   TiFlashレプリカの数を 0 [#3659](https://github.com/pingcap/tiflash/issues/3659)に設定した後、古いデータを再利用できないという問題を修正します。
    -   主キーが`handle` [#3569](https://github.com/pingcap/tiflash/issues/3569)の場合に主キー列を拡張すると、データの不整合が発生する可能性がある問題を修正
    -   SQL ステートメントに非常に長いネストされた式が含まれている場合に発生する可能性がある解析エラーを修正します[#3354](https://github.com/pingcap/tiflash/issues/3354)
    -   クエリに`where <string>`句[#3447](https://github.com/pingcap/tiflash/issues/3447)が含まれている場合に発生する可能性のある間違った結果を修正します
    -   `new_collations_enabled_on_first_bootstrap`が有効になっている場合に発生する可能性のある誤った結果を修正します[#3388](https://github.com/pingcap/tiflash/issues/3388) , [#3391](https://github.com/pingcap/tiflash/issues/3391)
    -   TLS が有効になっているときに発生するpanicの問題を修正します[#4196](https://github.com/pingcap/tiflash/issues/4196)
    -   メモリ制限が有効になっているときに発生するpanicの問題を修正します[#3902](https://github.com/pingcap/tiflash/issues/3902)
    -   MPP クエリを停止するとTiFlash がクラッシュすることがある問題を修正します[#3401](https://github.com/pingcap/tiflash/issues/3401)
    -   `Unexpected type of column: Nullable(Nothing)` [#3351](https://github.com/pingcap/tiflash/issues/3351)の予期しないエラーを修正
    -   遅れているリージョンピア[#4437](https://github.com/pingcap/tiflash/issues/4437)でのリージョンマージによって発生する可能性のあるメタデータの破損を修正します。
    -   エラーが発生した場合に`JOIN`含むクエリがハングする可能性がある問題を修正します[#4195](https://github.com/pingcap/tiflash/issues/4195)
    -   不適切な実行計画が原因で MPP クエリに対して返される可能性のある誤った結果を修正します[#3389](https://github.com/pingcap/tiflash/issues/3389)

-   ツール

    -   バックアップと復元 (BR)

        -   BR がRawKV [#32607](https://github.com/pingcap/tidb/issues/32607)のバックアップに失敗する問題を修正

    -   TiCDC

        -   デフォルト値をレプリケートできない問題を修正[#3793](https://github.com/pingcap/tiflow/issues/3793)
        -   場合によってはシーケンスが正しく複製されないというバグを修正[#4563](https://github.com/pingcap/tiflow/issues/4552)
        -   PD リーダーが強制終了されたときに TiCDC ノードが異常終了するバグを修正します[#4248](https://github.com/pingcap/tiflow/issues/4248)
        -   `batch-replace-enable`が無効になっている場合、MySQL シンクが重複した`replace` SQL ステートメントを生成するバグを修正します[#4501](https://github.com/pingcap/tiflow/issues/4501)
        -   デフォルトの列値[#3929](https://github.com/pingcap/tiflow/issues/3929)を出力するときに発生するpanicとデータの不整合の問題を修正します。
        -   `mq sink write row`監視データがない問題を修正[#3431](https://github.com/pingcap/tiflow/issues/3431)
        -   `min.insync.replicas`が`replication-factor` [#3994](https://github.com/pingcap/tiflow/issues/3994)より小さい場合にレプリケーションが実行できない問題を修正
        -   レプリケーション タスクが削除されたときに発生する潜在的なpanicの問題を修正します[#3128](https://github.com/pingcap/tiflow/issues/3128)
        -   必要なプロセッサ情報が存在しない場合に HTTP API がパニックするバグを修正[#3840](https://github.com/pingcap/tiflow/issues/3840)
        -   不正確なチェックポイント[#3545](https://github.com/pingcap/tiflow/issues/3545)によって引き起こされる潜在的なデータ損失の問題を修正します。
        -   デッドロックが原因でレプリケーション タスクがスタックする潜在的な問題を修正します[#4055](https://github.com/pingcap/tiflow/issues/4055)
        -   etcd [#2980](https://github.com/pingcap/tiflow/issues/2980)でタスク ステータスを手動でクリーニングするときに発生する TiCDCpanicの問題を修正します。
        -   DDL ステートメントの特殊なコメントによってレプリケーション タスクが停止する問題を修正します[#3755](https://github.com/pingcap/tiflow/issues/3755)
        -   `config.Metadata.Timeout` [#3352](https://github.com/pingcap/tiflow/issues/3352)の構成が正しくないために発生するレプリケーション停止の問題を修正します。
        -   RHEL リリース[#3584](https://github.com/pingcap/tiflow/issues/3584)でタイムゾーンの問題が原因でサービスを開始できない問題を修正
        -   `stopped`クラスターのアップグレード後に変更フィードが自動的に再開される問題を修正します[#3473](https://github.com/pingcap/tiflow/issues/3473)
        -   MySQL シンクのデッドロック[#2706](https://github.com/pingcap/tiflow/issues/2706)が原因で頻繁に警告が表示される問題を修正
        -   Canal および Maxwell プロトコル[#3676](https://github.com/pingcap/tiflow/issues/3676)で`enable-old-value`構成項目が自動的に`true`に設定されないバグを修正
        -   Avro シンクが JSON 型の列の解析をサポートしていない問題を修正します[#3624](https://github.com/pingcap/tiflow/issues/3624)
        -   changefeed チェックポイントラグ[#3010](https://github.com/pingcap/tiflow/issues/3010)の負の値のエラーを修正します。
        -   コンテナー環境での OOM の問題を修正する[#1798](https://github.com/pingcap/tiflow/issues/1798)
        -   DDL [#3174](https://github.com/pingcap/tiflow/issues/3174)の処理後のメモリリークの問題を修正します。
        -   テーブルが同じノード[#4464](https://github.com/pingcap/tiflow/issues/4464)で繰り返しスケジュールされると、changefeed が停止する問題を修正します。
        -   PD ノードが異常な場合、オープン API を介したステータスのクエリがブロックされる可能性があるバグを修正します[#4778](https://github.com/pingcap/tiflow/issues/4778)
        -   所有者の変更による不正確な指標の修正[#4774](https://github.com/pingcap/tiflow/issues/4774)
        -   Unified Sorter [#4447](https://github.com/pingcap/tiflow/issues/4447)が使用するワーカープールの安定性の問題を修正
        -   `cached region`モニタリング指標がマイナス[#4300](https://github.com/pingcap/tiflow/issues/4300)になる問題を修正

    -   TiDB Lightning

        -   TiDB Lightning が`mysql.tidb`テーブルへのアクセス権限を持っていない場合に発生する間違ったインポート結果の問題を修正[#31088](https://github.com/pingcap/tidb/issues/31088)
        -   チェックサム エラー「GC ライフ タイムがトランザクション期間よりも短い」を修正します[#32733](https://github.com/pingcap/tidb/issues/32733)
        -   一部のインポート タスクにソース ファイルが含まれていない場合、 TiDB Lightning がメタデータ スキーマを削除しないことがあるというバグを修正します[#28144](https://github.com/pingcap/tidb/issues/28144)
        -   S3storageパスが存在しない場合にTiDB Lightning がエラーを報告しない問題を修正[#28031](https://github.com/pingcap/tidb/issues/28031) [#30709](https://github.com/pingcap/tidb/issues/30709)
        -   GCS [#30377](https://github.com/pingcap/tidb/issues/30377)で 1000 を超えるキーを反復するときに発生するエラーを修正
