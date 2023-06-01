---
title: TiDB 5.1.2 Release Notes
---

# TiDB 5.1.2 リリースノート {#tidb-5-1-2-release-notes}

リリース日：2021年9月27日

TiDB バージョン: 5.1.2

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   次のバグ修正により実行結果が変更され、アップグレードの非互換性が発生する可能性があります。

        -   `greatest(datetime) union null`が空の文字列[<a href="https://github.com/pingcap/tidb/issues/26532">#26532</a>](https://github.com/pingcap/tidb/issues/26532)を返す問題を修正
        -   `having`句が正しく動作しない場合がある問題を修正[<a href="https://github.com/pingcap/tidb/issues/26496">#26496</a>](https://github.com/pingcap/tidb/issues/26496)
        -   `between`式の前後の照合順序が異なる場合に発生する間違った実行結果を修正します[<a href="https://github.com/pingcap/tidb/issues/27146">#27146</a>](https://github.com/pingcap/tidb/issues/27146)
        -   `group_concat`関数の列に非ビン照合順序がある場合に発生する間違った実行結果を修正します[<a href="https://github.com/pingcap/tidb/issues/27429">#27429</a>](https://github.com/pingcap/tidb/issues/27429)
        -   新しい照合順序が有効になっている場合に、複数の列で`count(distinct)`式を使用すると間違った結果が返される問題を修正します[<a href="https://github.com/pingcap/tidb/issues/27091">#27091</a>](https://github.com/pingcap/tidb/issues/27091)
        -   `extract`関数の引数が負の持続時間の場合に発生する結果が間違っていたのを修正[<a href="https://github.com/pingcap/tidb/issues/27236">#27236</a>](https://github.com/pingcap/tidb/issues/27236)
        -   `SQL_MODE`が &#39;STRICT_TRANS_TABLES&#39; [<a href="https://github.com/pingcap/tidb/issues/26762">#26762</a>](https://github.com/pingcap/tidb/issues/26762)の場合、無効な日付を挿入してもエラーが報告されない問題を修正します。
        -   `SQL_MODE`が &#39;NO_ZERO_IN_DATE&#39; [<a href="https://github.com/pingcap/tidb/issues/26766">#26766</a>](https://github.com/pingcap/tidb/issues/26766)の場合、無効なデフォルト日付を使用してもエラーが報告されない問題を修正します。

-   ツール

    -   TiCDC

        -   互換性のあるバージョンを`5.1.0-alpha` ～ `5.2.0-alpha`で設定します[<a href="https://github.com/pingcap/tiflow/pull/2659">#2659</a>](https://github.com/pingcap/tiflow/pull/2659)

## 改善点 {#improvements}

-   TiDB

    -   ヒストグラム行数による自動分析をトリガーし、このトリガー アクションの精度を高めます[<a href="https://github.com/pingcap/tidb/issues/24237">#24237</a>](https://github.com/pingcap/tidb/issues/24237)

-   TiKV

    -   TiCDC 構成の動的変更のサポート[<a href="https://github.com/tikv/tikv/issues/10645">#10645</a>](https://github.com/tikv/tikv/issues/10645)
    -   解決済み TS メッセージのサイズを削減して、ネットワーク帯域幅を節約します[<a href="https://github.com/pingcap/tiflow/issues/2448">#2448</a>](https://github.com/pingcap/tiflow/issues/2448)
    -   単一ストアによって報告されるハートビートメッセージ内のピア統計の数を制限する[<a href="https://github.com/tikv/tikv/pull/10621">#10621</a>](https://github.com/tikv/tikv/pull/10621)

-   PD

    -   空の領域をスケジュールできるようにし、散布範囲スケジューラ[<a href="https://github.com/tikv/pd/pull/4117">#4117</a>](https://github.com/tikv/pd/pull/4117)で別の許容値構成を使用します。
    -   PD 間のリージョン情報の同期パフォーマンスを向上[<a href="https://github.com/tikv/pd/pull/3933">#3933</a>](https://github.com/tikv/pd/pull/3933)
    -   生成された演算子に基づいてストアの再試行制限を動的に調整するサポート[<a href="https://github.com/tikv/pd/issues/3744">#3744</a>](https://github.com/tikv/pd/issues/3744)

-   TiFlash

    -   `DATE()`機能をサポート
    -   インスタンスごとの書き込みスループットのために Grafana パネルを追加します
    -   `leader-read`プロセスのパフォーマンスを最適化する
    -   MPP タスクのキャンセルプロセスを加速する

-   ツール

    -   TiCDC

        -   統合ソーターがデータの並べ替えにメモリを使用している場合、メモリ管理を最適化します[<a href="https://github.com/pingcap/tiflow/issues/2553">#2553</a>](https://github.com/pingcap/tiflow/issues/2553)
        -   同時実行性が高い場合、ゴルーチンを減らすためにワーカープールを最適化する[<a href="https://github.com/pingcap/tiflow/issues/2211">#2211</a>](https://github.com/pingcap/tiflow/issues/2211)
        -   テーブルのリージョンがTiKV ノードから転送される場合の goroutine の使用量を削減します[<a href="https://github.com/pingcap/tiflow/issues/2284">#2284</a>](https://github.com/pingcap/tiflow/issues/2284)
        -   グローバル gRPC 接続プールを追加し、KV クライアント間で gRPC 接続を共有する[<a href="https://github.com/pingcap/tiflow/pull/2534">#2534</a>](https://github.com/pingcap/tiflow/pull/2534)
        -   メジャー バージョンとマイナー バージョンにまたがる TiCDC クラスターの操作を禁止する[<a href="https://github.com/pingcap/tiflow/pull/2599">#2599</a>](https://github.com/pingcap/tiflow/pull/2599)

    -   Dumpling

        -   `START TRANSACTION ... WITH CONSISTENT SNAPSHOT`と`SHOW CREATE TABLE`をサポートしていない MySQL 互換データベースのバックアップをサポート[<a href="https://github.com/pingcap/dumpling/issues/309">#309</a>](https://github.com/pingcap/dumpling/issues/309)

## バグの修正 {#bug-fixes}

-   TiDB

    -   ハッシュ列が`ENUM`タイプ[<a href="https://github.com/pingcap/tidb/issues/27893">#27893</a>](https://github.com/pingcap/tidb/issues/27893)の場合のインデックス ハッシュ結合の潜在的な誤った結果を修正しました。
    -   アイドル状態の接続をリサイクルすると、まれにリクエストの送信がブロックされる可能性があるバッチ クライアントのバグを修正します[<a href="https://github.com/pingcap/tidb/pull/27678">#27678</a>](https://github.com/pingcap/tidb/pull/27678)
    -   `FLOAT64`種のオーバーフローチェックが[<a href="https://github.com/pingcap/tidb/issues/23897">#23897</a>](https://github.com/pingcap/tidb/issues/23897)と異なる問題を修正
    -   TiDB が`pd is timeout`エラー[<a href="https://github.com/pingcap/tidb/issues/26147">#26147</a>](https://github.com/pingcap/tidb/issues/26147)を返すはずなのに`unknow`エラーを返す問題を修正
    -   `case when`式[<a href="https://github.com/pingcap/tidb/issues/26662">#26662</a>](https://github.com/pingcap/tidb/issues/26662)の間違った文字セットと照合順序を修正します。
    -   MPP クエリ[<a href="https://github.com/pingcap/tidb/pull/28148">#28148</a>](https://github.com/pingcap/tidb/pull/28148)の潜在的なエラー`can not found column in Schema column`を修正
    -   TiFlashのシャットダウン時に TiDB がpanic可能性があるバグを修正[<a href="https://github.com/pingcap/tidb/issues/28096">#28096</a>](https://github.com/pingcap/tidb/issues/28096)
    -   `enum like 'x%'` [<a href="https://github.com/pingcap/tidb/issues/27130">#27130</a>](https://github.com/pingcap/tidb/issues/27130)の使用によって引き起こされる誤った範囲の問題を修正
    -   IndexLookupJoin [<a href="https://github.com/pingcap/tidb/issues/27410">#27410</a>](https://github.com/pingcap/tidb/issues/27410)で使用した場合の Common Table Expression (CTE) デッドロックの問題を修正
    -   再試行可能なデッドロックが`INFORMATION_SCHEMA.DEADLOCKS`テーブル[<a href="https://github.com/pingcap/tidb/issues/27400">#27400</a>](https://github.com/pingcap/tidb/issues/27400)に誤って記録されるバグを修正
    -   `TABLESAMPLE`パーティションテーブルからのクエリ結果が期待どおりに並べ替えられない問題を修正します[<a href="https://github.com/pingcap/tidb/issues/27349">#27349</a>](https://github.com/pingcap/tidb/issues/27349)
    -   未使用の`/debug/sub-optimal-plan` HTTP API [<a href="https://github.com/pingcap/tidb/pull/27265">#27265</a>](https://github.com/pingcap/tidb/pull/27265)を削除します。
    -   ハッシュパーティションテーブルが符号なしデータを扱う場合、クエリが間違った結果を返すことがあるバグを修正[<a href="https://github.com/pingcap/tidb/issues/26569">#26569</a>](https://github.com/pingcap/tidb/issues/26569)
    -   `NO_UNSIGNED_SUBTRACTION`を[<a href="https://github.com/pingcap/tidb/issues/26765">#26765</a>](https://github.com/pingcap/tidb/issues/26765)に設定するとパーティションの作成に失敗するバグを修正
    -   `Apply`を`Join` [<a href="https://github.com/pingcap/tidb/issues/26958">#26958</a>](https://github.com/pingcap/tidb/issues/26958)に変換するときに`distinct`フラグが欠落する問題を修正
    -   新しく回復されたTiFlashノードのブロック期間を設定して、この期間中のクエリのブロックを回避します[<a href="https://github.com/pingcap/tidb/pull/26897">#26897</a>](https://github.com/pingcap/tidb/pull/26897)
    -   CTE が複数回参照された場合に発生する可能性があるバグを修正[<a href="https://github.com/pingcap/tidb/issues/26212">#26212</a>](https://github.com/pingcap/tidb/issues/26212)
    -   MergeJoin 使用時の CTE バグを修正[<a href="https://github.com/pingcap/tidb/issues/25474">#25474</a>](https://github.com/pingcap/tidb/issues/25474)
    -   通常のテーブルがパーティションテーブル[<a href="https://github.com/pingcap/tidb/issues/26251">#26251</a>](https://github.com/pingcap/tidb/issues/26251)に結合する場合、 `SELECT FOR UPDATE`ステートメントがデータを正しくロックしないバグを修正
    -   通常のテーブルがパーティションテーブル[<a href="https://github.com/pingcap/tidb/issues/26250">#26250</a>](https://github.com/pingcap/tidb/issues/26250)に結合する場合、 `SELECT FOR UPDATE`ステートメントがエラーを返す問題を修正します。
    -   `PointGet`がロック[<a href="https://github.com/pingcap/tidb/pull/26562">#26562</a>](https://github.com/pingcap/tidb/pull/26562)を解決するライト バージョンを使用しない問題を修正します。

-   TiKV

    -   TiKV を v3.x からそれ以降のバージョンにアップグレードした後に発生するpanicの問題を修正します[<a href="https://github.com/tikv/tikv/issues/10902">#10902</a>](https://github.com/tikv/tikv/issues/10902)
    -   破損したスナップショット ファイルによって引き起こされる潜在的なディスク フルの問題を修正します[<a href="https://github.com/tikv/tikv/issues/10813">#10813</a>](https://github.com/tikv/tikv/issues/10813)
    -   TiKV コプロセッサーの低速ログでは、リクエストの処理に費やした時間のみを考慮するようにします[<a href="https://github.com/tikv/tikv/issues/10841">#10841</a>](https://github.com/tikv/tikv/issues/10841)
    -   スロガー スレッドが過負荷になってキューがいっぱいになった場合、スレッドをブロックする代わりにログを削除します[<a href="https://github.com/tikv/tikv/issues/10841">#10841</a>](https://github.com/tikv/tikv/issues/10841)
    -   コプロセッサーの処理がタイムアウトしたときに発生するpanicの問題を修正します[<a href="https://github.com/tikv/tikv/issues/10852">#10852</a>](https://github.com/tikv/tikv/issues/10852)
    -   Titan が有効になっている 5.0 より前のバージョンからアップグレードするときに発生する TiKVpanicの問題を修正します[<a href="https://github.com/tikv/tikv/pull/10842">#10842</a>](https://github.com/tikv/tikv/pull/10842)
    -   新しいバージョンの TiKV を v5.0.x にロールバックできない問題を修正します[<a href="https://github.com/tikv/tikv/pull/10842">#10842</a>](https://github.com/tikv/tikv/pull/10842)
    -   TiKV が RocksDB にデータを取り込む前にファイルを削除する可能性がある問題を修正[<a href="https://github.com/tikv/tikv/issues/10438">#10438</a>](https://github.com/tikv/tikv/issues/10438)
    -   左側の悲観的ロック[<a href="https://github.com/pingcap/tidb/issues/26404">#26404</a>](https://github.com/pingcap/tidb/issues/26404)によって引き起こされる解析エラーを修正します。

-   PD

    -   PD がダウンしたピアを時間内に修復しない問題を修正します[<a href="https://github.com/tikv/pd/issues/4077">#4077</a>](https://github.com/tikv/pd/issues/4077)
    -   デフォルトの配置ルールのレプリカ数が`replication.max-replicas`が更新された後も一定になる問題を修正[<a href="https://github.com/tikv/pd/issues/3886">#3886</a>](https://github.com/tikv/pd/issues/3886)
    -   TiKV [<a href="https://github.com/tikv/pd/issues/3868">#3868</a>](https://github.com/tikv/pd/issues/3868)をスケールアウトするときに PD がpanicになる可能性があるバグを修正
    -   クラスターにエビクト リーダー スケジューラ[<a href="https://github.com/tikv/pd/issues/3697">#3697</a>](https://github.com/tikv/pd/issues/3697)がある場合、ホットリージョンスケジューラが動作できないバグを修正

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

        -   データのバックアップおよび復元中に平均速度が正確ではない問題を修正[<a href="https://github.com/pingcap/br/issues/1405">#1405</a>](https://github.com/pingcap/br/issues/1405)

    -   Dumpling

        -   [<a href="https://github.com/pingcap/dumpling/issues/322">#322</a>](https://github.com/pingcap/dumpling/issues/322)の MySQL バージョン (8.0.3 および 8.0.23) で`show table status`間違った結果を返すとDumplingが保留になる問題を修正します。
        -   デフォルト`sort-engine`オプション[<a href="https://github.com/pingcap/tiflow/issues/2373">#2373</a>](https://github.com/pingcap/tiflow/issues/2373)での 4.0.x クラスターとの CLI 互換性の問題を修正します。

    -   TiCDC

        -   JSON エンコードにより、文字列型の値が`string`または`[]byte` [<a href="https://github.com/pingcap/tiflow/issues/2758">#2758</a>](https://github.com/pingcap/tiflow/issues/2758)時にpanicが発生する可能性があるバグを修正
        -   OOM [<a href="https://github.com/pingcap/tiflow/issues/2673">#2673</a>](https://github.com/pingcap/tiflow/issues/2673)を回避するために gRPC ウィンドウ サイズを縮小します。
        -   メモリ負荷が高い場合の gRPC `keepalive`エラーを修正[<a href="https://github.com/pingcap/tiflow/issues/2202">#2202</a>](https://github.com/pingcap/tiflow/issues/2202)
        -   符号なし`tinyint`により TiCDC がpanicになるバグを修正[<a href="https://github.com/pingcap/tiflow/issues/2648">#2648</a>](https://github.com/pingcap/tiflow/issues/2648)
        -   TiCDC オープン プロトコルの空の値の問題を修正しました。 1つのトランザクションに変更がない場合に空の値が出力されなくなりました。 [<a href="https://github.com/pingcap/tiflow/issues/2612">#2612</a>](https://github.com/pingcap/tiflow/issues/2612)
        -   手動再起動中の DDL 処理のバグを修正[<a href="https://github.com/pingcap/tiflow/issues/2603">#2603</a>](https://github.com/pingcap/tiflow/issues/2603)
        -   メタデータ[<a href="https://github.com/pingcap/tiflow/pull/2559">#2559</a>](https://github.com/pingcap/tiflow/pull/2559)を管理するときに、 `EtcdWorker`のスナップショット分離が誤って違反される可能性がある問題を修正します。
        -   TiCDC がテーブル[<a href="https://github.com/pingcap/tiflow/issues/2230">#2230</a>](https://github.com/pingcap/tiflow/issues/2230)を再スケジュールしているときに、複数のプロセッサが同じテーブルにデータを書き込む可能性があるバグを修正
        -   TiCDC が`ErrSchemaStorageTableMiss`エラー[<a href="https://github.com/pingcap/tiflow/issues/2422">#2422</a>](https://github.com/pingcap/tiflow/issues/2422)を取得したときに変更フィードが予期せずリセットされる可能性があるバグを修正
        -   TiCDC が`ErrGCTTLExceeded`エラー[<a href="https://github.com/pingcap/tiflow/issues/2391">#2391</a>](https://github.com/pingcap/tiflow/issues/2391)を取得した場合に変更フィードを削除できないバグを修正
        -   TiCDC が大きなテーブルを cdclog [<a href="https://github.com/pingcap/tiflow/issues/1259">#1259</a>](https://github.com/pingcap/tiflow/issues/1259) [<a href="https://github.com/pingcap/tiflow/issues/2424">#2424</a>](https://github.com/pingcap/tiflow/issues/2424)に同期できないというバグを修正しました。
