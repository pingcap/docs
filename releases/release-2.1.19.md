---
title: TiDB 2.1.19 Release Notes
summary: TiDB 2.1.19は2019年12月27日にリリースされました。SQLオプティマイザー、SQL実行エンジン、サーバー、DDL、TiKV、PD、TiDB Ansibleに関する様々な修正と最適化が含まれています。主な修正としては、不正なクエリ結果の解決、メモリオーバーヘッドの削減、タイムゾーン、データ重複、panic発生に関連する問題の修正などが挙げられます。また、TiDB BinlogとTiDB Ansibleのアップグレードと最適化も含まれています。
---

# TiDB 2.1.19 リリースノート {#tidb-2-1-19-release-notes}

発売日：2019年12月27日

TiDB バージョン: 2.1.19

TiDB Ansible バージョン: 2.1.19

## TiDB {#tidb}

-   SQLオプティマイザー
    -   `select max(_tidb_rowid) from t`のシナリオを最適化して、テーブル全体のスキャンを回避する[＃13294](https://github.com/pingcap/tidb/pull/13294)
    -   クエリ内のユーザー変数に割り当てられた誤った値と述語のプッシュダウンによって発生する誤った結果を修正しました[＃13230](https://github.com/pingcap/tidb/pull/13230)
    -   統計情報の更新時にデータ競合が発生し、統計情報が正確でない問題を修正しました[＃13690](https://github.com/pingcap/tidb/pull/13690)
    -   `UPDATE`ステートメントにサブクエリとストアされた生成列の両方が含まれている場合に結果が正しくない問題を修正しました。3 `UPDATE`ステートメントに異なるデータベースの同じ名前のテーブルが 2 つ含まれている場合にステートメント実行エラーが発生する問題を修正しました[＃13357](https://github.com/pingcap/tidb/pull/13357)
    -   `PhysicalUnionScan`演算子が統計[＃14134](https://github.com/pingcap/tidb/pull/14134)誤って設定するため、クエリ プランが誤って選択される可能性がある問題を修正しました。
    -   `minAutoAnalyzeRatio`制約を取り除き、自動`ANALYZE`をよりタイムリーに[＃14013](https://github.com/pingcap/tidb/pull/14013)する
    -   `WHERE`節に一意キー[＃13385](https://github.com/pingcap/tidb/pull/13385)等号条件が含まれている場合に推定行数が`1`より大きくなる問題を修正しました。
-   SQL実行エンジン
    -   `ConvertJSONToInt` [＃13036](https://github.com/pingcap/tidb/pull/13036)で`unit64`中間結果として`int64`使用するときに精度オーバーフローが発生する問題を修正しました。
    -   クエリに`SLEEP`関数が含まれている場合（たとえば`select 1 from (select sleep(1)) t;)` ）、列の整理によってクエリ内の`sleep(1)`無効になる問題を修正しました[＃13039](https://github.com/pingcap/tidb/pull/13039)
    -   `INSERT ON DUPLICATE UPDATE`文[＃12999](https://github.com/pingcap/tidb/pull/12999)で`Chunk`再利用してメモリのオーバーヘッドを削減します
    -   `slow_query`テーブル[＃13129](https://github.com/pingcap/tidb/pull/13129)にトランザクション関連のフィールドを追加します。
        -   `Prewrite_time`
        -   `Commit_time`
        -   `Get_commit_ts_time`
        -   `Commit_backoff_time`
        -   `Backoff_types`
        -   `Resolve_lock_time`
        -   `Local_latch_wait_time`
        -   `Write_key`
        -   `Write_size`
        -   `Prewrite_region`
        -   `Txn_retry`
    -   `UPDATE`文に含まれるサブクエリが誤って変換される問題を修正しました。5 `WHERE`にサブクエリ[＃13120](https://github.com/pingcap/tidb/pull/13120)が含まれている場合に`UPDATE`実行エラーが発生する問題を修正しました。
    -   パーティションテーブル[＃13143](https://github.com/pingcap/tidb/pull/13143)で`ADMIN CHECK TABLE`実行をサポート
    -   列属性として`ON UPDATE CURRENT_TIMESTAMP`使用し、浮動小数点精度を指定した場合、 `SHOW CREATE TABLE`などのステートメントの精度が不完全になる問題を修正しました[＃12462](https://github.com/pingcap/tidb/pull/12462)
    -   列[＃14162](https://github.com/pingcap/tidb/pull/14162)削除、修正、または変更するときに外部キーがチェックされないため、 `SELECT * FROM information_schema.KEY_COLUMN_USAGE`文の実行時にpanicが発生する問題を修正しました。
    -   TiDB [＃13255](https://github.com/pingcap/tidb/pull/13255)で`Streaming`有効になっている場合に返されるデータが重複する可能性がある問題を修正しました
    -   夏時間[＃13624](https://github.com/pingcap/tidb/pull/13624)による`Invalid time format`エラーを修正
    -   整数を符号なし浮動小数点型または小数型に変換すると精度が失われ、データが正しくなくなる問題を修正[＃13756](https://github.com/pingcap/tidb/pull/13756)
    -   `Quote`関数が`NULL`値[＃13681](https://github.com/pingcap/tidb/pull/13681)処理するときに誤ったタイプの値が返される問題を修正しました
    -   `gotime.Local` [＃13792](https://github.com/pingcap/tidb/pull/13792)を使用して文字列から日付を解析した後にタイムゾーンが正しくない問題を修正しました
    -   `builtinIntervalRealSig` [＃13768](https://github.com/pingcap/tidb/pull/13768)の実装で`binSearch`関数がエラーを返さないため、結果が正しくない可能性がある問題を修正しました。
    -   `INSERT`文実行[＃14009](https://github.com/pingcap/tidb/pull/14009)で文字列型を浮動小数点型に変換するときにエラーが発生する可能性がある問題を修正
    -   `sum(distinct)`関数[＃13041](https://github.com/pingcap/tidb/pull/13041)から返される誤った結果を修正します
    -   関数`jsonUnquoteFunction`戻り型の長さに不正な値が与えられているため、同じ場所の`CAST` `union`データをマージされた型に変換すると`data too long`が返される問題を修正しました[＃13645](https://github.com/pingcap/tidb/pull/13645)
    -   権限チェックが厳しすぎるためパスワードを設定できない問題を修正[＃13805](https://github.com/pingcap/tidb/pull/13805)
-   サーバ
    -   `KILL CONNECTION`ゴルーチンリークを引き起こす可能性がある問題を修正[＃13252](https://github.com/pingcap/tidb/pull/13252)
    -   HTTP API [＃13188](https://github.com/pingcap/tidb/pull/13188)の`info/all`インターフェースを介してすべてのTiDBノードのbinlogステータスの取得をサポート
    -   Windows [＃13650](https://github.com/pingcap/tidb/pull/13650)で TiDB プロジェクトのビルドに失敗する問題を修正
    -   TiDBサーバー[＃13904](https://github.com/pingcap/tidb/pull/13904)のバージョンを制御および変更するための`server-version`構成項目を追加します。
    -   Go1.13でコンパイルされたバイナリ`plugin`正常に動作しない問題を修正[＃13527](https://github.com/pingcap/tidb/pull/13527)
-   DDL
    -   テーブルが作成され、テーブルに`COLLATE` [＃13190](https://github.com/pingcap/tidb/pull/13190)が含まれている場合、列のシステムのデフォルトの文字セットの代わりにテーブルの`COLLATE`使用します。
    -   テーブル[＃13311](https://github.com/pingcap/tidb/pull/13311)を作成するときにインデックス名の長さを制限する
    -   テーブル名を変更するときにテーブル名の長さがチェックされない問題を修正[＃13345](https://github.com/pingcap/tidb/pull/13345)
    -   `BIT`列目[＃13511](https://github.com/pingcap/tidb/pull/13511)列目の幅の範囲を確認する
    -   `change/modify column`から出力されるエラー情報をより分かりやすくする[＃13798](https://github.com/pingcap/tidb/pull/13798)
    -   下流のDrainerによってまだ処理されていない`drop column`操作を実行するときに、下流が影響を受ける列[＃13974](https://github.com/pingcap/tidb/pull/13974)のない DML 操作を受け取る可能性がある問題を修正しました。

## TiKV {#tikv}

-   Raftstore
    -   TiKVを再起動したときに発生するpanicを修正し、リージョンをマージしてCompact log [＃5884](https://github.com/tikv/tikv/pull/5884)を適用するプロセスで`is_merging`誤った値が与えられました。
-   輸入業者
    -   gRPC メッセージの長さの制限を解除[＃5809](https://github.com/tikv/tikv/pull/5809)

## PD {#pd}

-   すべてのリージョン[＃1988](https://github.com/pingcap/pd/pull/1988)を取得するための HTTP API のパフォーマンスを改善しました
-   etcd をアップグレードして、etcd PreVote がリーダーを選出できない問題を修正します (ダウングレードはサポートされていません) [＃2052](https://github.com/pingcap/pd/pull/2052)

## ツール {#tools}

-   TiDBBinlog
    -   binlogctl [＃777](https://github.com/pingcap/tidb-binlog/pull/777)を通じてノードステータス情報の出力を最適化します。
    -   Drainerフィルター設定[＃802](https://github.com/pingcap/tidb-binlog/pull/802)の値`nil`が原因でpanicが発生する問題を修正
    -   Pump[＃825](https://github.com/pingcap/tidb-binlog/pull/825)の`Graceful`出口を最適化する
    -   Pumpがbinlogデータを書き込むときに、より詳細な監視メトリックを追加します[＃830](https://github.com/pingcap/tidb-binlog/pull/830)
    -   Drainer がDDL 操作[＃836](https://github.com/pingcap/tidb-binlog/pull/836)を実行した後にテーブル情報を更新するように Drainer のロジックを最適化します。
    -   Pumpがこのbinlog[＃855](https://github.com/pingcap/tidb-binlog/pull/855)を受信しない場合、DDL操作のコミットbinlogが無視される問題を修正しました。

## TiDB アンシブル {#tidb-ansible}

-   TiDBサービスの監視項目`Uncommon Error OPM`名前を`Write Binlog Error`に変更し、対応するアラートメッセージ[＃1038](https://github.com/pingcap/tidb-ansible/pull/1038)を追加します。
-   TiSparkを2.1.8にアップグレード[＃1063](https://github.com/pingcap/tidb-ansible/pull/1063)
