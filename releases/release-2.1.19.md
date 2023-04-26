---
title: TiDB 2.1.19 Release Notes
---

# TiDB 2.1.19 リリースノート {#tidb-2-1-19-release-notes}

発売日：2019年12月27日

TiDB バージョン: 2.1.19

TiDB アンシブル バージョン: 2.1.19

## TiDB {#tidb}

-   SQL オプティマイザー
    -   `select max(_tidb_rowid) from t`のシナリオを最適化して、フル テーブル スキャンを回避する[#13294](https://github.com/pingcap/tidb/pull/13294)
    -   クエリでユーザー変数に割り当てられた誤った値と述語[#13230](https://github.com/pingcap/tidb/pull/13230)のプッシュダウンによって引き起こされた誤った結果を修正します。
    -   統計更新時にデータ競合が発生し、統計が正確でない問題を修正[#13690](https://github.com/pingcap/tidb/pull/13690)
    -   `UPDATE`ステートメントにサブクエリと格納された生成列の両方が含まれている場合、結果が正しくない問題を修正します。このステートメントに異なるデータベースの 2 つの同じ名前のテーブルが含まれている場合の`UPDATE`ステートメント実行エラーを修正します[#13357](https://github.com/pingcap/tidb/pull/13357)
    -   `PhysicalUnionScan`演算子が誤って統計を設定するため、クエリ プランが正しく選択されない可能性がある問題を修正します[#14134](https://github.com/pingcap/tidb/pull/14134)
    -   `minAutoAnalyzeRatio`制約を削除して、自動`ANALYZE`をよりタイムリーにします[#14013](https://github.com/pingcap/tidb/pull/14013)
    -   `WHERE`句に一意キー[#13385](https://github.com/pingcap/tidb/pull/13385)の等しい条件が含まれている場合、推定行数が`1`より大きい問題を修正します。
-   SQL 実行エンジン
    -   `ConvertJSONToInt` [#13036](https://github.com/pingcap/tidb/pull/13036)の`unit64`の中間結果として`int64`使用する場合の精度オーバーフローを修正します。
    -   `SLEEP`関数がクエリ内にある場合 (たとえば、 `select 1 from (select sleep(1)) t;)` )、列のプルーニングによってクエリ内の`sleep(1)`が無効になるという問題を修正します[#13039](https://github.com/pingcap/tidb/pull/13039)
    -   `INSERT ON DUPLICATE UPDATE`ステートメント[#12999](https://github.com/pingcap/tidb/pull/12999)で`Chunk`を再利用することにより、メモリオーバーヘッドを削減します。
    -   `slow_query`テーブル[#13129](https://github.com/pingcap/tidb/pull/13129)にトランザクション関連のフィールドを追加します。
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
    -   `UPDATE`ステートメントに含まれるサブクエリが正しく変換されない問題を修正します。 `WHERE`句にサブクエリが含まれている場合の`UPDATE`実行エラーを修正します[#13120](https://github.com/pingcap/tidb/pull/13120)
    -   分割されたテーブルでの実行をサポート`ADMIN CHECK TABLE` [#13143](https://github.com/pingcap/tidb/pull/13143)
    -   列属性に`ON UPDATE CURRENT_TIMESTAMP`を使用し、浮動小数点精度[#12462](https://github.com/pingcap/tidb/pull/12462)を指定した場合、 `SHOW CREATE TABLE`などのステートメントの精度が不完全になる問題を修正
    -   列[#14162](https://github.com/pingcap/tidb/pull/14162)の削除、変更、または変更時に外部キーがチェックされないため、 `SELECT * FROM information_schema.KEY_COLUMN_USAGE`ステートメントを実行するとpanicが発生する問題を修正
    -   TiDB [#13255](https://github.com/pingcap/tidb/pull/13255)で`Streaming`を有効にすると、返されるデータが重複する可能性がある問題を修正します。
    -   `Invalid time format`サマータイムによるエラーを修正[#13624](https://github.com/pingcap/tidb/pull/13624)
    -   整数を符号なし浮動小数点や 10 進数に変換すると精度が失われ、データが正しくなくなる問題を修正[#13756](https://github.com/pingcap/tidb/pull/13756)
    -   `Quote`関数が`NULL`値[#13681](https://github.com/pingcap/tidb/pull/13681)を処理するときに、誤ったタイプの値が返される問題を修正します。
    -   `gotime.Local` [#13792](https://github.com/pingcap/tidb/pull/13792)を使用して文字列から日付を解析した後、タイムゾーンが正しくない問題を修正します
    -   `builtinIntervalRealSig` [#13768](https://github.com/pingcap/tidb/pull/13768)の実装で`binSearch`関数がエラーを返さないため、結果が正しくない場合がある問題を修正
    -   `INSERT`文実行[#14009](https://github.com/pingcap/tidb/pull/14009)で文字列型を浮動小数点型に変換するとエラーになることがある問題を修正
    -   `sum(distinct)`関数[#13041](https://github.com/pingcap/tidb/pull/13041)から返された誤った結果を修正します
    -   関数の返される型の長さが正しくない値が与えられるため、同じ場所の`data too long` `union`データをマージされた型に変換すると`CAST`が`jsonUnquoteFunction`を返す問題を修正します[#13645](https://github.com/pingcap/tidb/pull/13645)
    -   権限チェックが厳しすぎてパスワードが設定できない問題を修正[#13805](https://github.com/pingcap/tidb/pull/13805)
-   サーバ
    -   `KILL CONNECTION`ゴルーチンリークが発生する可能性がある問題を修正[#13252](https://github.com/pingcap/tidb/pull/13252)
    -   HTTP API [#13188](https://github.com/pingcap/tidb/pull/13188)の`info/all`インターフェースを介してすべての TiDB ノードのbinlogステータスを取得するサポート
    -   Windows [#13650](https://github.com/pingcap/tidb/pull/13650)で TiDB プロジェクトをビルドできない問題を修正
    -   TiDBサーバー[#13904](https://github.com/pingcap/tidb/pull/13904)のバージョンを制御および変更するための`server-version`構成項目を追加します。
    -   Go1.13でコンパイルしたバイナリ`plugin`が正常に動作しない問題を修正[#13527](https://github.com/pingcap/tidb/pull/13527)
-   DDL
    -   テーブルが作成され、テーブルに`COLLATE` [#13190](https://github.com/pingcap/tidb/pull/13190)含まれている場合、列のシステムのデフォルト文字セットの代わりにテーブルの`COLLATE`使用します
    -   テーブルの作成時にインデックス名の長さを制限する[#13311](https://github.com/pingcap/tidb/pull/13311)
    -   テーブルの名前を変更するときにテーブル名の長さがチェックされない問題を修正します[#13345](https://github.com/pingcap/tidb/pull/13345)
    -   `BIT`列[#13511](https://github.com/pingcap/tidb/pull/13511)の幅の範囲を確認します
    -   `change/modify column`から出力されるエラー情報を分かりやすくする[#13798](https://github.com/pingcap/tidb/pull/13798)
    -   下流のDrainerによってまだ処理されていない`drop column`操作を実行すると、影響を受ける列[#13974](https://github.com/pingcap/tidb/pull/13974)なしで下流が DML 操作を受け取る可能性があるという問題を修正します。

## TiKV {#tikv}

-   Raftstore
    -   TiKV の再起動時に発生したpanicを修正し、リージョンをマージしてコンパクト ログ[#5884](https://github.com/tikv/tikv/pull/5884)を適用するプロセスで`is_merging`誤った値が与えられる
-   輸入業者
    -   gRPC メッセージ長の制限を削除します[#5809](https://github.com/tikv/tikv/pull/5809)

## PD {#pd}

-   すべてのリージョンを取得するための HTTP API のパフォーマンスを改善する[#1988](https://github.com/pingcap/pd/pull/1988)
-   etcd をアップグレードして、etcd PreVote がリーダーを選出できない問題を修正します (ダウングレードはサポートされていません) [#2052](https://github.com/pingcap/pd/pull/2052)

## ツール {#tools}

-   TiDBBinlog
    -   binlogctl [#777](https://github.com/pingcap/tidb-binlog/pull/777)を介して出力されるノード ステータス情報を最適化します。
    -   Drainerフィルター構成[#802](https://github.com/pingcap/tidb-binlog/pull/802)の値が`nil`あるために発生したpanicを修正します。
    -   Pump[#825](https://github.com/pingcap/tidb-binlog/pull/825)の`Graceful`の出口を最適化する
    -   Pump がbinlogデータを書き込むときに、より詳細な監視メトリックを追加します[#830](https://github.com/pingcap/tidb-binlog/pull/830)
    -   Drainerが DDL 操作を実行した後にテーブル情報を更新するように Drainer のロジックを最適化する[#836](https://github.com/pingcap/tidb-binlog/pull/836)
    -   Pumpがこのbinlogを受信しない場合、DDL 操作のコミットbinlogが無視される問題を修正します[#855](https://github.com/pingcap/tidb-binlog/pull/855)

## TiDB アンシブル {#tidb-ansible}

-   TiDB サービスの`Uncommon Error OPM`監視項目の名前を`Write Binlog Error`に変更し、対応するアラート メッセージ[#1038](https://github.com/pingcap/tidb-ansible/pull/1038)を追加します。
-   TiSpark を 2.1.8 にアップグレードする[#1063](https://github.com/pingcap/tidb-ansible/pull/1063)
