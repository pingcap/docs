---
title: TiDB 3.0 Beta Release Notes
---

# TiDB 3.0 ベータ版リリースノート {#tidb-3-0-beta-release-notes}

2019 年 1 月 19 日に、TiDB 3.0 ベータ版がリリースされました。対応する TiDB Ansible 3.0 Beta もリリースされています。 TiDB 3.0 ベータ版は、安定性、SQL オプティマイザー、統計、実行エンジンに重点を置いて TiDB 2.1 をベースに構築されています。

## TiDB {#tidb}

-   新機能
    -   サポートビュー
    -   サポートウィンドウの機能
    -   範囲分割のサポート
    -   ハッシュパーティショニングのサポート
-   SQLオプティマイザー
    -   `AggregationElimination` [#7676](https://github.com/pingcap/tidb/pull/7676)の最適化ルールを再サポートします。
    -   `NOT EXISTS`サブクエリを最適化し、Anti Semi Join [#7842](https://github.com/pingcap/tidb/pull/7842)に変換します。
    -   新しい Cascades オプティマイザーをサポートするには、 `tidb_enable_cascades_planner`変数を追加します。現在、カスケード オプティマイザーはまだ完全には実装されておらず、デフォルトではオフになっています[#7879](https://github.com/pingcap/tidb/pull/7879)
    -   トランザクションでのインデックス結合の使用のサポート[#7877](https://github.com/pingcap/tidb/pull/7877)
    -   外部結合での定数伝播を最適化することで、結合結果の外部テーブルに関連するフィルター条件を外部結合を通じて外部テーブルにプッシュダウンできるようになり、外部結合の無駄な計算が削減され、実行パフォーマンスが向上します[#7794](https://github.com/pingcap/tidb/pull/7794)
    -   冗長な`Project`演算子[#7909](https://github.com/pingcap/tidb/pull/7909)を避けるために、射影消去の最適化ルールを集計消去後の位置に調整します。
    -   `IFNULL`関数を最適化し、入力パラメータが非 NULL 属性を持つ場合はこの関数を削除します[#7924](https://github.com/pingcap/tidb/pull/7924)
    -   `_tidb_rowid`構築クエリのサポート範囲。テーブル全体のスキャンを回避し、クラスターのストレスを軽減します。 [#8047](https://github.com/pingcap/tidb/pull/8047)
    -   集計後に内部結合を実行するように`IN`サブクエリを最適化し、この最適化ルールを有効にしてデフォルトで開くかどうかを制御する`tidb_opt_insubq_to_join_and_agg`変数を追加します[#7531](https://github.com/pingcap/tidb/pull/7531)
    -   `DO`ステートメントでのサブクエリの使用のサポート[#8343](https://github.com/pingcap/tidb/pull/8343)
    -   外部結合除去の最適化ルールを追加して、不要なテーブル スキャンと結合操作を削減し、実行パフォーマンスを向上させます[#8021](https://github.com/pingcap/tidb/pull/8021)
    -   `TIDB_INLJ`オプティマイザーのヒント動作を変更すると、オプティマイザーはヒントで指定されたテーブルをインデックス結合[#8243](https://github.com/pingcap/tidb/pull/8243)内部テーブルとして使用します。
    -   `Prepare`ステートメントの実行プラン キャッシュが有効になるときに使用できるように、 `PointGet`広範囲で使用します[#8108](https://github.com/pingcap/tidb/pull/8108)
    -   貪欲`Join Reorder`アルゴリズムを導入して、複数のテーブルを結合する際の結合順序の選択を最適化します[#8394](https://github.com/pingcap/tidb/pull/8394)
    -   サポートビュー[#8757](https://github.com/pingcap/tidb/pull/8757)
    -   サポート窓口機能[#8630](https://github.com/pingcap/tidb/pull/8630)
    -   `TIDB_INLJ`が有効でない場合にクライアントに警告を返し、使いやすさを向上させます[#9037](https://github.com/pingcap/tidb/pull/9037)
    -   フィルタリング条件とテーブル統計に基づいてフィルタリングされたデータの統計を推定するサポート[#7921](https://github.com/pingcap/tidb/pull/7921)
    -   Range Partition [#8885](https://github.com/pingcap/tidb/pull/8885)のPartition Pruning最適化ルールを改善
-   SQLエグゼキュータ
    -   空の`ON`条件をサポートするように`Merge Join`演算子を最適化します[#9037](https://github.com/pingcap/tidb/pull/9037)
    -   ログを最適化し、ステートメント`EXECUTE`の実行時に使用されたユーザー変数を出力します[#7684](https://github.com/pingcap/tidb/pull/7684)
    -   `COMMIT`ステートメント[#7951](https://github.com/pingcap/tidb/pull/7951)の遅いクエリ情報を出力するようにログを最適化します。
    -   SQL チューニング プロセスを容易にする`EXPLAIN ANALYZE`機能のサポート[#7827](https://github.com/pingcap/tidb/pull/7827)
    -   多くの列を含む幅の広いテーブルの書き込みパフォーマンスを最適化する[#7935](https://github.com/pingcap/tidb/pull/7935)
    -   サポート`admin show next_row_id` [#8242](https://github.com/pingcap/tidb/pull/8242)
    -   `tidb_init_chunk_size`変数を追加して、実行エンジンによって使用される初期Chunkのサイズを制御します[#8480](https://github.com/pingcap/tidb/pull/8480)
    -   `shard_row_id_bits`を改善し、自動インクリメント ID をクロスチェックする[#8936](https://github.com/pingcap/tidb/pull/8936)
-   `Prepare`ステートメント
    -   `Prepare`異なるユーザー変数が入力された場合にクエリ プランが正しいことを保証するために、サブクエリを含むステートメントをクエリ プラン キャッシュに追加することを禁止します[#8064](https://github.com/pingcap/tidb/pull/8064)
    -   クエリ プラン キャッシュを最適化して、ステートメントに非決定的関数が含まれる場合でもプランをキャッシュできるようにします[#8105](https://github.com/pingcap/tidb/pull/8105)
    -   クエリ プラン キャッシュを最適化して、 `DELETE` / `UPDATE` / `INSERT`のクエリ プランをキャッシュできるようにします[#8107](https://github.com/pingcap/tidb/pull/8107)
    -   クエリ プラン キャッシュを最適化して、 `DEALLOCATE`ステートメント[#8332](https://github.com/pingcap/tidb/pull/8332)の実行時に対応するプランを削除します。
    -   メモリ使用量を制限することで、クエリ プラン キャッシュを最適化し、キャッシュするプランが多すぎることによって発生する TiDB OOM 問題を回避します[#8339](https://github.com/pingcap/tidb/pull/8339)
    -   `Prepare`ステートメントを最適化して、 `ORDER BY` / `GROUP BY` / `LIMIT`句の`?`プレースホルダーの使用をサポートします[#8206](https://github.com/pingcap/tidb/pull/8206)
-   権限管理
    -   `ANALYZE`ステートメント[#8486](https://github.com/pingcap/tidb/pull/8486)に権限チェックを追加します。
    -   `USE`ステートメント[#8414](https://github.com/pingcap/tidb/pull/8418)に権限チェックを追加します。
    -   `SET GLOBAL`ステートメント[#8837](https://github.com/pingcap/tidb/pull/8837)に権限チェックを追加します。
    -   `SHOW PROCESSLIST`ステートメント[#7858](https://github.com/pingcap/tidb/pull/7858)に権限チェックを追加します。
-   サーバ
    -   `Trace`機能[#9029](https://github.com/pingcap/tidb/pull/9029)をサポート
    -   プラグインフレームワーク[#8788](https://github.com/pingcap/tidb/pull/8788)のサポート
    -   `unix_socket`と TCP を同時に使用してデータベース[#8836](https://github.com/pingcap/tidb/pull/8836)に接続することをサポートします。
    -   `interactive_timeout`システム変数をサポートします[#8573](https://github.com/pingcap/tidb/pull/8573)
    -   `wait_timeout`システム変数をサポートします[#8346](https://github.com/pingcap/tidb/pull/8346)
    -   `tidb_batch_commit`変数[#8293](https://github.com/pingcap/tidb/pull/8293)を使用したステートメントの数に基づいてトランザクションを複数のトランザクションに分割することをサポートします。
    -   `ADMIN SHOW SLOW`ステートメントを使用した遅いログのチェックをサポート[#7785](https://github.com/pingcap/tidb/pull/7785)
-   互換性
    -   `ALLOW_INVALID_DATES` SQL モードをサポート[#9027](https://github.com/pingcap/tidb/pull/9027)
    -   `LoadData` CSV ファイルの耐障害性の向上[#9005](https://github.com/pingcap/tidb/pull/9005)
    -   MySQL 320 ハンドシェイク プロトコルのサポート[#8812](https://github.com/pingcap/tidb/pull/8812)
    -   符号なし`bigint`列を自動インクリメント列[#8181](https://github.com/pingcap/tidb/pull/8181)として使用するサポート
    -   `SHOW CREATE DATABASE IF NOT EXISTS`構文[#8926](https://github.com/pingcap/tidb/pull/8926)をサポートします。
    -   ユーザー変数を使用してウィンドウ関数の動作を模擬する MySQL の動作との互換性を向上させるために、フィルタリング条件にユーザー変数が含まれる場合、述語プッシュダウン操作を放棄します[#8412](https://github.com/pingcap/tidb/pull/8412)
-   DDL
    -   誤って削除されたテーブルの高速リカバリをサポート[#7937](https://github.com/pingcap/tidb/pull/7937)
    -   `ADD INDEX`の同時実行数の動的調整をサポート[#8295](https://github.com/pingcap/tidb/pull/8295)
    -   テーブルまたは列の文字セットの`utf8` / `utf8mb4` [#8037](https://github.com/pingcap/tidb/pull/8037)への変更をサポート
    -   デフォルトの文字セットを`utf8`から`utf8mb4`に変更します[#7965](https://github.com/pingcap/tidb/pull/7965)
    -   サポート範囲パーティション[#8011](https://github.com/pingcap/tidb/pull/8011)

## ツール {#tools}

-   TiDB Lightning
    -   SQL ステートメントから KV ペアへの変換が大幅に高速化[#110](https://github.com/pingcap/tidb-lightning/pull/110)
    -   インポートのパフォーマンスと安定性を向上させるために、単一テーブルのバッチ インポートをサポートします[#113](https://github.com/pingcap/tidb-lightning/pull/113)

## PD {#pd}

-   リージョンメタデータを個別に保存するには`RegionStorage`を追加します[#1237](https://github.com/pingcap/pd/pull/1237)
-   シャッフル ホットリージョンスケジューラ[#1361](https://github.com/pingcap/pd/pull/1361)を追加
-   スケジューリングパラメータ関連のメトリクスを追加[#1406](https://github.com/pingcap/pd/pull/1406)
-   クラスターラベル関連メトリックの追加[#1402](https://github.com/pingcap/pd/pull/1402)
-   インポートデータシミュレータ[#1263](https://github.com/pingcap/pd/pull/1263)の追加
-   リーダー選出[#1396](https://github.com/pingcap/pd/pull/1396)に関する`Watch`問題を修正

## TiKV {#tikv}

-   分散 GC [#3179](https://github.com/tikv/tikv/pull/3179)をサポート
-   Write Stall [#3606](https://github.com/tikv/tikv/pull/3606)を回避するには、スナップショットを適用する前に RocksDB レベル 0 ファイルを確認してください。
-   逆`raw_scan`および`raw_batch_scan`をサポート[#3742](https://github.com/tikv/tikv/pull/3724)
-   HTTP を使用した監視情報の取得のサポート[#3855](https://github.com/tikv/tikv/pull/3855)
-   DST のサポートの改善[#3786](https://github.com/tikv/tikv/pull/3786)
-   バッチ[#3931](https://github.com/tikv/tikv/pull/3913)でのRaftメッセージの送受信のサポート
-   新しいstorageエンジン Titan [#3985](https://github.com/tikv/tikv/pull/3985)を導入
-   gRPC を v1.17.2 にアップグレードする[#4023](https://github.com/tikv/tikv/pull/4023)
-   バッチ[#4043](https://github.com/tikv/tikv/pull/4043)でのクライアント要求の受信と応答の送信をサポート
-   マルチスレッド適用[#4044](https://github.com/tikv/tikv/pull/4044)サポート
-   マルチスレッドRaftstore [#4066](https://github.com/tikv/tikv/pull/4066)をサポート
