---
title: TiDB 3.0 Beta Release Notes
---

# TiDB3.0ベータリリースノート {#tidb-3-0-beta-release-notes}

2019年1月19日、TiDB3.0ベータ版がリリースされました。対応するTiDBAnsible3.0ベータ版もリリースされています。 TiDB 3.0 Betaは、安定性、SQLオプティマイザー、統計、および実行エンジンに重点を置いたTiDB2.1に基づいて構築されています。

## TiDB {#tidb}

-   新機能
    -   サポートビュー
    -   ウィンドウ関数のサポート
    -   範囲分割をサポート
    -   ハッシュ分割をサポートする
-   SQLオプティマイザー
    -   [＃7676](https://github.com/pingcap/tidb/pull/7676)の最適化ルールを再サポートし`AggregationElimination`
    -   `NOT EXISTS`のサブクエリを最適化し、それをアンチセミジョイン[＃7842](https://github.com/pingcap/tidb/pull/7842)に変換します
    -   新しいCascadesオプティマイザーをサポートするために`tidb_enable_cascades_planner`の変数を追加します。現在、Cascadesオプティマイザはまだ完全には実装されておらず、デフォルトでオフになっています[＃7879](https://github.com/pingcap/tidb/pull/7879)
    -   トランザクションでのインデックス結合の使用のサポート[＃7877](https://github.com/pingcap/tidb/pull/7877)
    -   外部結合での定数伝播を最適化して、結合結果の外部テーブルに関連するフィルタリング条件を外部結合を介して外部テーブルにプッシュダウンできるようにします。これにより、外部結合の無駄な計算が減り、実行パフォーマンスが向上します[＃7794](https://github.com/pingcap/tidb/pull/7794) 。
    -   冗長な`Project`演算子を避けるために、射影除去の最適化ルールを集計除去後の位置に調整します[＃7909](https://github.com/pingcap/tidb/pull/7909)
    -   `IFNULL`関数を最適化し、入力パラメーターにNULL以外の属性がある場合はこの関数を削除します[＃7924](https://github.com/pingcap/tidb/pull/7924)
    -   全表スキャンを回避し、クラスタのストレスを軽減するための`_tidb_rowid`の構築クエリのサポート範囲[＃8047](https://github.com/pingcap/tidb/pull/8047)
    -   `IN`のサブクエリを最適化して、集計後に内部結合を実行し、 `tidb_opt_insubq_to_join_and_agg`の変数を追加して、この最適化ルールを有効にしてデフォルトで開くかどうかを制御します[＃7531](https://github.com/pingcap/tidb/pull/7531)
    -   `DO`ステートメント[＃8343](https://github.com/pingcap/tidb/pull/8343)でのサブクエリの使用のサポート
    -   外部結合除去の最適化ルールを追加して、不要なテーブルスキャンと結合操作を減らし、実行パフォーマンスを向上させます[＃8021](https://github.com/pingcap/tidb/pull/8021)
    -   `TIDB_INLJ`オプティマイザーのヒントの動作を変更すると、オプティマイザーはヒントで指定されたテーブルをインデックス結合[＃8243](https://github.com/pingcap/tidb/pull/8243)の内部テーブルとして使用します。
    -   `Prepare`ステートメントの実行プランキャッシュが有効になるときに使用できるように、 `PointGet`を広範囲に使用します[＃8108](https://github.com/pingcap/tidb/pull/8108)
    -   複数のテーブルを結合するときに結合順序の選択を最適化するために、貪欲な`Join Reorder`アルゴリズムを導入します[＃8394](https://github.com/pingcap/tidb/pull/8394)
    -   サポートビュー[＃8757](https://github.com/pingcap/tidb/pull/8757)
    -   サポートウィンドウ関数[＃8630](https://github.com/pingcap/tidb/pull/8630)
    -   使いやすさを向上させるために、 `TIDB_INLJ`が有効でない場合は、クライアントに警告を返します[＃9037](https://github.com/pingcap/tidb/pull/9037)
    -   フィルタリング条件とテーブル統計に基づいてフィルタリングされたデータの統計を推定することをサポート[＃7921](https://github.com/pingcap/tidb/pull/7921)
    -   RangePartition1のPartitionPruning最適化ルールを改善し[＃8885](https://github.com/pingcap/tidb/pull/8885)
-   SQLエグゼキュータ
    -   空の`ON`条件[＃9037](https://github.com/pingcap/tidb/pull/9037)をサポートするように`Merge Join`演算子を最適化します
    -   ログを最適化し、 `EXECUTE`ステートメントの実行時に使用されるユーザー変数を出力します[＃7684](https://github.com/pingcap/tidb/pull/7684)
    -   ログを最適化して、 `COMMIT`ステートメントの低速クエリ情報を出力します[＃7951](https://github.com/pingcap/tidb/pull/7951)
    -   SQLチューニングプロセスを容易にする`EXPLAIN ANALYZE`つの機能をサポートする[＃7827](https://github.com/pingcap/tidb/pull/7827)
    -   多くの列を持つワイドテーブルの書き込みパフォーマンスを最適化する[＃7935](https://github.com/pingcap/tidb/pull/7935)
    -   [＃8242](https://github.com/pingcap/tidb/pull/8242) `admin show next_row_id`
    -   `tidb_init_chunk_size`変数を追加して、実行エンジン[＃8480](https://github.com/pingcap/tidb/pull/8480)が使用する初期チャンクのサイズを制御します。
    -   `shard_row_id_bits`を改善し、自動インクリメント[＃8936](https://github.com/pingcap/tidb/pull/8936)をクロスチェックします
-   `Prepare`ステートメント
    -   異なるユーザー変数が入力されたときにクエリプランが正しいことを保証するために、サブクエリを含む`Prepare`ステートメントをクエリプランキャッシュに追加することを禁止します[＃8064](https://github.com/pingcap/tidb/pull/8064)
    -   クエリプランキャッシュを最適化して、ステートメントに非決定論的関数が含まれている場合にプランをキャッシュできるようにします[＃8105](https://github.com/pingcap/tidb/pull/8105)
    -   クエリプランのキャッシュを最適化して、 `DELETE` / `UPDATE` / `INSERT`のクエリプランをキャッシュできるようにします[＃8107](https://github.com/pingcap/tidb/pull/8107)
    -   クエリプランキャッシュを最適化して、 `DEALLOCATE`ステートメントを実行するときに対応するプランを削除します[＃8332](https://github.com/pingcap/tidb/pull/8332)
    -   クエリプランのキャッシュを最適化して、メモリ使用量を制限することにより、あまりにも多くのプランをキャッシュすることによって引き起こされるTiDBOOMの問題を回避します[＃8339](https://github.com/pingcap/tidb/pull/8339)
    -   `Prepare`ステートメントを最適化して`ORDER BY`節`GROUP BY`の`?` [＃8206](https://github.com/pingcap/tidb/pull/8206)ホルダーの使用をサポートし`LIMIT`
-   権限管理
    -   `ANALYZE`ステートメントの特権チェックを追加します[＃8486](https://github.com/pingcap/tidb/pull/8486)
    -   `USE`ステートメントの特権チェックを追加します[＃8414](https://github.com/pingcap/tidb/pull/8418)
    -   `SET GLOBAL`ステートメントの特権チェックを追加します[＃8837](https://github.com/pingcap/tidb/pull/8837)
    -   `SHOW PROCESSLIST`ステートメントの特権チェックを追加します[＃7858](https://github.com/pingcap/tidb/pull/7858)
-   サーバ
    -   `Trace`つの機能をサポートする[＃9029](https://github.com/pingcap/tidb/pull/9029)
    -   プラグインフレームワークをサポートする[＃8788](https://github.com/pingcap/tidb/pull/8788)
    -   `unix_socket`とTCPを同時に使用してデータベースに接続することをサポートします[＃8836](https://github.com/pingcap/tidb/pull/8836)
    -   `interactive_timeout`のシステム変数[＃8573](https://github.com/pingcap/tidb/pull/8573)をサポートします
    -   `wait_timeout`のシステム変数[＃8346](https://github.com/pingcap/tidb/pull/8346)をサポートします
    -   `tidb_batch_commit`の変数[＃8293](https://github.com/pingcap/tidb/pull/8293)を使用して、ステートメントの数に基づいてトランザクションを複数のトランザクションに分割することをサポートします。
    -   遅いログをチェックするための`ADMIN SHOW SLOW`ステートメントの使用をサポート[＃7785](https://github.com/pingcap/tidb/pull/7785)
-   互換性
    -   `ALLOW_INVALID_DATES`モード[＃9027](https://github.com/pingcap/tidb/pull/9027)をサポートする
    -   CSVファイルの`LoadData`のフォールトトレランスを改善[＃9005](https://github.com/pingcap/tidb/pull/9005)
    -   MySQL320ハンドシェイクプロトコルをサポートする[＃8812](https://github.com/pingcap/tidb/pull/8812)
    -   符号なし`bigint`列を自動インクリメント列[＃8181](https://github.com/pingcap/tidb/pull/8181)として使用することをサポート
    -   `SHOW CREATE DATABASE IF NOT EXISTS`構文[＃8926](https://github.com/pingcap/tidb/pull/8926)をサポートします
    -   フィルタリング条件にユーザー変数が含まれている場合は、述語プッシュダウン操作を破棄して、ユーザー変数を使用してウィンドウ関数の動作をモックするMySQLの動作との互換性を向上させます[＃8412](https://github.com/pingcap/tidb/pull/8412)
-   DDL
    -   誤って削除されたテーブルの高速リカバリをサポート[＃7937](https://github.com/pingcap/tidb/pull/7937)
    -   `ADD INDEX`の同時実行数の動的な調整をサポート[＃8295](https://github.com/pingcap/tidb/pull/8295)
    -   テーブルまたは[＃8037](https://github.com/pingcap/tidb/pull/8037)の文字セットの`utf8`への変更を`utf8mb4`
    -   デフォルトの文字セットを`utf8`から[＃7965](https://github.com/pingcap/tidb/pull/7965)に変更し`utf8mb4`
    -   サポート範囲パーティション[＃8011](https://github.com/pingcap/tidb/pull/8011)

## ツール {#tools}

-   TiDB Lightning
    -   SQLステートメントからKVペアへの変換を大幅に高速化[＃110](https://github.com/pingcap/tidb-lightning/pull/110)
    -   単一のテーブルのバッチインポートをサポートして、インポートのパフォーマンスと安定性を向上させます[＃113](https://github.com/pingcap/tidb-lightning/pull/113)

## PD {#pd}

-   リージョンメタデータを個別に保存するには、 `RegionStorage`を追加します[＃1237](https://github.com/pingcap/pd/pull/1237)
-   シャッフルホットリージョンスケジューラを追加する[＃1361](https://github.com/pingcap/pd/pull/1361)
-   スケジューリングパラメータ関連のメトリックを追加する[＃1406](https://github.com/pingcap/pd/pull/1406)
-   クラスタラベル関連のメトリックを追加する[＃1402](https://github.com/pingcap/pd/pull/1402)
-   インポートするデータシミュレーターを追加する[＃1263](https://github.com/pingcap/pd/pull/1263)
-   リーダー選出に関する`Watch`の問題を修正[＃1396](https://github.com/pingcap/pd/pull/1396)

## TiKV {#tikv}

-   分散[＃3179](https://github.com/tikv/tikv/pull/3179)をサポート
-   書き込みストール[＃3606](https://github.com/tikv/tikv/pull/3606)を回避するために、スナップショットを適用する前にRocksDBレベル0ファイルを確認してください
-   リバース`raw_scan`および`raw_batch_scan`を[＃3742](https://github.com/tikv/tikv/pull/3724)
-   HTTPを使用した監視情報の取得のサポート[＃3855](https://github.com/tikv/tikv/pull/3855)
-   DSTをより適切にサポートする[＃3786](https://github.com/tikv/tikv/pull/3786)
-   バッチ[＃3931](https://github.com/tikv/tikv/pull/3913)でのRaftメッセージの送受信をサポート
-   新しいストレージエンジン[＃3985](https://github.com/tikv/tikv/pull/3985)を発表
-   gRPCをv1.17.2にアップグレードする[＃4023](https://github.com/tikv/tikv/pull/4023)
-   バッチ[＃4043](https://github.com/tikv/tikv/pull/4043)でのクライアント要求の受信と応答の送信をサポートします
-   マルチスレッド適用[＃4044](https://github.com/tikv/tikv/pull/4044)をサポート
-   マルチスレッド[＃4066](https://github.com/tikv/tikv/pull/4066)をサポート
