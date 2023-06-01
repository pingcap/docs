---
title: TiDB 5.2.4 Release Notes
category: Releases
---

# TiDB 5.2.4 リリースノート {#tidb-5-2-4-release-notes}

リリース日：2022年4月26日

TiDB バージョン: 5.2.4

## 互換性の変更 {#compatibility-change-s}

-   TiDB

    -   システム変数[<a href="/system-variables.md#tidb_analyze_version-new-in-v510">`tidb_analyze_version`</a>](/system-variables.md#tidb_analyze_version-new-in-v510)のデフォルト値を`2`から`1`に変更します[<a href="https://github.com/pingcap/tidb/issues/31748">#31748</a>](https://github.com/pingcap/tidb/issues/31748)

-   TiKV

    -   不要なRaftログを圧縮するための時間間隔 (デフォルトでは`"2s"` ) を制御するには[<a href="https://docs.pingcap.com/tidb/v5.2/tikv-configuration-file#raft-log-compact-sync-interval-new-in-v524">`raft-log-compact-sync-interval`</a>](https://docs.pingcap.com/tidb/v5.2/tikv-configuration-file#raft-log-compact-sync-interval-new-in-v524)を追加します[<a href="https://github.com/tikv/tikv/issues/11404">#11404</a>](https://github.com/tikv/tikv/issues/11404)
    -   デフォルト値の[<a href="/tikv-configuration-file.md#raft-log-gc-tick-interval">`raft-log-gc-tick-interval`</a>](/tikv-configuration-file.md#raft-log-gc-tick-interval)を`"10s"`から`"3s"`に変更します[<a href="https://github.com/tikv/tikv/issues/11404">#11404</a>](https://github.com/tikv/tikv/issues/11404)
    -   [<a href="/tikv-configuration-file.md#enable">`storage.flow-control.enable`</a>](/tikv-configuration-file.md#enable)を`true`に設定すると、 [<a href="/tikv-configuration-file.md#hard-pending-compaction-bytes-limit">`storage.flow-control.hard-pending-compaction-bytes-limit`</a>](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit)の値が[<a href="/tikv-configuration-file.md#hard-pending-compaction-bytes-limit-1">`rocksdb.(defaultcf|writecf|lockcf).hard-pending-compaction-bytes-limit`</a>](/tikv-configuration-file.md#hard-pending-compaction-bytes-limit-1) [<a href="https://github.com/tikv/tikv/issues/11424">#11424</a>](https://github.com/tikv/tikv/issues/11424)の値を上書きします。

-   ツール

    -   TiDB Lightning

        -   データ インポート[<a href="https://github.com/pingcap/tidb/issues/30018">#30018</a>](https://github.com/pingcap/tidb/issues/30018)後に空のリージョンが多すぎるのを避けるために、デフォルト値`regionMaxKeyCount`を 1_440_000 から 1_280_000 に変更します。

## 改善点 {#improvements}

-   TiKV

    -   リーダーシップを CDC オブザーバーに移管して、レイテンシージッター[<a href="https://github.com/tikv/tikv/issues/12111">#12111</a>](https://github.com/tikv/tikv/issues/12111)を削減します。
    -   ロックの解決ステップ[<a href="https://github.com/tikv/tikv/issues/11993">#11993</a>](https://github.com/tikv/tikv/issues/11993)を必要とするリージョンの数を減らすことで、TiCDC の回復時間を短縮します。
    -   proc ファイルシステム (procfs) を v0.12.0 に更新します[<a href="https://github.com/tikv/tikv/issues/11702">#11702</a>](https://github.com/tikv/tikv/issues/11702)
    -   Raftログへの GC を実行するときに書き込みバッチ サイズを増やすことで、ガベージ コレクション (GC) プロセスを高速化します[<a href="https://github.com/tikv/tikv/issues/11404">#11404</a>](https://github.com/tikv/tikv/issues/11404)
    -   検証プロセスを`Apply`スレッド プール[<a href="https://github.com/tikv/tikv/issues/11239">#11239</a>](https://github.com/tikv/tikv/issues/11239)から`Import`スレッド プールに移動することで、SST ファイルの挿入速度が向上しました。

-   ツール

    -   TiCDC

        -   TiCDC が Kafka パーティション間でメッセージをより均等に分散できるように、Kafka Sink のデフォルト値`partition-num`を[<a href="https://github.com/pingcap/tiflow/issues/3337">#3337</a>](https://github.com/pingcap/tiflow/issues/3337)に変更します。
        -   TiKV ストアがダウンした場合に KV クライアントが回復するまでの時間を短縮します[<a href="https://github.com/pingcap/tiflow/issues/3191">#3191</a>](https://github.com/pingcap/tiflow/issues/3191)
        -   Grafana [<a href="https://github.com/pingcap/tiflow/issues/4891">#4891</a>](https://github.com/pingcap/tiflow/issues/4891)に`Lag analyze`パネルを追加する
        -   Kafka プロデューサの構成パラメータを公開して、TiCDC [<a href="https://github.com/pingcap/tiflow/issues/4385">#4385</a>](https://github.com/pingcap/tiflow/issues/4385)で構成できるようにします。
        -   変更フィードを再開するための指数バックオフ メカニズムを追加します[<a href="https://github.com/pingcap/tiflow/issues/3329">#3329</a>](https://github.com/pingcap/tiflow/issues/3329)
        -   「EventFeed 再試行速度制限」ログの数を減らす[<a href="https://github.com/pingcap/tiflow/issues/4006">#4006</a>](https://github.com/pingcap/tiflow/issues/4006)
        -   デフォルト値の`max-message-bytes`を 10M [<a href="https://github.com/pingcap/tiflow/issues/4041">#4041</a>](https://github.com/pingcap/tiflow/issues/4041)に設定します。
        -   `no owner alert` 、 `mounter row` 、 `table sink total row` 、 `buffer sink total row`などの Prometheus および Grafana モニタリング メトリックとアラートを追加します[<a href="https://github.com/pingcap/tiflow/issues/4054">#4054</a>](https://github.com/pingcap/tiflow/issues/4054) [<a href="https://github.com/pingcap/tiflow/issues/1606">#1606</a>](https://github.com/pingcap/tiflow/issues/1606)
        -   Grafana ダッシュボードで複数の Kubernetes クラスターをサポート[<a href="https://github.com/pingcap/tiflow/issues/4665">#4665</a>](https://github.com/pingcap/tiflow/issues/4665)
        -   キャッチアップ ETA (到着予定時刻) を`changefeed checkpoint`モニタリング指標に追加します[<a href="https://github.com/pingcap/tiflow/issues/5232">#5232</a>](https://github.com/pingcap/tiflow/issues/5232)

## バグの修正 {#bug-fixes}

-   TiDB

    -   Enum 値[<a href="https://github.com/pingcap/tidb/issues/32428">#32428</a>](https://github.com/pingcap/tidb/issues/32428)に対する Nulleq 関数の間違った範囲計算結果を修正しました。
    -   INDEX HASH JOIN が`send on closed channel`エラー[<a href="https://github.com/pingcap/tidb/issues/31129">#31129</a>](https://github.com/pingcap/tidb/issues/31129)を返す問題を修正
    -   同時に列の型を変更すると、スキーマとデータの間で不整合が発生する問題を修正します[<a href="https://github.com/pingcap/tidb/issues/31048">#31048</a>](https://github.com/pingcap/tidb/issues/31048)
    -   楽観的トランザクション モード[<a href="https://github.com/pingcap/tidb/issues/30410">#30410</a>](https://github.com/pingcap/tidb/issues/30410)での潜在的なデータ インデックスの不一致の問題を修正します。
    -   JSON 型の列が`CHAR`型の列[<a href="https://github.com/pingcap/tidb/issues/29401">#29401</a>](https://github.com/pingcap/tidb/issues/29401)に結合すると SQL 操作がキャンセルされる問題を修正
    -   トランザクションを使用する場合と使用しない場合に、ウィンドウ関数が異なる結果を返す可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/29947">#29947</a>](https://github.com/pingcap/tidb/issues/29947)
    -   SQL ステートメントに自然結合[<a href="https://github.com/pingcap/tidb/issues/25041">#25041</a>](https://github.com/pingcap/tidb/issues/25041)が含まれる場合、予期せず`Column 'col_name' in field list is ambiguous`エラーが報告される問題を修正します。
    -   `Decimal` ～ `String` [<a href="https://github.com/pingcap/tidb/issues/29417">#29417</a>](https://github.com/pingcap/tidb/issues/29417)をキャストする際に長さ情報が間違っている問題を修正
    -   `tidb_enable_vectorized_expression`の値が異なるために`GREATEST`関数が一貫性のない結果を返す問題を修正します ( `on`または`off`に設定) [<a href="https://github.com/pingcap/tidb/issues/29434">#29434</a>](https://github.com/pingcap/tidb/issues/29434)
    -   `left join` [<a href="https://github.com/pingcap/tidb/issues/31321">#31321</a>](https://github.com/pingcap/tidb/issues/31321)を使用して複数のテーブルのデータを削除した場合の誤った結果を修正
    -   TiDB が重複したタスクをTiFlash [<a href="https://github.com/pingcap/tidb/issues/32814">#32814</a>](https://github.com/pingcap/tidb/issues/32814)にディスパッチする可能性があるバグを修正
    -   クエリ[<a href="https://github.com/pingcap/tidb/issues/31636">#31636</a>](https://github.com/pingcap/tidb/issues/31636)を実行するときの MPP タスク リストが空のエラーを修正しました。
    -   innerWorkerpanic[<a href="https://github.com/pingcap/tidb/issues/31494">#31494</a>](https://github.com/pingcap/tidb/issues/31494)によって引き起こされるインデックス結合の間違った結果を修正します。
    -   `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE`ステートメントを実行するとpanic[<a href="https://github.com/pingcap/tidb/issues/28078">#28078</a>](https://github.com/pingcap/tidb/issues/28078)が発生する問題を修正
    -   `Order By` [<a href="https://github.com/pingcap/tidb/issues/30271">#30271</a>](https://github.com/pingcap/tidb/issues/30271)の最適化による間違ったクエリ結果を修正
    -   `ENUM`型列[<a href="https://github.com/pingcap/tidb/issues/27831">#27831</a>](https://github.com/pingcap/tidb/issues/27831)で`JOIN`実行したときに発生する可能性がある間違った結果を修正しました。
    -   `ENUM`データ型[<a href="https://github.com/pingcap/tidb/issues/29357">#29357</a>](https://github.com/pingcap/tidb/issues/29357)で`CASE WHEN`関数を使用するときのpanicを修正しました。
    -   ベクトル化された式[<a href="https://github.com/pingcap/tidb/issues/29244">#29244</a>](https://github.com/pingcap/tidb/issues/29244)の関数`microsecond`の誤った結果を修正します。
    -   ウィンドウ関数により TiDB がエラーを報告する代わりにpanicを引き起こす問題を修正します[<a href="https://github.com/pingcap/tidb/issues/30326">#30326</a>](https://github.com/pingcap/tidb/issues/30326)
    -   特定の場合に Merge Join 演算子が間違った結果を取得する問題を修正します[<a href="https://github.com/pingcap/tidb/issues/33042">#33042</a>](https://github.com/pingcap/tidb/issues/33042)
    -   相関サブクエリが定数[<a href="https://github.com/pingcap/tidb/issues/32089">#32089</a>](https://github.com/pingcap/tidb/issues/32089)を返すと TiDB が間違った結果を取得する問題を修正
    -   `ENUM`列または`SET`列のエンコーディングが間違っているため、TiDB が間違ったデータを書き込む問題を修正します[<a href="https://github.com/pingcap/tidb/issues/32302">#32302</a>](https://github.com/pingcap/tidb/issues/32302)
    -   TiDB [<a href="https://github.com/pingcap/tidb/issues/31638">#31638</a>](https://github.com/pingcap/tidb/issues/31638)で新しい照合順序が有効になっている場合、 `ENUM`または`SET`列の`MAX`または`MIN`関数が間違った結果を返す問題を修正します。
    -   IndexHashJoin オペレーターが正常に終了しない問題を修正します[<a href="https://github.com/pingcap/tidb/issues/31062">#31062</a>](https://github.com/pingcap/tidb/issues/31062)
    -   テーブルに仮想列[<a href="https://github.com/pingcap/tidb/issues/30965">#30965</a>](https://github.com/pingcap/tidb/issues/30965)がある場合、TiDB が間違ったデータを読み取る可能性がある問題を修正
    -   スロークエリログ[<a href="https://github.com/pingcap/tidb/issues/30309">#30309</a>](https://github.com/pingcap/tidb/issues/30309)でログレベルの設定が反映されない問題を修正
    -   場合によっては、パーティション化されたテーブルがインデックスを完全に使用してデータをスキャンできない問題を修正します[<a href="https://github.com/pingcap/tidb/issues/33966">#33966</a>](https://github.com/pingcap/tidb/issues/33966)
    -   TiDB のバックグラウンド HTTP サービスが正常に終了せず、クラスターが異常な状態になる場合がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/30571">#30571</a>](https://github.com/pingcap/tidb/issues/30571)
    -   TiDB が予期せず認証失敗のログを多数出力する場合がある問題を修正[<a href="https://github.com/pingcap/tidb/issues/29709">#29709</a>](https://github.com/pingcap/tidb/issues/29709)
    -   システム変数`max_allowed_packet`が有効にならない問題を修正[<a href="https://github.com/pingcap/tidb/issues/31422">#31422</a>](https://github.com/pingcap/tidb/issues/31422)
    -   自動 ID が範囲[<a href="https://github.com/pingcap/tidb/issues/29483">#29483</a>](https://github.com/pingcap/tidb/issues/29483)の外にある場合、 `REPLACE`ステートメントが他の行を誤って変更する問題を修正します。
    -   スロークエリログが正常にログ出力できず、メモリを過剰に消費する可能性がある問題を修正[<a href="https://github.com/pingcap/tidb/issues/32656">#32656</a>](https://github.com/pingcap/tidb/issues/32656)
    -   NATURAL JOIN の結果に予期しない列が含まれる場合がある問題を修正[<a href="https://github.com/pingcap/tidb/issues/29481">#24981</a>](https://github.com/pingcap/tidb/issues/29481)
    -   データ[<a href="https://github.com/pingcap/tidb/issues/29711">#29711</a>](https://github.com/pingcap/tidb/issues/29711)のクエリにプレフィックス列インデックスが使用されている場合、1 つのステートメントで`ORDER BY`と`LIMIT`を一緒に使用すると間違った結果が出力される可能性がある問題を修正します。
    -   楽観的トランザクションのリトライ時にDOUBLE型の自動インクリメント列が変更される場合がある問題を修正[<a href="https://github.com/pingcap/tidb/issues/29892">#29892</a>](https://github.com/pingcap/tidb/issues/29892)
    -   STR_TO_DATE 関数がマイクロ秒部分の前のゼロを正しく処理できない問題を修正します[<a href="https://github.com/pingcap/tidb/issues/30078">#30078</a>](https://github.com/pingcap/tidb/issues/30078)
    -   TiFlash は空の範囲を持つテーブルの読み取りをまだサポートしていませんが、 TiFlashを使用して空の範囲を持つテーブルをスキャンすると、 TiFlashが間違った結果を取得する問題を修正します[<a href="https://github.com/pingcap/tidb/issues/33083">#33083</a>](https://github.com/pingcap/tidb/issues/33083)

-   TiKV

    -   古いメッセージによって TiKV がpanicになるバグを修正[<a href="https://github.com/tikv/tikv/issues/12023">#12023</a>](https://github.com/tikv/tikv/issues/12023)
    -   メモリメトリクス[<a href="https://github.com/tikv/tikv/issues/12160">#12160</a>](https://github.com/tikv/tikv/issues/12160)のオーバーフローによって引き起こされる断続的なパケット損失とメモリ不足 (OOM) の問題を修正します。
    -   TiKV が Ubuntu 18.04 でプロファイリングを実行するときに発生する潜在的なpanicの問題を修正します[<a href="https://github.com/tikv/tikv/issues/9765">#9765</a>](https://github.com/tikv/tikv/issues/9765)
    -   間違った文字列一致[<a href="https://github.com/tikv/tikv/issues/12329">#12329</a>](https://github.com/tikv/tikv/issues/12329)が原因で tikv-ctl が間違った結果を返す問題を修正
    -   レプリカの読み取りが線形化可能性[<a href="https://github.com/tikv/tikv/issues/12109">#12109</a>](https://github.com/tikv/tikv/issues/12109)に違反する可能性があるバグを修正
    -   TiKV が 2 年以上実行されている場合にpanicになる可能性があるバグを修正[<a href="https://github.com/tikv/tikv/issues/11940">#11940</a>](https://github.com/tikv/tikv/issues/11940)
    -   フロー制御が有効で、 `level0_slowdown_trigger`が明示的に設定されている場合の QPS ドロップの問題を修正します[<a href="https://github.com/tikv/tikv/issues/11424">#11424</a>](https://github.com/tikv/tikv/issues/11424)
    -   cgroup コントローラーがマウントされていないときに発生するpanicの問題を修正します[<a href="https://github.com/tikv/tikv/issues/11569">#11569</a>](https://github.com/tikv/tikv/issues/11569)
    -   遅れているリージョンピア[<a href="https://github.com/tikv/tikv/issues/11526">#11526</a>](https://github.com/tikv/tikv/issues/11526)でのリージョンのマージによって発生する可能性のあるメタデータの破損を修正します。
    -   TiKVの動作停止後にResolved TSのレイテンシーが増加する問題を修正[<a href="https://github.com/tikv/tikv/issues/11351">#11351</a>](https://github.com/tikv/tikv/issues/11351)
    -   極端な条件でリージョンのマージ、ConfChange、およびスナップショットが同時に発生したときに発生するpanicの問題を修正します[<a href="https://github.com/tikv/tikv/issues/11475">#11475</a>](https://github.com/tikv/tikv/issues/11475)
    -   tikv-ctl が正しいリージョン関連情報を返せないバグを修正[<a href="https://github.com/tikv/tikv/issues/11393">#11393</a>](https://github.com/tikv/tikv/issues/11393)
    -   10 進数の除算結果が 0 の場合の負号の問題を修正します[<a href="https://github.com/pingcap/tidb/issues/29586">#29586</a>](https://github.com/pingcap/tidb/issues/29586)
    -   悲観的トランザクションモードでプリライトリクエストを再試行すると、まれにデータ不整合のリスクが発生する可能性がある問題を修正します[<a href="https://github.com/tikv/tikv/issues/11187">#11187</a>](https://github.com/tikv/tikv/issues/11187)
    -   統計スレッド[<a href="https://github.com/tikv/tikv/issues/11195">#11195</a>](https://github.com/tikv/tikv/issues/11195)のデータ監視によって発生するメモリリークを修正しました。
    -   TiKV メトリクス[<a href="https://github.com/tikv/tikv/issues/11299">#11299</a>](https://github.com/tikv/tikv/issues/11299)でインスタンスごとの gRPC リクエストの平均レイテンシーが不正確である問題を修正します。
    -   ピアのステータスが`Applying` [<a href="https://github.com/tikv/tikv/issues/11746">#11746</a>](https://github.com/tikv/tikv/issues/11746)のときにスナップショット ファイルを削除することによって引き起こされるpanicの問題を修正します。
    -   GC ワーカーがビジー状態[<a href="https://github.com/tikv/tikv/issues/11903">#11903</a>](https://github.com/tikv/tikv/issues/11903)の場合、TiKV が一定範囲のデータを削除できない (内部コマンド`unsafe_destroy_range`が実行されることを意味します) というバグを修正します。
    -   初期化されていないレプリカを削除すると古いレプリカが再作成される可能性がある問題を修正します[<a href="https://github.com/tikv/tikv/issues/10533">#10533</a>](https://github.com/tikv/tikv/issues/10533)
    -   TiKV が逆テーブル スキャンを実行するときに TiKV がメモリロックを検出できない問題を修正します[<a href="https://github.com/tikv/tikv/issues/11440">#11440</a>](https://github.com/tikv/tikv/issues/11440)
    -   コルーチンの実行が速すぎる場合に時折発生するデッドロックの問題を修正します[<a href="https://github.com/tikv/tikv/issues/11549">#11549</a>](https://github.com/tikv/tikv/issues/11549)
    -   ピアを破棄するとレイテンシーが長くなる可能性がある問題を修正[<a href="https://github.com/tikv/tikv/issues/10210">#10210</a>](https://github.com/tikv/tikv/issues/10210)
    -   マージ対象のターゲットリージョンが無効なため、TiKV がパニックを起こして予期せずピアを破棄する問題を修正します[<a href="https://github.com/tikv/tikv/issues/12232">#12232</a>](https://github.com/tikv/tikv/issues/12232)
    -   リージョン[<a href="https://github.com/tikv/tikv/issues/12048">#12048</a>](https://github.com/tikv/tikv/issues/12048)をマージするときに、ターゲット ピアが初期化されずに破棄されたピアに置き換えられるときに発生する TiKVpanicの問題を修正します。
    -   スナップショットの適用が中止されたときに発生する TiKVpanicの問題を修正します[<a href="https://github.com/tikv/tikv/issues/11618">#11618</a>](https://github.com/tikv/tikv/issues/11618)
    -   オペレーターの実行が失敗した場合、TiKV が送信されるスナップショットの数を正しく計算できないバグを修正[<a href="https://github.com/tikv/tikv/issues/11341">#11341</a>](https://github.com/tikv/tikv/issues/11341)

-   PD

    -   リージョンスキャッタラー スケジューリングで一部のピアが失われる問題を修正します[<a href="https://github.com/tikv/pd/issues/4565">#4565</a>](https://github.com/tikv/pd/issues/4565)
    -   コールド ホットスポット データがホットスポット統計[<a href="https://github.com/tikv/pd/issues/4390">#4390</a>](https://github.com/tikv/pd/issues/4390)から削除できない問題を修正します。

-   TiFlash

    -   MPP タスクがスレッドを永久にリークする可能性があるバグを修正[<a href="https://github.com/pingcap/tiflash/issues/4238">#4238</a>](https://github.com/pingcap/tiflash/issues/4238)
    -   複数値式[<a href="https://github.com/pingcap/tiflash/issues/4016">#4016</a>](https://github.com/pingcap/tiflash/issues/4016)で`IN`の結果が正しくない問題を修正
    -   日付形式で`'\n'`無効な区切り文字[<a href="https://github.com/pingcap/tiflash/issues/4036">#4036</a>](https://github.com/pingcap/tiflash/issues/4036)として識別される問題を修正します。
    -   重い読み取りワークロードで列を追加した後の潜在的なクエリ エラーを修正[<a href="https://github.com/pingcap/tiflash/issues/3967">#3967</a>](https://github.com/pingcap/tiflash/issues/3967)
    -   無効なstorageディレクトリ構成が予期せぬ動作を引き起こすバグを修正[<a href="https://github.com/pingcap/tiflash/issues/4093">#4093</a>](https://github.com/pingcap/tiflash/issues/4093)
    -   一部の例外が正しく処理されないバグを修正[<a href="https://github.com/pingcap/tiflash/issues/4101">#4101</a>](https://github.com/pingcap/tiflash/issues/4101)
    -   `STR_TO_DATE()`関数がマイクロ秒[<a href="https://github.com/pingcap/tiflash/issues/3557">#3557</a>](https://github.com/pingcap/tiflash/issues/3557)を解析する際に先頭のゼロを誤って処理するバグを修正
    -   `INT`から`DECIMAL`にキャストするとオーバーフローが発生する可能性がある問題を修正[<a href="https://github.com/pingcap/tiflash/issues/3920">#3920</a>](https://github.com/pingcap/tiflash/issues/3920)
    -   `DATETIME`から`DECIMAL` [<a href="https://github.com/pingcap/tiflash/issues/4151">#4151</a>](https://github.com/pingcap/tiflash/issues/4151)をキャストするときに発生する間違った結果を修正
    -   `FLOAT` ～ `DECIMAL` [<a href="https://github.com/pingcap/tiflash/issues/3998">#3998</a>](https://github.com/pingcap/tiflash/issues/3998)キャスト時に発生するオーバーフローを修正
    -   TiFlashと TiDB または TiKV [<a href="https://github.com/pingcap/tiflash/issues/3475">#3475</a>](https://github.com/pingcap/tiflash/issues/3475)で`CastStringAsReal`動作が矛盾する問題を修正
    -   TiFlashと TiDB または TiKV [<a href="https://github.com/pingcap/tiflash/issues/3619">#3619</a>](https://github.com/pingcap/tiflash/issues/3619)で`CastStringAsDecimal`動作が矛盾する問題を修正
    -   TiFlashの再起動後に`EstablishMPPConnection`エラーが返されることがある問題を修正[<a href="https://github.com/pingcap/tiflash/issues/3615">#3615</a>](https://github.com/pingcap/tiflash/issues/3615)
    -   TiFlashレプリカの数を 0 [<a href="https://github.com/pingcap/tiflash/issues/3659">#3659</a>](https://github.com/pingcap/tiflash/issues/3659)に設定した後、古いデータを再利用できない問題を修正
    -   主キーが`handle` [<a href="https://github.com/pingcap/tiflash/issues/3569">#3569</a>](https://github.com/pingcap/tiflash/issues/3569)の主キー列を拡張するときに発生する可能性のあるデータの不整合を修正しました。
    -   SQL ステートメントに非常に長いネストされた式が含まれている場合に発生する可能性のある解析エラーを修正します[<a href="https://github.com/pingcap/tiflash/issues/3354">#3354</a>](https://github.com/pingcap/tiflash/issues/3354)
    -   クエリに`where <string>`句[<a href="https://github.com/pingcap/tiflash/issues/3447">#3447</a>](https://github.com/pingcap/tiflash/issues/3447)が含まれる場合に発生する可能性のある間違った結果を修正
    -   `new_collations_enabled_on_first_bootstrap`有効になっている場合に発生する可能性のある間違った結果を修正[<a href="https://github.com/pingcap/tiflash/issues/3388">#3388</a>](https://github.com/pingcap/tiflash/issues/3388) 、 [<a href="https://github.com/pingcap/tiflash/issues/3391">#3391</a>](https://github.com/pingcap/tiflash/issues/3391)
    -   TLS が有効になっているときに発生するpanicの問題を修正します[<a href="https://github.com/pingcap/tiflash/issues/4196">#4196</a>](https://github.com/pingcap/tiflash/issues/4196)
    -   メモリ制限が有効になっているときに発生するpanicの問題を修正します[<a href="https://github.com/pingcap/tiflash/issues/3902">#3902</a>](https://github.com/pingcap/tiflash/issues/3902)
    -   MPP クエリが停止するとTiFlashが時折クラッシュする問題を修正[<a href="https://github.com/pingcap/tiflash/issues/3401">#3401</a>](https://github.com/pingcap/tiflash/issues/3401)
    -   `Unexpected type of column: Nullable(Nothing)` [<a href="https://github.com/pingcap/tiflash/issues/3351">#3351</a>](https://github.com/pingcap/tiflash/issues/3351)の予期しないエラーを修正
    -   遅れているリージョンピア[<a href="https://github.com/pingcap/tiflash/issues/4437">#4437</a>](https://github.com/pingcap/tiflash/issues/4437)でのリージョンのマージによって発生する可能性のあるメタデータの破損を修正します。
    -   `JOIN`を含むクエリでエラーが発生した場合にハングする可能性がある問題を修正[<a href="https://github.com/pingcap/tiflash/issues/4195">#4195</a>](https://github.com/pingcap/tiflash/issues/4195)
    -   不正な実行プランにより、MPP クエリに対して誤った結果が返される可能性がある問題を修正[<a href="https://github.com/pingcap/tiflash/issues/3389">#3389</a>](https://github.com/pingcap/tiflash/issues/3389)

-   ツール

    -   バックアップと復元 (BR)

        -   BR がRawKV [<a href="https://github.com/pingcap/tidb/issues/32607">#32607</a>](https://github.com/pingcap/tidb/issues/32607)のバックアップに失敗する問題を修正

    -   TiCDC

        -   デフォルト値を複製できない問題を修正[<a href="https://github.com/pingcap/tiflow/issues/3793">#3793</a>](https://github.com/pingcap/tiflow/issues/3793)
        -   場合によってはシーケンスが不正に複製されるバグを修正[<a href="https://github.com/pingcap/tiflow/issues/4552">#4563</a>](https://github.com/pingcap/tiflow/issues/4552)
        -   PDリーダーがキルされた場合にTiCDCノードが異常終了するバグを修正[<a href="https://github.com/pingcap/tiflow/issues/4248">#4248</a>](https://github.com/pingcap/tiflow/issues/4248)
        -   `batch-replace-enable`が無効になっている場合、MySQL シンクが重複した`replace` SQL ステートメントを生成するバグを修正[<a href="https://github.com/pingcap/tiflow/issues/4501">#4501</a>](https://github.com/pingcap/tiflow/issues/4501)
        -   デフォルトの列値[<a href="https://github.com/pingcap/tiflow/issues/3929">#3929</a>](https://github.com/pingcap/tiflow/issues/3929)を出力するときに発生するpanicとデータの不整合の問題を修正します。
        -   `mq sink write row`監視データがない問題を修正[<a href="https://github.com/pingcap/tiflow/issues/3431">#3431</a>](https://github.com/pingcap/tiflow/issues/3431)
        -   `min.insync.replicas`が`replication-factor` [<a href="https://github.com/pingcap/tiflow/issues/3994">#3994</a>](https://github.com/pingcap/tiflow/issues/3994)より小さい場合にレプリケーションが実行できない問題を修正
        -   レプリケーション タスクが削除されたときに発生する潜在的なpanicの問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/3128">#3128</a>](https://github.com/pingcap/tiflow/issues/3128)
        -   必要なプロセッサ情報が存在しない場合にHTTP APIがパニックするバグを修正[<a href="https://github.com/pingcap/tiflow/issues/3840">#3840</a>](https://github.com/pingcap/tiflow/issues/3840)
        -   不正確なチェックポイント[<a href="https://github.com/pingcap/tiflow/issues/3545">#3545</a>](https://github.com/pingcap/tiflow/issues/3545)によって引き起こされる潜在的なデータ損失の問題を修正します。
        -   デッドロックによりレプリケーション タスクが停止するという潜在的な問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/4055">#4055</a>](https://github.com/pingcap/tiflow/issues/4055)
        -   etcd [<a href="https://github.com/pingcap/tiflow/issues/2980">#2980</a>](https://github.com/pingcap/tiflow/issues/2980)でタスクステータスを手動でクリーンアップするときに発生する TiCDCpanicの問題を修正します。
        -   DDL ステートメント内の特別なコメントによりレプリケーション タスクが停止する問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/3755">#3755</a>](https://github.com/pingcap/tiflow/issues/3755)
        -   `config.Metadata.Timeout` [<a href="https://github.com/pingcap/tiflow/issues/3352">#3352</a>](https://github.com/pingcap/tiflow/issues/3352)の誤った構成によって引き起こされるレプリケーション停止の問題を修正します。
        -   RHEL リリース[<a href="https://github.com/pingcap/tiflow/issues/3584">#3584</a>](https://github.com/pingcap/tiflow/issues/3584)のタイムゾーンの問題によりサービスを開始できない問題を修正
        -   `stopped`クラスターのアップグレード後に変更フィードが自動的に再開される問題を修正[<a href="https://github.com/pingcap/tiflow/issues/3473">#3473</a>](https://github.com/pingcap/tiflow/issues/3473)
        -   MySQL シンクのデッドロックによって引き起こされる過度に頻繁な警告の問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/2706">#2706</a>](https://github.com/pingcap/tiflow/issues/2706)
        -   Canal および Maxwell プロトコル[<a href="https://github.com/pingcap/tiflow/issues/3676">#3676</a>](https://github.com/pingcap/tiflow/issues/3676)で`enable-old-value`設定項目が自動的に`true`に設定されないバグを修正
        -   Avro シンクが JSON 型列の解析をサポートしていない問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/3624">#3624</a>](https://github.com/pingcap/tiflow/issues/3624)
        -   チェンジフィードチェックポイントラグ[<a href="https://github.com/pingcap/tiflow/issues/3010">#3010</a>](https://github.com/pingcap/tiflow/issues/3010)の負の値エラーを修正
        -   コンテナ環境の OOM 問題を修正する[<a href="https://github.com/pingcap/tiflow/issues/1798">#1798</a>](https://github.com/pingcap/tiflow/issues/1798)
        -   DDL 処理後のメモリリーク問題を修正[<a href="https://github.com/pingcap/tiflow/issues/3174">#3174</a>](https://github.com/pingcap/tiflow/issues/3174)
        -   同じノード[<a href="https://github.com/pingcap/tiflow/issues/4464">#4464</a>](https://github.com/pingcap/tiflow/issues/4464)でテーブルが繰り返しスケジュールされると、変更フィードがスタックする問題を修正します。
        -   PDノードが異常[<a href="https://github.com/pingcap/tiflow/issues/4778">#4778</a>](https://github.com/pingcap/tiflow/issues/4778)の場合、オープンAPIによるステータス問い合わせがブロックされる場合があるバグを修正
        -   所有者の変更によって引き起こされた誤ったメトリクスを修正する[<a href="https://github.com/pingcap/tiflow/issues/4774">#4774</a>](https://github.com/pingcap/tiflow/issues/4774)
        -   Unified Sorter [<a href="https://github.com/pingcap/tiflow/issues/4447">#4447</a>](https://github.com/pingcap/tiflow/issues/4447)によって使用されるワーカープールの安定性の問題を修正しました。
        -   `cached region`監視メトリクスがマイナス[<a href="https://github.com/pingcap/tiflow/issues/4300">#4300</a>](https://github.com/pingcap/tiflow/issues/4300)になる問題を修正

    -   TiDB Lightning

        -   TiDB Lightning にテーブル`mysql.tidb`へのアクセス権限[<a href="https://github.com/pingcap/tidb/issues/31088">#31088</a>](https://github.com/pingcap/tidb/issues/31088)ない場合にインポート結果が正しくない問題を修正
        -   チェックサム エラー「GC ライフタイムがトランザクション期間よりも短い」 [<a href="https://github.com/pingcap/tidb/issues/32733">#32733</a>](https://github.com/pingcap/tidb/issues/32733)を修正
        -   一部のインポートタスクにソースファイルが含まれていない場合、 TiDB Lightning がメタデータスキーマを削除できないことがあるバグを修正[<a href="https://github.com/pingcap/tidb/issues/28144">#28144</a>](https://github.com/pingcap/tidb/issues/28144)
        -   S3storageパスが存在しない場合にTiDB Lightning がエラーを報告しない問題を修正[<a href="https://github.com/pingcap/tidb/issues/28031">#28031</a>](https://github.com/pingcap/tidb/issues/28031) [<a href="https://github.com/pingcap/tidb/issues/30709">#30709</a>](https://github.com/pingcap/tidb/issues/30709)
        -   GCS [<a href="https://github.com/pingcap/tidb/issues/30377">#30377</a>](https://github.com/pingcap/tidb/issues/30377)で 1000 を超えるキーを反復するときに発生するエラーを修正
