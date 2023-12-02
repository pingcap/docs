---
title: TiDB 2.1.19 Release Notes
---

# TiDB 2.1.19 リリースノート {#tidb-2-1-19-release-notes}

発売日：2019年12月27日

TiDB バージョン: 2.1.19

TiDB Ansible バージョン: 2.1.19

## TiDB {#tidb}

-   SQLオプティマイザー
    -   フルテーブルスキャンを回避するために`select max(_tidb_rowid) from t`のシナリオを最適化する[#13294](https://github.com/pingcap/tidb/pull/13294)
    -   クエリ内のユーザー変数に割り当てられた不正な値と述語[#13230](https://github.com/pingcap/tidb/pull/13230)のプッシュダウンによって引き起こされる不正な結果を修正します。
    -   統計更新時にデータ競合が発生し、統計が不正確になる問題を修正[#13690](https://github.com/pingcap/tidb/pull/13690)
    -   `UPDATE`ステートメントにサブクエリと格納された生成列の両方が含まれている場合、結果が正しくないという問題を修正します。このステートメントに異なるデータベースの`UPDATE`つの同じ名前のテーブルが含まれている場合のステートメント実行エラーを修正します[#13357](https://github.com/pingcap/tidb/pull/13357)
    -   `PhysicalUnionScan`演算子が統計[#14134](https://github.com/pingcap/tidb/pull/14134)を誤って設定するため、クエリ プランが誤って選択される可能性がある問題を修正します。
    -   `minAutoAnalyzeRatio`制約を削除して、自動`ANALYZE`をよりタイムリーにします[#14013](https://github.com/pingcap/tidb/pull/14013)
    -   `WHERE`句に一意のキー[#13385](https://github.com/pingcap/tidb/pull/13385)に対する等しい条件が含まれている場合、推定行数が`1`より大きくなる問題を修正します。
-   SQL実行エンジン
    -   `ConvertJSONToInt` [#13036](https://github.com/pingcap/tidb/pull/13036)の`unit64`の中間結果として`int64`を使用する場合の精度オーバーフローを修正しました。
    -   `SLEEP`関数がクエリ内にある場合 (たとえば、 `select 1 from (select sleep(1)) t;)` )、列のプルーニングによりクエリ内の`sleep(1)` [#13039](https://github.com/pingcap/tidb/pull/13039)無効になる問題を修正します。
    -   `INSERT ON DUPLICATE UPDATE`ステートメントの`Chunk`を再利用することでメモリのオーバーヘッドを削減します[#12999](https://github.com/pingcap/tidb/pull/12999)
    -   `slow_query`テーブル[#13129](https://github.com/pingcap/tidb/pull/13129)にトランザクション関連フィールドを追加します。
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
    -   `UPDATE`ステートメントに含まれるサブクエリが誤って変換される問題を修正します。 `WHERE`句にサブクエリが含まれている場合の`UPDATE`実行エラーを修正[#13120](https://github.com/pingcap/tidb/pull/13120)
    -   パーティション化されたテーブル[#13143](https://github.com/pingcap/tidb/pull/13143)での`ADMIN CHECK TABLE`の実行をサポート
    -   列属性に`ON UPDATE CURRENT_TIMESTAMP`を使用し、浮動小数点精度を指定した場合、 `SHOW CREATE TABLE`などのステートメントの精度が不完全になる問題を修正[#12462](https://github.com/pingcap/tidb/pull/12462)
    -   カラム[#14162](https://github.com/pingcap/tidb/pull/14162)の削除、変更、または変更時に外部キーがチェックされないため、ステートメント`SELECT * FROM information_schema.KEY_COLUMN_USAGE`の実行時に発生したpanicを修正しました。
    -   TiDB [#13255](https://github.com/pingcap/tidb/pull/13255)で`Streaming`を有効にすると返されるデータが重複する可能性がある問題を修正
    -   夏時間によるエラー`Invalid time format`を修正[#13624](https://github.com/pingcap/tidb/pull/13624)
    -   整数を符号なし浮動小数点または 10 進数型[#13756](https://github.com/pingcap/tidb/pull/13756)に変換すると精度が失われるため、データが正しくなくなる問題を修正
    -   `Quote`関数が`NULL`値[#13681](https://github.com/pingcap/tidb/pull/13681)を処理するときに、間違ったタイプの値が返される問題を修正します。
    -   `gotime.Local` [#13792](https://github.com/pingcap/tidb/pull/13792)を使用して文字列から日付を解析した後にタイムゾーンが正しくなくなる問題を修正
    -   `builtinIntervalRealSig` [#13768](https://github.com/pingcap/tidb/pull/13768)の実装において`binSearch`関数がエラーを返さないため、結果が正しくない場合がある問題を修正
    -   `INSERT`ステートメント実行[#14009](https://github.com/pingcap/tidb/pull/14009)において文字列型から浮動小数点型への変換時にエラーが発生する場合がある問題を修正
    -   `sum(distinct)`関数[#13041](https://github.com/pingcap/tidb/pull/13041)から返される誤った結果を修正します。
    -   `CAST`同じ場所の`union`のデータをマージされた型に変換すると、 `jsonUnquoteFunction`関数の戻り値の型の長さが間違った値に指定されているため、 `data too long`返される問題を修正します。 [#13645](https://github.com/pingcap/tidb/pull/13645)
    -   権限チェックが厳しすぎるためパスワードが設定できない問題を修正[#13805](https://github.com/pingcap/tidb/pull/13805)
-   サーバ
    -   `KILL CONNECTION`が goroutine リークを引き起こす可能性がある問題を修正[#13252](https://github.com/pingcap/tidb/pull/13252)
    -   HTTP API の`info/all`インターフェイスを介したすべての TiDB ノードのbinlogステータスの取得をサポート[#13188](https://github.com/pingcap/tidb/pull/13188)
    -   Windows [#13650](https://github.com/pingcap/tidb/pull/13650)で TiDB プロジェクトをビルドできない問題を修正
    -   TiDBサーバー[#13904](https://github.com/pingcap/tidb/pull/13904)のバージョンを制御および変更するための`server-version`構成項目を追加します。
    -   Go1.13でコンパイルしたバイナリ`plugin`が正常に動作しない問題を修正[#13527](https://github.com/pingcap/tidb/pull/13527)
-   DDL
    -   テーブルが作成され、テーブルに`COLLATE` [#13190](https://github.com/pingcap/tidb/pull/13190)含まれている場合、列内のシステムのデフォルトの文字セットの代わりにテーブルの`COLLATE`使用します。
    -   テーブル作成時のインデックス名の長さを制限する[#13311](https://github.com/pingcap/tidb/pull/13311)
    -   テーブルの名前を変更するときにテーブル名の長さがチェックされない問題を修正[#13345](https://github.com/pingcap/tidb/pull/13345)
    -   `BIT`列[#13511](https://github.com/pingcap/tidb/pull/13511)の幅範囲を確認してください
    -   `change/modify column`で出力されるエラー情報を分かりやすくする[#13798](https://github.com/pingcap/tidb/pull/13798)
    -   ダウンストリームDrainerによってまだ処理されていない`drop column`操作を実行するときに、ダウンストリームが影響を受ける列[#13974](https://github.com/pingcap/tidb/pull/13974)なしで DML 操作を受信する可能性がある問題を修正します。

## TiKV {#tikv}

-   Raftstore
    -   TiKV の再起動時に発生したpanicを修正し、リージョンをマージしてコンパクト ログを適用するプロセスで`is_merging`誤った値が与えられるようにしました[#5884](https://github.com/tikv/tikv/pull/5884)
-   輸入者
    -   gRPC メッセージの長さの制限を削除します[#5809](https://github.com/tikv/tikv/pull/5809)

## PD {#pd}

-   すべてのリージョン[#1988](https://github.com/pingcap/pd/pull/1988)を取得するための HTTP API のパフォーマンスを向上させます。
-   etcd をアップグレードして、etcd PreVote がリーダーを選出できない問題を修正します (ダウングレードはサポートされていません) [#2052](https://github.com/pingcap/pd/pull/2052)

## ツール {#tools}

-   TiDBBinlog
    -   binlogctl [#777](https://github.com/pingcap/tidb-binlog/pull/777)を介して出力されるノードステータス情報を最適化します。
    -   Drainerフィルタ設定[#802](https://github.com/pingcap/tidb-binlog/pull/802)の値`nil`が原因で発生したpanicを修正しました。
    -   Pump[#825](https://github.com/pingcap/tidb-binlog/pull/825)の`Graceful`出口を最適化
    -   Pump がbinlogデータを書き込むときに、より詳細な監視メトリクスを追加します[#830](https://github.com/pingcap/tidb-binlog/pull/830)
    -   Drainerが DDL 操作を実行した後にテーブル情報を更新するように Drainer のロジックを最適化します[#836](https://github.com/pingcap/tidb-binlog/pull/836)
    -   Pumpがこのbinlog[#855](https://github.com/pingcap/tidb-binlog/pull/855)を受信しない場合、DDL 操作のコミットbinlogが無視される問題を修正します。

## TiDB Ansible {#tidb-ansible}

-   TiDB サービスの`Uncommon Error OPM`監視項目の名前を`Write Binlog Error`に変更し、対応するアラート メッセージ[#1038](https://github.com/pingcap/tidb-ansible/pull/1038)を追加します。
-   TiSpark を 2.1.8 にアップグレードする[#1063](https://github.com/pingcap/tidb-ansible/pull/1063)
