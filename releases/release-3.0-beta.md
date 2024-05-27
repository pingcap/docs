---
title: TiDB 3.0 Beta Release Notes
summary: 2019 年 1 月 19 日にリリースされた TiDB 3.0 ベータ版は、安定性、SQL オプティマイザー、統計、実行エンジンに重点を置いています。新しい機能には、ビュー、ウィンドウ関数、範囲パーティション、ハッシュ パーティションのサポートが含まれます。SQL オプティマイザーは、トランザクションでのインデックス結合のサポート、定数伝播の最適化、DO ステートメントでのサブクエリのサポートなど、さまざまな最適化によって強化されました。SQL エグゼキューターも最適化され、パフォーマンスが向上しました。権限管理、サーバー、互換性、DDL がすべて改善されました。TiDB TiDB Lightning は、単一テーブルのバッチ インポートをサポートするようになり、PD と TiKV にもさまざまな機能強化と新機能が追加されました。
---

# TiDB 3.0 ベータ リリース ノート {#tidb-3-0-beta-release-notes}

2019 年 1 月 19 日に、TiDB 3.0 ベータ版がリリースされました。対応する TiDB Ansible 3.0 ベータ版もリリースされました。TiDB 3.0 ベータ版は、安定性、SQL オプティマイザー、統計、実行エンジンに重点を置いて TiDB 2.1 をベースに構築されています。

## ティビ {#tidb}

-   新機能
    -   サポートビュー
    -   ウィンドウ関数のサポート
    -   範囲分割のサポート
    -   ハッシュパーティションをサポート
