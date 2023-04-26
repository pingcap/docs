---
title: TiDB 5.1.2 Release Notes
---

# TiDB 5.1.2 リリースノート {#tidb-5-1-2-release-notes}

リリース日：2021年9月27日

TiDB バージョン: 5.1.2

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   次のバグ修正により実行結果が変更され、アップグレードの非互換性が生じる可能性があります。

        -   `greatest(datetime) union null`が空の文字列[#26532](https://github.com/pingcap/tidb/issues/26532)を返す問題を修正
        -   `having`節が正しく動作しない場合がある問題を修正[#26496](https://github.com/pingcap/tidb/issues/26496)
        -   `between`式の前後の照合が異なる場合に発生する誤った実行結果を修正します[#27146](https://github.com/pingcap/tidb/issues/27146)
        -   `group_concat`関数の列に非ビン照合順序がある場合に発生する誤った実行結果を修正します[#27429](https://github.com/pingcap/tidb/issues/27429)
        -   新しい照合順序が有効になっている場合、複数の列で`count(distinct)`式を使用すると間違った結果が返される問題を修正します[#27091](https://github.com/pingcap/tidb/issues/27091)
        -   `extract`関数の引数が負の期間[#27236](https://github.com/pingcap/tidb/issues/27236)の場合に発生する結果の誤りを修正します。
        -   `SQL_MODE`が &#39;STRICT_TRANS_TABLES&#39; [#26762](https://github.com/pingcap/tidb/issues/26762)の場合、無効な日付を挿入してもエラーが報告されない問題を修正します。
        -   `SQL_MODE`が &#39;NO_ZERO_IN_DATE&#39; [#26766](https://github.com/pingcap/tidb/issues/26766)の場合、無効なデフォルト日付を使用してもエラーが報告されない問題を修正します。

-   ツール

    -   TiCDC

        -   互換性のあるバージョンを`5.1.0-alpha`から`5.2.0-alpha` [#2659](https://github.com/pingcap/tiflow/pull/2659)に設定します

## 改良点 {#improvements}

-   TiDB

    -   ヒストグラムの行数によって自動分析をトリガーし、このトリガー アクションの精度を高めます[#24237](https://github.com/pingcap/tidb/issues/24237)

-   TiKV

    -   TiCDC 構成の動的変更のサポート[#10645](https://github.com/tikv/tikv/issues/10645)
    -   Resolved TS メッセージのサイズを小さくしてネットワーク帯域幅を節約する[#2448](https://github.com/pingcap/tiflow/issues/2448)
    -   1 つのストアから報告されるハートビートメッセージ内のピア統計のカウントを制限する[#10621](https://github.com/tikv/tikv/pull/10621)

-   PD

    -   空のリージョンのスケジュールを許可し、分散範囲スケジューラ[#4117](https://github.com/tikv/pd/pull/4117)で別の許容値構成を使用します
    -   PD 間のリージョン情報の同期のパフォーマンスを向上させます[#3933](https://github.com/tikv/pd/pull/3933)
    -   生成されたオペレーターに基づいてストアの再試行制限を動的に調整するサポート[#3744](https://github.com/tikv/pd/issues/3744)

-   TiFlash

    -   `DATE()`機能をサポート
    -   インスタンスごとの書き込みスループット用に Grafana パネルを追加する
    -   `leader-read`プロセスのパフォーマンスを最適化する
    -   MPP タスクをキャンセルするプロセスを加速する

-   ツール

    -   TiCDC

        -   ユニファイド ソーターがデータの並べ替えにメモリを使用している場合のメモリ管理を最適化する[#2553](https://github.com/pingcap/tiflow/issues/2553)
        -   同時実行性が高い場合、より少ないゴルーチンのためにワーカープールを最適化します[#2211](https://github.com/pingcap/tiflow/issues/2211)
        -   テーブルのリージョンがTiKV ノードから移動するときのゴルーチンの使用量を減らす[#2284](https://github.com/pingcap/tiflow/issues/2284)
        -   グローバル gRPC 接続プールを追加し、KV クライアント間で gRPC 接続を共有する[#2534](https://github.com/pingcap/tiflow/pull/2534)
        -   メジャー バージョンとマイナー バージョンをまたがる TiCDC クラスタの動作を禁止する[#2599](https://github.com/pingcap/tiflow/pull/2599)

    -   Dumpling

        -   `START TRANSACTION ... WITH CONSISTENT SNAPSHOT`および`SHOW CREATE TABLE` [#309](https://github.com/pingcap/dumpling/issues/309)をサポートしていない MySQL 互換データベースのバックアップをサポート

## バグの修正 {#bug-fixes}

-   TiDB

    -   ハッシュ列が`ENUM`タイプ[#27893](https://github.com/pingcap/tidb/issues/27893)の場合に、インデックス ハッシュ結合の潜在的に間違った結果を修正します。
    -   アイドル状態の接続をリサイクルすると、まれにリクエストの送信がブロックされる可能性があるというバッチ クライアントのバグを修正します[#27678](https://github.com/pingcap/tidb/pull/27678)
    -   `FLOAT64`型のオーバーフローチェックがMySQL [#23897](https://github.com/pingcap/tidb/issues/23897)と異なる問題を修正
    -   TiDB が`pd is timeout`エラー[#26147](https://github.com/pingcap/tidb/issues/26147)を返すはずなのに`unknow`エラーを返す問題を修正
    -   `case when`式[#26662](https://github.com/pingcap/tidb/issues/26662)の間違った文字セットと照合順序を修正します
    -   MPP クエリの潜在的な`can not found column in Schema column`エラーを修正します[#28148](https://github.com/pingcap/tidb/pull/28148)
    -   TiFlashのシャットダウン時に TiDB がpanicことがあるバグを修正[#28096](https://github.com/pingcap/tidb/issues/28096)
    -   `enum like 'x%'` [#27130](https://github.com/pingcap/tidb/issues/27130)を使用することによって引き起こされる間違った範囲の問題を修正します
    -   IndexLookupJoin [#27410](https://github.com/pingcap/tidb/issues/27410)で使用した場合の Common Table Expression (CTE) デッド ロックの問題を修正します。
    -   再試行可能なデッドロックが誤って`INFORMATION_SCHEMA.DEADLOCKS`テーブルに記録されるバグを修正[#27400](https://github.com/pingcap/tidb/issues/27400)
    -   `TABLESAMPLE`分割されたテーブルからのクエリ結果が期待どおりにソートされない問題を修正します[#27349](https://github.com/pingcap/tidb/issues/27349)
    -   未使用の`/debug/sub-optimal-plan` HTTP API を削除する[#27265](https://github.com/pingcap/tidb/pull/27265)
    -   ハッシュパーティションテーブルていないデータを処理する場合、クエリが間違った結果を返すことがあるというバグを修正します[#26569](https://github.com/pingcap/tidb/issues/26569)
    -   `NO_UNSIGNED_SUBTRACTION`を[#26765](https://github.com/pingcap/tidb/issues/26765)に設定するとパーティション作成に失敗する不具合を修正
    -   `Apply`を`Join` [#26958](https://github.com/pingcap/tidb/issues/26958)に変換すると`distinct`フラグが欠落する問題を修正
    -   新しく復旧したTiFlashノードのブロック期間を設定して、この時間中にクエリがブロックされないようにします[#26897](https://github.com/pingcap/tidb/pull/26897)
    -   CTE が複数回参照された場合に発生する可能性があるバグを修正します[#26212](https://github.com/pingcap/tidb/issues/26212)
    -   MergeJoin 使用時の CTE バグを修正[#25474](https://github.com/pingcap/tidb/issues/25474)
    -   通常のテーブルがパーティションテーブルを結合するときに、 `SELECT FOR UPDATE`ステートメントがデータを正しくロックしないというバグを修正します[#26251](https://github.com/pingcap/tidb/issues/26251)
    -   通常のテーブルがパーティションテーブルを結合するときに`SELECT FOR UPDATE`ステートメントがエラーを返す問題を修正します[#26250](https://github.com/pingcap/tidb/issues/26250)
    -   `PointGet`が解決ロック[#26562](https://github.com/pingcap/tidb/pull/26562)のライトバージョンを使用しない問題を修正

-   TiKV

    -   TiKV を v3.x から[#10902](https://github.com/tikv/tikv/issues/10902)以降のバージョンにアップグレードした後に発生するpanicの問題を修正します。
    -   破損したスナップショット ファイルが原因で発生する可能性のあるディスクがいっぱいになる問題を修正します[#10813](https://github.com/tikv/tikv/issues/10813)
    -   TiKV コプロセッサーのスローログを、リクエストの処理に費やされた時間のみを考慮するようにします[#10841](https://github.com/tikv/tikv/issues/10841)
    -   slogger スレッドが過負荷になり、キューがいっぱいになったときに、スレッドをブロックする代わりにログを削除します[#10841](https://github.com/tikv/tikv/issues/10841)
    -   コプロセッサー要求の処理がタイムアウトしたときに発生するpanicの問題を修正します[#10852](https://github.com/tikv/tikv/issues/10852)
    -   Titan を有効にして 5.0 より前のバージョンからアップグレードするときに発生する TiKVpanicの問題を修正します[#10842](https://github.com/tikv/tikv/pull/10842)
    -   新しいバージョンの TiKV が v5.0.x にロールバックできない問題を修正[#10842](https://github.com/tikv/tikv/pull/10842)
    -   TiKV が RocksDB にデータを取り込む前にファイルを削除する可能性がある問題を修正します[#10438](https://github.com/tikv/tikv/issues/10438)
    -   左悲観的ロックによる解析エラーを修正[#26404](https://github.com/pingcap/tidb/issues/26404)

-   PD

    -   PD が時間[#4077](https://github.com/tikv/pd/issues/4077)でダウンしたピアを修正しない問題を修正します。
    -   `replication.max-replicas`が更新された後、デフォルトの配置ルールのレプリカ数が一定のままになる問題を修正します[#3886](https://github.com/tikv/pd/issues/3886)
    -   TiKV [#3868](https://github.com/tikv/pd/issues/3868)をスケールアウトすると PD がpanicになることがあるバグを修正
    -   クラスターに evict リーダー スケジューラー[#3697](https://github.com/tikv/pd/issues/3697)がある場合、ホットリージョンスケジューラーが動作しないというバグを修正します。

-   TiFlash

    -   TiFlash がMPP 接続の確立に失敗したときの予期しない結果の問題を修正
    -   TiFlash が複数のディスクに展開されている場合に発生する可能性のあるデータの不整合の問題を修正します。
    -   TiFlashサーバーの負荷が高い場合に MPP クエリが間違った結果になるバグを修正
    -   MPP クエリが永久にハングする潜在的なバグを修正します
    -   ストアの初期化と DDL を同時に操作する際のpanicの問題を修正
    -   クエリに`CONSTANT` 、 `<` 、 `<=` 、 `>` 、 `>=` 、または`COLUMN`などのフィルターが含まれている場合に発生する誤った結果のバグを修正します
    -   複数の DDL 操作で`Snapshot`同時に適用された場合に発生する可能性のpanicの問題を修正します
    -   負荷の高い書き込みでメトリクスのストア サイズが不正確になる問題を修正
    -   長時間実行した後、 TiFlash がデルタ データをガベージ コレクションできないという潜在的な問題を修正します。
    -   新しい照合順序が有効になっている場合に間違った結果が表示される問題を修正
    -   ロックを解決するときに発生する潜在的なpanicの問題を修正します
    -   メトリクスが間違った値を表示する潜在的なバグを修正

-   ツール

    -   バックアップと復元 (BR)

        -   データのバックアップと復元中に平均速度が正確でない問題を修正[#1405](https://github.com/pingcap/br/issues/1405)

    -   Dumpling

        -   一部の MySQL バージョン (8.0.3 および 8.0.23) で誤った結果が返された場合にDumplingが`show table status`中になる問題を修正します[#322](https://github.com/pingcap/dumpling/issues/322)
        -   デフォルト`sort-engine`オプション[#2373](https://github.com/pingcap/tiflow/issues/2373)での 4.0.x クラスターの CLI 互換性の問題を修正します。

    -   TiCDC

        -   `string`または`[]byte` [#2758](https://github.com/pingcap/tiflow/issues/2758)列型の値を処理するときに、JSON エンコーディングがpanicを引き起こす可能性があるというバグを修正します。
        -   OOM [#2673](https://github.com/pingcap/tiflow/issues/2673)を回避するために gRPC ウィンドウ サイズを小さくする
        -   高いメモリプレッシャ下での gRPC `keepalive`エラーを修正します[#2202](https://github.com/pingcap/tiflow/issues/2202)
        -   署名されていない`tinyint`が TiCDC をpanic[#2648](https://github.com/pingcap/tiflow/issues/2648)にするバグを修正
        -   TiCDC Open Protocol の空の値の問題を修正します。 1 つのトランザクションで変更がない場合、空の値が出力されなくなりました。 [#2612](https://github.com/pingcap/tiflow/issues/2612)
        -   手動再起動中の DDL 処理のバグを修正します[#2603](https://github.com/pingcap/tiflow/issues/2603)
        -   メタデータの管理時に`EtcdWorker`のスナップショット分離が誤って違反される可能性がある問題を修正します[#2559](https://github.com/pingcap/tiflow/pull/2559)
        -   TiCDC がテーブルを再スケジュールしているときに、複数のプロセッサが同じテーブルにデータを書き込む可能性があるというバグを修正します[#2230](https://github.com/pingcap/tiflow/issues/2230)
        -   TiCDC が`ErrSchemaStorageTableMiss`エラー[#2422](https://github.com/pingcap/tiflow/issues/2422)を取得したときに、changefeed が予期せずリセットされることがあるというバグを修正します。
        -   TiCDC が`ErrGCTTLExceeded`エラー[#2391](https://github.com/pingcap/tiflow/issues/2391)を取得すると、changefeed を削除できないバグを修正します。
        -   TiCDC が大きなテーブルを cdclog に同期できないバグを修正[#1259](https://github.com/pingcap/tiflow/issues/1259) [#2424](https://github.com/pingcap/tiflow/issues/2424)
