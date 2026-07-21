---
title: TiDB 5.2.4 Release Notes
category: Releases
summary: TiDB 5.2.4 の新機能、互換性の変更点、改善点、およびバグ修正についてご確認ください。
---

# TiDB 5.2.4 リリースノート {#tidb-5-2-4-release-notes}

リリース日：2022年4月26日

TiDBバージョン：5.2.4

## 互換性の変更点 {#compatibility-change-s}

-   TiDB

    -   システム変数[`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510)のデフォルト値を`2`から`1`に変更します。 [#31748](https://github.com/pingcap/tidb/issues/31748)

-   TiKV

    -   不要なRaftログを圧縮する時間間隔 (デフォルトでは`"2s"` ) を制御するために[`raft-log-compact-sync-interval`](https://docs-archive.pingcap.com/tidb/v5.2/tikv-configuration-file#raft-log-compact-sync-interval-new-in-v524)を追加する [#11404](https://github.com/tikv/tikv/issues/11404)
    -   [`raft-log-gc-tick-interval`](/tikv-configuration-file.md#raft-log-gc-tick-interval)のデフォルト値を`"10s"`から`"3s"`に変更する [#11404](https://github.com/tikv/tikv/issues/11404)
    -   [`storage.flow-control.enable`](/tikv-configuration-file.md#enable)が`true`に設定されている場合、 [`storage.flow-control.hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit)の値が[`rocksdb.(defaultcf|writecf|lockcf).hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit-1)の値を上書きします [#11424](https://github.com/tikv/tikv/issues/11424)

-   ツール

    -   TiDB Lightning

        -   データインポート後に空のリージョンが多すぎるのを避けるため、 `regionMaxKeyCount`のデフォルト値を 1_440_000 から 1_280_000 に変更します [#30018](https://github.com/pingcap/tidb/issues/30018)

## 改善点 {#improvements}

-   TiKV

    -   レイテンシージッターを低減するために、リーダーシップをCDCオブザーバーに移管する [#12111](https://github.com/tikv/tikv/issues/12111)
    -   解決ロック手順を必要とするリージョンの数を減らすことで、TiCDC のリカバリ時間を短縮します。 [#11993](https://github.com/tikv/tikv/issues/11993)
    -   procファイルシステム（procfs）をv0.12.0にアップデートする [#11702](https://github.com/tikv/tikv/issues/11702)
    -   RaftログへのGC実行時に書き込みバッチサイズを増やすことで、ガベージコレクション（GC）プロセスを高速化する [#11404](https://github.com/tikv/tikv/issues/11404)
    -   検証プロセスを`Import`スレッドプールから`Apply`スレッドプールに移動することで、SSTファイルの挿入速度を向上させます [#11239](https://github.com/tikv/tikv/issues/11239)

-   ツール

    -   TiCDC

        -   TiCDCがKafkaパーティション全体にメッセージをより均等に分散するように、Kafkaシンクのデフォルト値`partition-num` 3に変更します。 [#3337](https://github.com/pingcap/tiflow/issues/3337)
        -   TiKVストアがダウンした際にKVクライアントが復旧するまでの時間を短縮する [#3191](https://github.com/pingcap/tiflow/issues/3191)
        -   Grafanaに`Lag analyze`パネルを追加する [#4891](https://github.com/pingcap/tiflow/issues/4891)
        -   TiCDCでKafkaプロデューサーの設定パラメータを公開し、設定可能にする [#4385](https://github.com/pingcap/tiflow/issues/4385)
        -   変更フィードを再開するための指数バックオフメカニズムを追加 [#3329](https://github.com/pingcap/tiflow/issues/3329)
        -   「EventFeed retry rate limited」ログの数を減らす [#4006](https://github.com/pingcap/tiflow/issues/4006)
        -   `max-message-bytes`のデフォルト値を 10M に設定します [#4041](https://github.com/pingcap/tiflow/issues/4041)
        -   `no owner alert` 、 `mounter row` 、 `table sink total row`を含む、 `buffer sink total row`および Grafana の監視メトリクスとアラートをさらに追加します[#4054](https://github.com/pingcap/tiflow/issues/4054) [#1606](https://github.com/pingcap/tiflow/issues/1606)
        -   Grafanaダッシュボードで複数のKubernetesクラスターをサポートする [#4665](https://github.com/pingcap/tiflow/issues/4665)
        -   `changefeed checkpoint` モニタリングメトリックに、キャッチアップ ETA (到着予定時刻) を追加します。 [#5232](https://github.com/pingcap/tiflow/issues/5232)

## バグ修正 {#bug-fixes}

-   TiDB

    -   Enum値に対するNulleq関数の範囲計算結果の誤りを修正 [#32428](https://github.com/pingcap/tidb/issues/32428)
    -   INDEX HASH JOIN が`send on closed channel`エラーを返す問題を修正します [#31129](https://github.com/pingcap/tidb/issues/31129)
    -   同時実行される列型変更によってスキーマとデータの間に不整合が生じる問題を修正します [#31048](https://github.com/pingcap/tidb/issues/31048)
    -   楽観的トランザクションモードにおける潜在的なデータインデックスの不整合の問題を修正 [#30410](https://github.com/pingcap/tidb/issues/30410)
    -   SQL操作がJSON型の列と`CHAR`型の列を結合する際にキャンセルされる問題を修正しました [#29401](https://github.com/pingcap/tidb/issues/29401)
    -   ウィンドウ関数がトランザクションを使用する場合と使用しない場合で異なる結果を返す可能性がある問題を修正しました [#29947](https://github.com/pingcap/tidb/issues/29947)
    -   SQL文に自然結合が含まれている場合に`Column 'col_name' in field list is ambiguous`エラーが予期せず報告される問題を修正しました [#25041](https://github.com/pingcap/tidb/issues/25041)
    -   `Decimal`を`String`にキャストする際に長さ情報が間違っている問題を修正しました [#29417](https://github.com/pingcap/tidb/issues/29417)
    -   `GREATEST`関数が`tidb_enable_vectorized_expression`の値が異なる場合（{{B-PLACEHOLDER-2- `on`または`off` 。 [#29434](https://github.com/pingcap/tidb/issues/29434)
    -   `left join`を使用して複数のテーブルのデータを削除する際の誤った結果を修正 [#31321](https://github.com/pingcap/tidb/issues/31321)
    -   TiDBがTiFlashに重複したタスクをディスパッチする可能性があるバグを修正しました [#32814](https://github.com/pingcap/tidb/issues/32814)
    -   クエリ実行時に発生するMPPタスクリストの空エラーを修正する [#31636](https://github.com/pingcap/tidb/issues/31636)
    -   innerWorkerのpanicによって発生したインデックス結合の誤った結果を修正 [#31494](https://github.com/pingcap/tidb/issues/31494)
    -   `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE`ステートメントを実行するとpanicが発生する問題を修正しました [#28078](https://github.com/pingcap/tidb/issues/28078)
    -   `Order By`の最適化による誤ったクエリ結果を修正 [#30271](https://github.com/pingcap/tidb/issues/30271)
    -   `ENUM`型の列で`JOIN`を実行した際に発生する可能性のある誤った結果を修正します [#27831](https://github.com/pingcap/tidb/issues/27831)
    -   `CASE WHEN`データ型で`ENUM`関数を使用した際に発生panicを修正しました [#29357](https://github.com/pingcap/tidb/issues/29357)
    -   ベクトル化された式における`microsecond`関数の誤った結果を修正 [#29244](https://github.com/pingcap/tidb/issues/29244)
    -   ウィンドウ関数がエラーを報告する代わりにTiDBをpanicにする問題を修正しました [#30326](https://github.com/pingcap/tidb/issues/30326)
    -   マージ結合演算子が特定の場合に誤った結果を返す問題を修正しました [#33042](https://github.com/pingcap/tidb/issues/33042)
    -   相関サブクエリが定数を返す場合に TiDB が誤った結果を取得する問題を修正 [#32089](https://github.com/pingcap/tidb/issues/32089)
    -   `ENUM`または`SET`列のエンコーディングが間違っているために TiDB が誤ったデータを書き込む問題を修正しました [#32302](https://github.com/pingcap/tidb/issues/32302)
    -   TiDB で新しい照合順序が有効になっている場合`MAX`または`MIN`関数が`ENUM`または`SET`列に対して誤った結果を返す照合順序を修正します。 [#31638](https://github.com/pingcap/tidb/issues/31638)
    -   IndexHashJoin オペレーターが正常に終了しない問題を修正しました [#31062](https://github.com/pingcap/tidb/issues/31062)
    -   テーブルに仮想列がある場合、TiDBが誤ったデータを読み取る可能性がある問題を修正しました [#30965](https://github.com/pingcap/tidb/issues/30965)
    -   ログレベルの設定がスロークエリログに反映されない問題を修正しました [#30309](https://github.com/pingcap/tidb/issues/30309)
    -   パーティションテーブルが場合によってはインデックスを完全に利用してデータをスキャンできない問題を修正しました [#33966](https://github.com/pingcap/tidb/issues/33966)
    -   TiDBのバックグラウンドHTTPサービスが正常に終了せず、クラスタが異常な状態になる問題を修正しました [#30571](https://github.com/pingcap/tidb/issues/30571)
    -   TiDBが認証失敗のログを予期せず多数出力する可能性がある問題を修正しました [#29709](https://github.com/pingcap/tidb/issues/29709)
    -   システム変数`max_allowed_packet`が有効にならない問題を修正します [#31422](https://github.com/pingcap/tidb/issues/31422)
    -   `REPLACE`ステートメントが自動 ID が範囲外の場合に他の行を誤って変更してしまう問題を修正しました [#29483](https://github.com/pingcap/tidb/issues/29483)
    -   スロークエリログが正常にログを出力できず、メモリを過剰に消費する可能性がある問題を修正しました [#32656](https://github.com/pingcap/tidb/issues/32656)
    -   NATURAL JOINの結果に予期しない列が含まれる可能性がある問題を修正しました [#29481](https://github.com/pingcap/tidb/issues/29481)
    -   `ORDER BY`と`LIMIT`を 1 つのステートメントで一緒に使用すると、プレフィックス列インデックスを使用してデータをクエリする場合に誤った結果が出力される可能性がある問題を修正しました [#29711](https://github.com/pingcap/tidb/issues/29711)
    -   楽観的トランザクションの再試行時に、DOUBLE型のAUTO_INCREMENT列が変更される可能性がある問題を修正しました [#29892](https://github.com/pingcap/tidb/issues/29892)
    -   STR_TO_DATE関数がマイクロ秒部分の先頭のゼロを正しく処理できない問題を修正しました [#30078](https://github.com/pingcap/tidb/issues/30078)
    -   TiFlashがまだ空の範囲のテーブル読み取りをサポートしていないにもかかわらず、TiDBが空の範囲のテーブルをスキャンする際に誤った結果を取得する問題を修正します。 [#33083](https://github.com/pingcap/tidb/issues/33083)

-   TiKV

    -   古いメッセージが原因で TiKV がpanicを起こすバグを修正しました [#12023](https://github.com/tikv/tikv/issues/12023)
    -   メモリメトリックのオーバーフローによって引き起こされる、断続的なパケット損失とメモリ不足（OOM）の問題を修正します [#12160](https://github.com/tikv/tikv/issues/12160)
    -   TiKVがUbuntu 18.04でプロファイリングを実行する際に発生する可能性のあるpanic問題を修正します [#9765](https://github.com/tikv/tikv/issues/9765)
    -   tikv-ctlが誤った文字列マッチングのために誤った結果を返す問題を修正しました [#12329](https://github.com/tikv/tikv/issues/12329)
    -   レプリカ読み取りが線形化可能性に違反する可能性があるバグを修正 [#12109](https://github.com/tikv/tikv/issues/12109)
    -   TiKVが2年以上実行されている場合にpanic可能性があるバグを修正しました [#11940](https://github.com/tikv/tikv/issues/11940)
    -   フロー制御が有効で、 `level0_slowdown_trigger`が明示的に設定されている場合にQPSが低下する問題を修正します [#11424](https://github.com/tikv/tikv/issues/11424)
    -   cgroupコントローラがマウントされていない場合に発生するpanic問題を修正 [#11569](https://github.com/tikv/tikv/issues/11569)
    -   遅延しているリージョンピアでのリージョンマージによって発生する可能性のあるメタデータ破損を修正 [#11526](https://github.com/tikv/tikv/issues/11526)
    -   TiKVの動作停止後に解決済みTSのレイテンシーが増加する問題を修正 [#11351](https://github.com/tikv/tikv/issues/11351)
    -   極端な状況下でリージョンマージ、ConfChange、スナップショットが同時に発生した際に発生するpanic問題を修正します [#11475](https://github.com/tikv/tikv/issues/11475)
    -   tikv-ctlが正しいリージョン関連情報を返せないバグを修正 [#11393](https://github.com/tikv/tikv/issues/11393)
    -   小数除算の結果がゼロの場合に負の符号が発生する問題を修正 [#29586](https://github.com/pingcap/tidb/issues/29586)
    -   悲観的トランザクションモードでプリライト要求を再試行すると、まれにデータ不整合のリスクが発生する可能性がある問題を修正しました [#11187](https://github.com/tikv/tikv/issues/11187)
    -   統計スレッドのデータ監視によって引き起こされるメモリリークを修正 [#11195](https://github.com/tikv/tikv/issues/11195)
    -   TiKVメトリクスにおけるインスタンスごとのgRPCリクエストの平均レイテンシーが不正確である問題を修正しました [#11299](https://github.com/tikv/tikv/issues/11299)
    -   ピアの状態が`Applying`のときにスナップショット ファイルを削除すると発生するpanic問題を修正します [#11746](https://github.com/tikv/tikv/issues/11746)
    -   GCワーカーがビジー状態のときにTiKVがデータ範囲を削除できない（つまり、内部コマンド`unsafe_destroy_range`が実行される）バグを修正しました [#11903](https://github.com/tikv/tikv/issues/11903)
    -   初期化されていないレプリカを削除すると、古いレプリカが再作成される可能性がある問題を修正しました [#10533](https://github.com/tikv/tikv/issues/10533)
    -   TiKVがリバーステーブルスキャンを実行する際にメモリロックを検出できない問題を修正しました [#11440](https://github.com/tikv/tikv/issues/11440)
    -   コルーチンの実行速度が速すぎる場合に時折発生するデッドロック問題を修正します [#11549](https://github.com/tikv/tikv/issues/11549)
    -   ピアを削除するとレイテンシーが高くなる可能性がある問題を修正しました [#10210](https://github.com/tikv/tikv/issues/10210)
    -   TiKVがパニックを起こし、マージ対象のリージョンが無効なためにピアを予期せず破壊してしまう問題を修正しました [#12232](https://github.com/tikv/tikv/issues/12232)
    -   リージョンをマージする際に、初期化されずに破棄されたピアでターゲットピアが置き換えられた場合に発生する TiKV panicの問題を修正します [#12048](https://github.com/tikv/tikv/issues/12048)
    -   スナップショットの適用が中止された際に発生する TiKV panicの問題を修正 [#11618](https://github.com/tikv/tikv/issues/11618)
    -   オペレーターの実行が失敗した場合に、TiKVが送信されるスナップショットの数を正しく計算できないバグを修正しました [#11341](https://github.com/tikv/tikv/issues/11341)

-   PD

    -   リージョンスキャッタラーのスケジューリングで一部のピアが失われる問題を修正しました [#4565](https://github.com/tikv/pd/issues/4565)
    -   コールドホットスポットのデータがホットスポット統計から削除できない問題を修正しました [#4390](https://github.com/tikv/pd/issues/4390)

-   TiFlash

    -   MPPタスクがスレッドを永久にリークする可能性があるバグを修正 [#4238](https://github.com/pingcap/tiflash/issues/4238)
    -   `IN`の結果が複数値式で正しくない問題を修正 [#4016](https://github.com/pingcap/tiflash/issues/4016)
    -   日付フォーマットが`'\n'`無効な区切り文字として認識する問題を修正 [#4036](https://github.com/pingcap/tiflash/issues/4036)
    -   読み取り負荷の高い環境で列を追加した後に発生する可能性のあるクエリエラーを修正する [#3967](https://github.com/pingcap/tiflash/issues/3967)
    -   無効なストレージディレクトリ構成が予期しない動作を引き起こすバグを修正 [#4093](https://github.com/pingcap/tiflash/issues/4093)
    -   一部の例外が正しく処理されないバグを修正 [#4101](https://github.com/pingcap/tiflash/issues/4101)
    -   `STR_TO_DATE()`関数がマイクロ秒を解析する際に先頭のゼロを正しく処理しないバグを修正しました [#3557](https://github.com/pingcap/tiflash/issues/3557)
    -   `INT`を`DECIMAL`にキャストするとオーバーフローが発生する可能性がある問題を修正しました [#3920](https://github.com/pingcap/tiflash/issues/3920)
    -   `DATETIME`を`DECIMAL`にキャストした際に発生する誤った結果を修正します [#4151](https://github.com/pingcap/tiflash/issues/4151)
    -   `FLOAT`を`DECIMAL`にキャストする際に発生するオーバーフローを修正します [#3998](https://github.com/pingcap/tiflash/issues/3998)
    -   TiFlashとTiDBまたはTiKVで`CastStringAsReal`の動作が一貫していない問題を修正します [#3475](https://github.com/pingcap/tiflash/issues/3475)
    -   TiFlashとTiDBまたはTiKVで`CastStringAsDecimal`の動作が一貫していない問題を修正します [#3619](https://github.com/pingcap/tiflash/issues/3619)
    -   TiFlashが再起動後に`EstablishMPPConnection`エラーを返す可能性がある問題を修正しました [#3615](https://github.com/pingcap/tiflash/issues/3615)
    -   TiFlashレプリカ数を0に設定した後、古いデータを回収できない問題を修正しました [#3659](https://github.com/pingcap/tiflash/issues/3659)
    -   主キーが`handle`の場合に主キー列の幅を広げた際に発生する可能性のあるデータ不整合を修正します [#3569](https://github.com/pingcap/tiflash/issues/3569)
    -   SQL文に非常に長いネストされた式が含まれている場合に発生する可能性のある解析エラーを修正する [#3354](https://github.com/pingcap/tiflash/issues/3354)
    -   クエリに`where <string>`句が含まれている場合に発生する可能性のある誤った結果を修正 [#3447](https://github.com/pingcap/tiflash/issues/3447)
    -   `new_collations_enabled_on_first_bootstrap`が有効になっている場合に発生する可能性のある誤った結果を修正[#3388](https://github.com/pingcap/tiflash/issues/3388) 、 [#3391](https://github.com/pingcap/tiflash/issues/3391)
    -   TLSが有効になっているときに発生するpanic問題を修正 [#4196](https://github.com/pingcap/tiflash/issues/4196)
    -   メモリ制限が有効になっているときに発生するpanic問題を修正 [#3902](https://github.com/pingcap/tiflash/issues/3902)
    -   MPPクエリが停止した際にTiFlashが時折クラッシュする問題を修正しました [#3401](https://github.com/pingcap/tiflash/issues/3401)
    -   `Unexpected type of column: Nullable(Nothing)` の予期しないエラーを修正します。 [#3351](https://github.com/pingcap/tiflash/issues/3351)
    -   遅延しているリージョンピアでのリージョンマージによって発生する可能性のあるメタデータ破損を修正 [#4437](https://github.com/pingcap/tiflash/issues/4437)
    -   `JOIN`を含むクエリでエラーが発生した場合にハングアップする可能性がある問題を修正しました [#4195](https://github.com/pingcap/tiflash/issues/4195)
    -   実行プランの誤りにより、MPPクエリで誤った結果が返される可能性がある問題を修正 [#3389](https://github.com/pingcap/tiflash/issues/3389)

-   ツール

    -   Backup & Restore (BR)

        -   BRがRawKVのバックアップに失敗する問題を修正 [#32607](https://github.com/pingcap/tidb/issues/32607)

    -   TiCDC

        -   デフォルト値が複製できない問題を修正 [#3793](https://github.com/pingcap/tiflow/issues/3793)
        -   シーケンスが一部のケースで誤って複製されるバグを修正しました [#4552](https://github.com/pingcap/tiflow/issues/4552)
        -   PDリーダーが強制終了された際にTiCDCノードが異常終了するバグを修正しました [#4248](https://github.com/pingcap/tiflow/issues/4248)
        -   `replace`が無効になっている場合に、MySQLシンクが重複した`batch-replace-enable` SQLステートメントを生成するバグを修正しました [#4501](https://github.com/pingcap/tiflow/issues/4501)
        -   デフォルト列値を出力する際に​​発生するpanicとデータ不整合の問題を修正しました [#3929](https://github.com/pingcap/tiflow/issues/3929)
        -   `mq sink write row`に監視データがない問題を修正 [#3431](https://github.com/pingcap/tiflow/issues/3431)
        -   `min.insync.replicas`が`replication-factor`より小さい場合にレプリケーションが実行できない問題を修正します [#3994](https://github.com/pingcap/tiflow/issues/3994)
        -   レプリケーションタスクが削除された際に発生する可能性のあるpanic問題を修正 [#3128](https://github.com/pingcap/tiflow/issues/3128)
        -   必要なプロセッサ情報が存在しない場合、HTTP APIがパニックを起こすバグを修正しました [#3840](https://github.com/pingcap/tiflow/issues/3840)
        -   不正確なチェックポイントによって引き起こされる可能性のあるデータ損失の問題を修正しました [#3545](https://github.com/pingcap/tiflow/issues/3545)
        -   デッドロックによってレプリケーションタスクが停止する可能性のある問題を修正します [#4055](https://github.com/pingcap/tiflow/issues/4055)
        -   etcdでタスクの状態を手動でクリーンアップした際に発生するTiCDC panic問題を修正 [#2980](https://github.com/pingcap/tiflow/issues/2980)
        -   DDLステートメント内の特殊コメントがレプリケーションタスクの停止を引き起こす問題を修正 [#3755](https://github.com/pingcap/tiflow/issues/3755)
        -   `config.Metadata.Timeout`の設定ミスが原因で発生するレプリケーション停止の問題を修正します [#3352](https://github.com/pingcap/tiflow/issues/3352)
        -   RHEL リリースにおいて、タイムゾーンの問題によりサービスを開始できない問題を修正しました。 [#3584](https://github.com/pingcap/tiflow/issues/3584)
        -   `stopped`の変更フィードがクラスタのアップグレード後に自動的に再開される問題を修正します [#3473](https://github.com/pingcap/tiflow/issues/3473)
        -   MySQLシンクのデッドロックによって発生する、警告が頻繁に発生する問題を修正しました [#2706](https://github.com/pingcap/tiflow/issues/2706)
        -   Canalプロトコルで`enable-old-value`設定項目が`true`に自動的に設定されないバグを修正しました [#3676](https://github.com/pingcap/tiflow/issues/3676)
        -   AvroシンクがJSON型カラムの解析をサポートしていない問題を修正 [#3624](https://github.com/pingcap/tiflow/issues/3624)
        -   changefeedチェックポイントの遅延における負の値エラーを修正 [#3010](https://github.com/pingcap/tiflow/issues/3010)
        -   コンテナ環境におけるOOM問題を修正 [#1798](https://github.com/pingcap/tiflow/issues/1798)
        -   DDL処理後のメモリリーク問題を修正 [#3174](https://github.com/pingcap/tiflow/issues/3174)
        -   テーブルが同じノードで繰り返しスケジュールされると、changefeedが停止する問題を修正します [#4464](https://github.com/pingcap/tiflow/issues/4464)
        -   PDノードが異常な場合に、オープンAPI経由でステータスを照会するとブロックされる可能性があるバグを修正しました [#4778](https://github.com/pingcap/tiflow/issues/4778)
        -   所有者変更によって発生した不正確なメトリクスを修正 [#4774](https://github.com/pingcap/tiflow/issues/4774)
        -   Unified Sorterで使用されるワーカープールの安定性の問題を修正しました [#4447](https://github.com/pingcap/tiflow/issues/4447)
        -   `cached region`モニタリングメトリックが負の値になる問題を修正しました [#4300](https://github.com/pingcap/tiflow/issues/4300)

    -   TiDB Lightning

        -   TiDB Lightningが`mysql.tidb`テーブルにアクセスする権限を持たない場合に発生する、インポート結果の誤りに関する問題を修正しました [#31088](https://github.com/pingcap/tidb/issues/31088)
        -   チェックサムエラー「GCの有効期間がトランザクション期間より短い」を修正 [#32733](https://github.com/pingcap/tidb/issues/32733)
        -   TiDB Lightningが、一部のインポートタスクにソースファイルが含まれていない場合にメタデータスキーマを削除しない可能性があるバグを修正しました [#28144](https://github.com/pingcap/tidb/issues/28144)
        -   S3ストレージパスが存在しない場合にTiDB Lightningがエラーを報告しない問題を修正[#28031](https://github.com/pingcap/tidb/issues/28031) [#30709](https://github.com/pingcap/tidb/issues/30709)
        -   GCSで1000個以上のキーを反復処理する際に発生するエラーを修正しました [#30377](https://github.com/pingcap/tidb/issues/30377)
