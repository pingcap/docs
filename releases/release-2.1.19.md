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
    -   `PhysicalUnionScan`演算子が統計誤って設定するため、クエリ プランが誤って選択される可能性がある問題を修正しました。 [＃14134](https://github.com/pingcap/tidb/pull/14134)
    -   `minAutoAnalyzeRatio`制約を取り除き、自動`ANALYZE`をよりタイムリーにする [＃14013](https://github.com/pingcap/tidb/pull/14013)
    -   `WHERE`句に一意キー等号条件が含まれている場合に推定行数が`1`より大きくなる問題を修正しました。 [＃13385](https://github.com/pingcap/tidb/pull/13385)
-   SQL実行エンジン
    -   `ConvertJSONToInt` で`unit64`中間結果として`int64`使用するときに精度オーバーフローが発生する問題を修正しました。 [＃13036](https://github.com/pingcap/tidb/pull/13036)
    -   クエリに`SLEEP`関数が含まれている場合（たとえば`select 1 from (select sleep(1)) t;)` ）、列の整理によってクエリ内の`sleep(1)`無効になる問題を修正しました[＃13039](https://github.com/pingcap/tidb/pull/13039)
    -   `INSERT ON DUPLICATE UPDATE`文で`Chunk`再利用してメモリのオーバーヘッドを削減します [＃12999](https://github.com/pingcap/tidb/pull/12999)
    -   `slow_query`テーブルにトランザクション関連のフィールドを追加します。 [＃13129](https://github.com/pingcap/tidb/pull/13129)
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
    -   `UPDATE`文に含まれるサブクエリが誤って変換される問題を修正しました。`WHERE`句にサブクエリが含まれている場合に`UPDATE`実行エラーが発生する問題を修正しました。 [＃13120](https://github.com/pingcap/tidb/pull/13120)
    -   パーティションテーブルで`ADMIN CHECK TABLE`実行をサポート [＃13143](https://github.com/pingcap/tidb/pull/13143)
    -   列属性として`ON UPDATE CURRENT_TIMESTAMP`使用し、浮動小数点精度を指定した場合、 `SHOW CREATE TABLE`などのステートメントの精度が不完全になる問題を修正しました[＃12462](https://github.com/pingcap/tidb/pull/12462)
    -   列削除、修正、または変更するときに外部キーがチェックされないため、 `SELECT * FROM information_schema.KEY_COLUMN_USAGE`文の実行時にpanicが発生する問題を修正しました。 [＃14162](https://github.com/pingcap/tidb/pull/14162)
    -   TiDB で`Streaming`有効になっている場合に返されるデータが重複する可能性がある問題を修正しました [＃13255](https://github.com/pingcap/tidb/pull/13255)
    -   夏時間による`Invalid time format`エラーを修正 [＃13624](https://github.com/pingcap/tidb/pull/13624)
    -   整数を符号なし浮動小数点型または小数型に変換すると精度が失われ、データが正しくなくなる問題を修正[＃13756](https://github.com/pingcap/tidb/pull/13756)
    -   `Quote`関数が`NULL`値処理するときに誤ったタイプの値が返される問題を修正しました [＃13681](https://github.com/pingcap/tidb/pull/13681)
    -   `gotime.Local` を使用して文字列から日付を解析した後にタイムゾーンが正しくない問題を修正しました [＃13792](https://github.com/pingcap/tidb/pull/13792)
    -   `builtinIntervalRealSig` の実装で`binSearch`関数がエラーを返さないため、結果が正しくない可能性がある問題を修正しました。 [＃13768](https://github.com/pingcap/tidb/pull/13768)
    -   `INSERT`文実行で文字列型を浮動小数点型に変換するときにエラーが発生する可能性がある問題を修正 [＃14009](https://github.com/pingcap/tidb/pull/14009)
    -   `sum(distinct)`関数から返される誤った結果を修正します [＃13041](https://github.com/pingcap/tidb/pull/13041)
    -   関数`jsonUnquoteFunction`戻り型の長さに不正な値が与えられているため、同じ場所の`CAST` `union`データをマージされた型に変換すると`data too long`が返される問題を修正しました[＃13645](https://github.com/pingcap/tidb/pull/13645)
    -   権限チェックが厳しすぎるためパスワードを設定できない問題を修正[＃13805](https://github.com/pingcap/tidb/pull/13805)
-   サーバ
    -   `KILL CONNECTION`ゴルーチンリークを引き起こす可能性がある問題を修正[＃13252](https://github.com/pingcap/tidb/pull/13252)
    -   HTTP API の`info/all`インターフェースを介してすべてのTiDBノードのbinlogステータスの取得をサポート [＃13188](https://github.com/pingcap/tidb/pull/13188)
    -   Windows で TiDB プロジェクトのビルドに失敗する問題を修正 [＃13650](https://github.com/pingcap/tidb/pull/13650)
    -   TiDBサーバーのバージョンを制御および変更するための`server-version`構成項目を追加します。 [＃13904](https://github.com/pingcap/tidb/pull/13904)
    -   Go1.13でコンパイルされたバイナリ`plugin`正常に動作しない問題を修正[＃13527](https://github.com/pingcap/tidb/pull/13527)
-   DDL
    -   テーブルが作成され、テーブルに`COLLATE` が含まれている場合、列のシステムのデフォルトの文字セットの代わりにテーブルの`COLLATE`使用します。 [＃13190](https://github.com/pingcap/tidb/pull/13190)
    -   テーブルを作成するときにインデックス名の長さを制限する [＃13311](https://github.com/pingcap/tidb/pull/13311)
    -   テーブル名を変更するときにテーブル名の長さがチェックされない問題を修正[＃13345](https://github.com/pingcap/tidb/pull/13345)
    -   `BIT`列の幅の範囲を確認する [＃13511](https://github.com/pingcap/tidb/pull/13511)
    -   `change/modify column`から出力されるエラー情報をより分かりやすくする[＃13798](https://github.com/pingcap/tidb/pull/13798)
    -   下流のDrainerによってまだ処理されていない`drop column`操作を実行するときに、下流が影響を受ける列のない DML 操作を受け取る可能性がある問題を修正しました。 [＃13974](https://github.com/pingcap/tidb/pull/13974)

## TiKV {#tikv}

-   Raftstore
    -   TiKVを再起動したときに発生するpanicを修正し、リージョンをマージしてCompact log を適用するプロセスで`is_merging`誤った値が与えられました。 [＃5884](https://github.com/tikv/tikv/pull/5884)
-   Importer
    -   gRPC メッセージの長さの制限を解除[＃5809](https://github.com/tikv/tikv/pull/5809)

## PD {#pd}

-   すべてのリージョンを取得するための HTTP API のパフォーマンスを改善しました [＃1988](https://github.com/pingcap/pd/pull/1988)
-   etcd をアップグレードして、etcd PreVote がリーダーを選出できない問題を修正します (ダウングレードはサポートされていません) [＃2052](https://github.com/pingcap/pd/pull/2052)

## ツール {#tools}

-   TiDB Binlog
    -   binlogctl を通じてノードステータス情報の出力を最適化します。 [＃777](https://github.com/pingcap/tidb-binlog/pull/777)
    -   Drainerフィルター設定の値`nil`が原因でpanicが発生する問題を修正 [＃802](https://github.com/pingcap/tidb-binlog/pull/802)
    -   Pumpの`Graceful`出口を最適化する [＃825](https://github.com/pingcap/tidb-binlog/pull/825)
    -   Pumpがbinlogデータを書き込むときに、より詳細な監視メトリックを追加します[＃830](https://github.com/pingcap/tidb-binlog/pull/830)
    -   Drainer がDDL 操作を実行した後にテーブル情報を更新するように Drainer のロジックを最適化します。 [＃836](https://github.com/pingcap/tidb-binlog/pull/836)
    -   Pumpがこのbinlogを受信しない場合、DDL操作のコミットbinlogが無視される問題を修正しました。 [＃855](https://github.com/pingcap/tidb-binlog/pull/855)

## TiDB Ansible {#tidb-ansible}

-   TiDBサービスの監視項目`Uncommon Error OPM`名前を`Write Binlog Error`に変更し、対応するアラートメッセージを追加します。 [＃1038](https://github.com/pingcap/tidb-ansible/pull/1038)
-   TiSparkを2.1.8にアップグレード[＃1063](https://github.com/pingcap/tidb-ansible/pull/1063)