-   SQL オプティマイザー
    -   `AggregationElimination` [＃7676](https://github.com/pingcap/tidb/pull/7676)の最適化ルールを再サポート
    -   `NOT EXISTS`サブクエリを最適化し、Anti Semi Join [＃7842](https://github.com/pingcap/tidb/pull/7842)に変換する
    -   新しい Cascades オプティマイザーをサポートするために`tidb_enable_cascades_planner`変数を追加します。現在、Cascades オプティマイザーはまだ完全に実装されておらず、デフォルトではオフになっています[＃7879](https://github.com/pingcap/tidb/pull/7879)
    -   トランザクション[＃7877](https://github.com/pingcap/tidb/pull/7877)でのインデックス結合の使用をサポート
    -   外部結合の定数伝播を最適化し、結合結果の外部テーブルに関連するフィルタリング条件を外部結合を介して外部テーブルにプッシュダウンできるようにすることで、外部結合の無駄な計算を減らし、実行パフォーマンスを向上させます[＃7794](https://github.com/pingcap/tidb/pull/7794)
    -   投影除去の最適化ルールを集計除去の後の位置に調整し、冗長な`Project`演算子[＃7909](https://github.com/pingcap/tidb/pull/7909)を回避する
    -   `IFNULL`関数を最適化し、入力パラメータに NULL 以外の属性[＃7924](https://github.com/pingcap/tidb/pull/7924)がある場合はこの関数を削除します。
    -   `_tidb_rowid`構築クエリの範囲をサポートし、テーブル全体のスキャンを回避してクラスターのストレスを軽減します[＃8047](https://github.com/pingcap/tidb/pull/8047)
    -   `IN`サブクエリを最適化して集計後に内部結合を実行し、この最適化ルールを有効にしてデフォルトで開くかどうかを制御する`tidb_opt_insubq_to_join_and_agg`変数を追加します[＃7531](https://github.com/pingcap/tidb/pull/7531)
    -   `DO`文[＃8343](https://github.com/pingcap/tidb/pull/8343)でのサブクエリの使用をサポート
    -   不要なテーブルスキャンと結合操作を削減し、実行パフォーマンスを向上させるために、外部結合除去の最適化ルールを追加します[＃8021](https://github.com/pingcap/tidb/pull/8021)
    -   `TIDB_INLJ`オプティマイザのヒント動作を変更すると、オプティマイザはヒントで指定されたテーブルをインデックス結合[＃8243](https://github.com/pingcap/tidb/pull/8243)の内部テーブルとして使用します。
    -   `Prepare`文の実行計画キャッシュが有効になったときに使用できるように、 `PointGet`広い範囲で使用する[＃8108](https://github.com/pingcap/tidb/pull/8108)
    -   複数のテーブルを結合する際の結合順序の選択を最適化するために貪欲アルゴリズム`Join Reorder`を導入する[＃8394](https://github.com/pingcap/tidb/pull/8394)
    -   サポートビュー[＃8757](https://github.com/pingcap/tidb/pull/8757)
    -   サポートウィンドウ機能[＃8630](https://github.com/pingcap/tidb/pull/8630)
    -   `TIDB_INLJ`が有効でない場合はクライアントに警告を返し、ユーザビリティを向上させる[＃9037](https://github.com/pingcap/tidb/pull/9037)
    -   フィルタリング条件とテーブル統計に基づいてフィルタリングされたデータの統計を推測する機能をサポート[＃7921](https://github.com/pingcap/tidb/pull/7921)
    -   範囲パーティション[＃8885](https://github.com/pingcap/tidb/pull/8885)のパーティション プルーニング最適化ルールを改善する
-   SQL エグゼキュータ
    -   空の`ON`条件[＃9037](https://github.com/pingcap/tidb/pull/9037)をサポートするために`Merge Join`演算子を最適化する
    -   ログを最適化し、 `EXECUTE`ステートメント[＃7684](https://github.com/pingcap/tidb/pull/7684)を実行するときに使用されるユーザー変数を出力します。
    -   `COMMIT`ステートメント[＃7951](https://github.com/pingcap/tidb/pull/7951)の遅いクエリ情報を出力するためにログを最適化します。
    -   SQLチューニングプロセスを容易にする`EXPLAIN ANALYZE`機能をサポートする[＃7827](https://github.com/pingcap/tidb/pull/7827)
    -   多数の列を持つ幅の広いテーブルの書き込みパフォーマンスを最適化[＃7935](https://github.com/pingcap/tidb/pull/7935)
    -   サポート`admin show next_row_id` [＃8242](https://github.com/pingcap/tidb/pull/8242)
    -   実行エンジン[＃8480](https://github.com/pingcap/tidb/pull/8480)で使用される初期Chunkのサイズを制御するための`tidb_init_chunk_size`変数を追加します。
    -   `shard_row_id_bits`改善し、自動増分ID [＃8936](https://github.com/pingcap/tidb/pull/8936)をクロスチェックする
-   `Prepare`ステートメント
    -   異なるユーザー変数が入力された場合にクエリプランが正しいことを保証するために、サブクエリを含む`Prepare`ステートメントをクエリプランキャッシュに追加することを禁止します[＃8064](https://github.com/pingcap/tidb/pull/8064)
    -   クエリプランキャッシュを最適化して、ステートメントに非決定的関数が含まれている場合にプランがキャッシュされることを保証します[＃8105](https://github.com/pingcap/tidb/pull/8105)
    -   クエリプランキャッシュを最適化して、 `DELETE` / `UPDATE` / `INSERT`のクエリプランがキャッシュされることを保証する[＃8107](https://github.com/pingcap/tidb/pull/8107)
    -   クエリプランキャッシュを最適化して、 `DEALLOCATE`文[＃8332](https://github.com/pingcap/tidb/pull/8332)を実行するときに対応するプランを削除します。
    -   メモリ使用量を制限して、クエリプランキャッシュを最適化し、プランを過剰にキャッシュすることで発生する TiDB OOM の問題を回避します[＃8339](https://github.com/pingcap/tidb/pull/8339)
    -   `Prepare`文を最適化して、 `ORDER BY` / `GROUP BY` / `LIMIT`節[＃8206](https://github.com/pingcap/tidb/pull/8206)の`?`プレースホルダーの使用をサポートする
-   権限管理
    -   `ANALYZE`文[＃8486](https://github.com/pingcap/tidb/pull/8486)の権限チェックを追加する
    -   `USE`文[＃8414](https://github.com/pingcap/tidb/pull/8418)の権限チェックを追加する
    -   `SET GLOBAL`文[＃8837](https://github.com/pingcap/tidb/pull/8837)の権限チェックを追加する
    -   `SHOW PROCESSLIST`文[＃7858](https://github.com/pingcap/tidb/pull/7858)の権限チェックを追加する
-   サーバ
    -   `Trace`機能[＃9029](https://github.com/pingcap/tidb/pull/9029)サポートする
    -   プラグインフレームワーク[＃8788](https://github.com/pingcap/tidb/pull/8788)をサポート
    -   `unix_socket`とTCPを同時に使用してデータベース[＃8836](https://github.com/pingcap/tidb/pull/8836)に接続することをサポートします
    -   `interactive_timeout`システム変数[＃8573](https://github.com/pingcap/tidb/pull/8573)サポート
    -   `wait_timeout`システム変数[＃8346](https://github.com/pingcap/tidb/pull/8346)サポート
    -   `tidb_batch_commit`変数[＃8293](https://github.com/pingcap/tidb/pull/8293)を使用して、ステートメントの数に基づいてトランザクションを複数のトランザクションに分割することをサポートします。
    -   `ADMIN SHOW SLOW`ステートメントを使用してスローログ[＃7785](https://github.com/pingcap/tidb/pull/7785)をチェックするサポート
-   互換性
    -   `ALLOW_INVALID_DATES` SQLモード[＃9027](https://github.com/pingcap/tidb/pull/9027)サポート
    -   CSVファイルのフォールトトレランス`LoadData`改善[＃9005](https://github.com/pingcap/tidb/pull/9005)
    -   MySQL 320ハンドシェイクプロトコル[＃8812](https://github.com/pingcap/tidb/pull/8812)サポート
    -   自動増分列[＃8181](https://github.com/pingcap/tidb/pull/8181)として符号なし`bigint`列の使用をサポート
    -   `SHOW CREATE DATABASE IF NOT EXISTS`構文[＃8926](https://github.com/pingcap/tidb/pull/8926)をサポートする
    -   フィルタリング条件にユーザー変数が含まれている場合、述語プッシュダウン操作を中止して、ユーザー変数を使用してウィンドウ関数の動作をモックするMySQLの動作との互換性を向上させます[＃8412](https://github.com/pingcap/tidb/pull/8412)
-   DDL
    -   誤って削除されたテーブルの高速回復をサポート[＃7937](https://github.com/pingcap/tidb/pull/7937)
    -   同時実行数を動的に調整するサポート`ADD INDEX` [＃8295](https://github.com/pingcap/tidb/pull/8295)
    -   テーブルまたは列の文字セットを`utf8` / `utf8mb4` [＃8037](https://github.com/pingcap/tidb/pull/8037)に変更するサポート
    -   デフォルトの文字セットを`utf8`から`utf8mb4`に変更します[＃7965](https://github.com/pingcap/tidb/pull/7965)
    -   サポート範囲パーティション[＃8011](https://github.com/pingcap/tidb/pull/8011)

## ツール {#tools}

-   TiDB Lightning
    -   SQL文をKVペアに変換する速度が大幅に向上[＃110](https://github.com/pingcap/tidb-lightning/pull/110)
    -   インポートのパフォーマンスと安定性を向上させるために、単一テーブルのバッチインポートをサポートします[＃113](https://github.com/pingcap/tidb-lightning/pull/113)

## PD {#pd}

-   リージョンメタデータを個別に格納するには`RegionStorage`追加します[＃1237](https://github.com/pingcap/pd/pull/1237)
-   シャッフルホットリージョンスケジューラ[＃1361](https://github.com/pingcap/pd/pull/1361)を追加
-   スケジュールパラメータ関連のメトリック[＃1406](https://github.com/pingcap/pd/pull/1406)を追加する
-   クラスターラベル関連のメトリック[＃1402](https://github.com/pingcap/pd/pull/1402)を追加する
-   インポートデータシミュレータ[＃1263](https://github.com/pingcap/pd/pull/1263)を追加
-   リーダー選挙に関する`Watch`問題を修正[＃1396](https://github.com/pingcap/pd/pull/1396)

## ティクヴ {#tikv}

-   分散GC [＃3179](https://github.com/tikv/tikv/pull/3179)サポート
-   書き込みストール[＃3606](https://github.com/tikv/tikv/pull/3606)を回避するために、スナップショットを適用する前に RocksDB レベル 0 ファイルをチェックします。
-   リバース`raw_scan`と`raw_batch_scan` [＃3742](https://github.com/tikv/tikv/pull/3724)をサポート
-   HTTPを使用した監視情報の取得をサポート[＃3855](https://github.com/tikv/tikv/pull/3855)
-   DST をより良くサポート[＃3786](https://github.com/tikv/tikv/pull/3786)
-   バッチ[＃3931](https://github.com/tikv/tikv/pull/3913)でのRaftメッセージの受信と送信をサポート
-   新しいstorageエンジン Titan [＃3985](https://github.com/tikv/tikv/pull/3985)を導入
-   gRPCをv1.17.2にアップグレード[＃4023](https://github.com/tikv/tikv/pull/4023)
-   バッチ[＃4043](https://github.com/tikv/tikv/pull/4043)でクライアント要求を受信して​​応答を送信することをサポートします。
-   マルチスレッド対応[＃4044](https://github.com/tikv/tikv/pull/4044)
-   マルチスレッドRaftstore [＃4066](https://github.com/tikv/tikv/pull/4066)サポート
