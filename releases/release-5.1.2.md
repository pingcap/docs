---
title: TiDB 5.1.2 Release Notes
---

# TiDB 5.1.2 リリースノート {#tidb-5-1-2-release-notes}

リリース日：2021年9月27日

TiDB バージョン: 5.1.2

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   次のバグ修正により実行結果が変更され、アップグレードの非互換性が発生する可能性があります。

        -   `greatest(datetime) union null`が空の文字列[#26532](https://github.com/pingcap/tidb/issues/26532)を返す問題を修正
        -   `having`句が正しく動作しない場合がある問題を修正[#26496](https://github.com/pingcap/tidb/issues/26496)
        -   `between`式の前後の照合順序が異なる場合に発生する間違った実行結果を修正します[#27146](https://github.com/pingcap/tidb/issues/27146)
        -   `group_concat`関数の列に非ビン照合順序がある場合に発生する間違った実行結果を修正します[#27429](https://github.com/pingcap/tidb/issues/27429)
        -   新しい照合順序が有効になっている場合に、複数の列で`count(distinct)`式を使用すると間違った結果が返される問題を修正します[#27091](https://github.com/pingcap/tidb/issues/27091)
        -   `extract`関数の引数が負の持続時間の場合に発生する結果が間違っていたのを修正[#27236](https://github.com/pingcap/tidb/issues/27236)
        -   `SQL_MODE`が &#39;STRICT_TRANS_TABLES&#39; [#26762](https://github.com/pingcap/tidb/issues/26762)の場合、無効な日付を挿入してもエラーが報告されない問題を修正します。
        -   `SQL_MODE`が &#39;NO_ZERO_IN_DATE&#39; [#26766](https://github.com/pingcap/tidb/issues/26766)の場合、無効なデフォルト日付を使用してもエラーが報告されない問題を修正します。

-   ツール

    -   TiCDC

        -   互換性のあるバージョンを`5.1.0-alpha` ～ `5.2.0-alpha`で設定します[#2659](https://github.com/pingcap/tiflow/pull/2659)

## 改善点 {#improvements}

-   TiDB

    -   ヒストグラム行数による自動分析をトリガーし、このトリガー アクションの精度を高めます[#24237](https://github.com/pingcap/tidb/issues/24237)

-   TiKV

    -   TiCDC 構成の動的変更のサポート[#10645](https://github.com/tikv/tikv/issues/10645)
    -   解決済み TS メッセージのサイズを削減して、ネットワーク帯域幅を節約します[#2448](https://github.com/pingcap/tiflow/issues/2448)
    -   単一ストアによって報告されるハートビートメッセージ内のピア統計の数を制限する[#10621](https://github.com/tikv/tikv/pull/10621)

-   PD

    -   空の領域をスケジュールできるようにし、散布範囲スケジューラ[#4117](https://github.com/tikv/pd/pull/4117)で別の許容値構成を使用します。
    -   PD 間のリージョン情報の同期パフォーマンスを向上[#3933](https://github.com/tikv/pd/pull/3933)
    -   生成された演算子に基づいてストアの再試行制限を動的に調整するサポート[#3744](https://github.com/tikv/pd/issues/3744)

-   TiFlash

    -   `DATE()`機能をサポート
    -   インスタンスごとの書き込みスループットのために Grafana パネルを追加します
    -   `leader-read`プロセスのパフォーマンスを最適化する
    -   MPP タスクのキャンセルプロセスを高速化する

-   ツール

    -   TiCDC

        -   統合ソーターがデータの並べ替えにメモリを使用している場合、メモリ管理を最適化します[#2553](https://github.com/pingcap/tiflow/issues/2553)
        -   同時実行性が高い場合、ゴルーチンを減らすためにワーカープールを最適化する[#2211](https://github.com/pingcap/tiflow/issues/2211)
        -   テーブルのリージョンがTiKV ノードから転送される場合の goroutine の使用量を削減します[#2284](https://github.com/pingcap/tiflow/issues/2284)
        -   グローバル gRPC 接続プールを追加し、KV クライアント間で gRPC 接続を共有する[#2534](https://github.com/pingcap/tiflow/pull/2534)
        -   メジャー バージョンとマイナー バージョンにまたがる TiCDC クラスターの操作を禁止する[#2599](https://github.com/pingcap/tiflow/pull/2599)

    -   Dumpling

        -   `START TRANSACTION ... WITH CONSISTENT SNAPSHOT`と`SHOW CREATE TABLE`をサポートしていない MySQL 互換データベースのバックアップをサポート[#309](https://github.com/pingcap/dumpling/issues/309)

## バグの修正 {#bug-fixes}

-   TiDB

    -   ハッシュ列が`ENUM`タイプ[#27893](https://github.com/pingcap/tidb/issues/27893)の場合のインデックス ハッシュ結合の潜在的な誤った結果を修正しました。
    -   アイドル状態の接続をリサイクルすると、まれにリクエストの送信がブロックされる可能性があるバッチ クライアントのバグを修正します[#27678](https://github.com/pingcap/tidb/pull/27678)
    -   `FLOAT64`種のオーバーフローチェックが[#23897](https://github.com/pingcap/tidb/issues/23897)と異なる問題を修正
    -   TiDB が`pd is timeout`エラー[#26147](https://github.com/pingcap/tidb/issues/26147)を返すはずなのに`unknow`エラーを返す問題を修正
    -   `case when`式[#26662](https://github.com/pingcap/tidb/issues/26662)の間違った文字セットと照合順序を修正します。
    -   MPP クエリ[#28148](https://github.com/pingcap/tidb/pull/28148)の潜在的なエラー`can not found column in Schema column`を修正
    -   TiFlashのシャットダウン時に TiDB がpanic可能性があるバグを修正[#28096](https://github.com/pingcap/tidb/issues/28096)
    -   `enum like 'x%'` [#27130](https://github.com/pingcap/tidb/issues/27130)の使用によって引き起こされる誤った範囲の問題を修正
    -   IndexLookupJoin [#27410](https://github.com/pingcap/tidb/issues/27410)で使用した場合の Common Table Expression (CTE) デッドロックの問題を修正
    -   再試行可能なデッドロックが`INFORMATION_SCHEMA.DEADLOCKS`テーブル[#27400](https://github.com/pingcap/tidb/issues/27400)に誤って記録されるバグを修正
    -   `TABLESAMPLE`パーティションテーブルからのクエリ結果が期待どおりに並べ替えられない問題を修正します[#27349](https://github.com/pingcap/tidb/issues/27349)
    -   未使用の`/debug/sub-optimal-plan` HTTP API [#27265](https://github.com/pingcap/tidb/pull/27265)を削除します。
    -   ハッシュパーティションテーブルが符号なしデータを扱う場合、クエリが間違った結果を返すことがあるバグを修正[#26569](https://github.com/pingcap/tidb/issues/26569)
    -   `NO_UNSIGNED_SUBTRACTION`を[#26765](https://github.com/pingcap/tidb/issues/26765)に設定するとパーティションの作成に失敗するバグを修正
    -   `Apply`を`Join` [#26958](https://github.com/pingcap/tidb/issues/26958)に変換するときに`distinct`フラグが欠落する問題を修正
    -   新しく回復されたTiFlashノードのブロック期間を設定して、この期間中のクエリのブロックを回避します[#26897](https://github.com/pingcap/tidb/pull/26897)
    -   CTE が複数回参照された場合に発生する可能性があるバグを修正[#26212](https://github.com/pingcap/tidb/issues/26212)
    -   MergeJoin 使用時の CTE バグを修正[#25474](https://github.com/pingcap/tidb/issues/25474)
    -   通常のテーブルがパーティションテーブル[#26251](https://github.com/pingcap/tidb/issues/26251)に結合する場合、 `SELECT FOR UPDATE`ステートメントがデータを正しくロックしないバグを修正
    -   通常のテーブルがパーティションテーブル[#26250](https://github.com/pingcap/tidb/issues/26250)に結合する場合、 `SELECT FOR UPDATE`ステートメントがエラーを返す問題を修正します。
    -   `PointGet`がロック[#26562](https://github.com/pingcap/tidb/pull/26562)を解決するライト バージョンを使用しない問題を修正します。

-   TiKV

    -   TiKV を v3.x からそれ以降のバージョンにアップグレードした後に発生するpanicの問題を修正します[#10902](https://github.com/tikv/tikv/issues/10902)
    -   破損したスナップショット ファイルによって引き起こされる潜在的なディスク フルの問題を修正します[#10813](https://github.com/tikv/tikv/issues/10813)
    -   TiKV コプロセッサーの低速ログでは、リクエストの処理に費やした時間のみを考慮するようにします[#10841](https://github.com/tikv/tikv/issues/10841)
    -   スロガー スレッドが過負荷になってキューがいっぱいになった場合、スレッドをブロックする代わりにログを削除します[#10841](https://github.com/tikv/tikv/issues/10841)
    -   コプロセッサーの処理がタイムアウトしたときに発生するpanicの問題を修正します[#10852](https://github.com/tikv/tikv/issues/10852)
    -   Titan が有効になっている 5.0 より前のバージョンからアップグレードするときに発生する TiKVpanicの問題を修正します[#10842](https://github.com/tikv/tikv/pull/10842)
    -   新しいバージョンの TiKV を v5.0.x にロールバックできない問題を修正します[#10842](https://github.com/tikv/tikv/pull/10842)
    -   TiKV が RocksDB にデータを取り込む前にファイルを削除する可能性がある問題を修正[#10438](https://github.com/tikv/tikv/issues/10438)
    -   左側の悲観的ロック[#26404](https://github.com/pingcap/tidb/issues/26404)によって引き起こされる解析エラーを修正します。

-   PD

    -   PD がダウンしたピアを時間内に修復しない問題を修正します[#4077](https://github.com/tikv/pd/issues/4077)
    -   デフォルトの配置ルールのレプリカ数が`replication.max-replicas`が更新された後も一定になる問題を修正[#3886](https://github.com/tikv/pd/issues/3886)
    -   TiKV [#3868](https://github.com/tikv/pd/issues/3868)をスケールアウトするときに PD がpanicになる可能性があるバグを修正
    -   クラスターにエビクト リーダー スケジューラ[#3697](https://github.com/tikv/pd/issues/3697)がある場合、ホットリージョンスケジューラが動作できないバグを修正

-   TiFlash

    -   TiFlash がMPP 接続の確立に失敗した場合に予期しない結果が発生する問題を修正
    -   TiFlash が複数のディスクに展開されている場合に発生するデータの不整合の潜在的な問題を修正
    -   TiFlashサーバーの負荷が高い場合に MPP クエリが誤った結果を取得するバグを修正
    -   MPP クエリが永久にハングする潜在的なバグを修正
    -   ストアの初期化と DDL を同時に操作する場合のpanicの問題を修正
    -   クエリに`CONSTANT` 、 `<` 、 `<=` 、 `>` 、 `>=` 、または`COLUMN`などのフィルターが含まれている場合に発生する誤った結果のバグを修正しました。
    -   複数の DDL 操作と同時に`Snapshot`が適用された場合の潜在的なpanicの問題を修正
    -   大量の書き込み時にメトリクスのストア サイズが不正確になる問題を修正
    -   TiFlash が長時間実行した後にデルタ データをガベージ コレクションできないという潜在的な問題を修正
    -   新しい照合順序が有効になっている場合に誤った結果が表示される問題を修正
    -   ロックを解決するときに発生する潜在的なpanicの問題を修正します。
    -   メトリクスに間違った値が表示される潜在的なバグを修正

-   ツール

    -   バックアップと復元 (BR)

        -   データのバックアップおよび復元中に平均速度が正確ではない問題を修正[#1405](https://github.com/pingcap/br/issues/1405)

    -   Dumpling

        -   [#322](https://github.com/pingcap/dumpling/issues/322)の MySQL バージョン (8.0.3 および 8.0.23) で`show table status`間違った結果を返すとDumplingが保留になる問題を修正します。
        -   デフォルト`sort-engine`オプション[#2373](https://github.com/pingcap/tiflow/issues/2373)での 4.0.x クラスターとの CLI 互換性の問題を修正します。

    -   TiCDC

        -   JSON エンコードにより、文字列型の値が`string`または`[]byte` [#2758](https://github.com/pingcap/tiflow/issues/2758)時にpanicが発生する可能性があるバグを修正
        -   OOM [#2673](https://github.com/pingcap/tiflow/issues/2673)を回避するために gRPC ウィンドウ サイズを縮小します。
        -   メモリ負荷が高い場合の gRPC `keepalive`エラーを修正[#2202](https://github.com/pingcap/tiflow/issues/2202)
        -   符号なし`tinyint`により TiCDC がpanicになるバグを修正[#2648](https://github.com/pingcap/tiflow/issues/2648)
        -   TiCDC オープン プロトコルの空の値の問題を修正しました。 1つのトランザクションに変更がない場合に空の値が出力されなくなりました。 [#2612](https://github.com/pingcap/tiflow/issues/2612)
        -   手動再起動中の DDL 処理のバグを修正[#2603](https://github.com/pingcap/tiflow/issues/2603)
        -   メタデータ[#2559](https://github.com/pingcap/tiflow/pull/2559)を管理するときに、 `EtcdWorker`のスナップショット分離が誤って違反される可能性がある問題を修正します。
        -   TiCDC がテーブル[#2230](https://github.com/pingcap/tiflow/issues/2230)を再スケジュールしているときに、複数のプロセッサが同じテーブルにデータを書き込む可能性があるバグを修正
        -   TiCDC が`ErrSchemaStorageTableMiss`エラー[#2422](https://github.com/pingcap/tiflow/issues/2422)を取得したときに変更フィードが予期せずリセットされる可能性があるバグを修正
        -   TiCDC が`ErrGCTTLExceeded`エラー[#2391](https://github.com/pingcap/tiflow/issues/2391)を取得した場合に変更フィードを削除できないバグを修正
        -   TiCDC が大きなテーブルを cdclog [#1259](https://github.com/pingcap/tiflow/issues/1259) [#2424](https://github.com/pingcap/tiflow/issues/2424)に同期できないというバグを修正しました。
