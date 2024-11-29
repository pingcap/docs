---
title: TiDB 5.2.4 Release Notes
category: Releases
summary: TiDB 5.2.4 の新機能、互換性の変更、改善、バグ修正について説明します。
---

# TiDB 5.2.4 リリースノート {#tidb-5-2-4-release-notes}

リリース日：2022年4月26日

TiDB バージョン: 5.2.4

## 互換性の変更 {#compatibility-change-s}

-   ティビ

    -   システム変数[`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510)のデフォルト値を`2`から`1` [＃31748](https://github.com/pingcap/tidb/issues/31748)に変更します

-   ティクヴ

    -   不要なRaftログを圧縮するための時間間隔を制御するには[`raft-log-compact-sync-interval`](https://docs.pingcap.com/tidb/v5.2/tikv-configuration-file#raft-log-compact-sync-interval-new-in-v524)を追加します[＃11404](https://github.com/tikv/tikv/issues/11404)デフォルトでは`"2s"` )。
    -   デフォルト値[`raft-log-gc-tick-interval`](/tikv-configuration-file.md#raft-log-gc-tick-interval)を`"10s"`から`"3s"` [＃11404](https://github.com/tikv/tikv/issues/11404)に変更します
    -   [`storage.flow-control.enable`](/tikv-configuration-file.md#enable) `true`に設定すると、 [`storage.flow-control.hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit)の値が[`rocksdb.(defaultcf|writecf|lockcf).hard-pending-compaction-bytes-limit`](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit-1)の値を上書きします[＃11424](https://github.com/tikv/tikv/issues/11424)

-   ツール

    -   TiDB Lightning

        -   データのインポート後に空の領域が多すぎるのを避けるため、デフォルト値`regionMaxKeyCount`を 1_440_000 から 1_280_000 に変更します[#30018](https://github.com/pingcap/tidb/issues/30018)

## 改善点 {#improvements}

-   ティクヴ

    -   レイテンシージッターを減らすためにリーダーシップをCDCオブザーバーに移譲する[＃12111](https://github.com/tikv/tikv/issues/12111)
    -   解決ロックを必要とする領域の数を減らすことで、TiCDC の回復時間を短縮します (手順[＃11993](https://github.com/tikv/tikv/issues/11993)
    -   procファイルシステム（procfs）をv0.12.0 [＃11702](https://github.com/tikv/tikv/issues/11702)に更新する
    -   Raftログ[＃11404](https://github.com/tikv/tikv/issues/11404)へのガベージ コレクション (GC) を実行するときに書き込みバッチ サイズを増やすことで、GC プロセスを高速化します。
    -   検証プロセスを`Apply`スレッドプール[＃11239](https://github.com/tikv/tikv/issues/11239)から`Import`スレッドプールに移動することで、SSTファイルの挿入速度が向上します。

-   ツール

    -   ティCDC

        -   TiCDC がメッセージを Kafka パーティション間でより均等に分散するように、Kafka シンクのデフォルト値を`partition-num`から 3 に変更します[＃3337](https://github.com/pingcap/tiflow/issues/3337)
        -   TiKVストアがダウンしたときにKVクライアントが回復するまでの時間を短縮する[＃3191](https://github.com/pingcap/tiflow/issues/3191)
        -   Grafana [＃4891](https://github.com/pingcap/tiflow/issues/4891)に`Lag analyze`パネルを追加する
        -   Kafka プロデューサーの設定パラメータを公開して、TiCDC [＃4385](https://github.com/pingcap/tiflow/issues/4385)で設定できるようにします。
        -   チェンジフィードを再開するための指数バックオフメカニズムを追加する[＃3329](https://github.com/pingcap/tiflow/issues/3329)
        -   「EventFeed 再試行レート制限」ログの数を減らす[＃4006](https://github.com/pingcap/tiflow/issues/4006)
        -   デフォルト値`max-message-bytes`を10M [＃4041](https://github.com/pingcap/tiflow/issues/4041)に設定する
        -   `no owner alert` `table sink total row`含むPrometheusと[＃4054](https://github.com/pingcap/tiflow/issues/4054) `mounter row`監視`buffer sink total row`とアラートを追加します[＃1606](https://github.com/pingcap/tiflow/issues/1606)
        -   Grafanaダッシュボードで複数のKubernetesクラスターをサポート[＃4665](https://github.com/pingcap/tiflow/issues/4665)
        -   `changefeed checkpoint`監視指標[＃5232](https://github.com/pingcap/tiflow/issues/5232)にキャッチアップ ETA (到着予定時刻) を追加する

## バグ修正 {#bug-fixes}

-   ティビ

    -   列挙値[＃32428](https://github.com/pingcap/tidb/issues/32428)の Nulleq 関数の誤った範囲計算結果を修正
    -   INDEX HASH JOINが`send on closed channel`エラーを返す問題を修正しました[＃31129](https://github.com/pingcap/tidb/issues/31129)
    -   同時列型変更によりスキーマとデータの間に不整合が発生する問題を修正[＃31048](https://github.com/pingcap/tidb/issues/31048)
    -   楽観的トランザクションモード[＃30410](https://github.com/pingcap/tidb/issues/30410)でデータインデックスの不整合が発生する可能性がある問題を修正
    -   JSON 型の列が`CHAR`型の列[＃29401](https://github.com/pingcap/tidb/issues/29401)に結合すると SQL 操作がキャンセルされる問題を修正しました。
    -   トランザクションを使用する場合と使用しない場合でウィンドウ関数が異なる結果を返す可能性がある問題を修正しました[＃29947](https://github.com/pingcap/tidb/issues/29947)
    -   SQL文に自然結合[＃25041](https://github.com/pingcap/tidb/issues/25041)含まれている場合に`Column 'col_name' in field list is ambiguous`エラーが予期せず報告される問題を修正
    -   `Decimal`から`String` [＃29417](https://github.com/pingcap/tidb/issues/29417)へのキャスト時に長さ情報が間違っている問題を修正
    -   `GREATEST`関数が`tidb_enable_vectorized_expression`の値が異なるために矛盾した結果を返す問題を修正 ( `on`または`off`に設定) [＃29434](https://github.com/pingcap/tidb/issues/29434)
    -   `left join` [＃31321](https://github.com/pingcap/tidb/issues/31321)を使用して複数のテーブルのデータを削除した場合の誤った結果を修正
    -   TiDB がTiFlash [＃32814](https://github.com/pingcap/tidb/issues/32814)に重複したタスクをディスパッチする可能性があるバグを修正
    -   クエリ[＃31636](https://github.com/pingcap/tidb/issues/31636)を実行するときに MPP タスク リストが空になるエラーを修正
    -   innerWorkerpanicによって発生するインデックス結合の誤った結果を修正[＃31494](https://github.com/pingcap/tidb/issues/31494)
    -   `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE`文を実行するとpanic[＃28078](https://github.com/pingcap/tidb/issues/28078)が発生する問題を修正
    -   `Order By` [＃30271](https://github.com/pingcap/tidb/issues/30271)の最適化による誤ったクエリ結果を修正
    -   `ENUM`種類の列[＃27831](https://github.com/pingcap/tidb/issues/27831)に対して`JOIN`実行したときに発生する可能性のある誤った結果を修正します。
    -   `ENUM`データ型[＃29357](https://github.com/pingcap/tidb/issues/29357)で`CASE WHEN`関数を使用するときに発生するpanicを修正
    -   ベクトル化された式[＃29244](https://github.com/pingcap/tidb/issues/29244)の関数`microsecond`の誤った結果を修正
    -   ウィンドウ関数がエラーを報告する代わりに TiDB をpanicせる問題を修正[＃30326](https://github.com/pingcap/tidb/issues/30326)
    -   特定のケースで Merge Join 演算子が間違った結果を返す問題を修正[＃33042](https://github.com/pingcap/tidb/issues/33042)
    -   相関サブクエリが定数[＃32089](https://github.com/pingcap/tidb/issues/32089)返すときに TiDB が誤った結果を取得する問題を修正しました。
    -   `ENUM`列目または`SET`列目のエンコードが間違っているためにTiDBが間違ったデータを書き込む問題を修正しました[＃32302](https://github.com/pingcap/tidb/issues/32302)
    -   TiDB [＃31638](https://github.com/pingcap/tidb/issues/31638)で新しい照合順序が有効になっているときに、 `ENUM`または`SET`列の`MAX`または`MIN`関数が間違った結果を返す問題を修正しました。
    -   IndexHashJoin演算子が正常に終了しない問題を修正[＃31062](https://github.com/pingcap/tidb/issues/31062)
    -   テーブルに仮想列[＃30965](https://github.com/pingcap/tidb/issues/30965)がある場合に TiDB が誤ったデータを読み取る可能性がある問題を修正しました。
    -   スロークエリログ[#30309](https://github.com/pingcap/tidb/issues/30309)にログレベルの設定が反映されない問題を修正
    -   パーティションテーブルがインデックスを完全に使用してデータをスキャンできない場合がある問題を修正[＃33966](https://github.com/pingcap/tidb/issues/33966)
    -   TiDB のバックグラウンド HTTP サービスが正常に終了せず、クラスターが異常な状態になる問題を修正しました[＃30571](https://github.com/pingcap/tidb/issues/30571)
    -   TiDB が予期せず認証失敗のログを多数出力する可能性がある問題を修正[＃29709](https://github.com/pingcap/tidb/issues/29709)
    -   システム変数`max_allowed_packet`が有効にならない問題を修正[＃31422](https://github.com/pingcap/tidb/issues/31422)
    -   自動IDが範囲外の場合に`REPLACE`文が他の行を誤って変更する問題を修正[＃29483](https://github.com/pingcap/tidb/issues/29483)
    -   スロークエリログが正常にログを出力できず、メモリを過剰に消費する可能性がある問題を修正[＃32656](https://github.com/pingcap/tidb/issues/32656)
    -   NATURAL JOINの結果に予期しない列が含まれる可能性がある問題を修正[＃29481](https://github.com/pingcap/tidb/issues/29481)
    -   プレフィックス列インデックスを使用してデータ[＃29711](https://github.com/pingcap/tidb/issues/29711)をクエリする場合、 `ORDER BY`と`LIMIT` 1 つのステートメントで一緒に使用すると間違った結果が出力される可能性がある問題を修正しました。
    -   楽観的トランザクションの再試行時にDOUBLE型の自動インクリメント列が変更される可能性がある問題を修正[＃29892](https://github.com/pingcap/tidb/issues/29892)
    -   STR_TO_DATE関数がマイクロ秒部分の先頭のゼロを正しく処理できない問題を修正[＃30078](https://github.com/pingcap/tidb/issues/30078)
    -   TiFlash が空の範囲を持つテーブルの読み取りをまだサポートしていないにもかかわらず、 TiFlashを使用して空の範囲を持つテーブルをスキャンすると、TiDB が間違った結果を取得する問題を修正しました[＃33083](https://github.com/pingcap/tidb/issues/33083)

-   ティクヴ

    -   古いメッセージにより TiKV がpanicを起こすバグを修正[＃12023](https://github.com/tikv/tikv/issues/12023)
    -   メモリメトリックのオーバーフローによって発生する断続的なパケット損失とメモリ不足 (OOM) の問題を修正しました[＃12160](https://github.com/tikv/tikv/issues/12160)
    -   Ubuntu 18.04 [＃9765](https://github.com/tikv/tikv/issues/9765)でTiKVがプロファイリングを実行するときに発生する潜在的なpanic問題を修正
    -   tikv-ctl が間違った文字列一致のために誤った結果を返す問題を修正[＃12329](https://github.com/tikv/tikv/issues/12329)
    -   レプリカ読み取りが線形化可能性[＃12109](https://github.com/tikv/tikv/issues/12109)に違反する可能性があるバグを修正
    -   TiKV が 2 年以上実行されている場合にpanicする可能性があるバグを修正[＃11940](https://github.com/tikv/tikv/issues/11940)
    -   フロー制御が有効で、 `level0_slowdown_trigger`明示的に設定されている場合に QPS が低下する問題を修正[＃11424](https://github.com/tikv/tikv/issues/11424)
    -   cgroup コントローラがマウントされていない場合に発生するpanic問題を修正[＃11569](https://github.com/tikv/tikv/issues/11569)
    -   遅延リージョンピア[＃11526](https://github.com/tikv/tikv/issues/11526)でのリージョンマージによって発生する可能性のあるメタデータ破損を修正
    -   TiKVの動作が停止した後にResolved TSのレイテンシーが増加する問題を修正[＃11351](https://github.com/tikv/tikv/issues/11351)
    -   極端な状況でリージョンのマージ、ConfChange、スナップショットが同時に発生した場合に発生するpanicの問題を修正[＃11475](https://github.com/tikv/tikv/issues/11475)
    -   tikv-ctl が正しい地域関連情報を返すことができないバグを修正[＃11393](https://github.com/tikv/tikv/issues/11393)
    -   小数点以下の除算結果がゼロの場合の負の符号の問題を修正[＃29586](https://github.com/pingcap/tidb/issues/29586)
    -   悲観的トランザクションモードで事前書き込み要求を再試行すると、まれにデータの不整合が発生するリスクがある問題を修正しました[＃11187](https://github.com/tikv/tikv/issues/11187)
    -   統計スレッド[＃11195](https://github.com/tikv/tikv/issues/11195)のデータの監視によって発生するメモリリークを修正
    -   TiKV メトリック[＃11299](https://github.com/tikv/tikv/issues/11299)でインスタンスごとの gRPC リクエストの平均レイテンシーが不正確になる問題を修正
    -   ピアステータスが`Applying` [＃11746](https://github.com/tikv/tikv/issues/11746)ときにスナップショットファイルを削除すると発生するpanic問題を修正しました。
    -   GCワーカーがビジー状態のときにTiKVがデータの範囲を削除できない（つまり内部コマンド`unsafe_destroy_range`が実行される）バグを修正[＃11903](https://github.com/tikv/tikv/issues/11903)
    -   初期化されていないレプリカを削除すると古いレプリカが再作成される可能性がある問題を修正[＃10533](https://github.com/tikv/tikv/issues/10533)
    -   TiKVが逆テーブルスキャンを実行するときにメモリロックを検出できない問題を修正[＃11440](https://github.com/tikv/tikv/issues/11440)
    -   コルーチンの実行速度が速すぎる場合に時々発生するデッドロックの問題を修正[＃11549](https://github.com/tikv/tikv/issues/11549)
    -   ピアを破棄するとレイテンシーが大きくなる可能性がある問題を修正[＃10210](https://github.com/tikv/tikv/issues/10210)
    -   マージ対象のリージョンが無効であるため、TiKV がパニックを起こしてピアを予期せず破棄する問題を修正[＃12232](https://github.com/tikv/tikv/issues/12232)
    -   リージョン[＃12048](https://github.com/tikv/tikv/issues/12048)をマージする際に、ターゲットピアが初期化されずに破棄されたピアに置き換えられたときに発生するTiKVpanicの問題を修正しました。
    -   スナップショットの適用が中止されたときに発生する TiKVpanicの問題を修正[＃11618](https://github.com/tikv/tikv/issues/11618)
    -   オペレータの実行が失敗したときに、TiKV が送信されるスナップショットの数を正しく計算できないバグを修正[＃11341](https://github.com/tikv/tikv/issues/11341)

-   PD

    -   リージョンスキャッタラーのスケジューリングで一部のピアが失われる問題を修正[＃4565](https://github.com/tikv/pd/issues/4565)
    -   ホットスポット統計からコールドホットスポットデータを削除できない問題を修正[＃4390](https://github.com/tikv/pd/issues/4390)

-   TiFlash

    -   MPP タスクがスレッドを永久にリークする可能性があるバグを修正[＃4238](https://github.com/pingcap/tiflash/issues/4238)
    -   複数値式[＃4016](https://github.com/pingcap/tiflash/issues/4016)で`IN`の結果が正しくない問題を修正
    -   日付の形式で`'\n'`無効な区切り文字として認識される問題を修正[＃4036](https://github.com/pingcap/tiflash/issues/4036)
    -   読み取り負荷が高い状態で列を追加した後に発生する可能性のあるクエリエラーを修正[＃3967](https://github.com/pingcap/tiflash/issues/3967)
    -   無効なstorageディレクトリ構成が予期しない動作を引き起こすバグを修正[＃4093](https://github.com/pingcap/tiflash/issues/4093)
    -   一部の例外が適切に処理されないバグを修正[＃4101](https://github.com/pingcap/tiflash/issues/4101)
    -   `STR_TO_DATE()`関数がマイクロ秒を解析するときに先頭のゼロを誤って処理するバグを修正[＃3557](https://github.com/pingcap/tiflash/issues/3557)
    -   `INT` `DECIMAL`にキャストするとオーバーフロー[＃3920](https://github.com/pingcap/tiflash/issues/3920)が発生する可能性がある問題を修正
    -   `DATETIME` `DECIMAL` [＃4151](https://github.com/pingcap/tiflash/issues/4151)にキャストするときに発生する誤った結果を修正
    -   `FLOAT` `DECIMAL` [＃3998](https://github.com/pingcap/tiflash/issues/3998)にキャストするときに発生するオーバーフローを修正
    -   `CastStringAsReal`動作がTiFlashと TiDB または TiKV [＃3475](https://github.com/pingcap/tiflash/issues/3475)で一致しない問題を修正
    -   `CastStringAsDecimal`動作がTiFlashと TiDB または TiKV [＃3619](https://github.com/pingcap/tiflash/issues/3619)で一致しない問題を修正
    -   TiFlashが再起動後に`EstablishMPPConnection`エラーを返す可能性がある問題を修正しました[＃3615](https://github.com/pingcap/tiflash/issues/3615)
    -   TiFlashレプリカの数を0 [＃3659](https://github.com/pingcap/tiflash/issues/3659)に設定した後、古いデータを再利用できない問題を修正
    -   主キーが`handle` [＃3569](https://github.com/pingcap/tiflash/issues/3569)のときに主キー列を拡張すると、データの不整合が発生する可能性がある問題を修正しました。
    -   SQL 文に非常に長いネストされた式が含まれている場合に発生する可能性のある解析エラーを修正[＃3354](https://github.com/pingcap/tiflash/issues/3354)
    -   クエリに`where <string>`句[＃3447](https://github.com/pingcap/tiflash/issues/3447)含まれている場合に発生する可能性のある誤った結果を修正
    -   `new_collations_enabled_on_first_bootstrap`が有効になっている場合に誤った結果が発生する可能性を修正[＃3388](https://github.com/pingcap/tiflash/issues/3388) 、 [＃3391](https://github.com/pingcap/tiflash/issues/3391)
    -   TLS が有効になっているときに発生するpanic問題を修正[＃4196](https://github.com/pingcap/tiflash/issues/4196)
    -   メモリ制限が有効になっているときに発生するpanic問題を修正[＃3902](https://github.com/pingcap/tiflash/issues/3902)
    -   MPPクエリが停止したときにTiFlashが時々クラッシュする問題を修正[＃3401](https://github.com/pingcap/tiflash/issues/3401)
    -   `Unexpected type of column: Nullable(Nothing)` [＃3351](https://github.com/pingcap/tiflash/issues/3351)の予期しないエラーを修正
    -   遅延リージョンピア[＃4437](https://github.com/pingcap/tiflash/issues/4437)でのリージョンマージによって発生する可能性のあるメタデータ破損を修正
    -   エラーが発生した場合に`JOIN`含むクエリがハングする可能性がある問題を修正しました[＃4195](https://github.com/pingcap/tiflash/issues/4195)
    -   実行プランが正しくないために MPP クエリで返される可能性のある誤った結果を修正[＃3389](https://github.com/pingcap/tiflash/issues/3389)

-   ツール

    -   バックアップと復元 (BR)

        -   BRがRawKV [＃32607](https://github.com/pingcap/tidb/issues/32607)バックアップに失敗する問題を修正

    -   ティCDC

        -   デフォルト値を複製できない問題を修正[＃3793](https://github.com/pingcap/tiflow/issues/3793)
        -   一部のケースでシーケンスが誤って複製されるバグを修正[＃4552](https://github.com/pingcap/tiflow/issues/4552)
        -   PDリーダーが強制終了するとTiCDCノードが異常終了するバグを修正[＃4248](https://github.com/pingcap/tiflow/issues/4248)
        -   `batch-replace-enable`が無効になっている場合に MySQL シンクが重複した`replace` SQL 文を生成するバグを修正[＃4501](https://github.com/pingcap/tiflow/issues/4501)
        -   デフォルトの列値[＃3929](https://github.com/pingcap/tiflow/issues/3929)を出力するときに発生するpanicとデータの不整合の問題を修正
        -   `mq sink write row`に監視データがない問題を修正[＃3431](https://github.com/pingcap/tiflow/issues/3431)
        -   `min.insync.replicas`が`replication-factor`より小さい場合にレプリケーションを実行できない問題を修正しました[＃3994](https://github.com/pingcap/tiflow/issues/3994)
        -   レプリケーションタスクが削除されたときに発生する可能性のあるpanic問題を修正[＃3128](https://github.com/pingcap/tiflow/issues/3128)
        -   必要なプロセッサ情報が存在しない場合にHTTP APIがパニックになるバグを修正[＃3840](https://github.com/pingcap/tiflow/issues/3840)
        -   不正確なチェックポイント[＃3545](https://github.com/pingcap/tiflow/issues/3545)によって発生する潜在的なデータ損失の問題を修正
        -   デッドロックによりレプリケーションタスクが停止する可能性がある問題を修正[＃4055](https://github.com/pingcap/tiflow/issues/4055)
        -   etcd [＃2980](https://github.com/pingcap/tiflow/issues/2980)でタスク ステータスを手動でクリーンアップするときに発生する TiCDCpanicの問題を修正しました。
        -   DDL ステートメント内の特別なコメントによってレプリケーション タスクが停止する問題を修正[＃3755](https://github.com/pingcap/tiflow/issues/3755)
        -   `config.Metadata.Timeout` [＃3352](https://github.com/pingcap/tiflow/issues/3352)の誤った構成によって発生するレプリケーション停止の問題を修正
        -   RHELリリース[＃3584](https://github.com/pingcap/tiflow/issues/3584)のタイムゾーンの問題によりサービスを開始できない問題を修正
        -   クラスターのアップグレード後に`stopped`チェンジフィードが自動的に再開される問題を修正[＃3473](https://github.com/pingcap/tiflow/issues/3473)
        -   MySQLシンクデッドロック[＃2706](https://github.com/pingcap/tiflow/issues/2706)による警告が頻繁に発生する問題を修正
        -   Canalプロトコル[＃3676](https://github.com/pingcap/tiflow/issues/3676)で設定項目`enable-old-value`が`true`に自動的に設定されないバグを修正
        -   AvroシンクがJSON型列[＃3624](https://github.com/pingcap/tiflow/issues/3624)の解析をサポートしていない問題を修正
        -   チェンジフィードチェックポイントラグ[＃3010](https://github.com/pingcap/tiflow/issues/3010)の負の値エラーを修正
        -   コンテナ環境のOOM問題を修正[＃1798](https://github.com/pingcap/tiflow/issues/1798)
        -   DDL [＃3174](https://github.com/pingcap/tiflow/issues/3174)の処理後のメモリリークの問題を修正
        -   同じノード[＃4464](https://github.com/pingcap/tiflow/issues/4464)でテーブルが繰り返しスケジュールされると、changefeed が停止する問題を修正しました。
        -   PDノードが異常な場合にオープンAPI経由でステータスを照会するとブロックされることがあるバグを修正[＃4778](https://github.com/pingcap/tiflow/issues/4778)
        -   所有者の変更によって生じた誤ったメトリックを修正[＃4774](https://github.com/pingcap/tiflow/issues/4774)
        -   Unified Sorter [＃4447](https://github.com/pingcap/tiflow/issues/4447)で使用されるワーカープールの安定性の問題を修正
        -   `cached region`監視メトリックが負の[＃4300](https://github.com/pingcap/tiflow/issues/4300)になる問題を修正

    -   TiDB Lightning

        -   TiDB Lightningに`mysql.tidb`テーブル[＃31088](https://github.com/pingcap/tidb/issues/31088)にアクセスする権限がない場合に発生する誤ったインポート結果の問題を修正しました。
        -   チェックサムエラー「GC の存続期間がトランザクション期間より短い」を修正[＃32733](https://github.com/pingcap/tidb/issues/32733)
        -   一部のインポートタスクにソースファイルが含まれていない場合に、 TiDB Lightning がメタデータスキーマを削除しない可能性があるバグを修正しました[＃28144](https://github.com/pingcap/tidb/issues/28144)
        -   S3storageパスが存在しない場合にTiDB Lightning がエラーを報告しない問題を修正[＃28031](https://github.com/pingcap/tidb/issues/28031) [＃30709](https://github.com/pingcap/tidb/issues/30709)
        -   GCS [＃30377](https://github.com/pingcap/tidb/issues/30377)で 1000 個を超えるキーを反復処理するときに発生するエラーを修正
