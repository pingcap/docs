---
title: TiDB 3.0 Beta Release Notes
---

# TiDB 3.0 ベータ リリース ノート {#tidb-3-0-beta-release-notes}

2019 年 1 月 19 日に、TiDB 3.0 ベータ版がリリースされました。対応する TiDB Ansible 3.0 Beta もリリースされています。 TiDB 3.0 Beta は TiDB 2.1 に基づいており、安定性、SQL オプティマイザー、統計、および実行エンジンに重点が置かれています。

## TiDB {#tidb}

-   新機能
    -   サポート ビュー
    -   サポート窓口機能
    -   範囲分割のサポート
    -   ハッシュパーティショニングをサポート
-   SQL オプティマイザー
    -   `AggregationElimination` [#7676](https://github.com/pingcap/tidb/pull/7676)の最適化ルールを再サポート
    -   `NOT EXISTS`サブクエリを最適化し、アンチ セミ ジョイン[#7842](https://github.com/pingcap/tidb/pull/7842)に変換する
    -   新しい Cascades オプティマイザーをサポートするために`tidb_enable_cascades_planner`変数を追加します。現在、Cascades オプティマイザはまだ完全には実装されておらず、デフォルトでオフになっています[#7879](https://github.com/pingcap/tidb/pull/7879)
    -   トランザクションでの Index Join の使用のサポート[#7877](https://github.com/pingcap/tidb/pull/7877)
    -   外部結合の定数伝播を最適化し、結合結果の外部テーブルに関連するフィルタリング条件が外部結合を介して外部テーブルにプッシュダウンできるようにし、外部結合の無駄な計算を減らし、実行パフォーマンスを向上させます[#7794](https://github.com/pingcap/tidb/pull/7794)
    -   冗長な演算子を避けるために、射影消去の最適化ルールを集計消去の後の位置に調整します。 `Project`演算子[#7909](https://github.com/pingcap/tidb/pull/7909)
    -   入力パラメーターが非 NULL 属性を持つ場合、 `IFNULL`関数を最適化し、この関数を削除します[#7924](https://github.com/pingcap/tidb/pull/7924)
    -   フル テーブル スキャンを回避し、クラスタ ストレスを軽減するための`_tidb_rowid`構築クエリのサポート範囲[#8047](https://github.com/pingcap/tidb/pull/8047)
    -   `IN`サブクエリを最適化して、集計後に内部結合を実行し、 `tidb_opt_insubq_to_join_and_agg`変数を追加して、この最適化ルールを有効にするかどうかを制御し、デフォルトで開く[#7531](https://github.com/pingcap/tidb/pull/7531)
    -   `DO`ステートメントでのサブクエリの使用のサポート[#8343](https://github.com/pingcap/tidb/pull/8343)
    -   外部結合除去の最適化ルールを追加して、不要なテーブル スキャンと結合操作を削減し、実行パフォーマンスを向上させます[#8021](https://github.com/pingcap/tidb/pull/8021)
    -   `TIDB_INLJ`オプティマイザの Hint の動作を変更すると、オプティマイザは Hint で指定されたテーブルを Index Join [#8243](https://github.com/pingcap/tidb/pull/8243)の内部テーブルとして使用します
    -   `Prepare`ステートメントの実行計画キャッシュが有効になったときに使用できるように、広い範囲で`PointGet`を使用します[#8108](https://github.com/pingcap/tidb/pull/8108)
    -   複数のテーブルを結合する際の結合順序の選択を最適化するために貪欲`Join Reorder`アルゴリズムを導入する[#8394](https://github.com/pingcap/tidb/pull/8394)
    -   サポートビュー[#8757](https://github.com/pingcap/tidb/pull/8757)
    -   サポートウィンドウ機能[#8630](https://github.com/pingcap/tidb/pull/8630)
    -   `TIDB_INLJ`有効でない場合にクライアントに警告を返し、使いやすさを向上させる[#9037](https://github.com/pingcap/tidb/pull/9037)
    -   フィルタリング条件とテーブル統計に基づいてフィルタリングされたデータの統計を推測するサポート[#7921](https://github.com/pingcap/tidb/pull/7921)
    -   Range Partition [#8885](https://github.com/pingcap/tidb/pull/8885)の Partition Pruning 最適化ルールを改善する
-   SQL エグゼキュータ
    -   `Merge Join`演算子を最適化して、空の`ON`条件[#9037](https://github.com/pingcap/tidb/pull/9037)をサポートする
    -   ログを最適化し、 `EXECUTE`ステートメントの実行時に使用されたユーザー変数を出力します[#7684](https://github.com/pingcap/tidb/pull/7684)
    -   ログを最適化して、 `COMMIT`ステートメント[#7951](https://github.com/pingcap/tidb/pull/7951)のスロー クエリ情報を出力します。
    -   `EXPLAIN ANALYZE` SQL チューニング プロセスを容易にする機能をサポート[#7827](https://github.com/pingcap/tidb/pull/7827)
    -   多くの列を持つ幅の広いテーブルの書き込みパフォーマンスを最適化する[#7935](https://github.com/pingcap/tidb/pull/7935)
    -   サポート`admin show next_row_id` [#8242](https://github.com/pingcap/tidb/pull/8242)
    -   `tidb_init_chunk_size`変数を追加して、実行エンジンが使用する初期Chunkのサイズを制御します[#8480](https://github.com/pingcap/tidb/pull/8480)
    -   改善`shard_row_id_bits`と自動インクリメント ID のクロスチェック[#8936](https://github.com/pingcap/tidb/pull/8936)
-   `Prepare`ステートメント
    -   サブクエリを含む`Prepare`ステートメントをクエリ プラン キャッシュに追加することを禁止して、異なるユーザー変数が入力されたときにクエリ プランが正しいことを保証する[#8064](https://github.com/pingcap/tidb/pull/8064)
    -   クエリ プラン キャッシュを最適化して、ステートメントに非決定論的関数が含まれている場合にプランを確実にキャッシュできるようにする[#8105](https://github.com/pingcap/tidb/pull/8105)
    -   クエリ プラン キャッシュを最適化して、 `DELETE` / `UPDATE` / `INSERT`のクエリ プランを確実にキャッシュできるようにする[#8107](https://github.com/pingcap/tidb/pull/8107)
    -   クエリ プラン キャッシュを最適化して、 `DEALLOCATE`ステートメントの実行時に対応するプランを削除する[#8332](https://github.com/pingcap/tidb/pull/8332)
    -   クエリ プラン キャッシュを最適化して、メモリ使用量を制限することで、あまりにも多くのプランをキャッシュすることによって発生する TiDB OOM の問題を回避します[#8339](https://github.com/pingcap/tidb/pull/8339)
    -   `ORDER BY` / `GROUP BY` / `LIMIT`句で`?`プレースホルダーの使用をサポートするために`Prepare`ステートメントを最適化します[#8206](https://github.com/pingcap/tidb/pull/8206)
-   権限管理
    -   `ANALYZE`ステートメント[#8486](https://github.com/pingcap/tidb/pull/8486)の特権チェックを追加します。
    -   `USE`ステートメント[#8414](https://github.com/pingcap/tidb/pull/8418)の特権チェックを追加します。
    -   `SET GLOBAL`ステートメント[#8837](https://github.com/pingcap/tidb/pull/8837)の特権チェックを追加します。
    -   `SHOW PROCESSLIST`ステートメント[#7858](https://github.com/pingcap/tidb/pull/7858)の特権チェックを追加します。
-   サーバ
    -   `Trace`機能[#9029](https://github.com/pingcap/tidb/pull/9029)をサポート
    -   プラグイン フレームワークのサポート[#8788](https://github.com/pingcap/tidb/pull/8788)
    -   `unix_socket`と TCP を同時に使用してデータベースに接続することをサポート[#8836](https://github.com/pingcap/tidb/pull/8836)
    -   `interactive_timeout`システム変数[#8573](https://github.com/pingcap/tidb/pull/8573)をサポート
    -   `wait_timeout`システム変数[#8346](https://github.com/pingcap/tidb/pull/8346)をサポート
    -   `tidb_batch_commit`変数[#8293](https://github.com/pingcap/tidb/pull/8293)を使用して、ステートメントの数に基づいてトランザクションを複数のトランザクションに分割するサポート
    -   スローログをチェックする`ADMIN SHOW SLOW`ステートメントを使用したサポート[#7785](https://github.com/pingcap/tidb/pull/7785)
-   互換性
    -   `ALLOW_INVALID_DATES` SQL モード[#9027](https://github.com/pingcap/tidb/pull/9027)をサポート
    -   CSVファイルのフォールトトレランスの向上`LoadData` [#9005](https://github.com/pingcap/tidb/pull/9005)
    -   MySQL 320 ハンドシェイク プロトコルのサポート[#8812](https://github.com/pingcap/tidb/pull/8812)
    -   自動インクリメント列[#8181](https://github.com/pingcap/tidb/pull/8181)として符号なし`bigint`列を使用するサポート
    -   `SHOW CREATE DATABASE IF NOT EXISTS`構文[#8926](https://github.com/pingcap/tidb/pull/8926)をサポート
    -   フィルタリング条件にユーザー変数が含まれている場合、述語プッシュダウン操作を放棄して、ユーザー変数を使用してウィンドウ関数の動作をモックする MySQL の動作との互換性を向上させます[#8412](https://github.com/pingcap/tidb/pull/8412)
-   DDL
    -   誤って削除されたテーブルの高速リカバリをサポート[#7937](https://github.com/pingcap/tidb/pull/7937)
    -   `ADD INDEX`の同時実行数の動的な調整をサポート[#8295](https://github.com/pingcap/tidb/pull/8295)
    -   テーブルまたは列の文字セットを`utf8` / `utf8mb4` [#8037](https://github.com/pingcap/tidb/pull/8037)に変更するサポート
    -   デフォルトの文字セットを`utf8`から`utf8mb4` [#7965](https://github.com/pingcap/tidb/pull/7965)に変更します
    -   サポート範囲パーティション[#8011](https://github.com/pingcap/tidb/pull/8011)

## ツール {#tools}

-   TiDB Lightning
    -   SQL ステートメントから KV ペアへの変換を大幅に高速化する[#110](https://github.com/pingcap/tidb-lightning/pull/110)
    -   単一テーブルのバッチ インポートをサポートして、インポートのパフォーマンスと安定性を向上させます[#113](https://github.com/pingcap/tidb-lightning/pull/113)

## PD {#pd}

-   リージョンのメタデータを個別に保存するには`RegionStorage`を追加します[#1237](https://github.com/pingcap/pd/pull/1237)
-   シャッフル ホットリージョンスケジューラを追加[#1361](https://github.com/pingcap/pd/pull/1361)
-   スケジューリング パラメーター関連のメトリックを追加する[#1406](https://github.com/pingcap/pd/pull/1406)
-   クラスター ラベル関連のメトリックを追加する[#1402](https://github.com/pingcap/pd/pull/1402)
-   インポート データ シミュレーター[#1263](https://github.com/pingcap/pd/pull/1263)を追加する
-   リーダー選挙に関する`Watch`問題を修正[#1396](https://github.com/pingcap/pd/pull/1396)

## TiKV {#tikv}

-   分散 GC をサポート[#3179](https://github.com/tikv/tikv/pull/3179)
-   Write Stall [#3606](https://github.com/tikv/tikv/pull/3606)を回避するために、スナップショットを適用する前に RocksDB レベル 0 ファイルを確認します。
-   リバース`raw_scan`および`raw_batch_scan` [#3742](https://github.com/tikv/tikv/pull/3724)をサポート
-   HTTP を使用したモニタリング情報取得のサポート[#3855](https://github.com/tikv/tikv/pull/3855)
-   DST をよりよくサポート[#3786](https://github.com/tikv/tikv/pull/3786)
-   バッチ[#3931](https://github.com/tikv/tikv/pull/3913)でRaftメッセージの送受信をサポート
-   新しいstorageエンジン Titan [#3985](https://github.com/tikv/tikv/pull/3985)の導入
-   gRPC を v1.17.2 にアップグレードする[#4023](https://github.com/tikv/tikv/pull/4023)
-   バッチ[#4043](https://github.com/tikv/tikv/pull/4043)でのクライアント要求の受信と応答の送信をサポート
-   マルチスレッド適用[#4044](https://github.com/tikv/tikv/pull/4044)をサポート
-   マルチスレッドRaftstore [#4066](https://github.com/tikv/tikv/pull/4066)をサポート
