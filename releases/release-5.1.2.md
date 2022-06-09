---
title: TiDB 5.1.2 Release Notes
---

# TiDB5.1.2リリースノート {#tidb-5-1-2-release-notes}

発売日：2021年9月27日

TiDBバージョン：5.1.2

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   次のバグ修正により、実行結果が変更され、アップグレードの非互換性が発生する可能性があります。

        -   `greatest(datetime) union null`が空の文字列[＃26532](https://github.com/pingcap/tidb/issues/26532)を返す問題を修正します
        -   `having`句が正しく機能しない可能性がある問題を修正します[＃26496](https://github.com/pingcap/tidb/issues/26496)
        -   `between`式の周りの照合が異なる場合に発生する誤った実行結果を修正します[＃27146](https://github.com/pingcap/tidb/issues/27146)
        -   `group_concat`関数の列に非ビン照合順序[＃27429](https://github.com/pingcap/tidb/issues/27429)がある場合に発生する誤った実行結果を修正します
        -   複数の列で`count(distinct)`式を使用すると、新しい照合順序が有効になっているときに誤った結果が返される問題を修正します[＃27091](https://github.com/pingcap/tidb/issues/27091)
        -   `extract`関数の引数が負の期間[＃27236](https://github.com/pingcap/tidb/issues/27236)である場合に発生する誤った結果を修正します
        -   `SQL_MODE`が&#39; [＃26762](https://github.com/pingcap/tidb/issues/26762)の場合、無効な日付を挿入してもエラーが報告されない問題を修正します。
        -   `SQL_MODE`が「NO_ZERO_IN_DATE」の場合に無効なデフォルトの日付を使用してもエラーが報告されない問題を修正します[＃26766](https://github.com/pingcap/tidb/issues/26766)

-   ツール

    -   TiCDC

        -   互換性のあるバージョンを`5.1.0-alpha`から[＃2659](https://github.com/pingcap/tiflow/pull/2659)に設定し`5.2.0-alpha`

## 改善 {#improvements}

-   TiDB

    -   ヒストグラムの行数で自動分析をトリガーし、このトリガーアクションの精度を高めます[＃24237](https://github.com/pingcap/tidb/issues/24237)

-   TiKV

    -   TiCDC構成の動的変更のサポート[＃10645](https://github.com/tikv/tikv/issues/10645)
    -   解決済みTSメッセージのサイズを縮小して、ネットワーク帯域幅を節約します[＃2448](https://github.com/pingcap/tiflow/issues/2448)
    -   単一のストアによって報告されるハートビートメッセージのピア統計の数を制限する[＃10621](https://github.com/tikv/tikv/pull/10621)

-   PD

    -   空のリージョンのスケジュールを許可し、スキャッターレンジスケジューラ[＃4117](https://github.com/tikv/pd/pull/4117)で個別の許容範囲構成を使用します
    -   PD間でリージョン情報を同期するパフォーマンスを向上させる[＃3933](https://github.com/tikv/pd/pull/3933)
    -   生成された演算子に基づいてストアの再試行制限を動的に調整することをサポートします[＃3744](https://github.com/tikv/pd/issues/3744)

-   TiFlash

    -   `DATE()`機能をサポート
    -   インスタンスごとの書き込みスループットのためにGrafanaパネルを追加します
    -   `leader-read`のプロセスのパフォーマンスを最適化する
    -   MPPタスクをキャンセルするプロセスを加速します

-   ツール

    -   TiCDC

        -   ユニファイドソーターがメモリを使用してデータをソートしているときにメモリ管理を最適化する[＃2553](https://github.com/pingcap/tiflow/issues/2553)
        -   同時実行性が高い場合に、ワーカープールを最適化してゴルーチンを減らします[＃2211](https://github.com/pingcap/tiflow/issues/2211)
        -   テーブルのリージョンがTiKVノードから転送されるときのゴルーチンの使用量を減らす[＃2284](https://github.com/pingcap/tiflow/issues/2284)
        -   グローバルgRPC接続プールを追加し、KVクライアント間でgRPC接続を共有します[＃2534](https://github.com/pingcap/tiflow/pull/2534)
        -   メジャーバージョンとマイナーバージョンでTiCDCクラスターを操作することを禁止する[＃2599](https://github.com/pingcap/tiflow/pull/2599)

    -   Dumpling

        -   `START TRANSACTION ... WITH CONSISTENT SNAPSHOT`および`SHOW CREATE TABLE`をサポートしない[＃309](https://github.com/pingcap/dumpling/issues/309)互換データベースのバックアップをサポートする

## バグの修正 {#bug-fixes}

-   TiDB

    -   ハッシュ列が`ENUM`タイプ[＃27893](https://github.com/pingcap/tidb/issues/27893)の場合に、インデックスハッシュ結合の潜在的な誤った結果を修正します。
    -   まれに、アイドル状態の接続をリサイクルするとリクエストの送信がブロックされる可能性があるバッチクライアントのバグを修正します[＃27678](https://github.com/pingcap/tidb/pull/27678)
    -   `FLOAT64`タイプのオーバーフローチェックがMySQL3のオーバーフローチェックと異なる問題を修正し[＃23897](https://github.com/pingcap/tidb/issues/23897)
    -   TiDBが`pd is timeout`エラー[＃26147](https://github.com/pingcap/tidb/issues/26147)を返す必要があるのに`unknow`エラーを返す問題を修正します
    -   `case when`式[＃26662](https://github.com/pingcap/tidb/issues/26662)の間違った文字セットと照合順序を修正します
    -   MPPクエリの潜在的な`can not found column in Schema column`エラーを修正します[＃28148](https://github.com/pingcap/tidb/pull/28148)
    -   TiFlashがシャットダウンしているときにTiDBがパニックになる可能性があるバグを修正します[＃28096](https://github.com/pingcap/tidb/issues/28096)
    -   `enum like 'x%'`を使用することによって引き起こされる間違った範囲の問題を修正し[＃27130](https://github.com/pingcap/tidb/issues/27130)
    -   IndexLookupJoin [＃27410](https://github.com/pingcap/tidb/issues/27410)で使用した場合の、共通テーブル式（CTE）のデッドロックの問題を修正します。
    -   再試行可能なデッドロックが`INFORMATION_SCHEMA.DEADLOCKS`テーブル[＃27400](https://github.com/pingcap/tidb/issues/27400)に誤って記録されるバグを修正します。
    -   パーティション化されたテーブルからの`TABLESAMPLE`のクエリ結果が期待どおりにソートされない問題を修正します[＃27349](https://github.com/pingcap/tidb/issues/27349)
    -   未使用の`/debug/sub-optimal-plan`を削除し[＃27265](https://github.com/pingcap/tidb/pull/27265)
    -   ハッシュ分割テーブルが署名されていないデータを処理するときにクエリが間違った結果を返す可能性があるバグを修正します[＃26569](https://github.com/pingcap/tidb/issues/26569)
    -   `NO_UNSIGNED_SUBTRACTION`が設定されている場合にパーティションの作成が失敗するバグを修正します[＃26765](https://github.com/pingcap/tidb/issues/26765)
    -   `Apply`が[＃26958](https://github.com/pingcap/tidb/issues/26958)に変換されるときに`distinct`フラグが欠落する問題を修正し`Join`
    -   新しく回復されたTiFlashノードのブロック期間を設定して、この期間中にクエリがブロックされないようにします[＃26897](https://github.com/pingcap/tidb/pull/26897)
    -   CTEが複数回参照されるときに発生する可能性のあるバグを修正します[＃26212](https://github.com/pingcap/tidb/issues/26212)
    -   MergeJoinが使用されている場合のCTEバグを修正します[＃25474](https://github.com/pingcap/tidb/issues/25474)
    -   通常のテーブルがパーティション化されたテーブル[＃26251](https://github.com/pingcap/tidb/issues/26251)に結合するときに、 `SELECT FOR UPDATE`ステートメントがデータを正しくロックしないというバグを修正します。
    -   通常のテーブルがパーティションテーブル[＃26250](https://github.com/pingcap/tidb/issues/26250)に結合すると、 `SELECT FOR UPDATE`ステートメントがエラーを返す問題を修正します。
    -   `PointGet`がロック[＃26562](https://github.com/pingcap/tidb/pull/26562)を解決するライトバージョンを使用しないという問題を修正します

-   TiKV

    -   TiKVがv3.xからそれ以降のバージョンにアップグレードされた後に発生するパニックの問題を修正します[＃10902](https://github.com/tikv/tikv/issues/10902)
    -   破損したスナップショットファイルによって引き起こされる潜在的なディスクフルの問題を修正する[＃10813](https://github.com/tikv/tikv/issues/10813)
    -   TiKVコプロセッサーの遅いログに、要求の処理に費やされた時間のみを考慮させる[＃10841](https://github.com/tikv/tikv/issues/10841)
    -   sloggerスレッドが過負荷になり、キューがいっぱいになったときにスレッドをブロックする代わりにログをドロップする[＃10841](https://github.com/tikv/tikv/issues/10841)
    -   コプロセッサー要求の処理がタイムアウトしたときに発生するパニックの問題を修正します[＃10852](https://github.com/tikv/tikv/issues/10852)
    -   Titanが有効になっている5.0より前のバージョンからアップグレードするときに発生するTiKVパニックの問題を修正します[＃10842](https://github.com/tikv/tikv/pull/10842)
    -   新しいバージョンのTiKVをv5.0.xにロールバックできない問題を修正します[＃10842](https://github.com/tikv/tikv/pull/10842)
    -   RocksDB1にデータを取り込む前にTiKVがファイルを削除する可能性がある問題を修正し[＃10438](https://github.com/tikv/tikv/issues/10438)
    -   左の悲観的なロックによって引き起こされた解析の失敗を修正します[＃26404](https://github.com/pingcap/tidb/issues/26404)

-   PD

    -   PDが時間内にダウンピアを修正しないという問題を修正します[＃4077](https://github.com/tikv/pd/issues/4077)
    -   `replication.max-replicas`が更新された後、デフォルトの配置ルールのレプリカ数が一定のままになる問題を修正します[＃3886](https://github.com/tikv/pd/issues/3886)
    -   TiKV1をスケールアウトするときにPDがパニックになる可能性があるバグを修正し[＃3868](https://github.com/tikv/pd/issues/3868)
    -   クラスタにエビクトリーダースケジューラーがある場合にホットリージョンスケジューラーが機能しないバグを修正します[＃3697](https://github.com/tikv/pd/issues/3697)

-   TiFlash

    -   TiFlashがMPP接続の確立に失敗した場合の予期しない結果の問題を修正します
    -   TiFlashが複数のディスクに展開されているときに発生するデータの不整合の潜在的な問題を修正します
    -   TiFlashサーバーに高負荷がかかっているときにMPPクエリが間違った結果を取得するバグを修正します
    -   MPPクエリが永久にハングする潜在的なバグを修正します
    -   ストアの初期化とDDLを同時に操作するときのパニックの問題を修正します
    -   `<=`に`CONSTANT`などの`>`が含まれている場合に発生する`COLUMN`た結果の`>=`を修正し`<`
    -   `Snapshot`が複数のDDL操作と同時に適用される場合の潜在的なパニックの問題を修正します
    -   大量の書き込みの下でメトリックのストアサイズが不正確になる問題を修正します
    -   TiFlashが長時間実行した後にデルタデータをガベージコレクションできないという潜在的な問題を修正します
    -   新しい照合順序が有効になっている場合の誤った結果の問題を修正します
    -   ロックを解決するときに発生する可能性のあるパニックの問題を修正します
    -   メトリックが間違った値を表示する潜在的なバグを修正します

-   ツール

    -   バックアップと復元（BR）

        -   データのバックアップと復元中に平均速度が正確でないという問題を修正します[＃1405](https://github.com/pingcap/br/issues/1405)

    -   Dumpling

        -   一部のMySQLバージョン（8.0.3および8.0.23）で`show table status`が誤った結果を返す場合にDumplingが保留される問題を修正します[＃322](https://github.com/pingcap/dumpling/issues/322)
        -   デフォルトの`sort-engine`オプション[＃2373](https://github.com/pingcap/tiflow/issues/2373)での4.0.xクラスターとのCLI互換性の問題を修正します

    -   TiCDC

        -   `string`または[＃2758](https://github.com/pingcap/tiflow/issues/2758)の文字列型の値を処理するときにJSONエンコーディングがパニックを引き起こす可能性があるバグを修正し`[]byte`
        -   OOM [＃2673](https://github.com/pingcap/tiflow/issues/2673)を回避するために、gRPCウィンドウサイズを縮小します
        -   高いメモリプレッシャーの下での`keepalive`エラーを修正します[＃2202](https://github.com/pingcap/tiflow/issues/2202)
        -   署名されていない`tinyint`がTiCDCをパニックに陥らせるバグを修正します[＃2648](https://github.com/pingcap/tiflow/issues/2648)
        -   TiCDCOpenProtocolの空の値の問題を修正します。 1つのトランザクションに変更がない場合、空の値は出力されなくなりました。 [＃2612](https://github.com/pingcap/tiflow/issues/2612)
        -   手動再起動中のDDL処理のバグを修正[＃2603](https://github.com/pingcap/tiflow/issues/2603)
        -   メタデータを管理するときに`EtcdWorker`のスナップショットアイソレーションが誤って違反される可能性があるという問題を修正します[＃2559](https://github.com/pingcap/tiflow/pull/2559)
        -   TiCDCがテーブルを再スケジュールしているときに複数のプロセッサが同じテーブルにデータを書き込む可能性があるバグを修正します[＃2230](https://github.com/pingcap/tiflow/issues/2230)
        -   TiCDCが`ErrSchemaStorageTableMiss`エラー[＃2422](https://github.com/pingcap/tiflow/issues/2422)を取得したときにchangefeedが予期せずリセットされる可能性があるバグを修正します
        -   TiCDCが`ErrGCTTLExceeded`エラー[＃2391](https://github.com/pingcap/tiflow/issues/2391)を取得したときにchangefeedを削除できないバグを修正します
        -   TiCDCが大きなテーブルを[＃1259](https://github.com/pingcap/tiflow/issues/1259)に同期できないバグを修正し[＃2424](https://github.com/pingcap/tiflow/issues/2424) 。
