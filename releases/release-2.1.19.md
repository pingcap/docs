---
title: TiDB 2.1.19 Release Notes
---

# TiDB 2.1.19 リリースノート {#tidb-2-1-19-release-notes}

発売日：2019年12月27日

TiDB バージョン: 2.1.19

TiDB Ansible バージョン: 2.1.19

## TiDB {#tidb}

-   SQLオプティマイザー
    -   フルテーブルスキャンを回避するために`select max(_tidb_rowid) from t`のシナリオを最適化する[<a href="https://github.com/pingcap/tidb/pull/13294">#13294</a>](https://github.com/pingcap/tidb/pull/13294)
    -   クエリ内のユーザー変数に割り当てられた不正な値と述語[<a href="https://github.com/pingcap/tidb/pull/13230">#13230</a>](https://github.com/pingcap/tidb/pull/13230)のプッシュダウンによって引き起こされる不正な結果を修正します。
    -   統計更新時にデータ競合が発生し、統計が不正確になる問題を修正[<a href="https://github.com/pingcap/tidb/pull/13690">#13690</a>](https://github.com/pingcap/tidb/pull/13690)
    -   `UPDATE`ステートメントにサブクエリと格納された生成列の両方が含まれている場合、結果が正しくないという問題を修正します。このステートメントに異なるデータベースの`UPDATE`つの同じ名前のテーブルが含まれている場合のステートメント実行エラーを修正します[<a href="https://github.com/pingcap/tidb/pull/13357">#13357</a>](https://github.com/pingcap/tidb/pull/13357)
    -   `PhysicalUnionScan`演算子が統計[<a href="https://github.com/pingcap/tidb/pull/14134">#14134</a>](https://github.com/pingcap/tidb/pull/14134)を誤って設定するため、クエリ プランが誤って選択される可能性がある問題を修正します。
    -   `minAutoAnalyzeRatio`制約を削除して、自動`ANALYZE`をよりタイムリーにします[<a href="https://github.com/pingcap/tidb/pull/14013">#14013</a>](https://github.com/pingcap/tidb/pull/14013)
    -   `WHERE`句に一意のキー[<a href="https://github.com/pingcap/tidb/pull/13385">#13385</a>](https://github.com/pingcap/tidb/pull/13385)に対する等しい条件が含まれている場合、推定行数が`1`より大きくなる問題を修正します。
-   SQL実行エンジン
    -   `ConvertJSONToInt` [<a href="https://github.com/pingcap/tidb/pull/13036">#13036</a>](https://github.com/pingcap/tidb/pull/13036)の`unit64`の中間結果として`int64`を使用する場合の精度オーバーフローを修正しました。
    -   `SLEEP`関数がクエリ内にある場合 (たとえば、 `select 1 from (select sleep(1)) t;)` )、列のプルーニングによりクエリ内の`sleep(1)` [<a href="https://github.com/pingcap/tidb/pull/13039">#13039</a>](https://github.com/pingcap/tidb/pull/13039)無効になる問題を修正します。
    -   `INSERT ON DUPLICATE UPDATE`ステートメントの`Chunk`を再利用することでメモリのオーバーヘッドを削減します[<a href="https://github.com/pingcap/tidb/pull/12999">#12999</a>](https://github.com/pingcap/tidb/pull/12999)
    -   `slow_query`テーブル[<a href="https://github.com/pingcap/tidb/pull/13129">#13129</a>](https://github.com/pingcap/tidb/pull/13129)にトランザクション関連フィールドを追加します。
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
    -   `UPDATE`ステートメントに含まれるサブクエリが誤って変換される問題を修正します。 `WHERE`句にサブクエリが含まれている場合の`UPDATE`実行エラーを修正[<a href="https://github.com/pingcap/tidb/pull/13120">#13120</a>](https://github.com/pingcap/tidb/pull/13120)
    -   パーティション化されたテーブル[<a href="https://github.com/pingcap/tidb/pull/13143">#13143</a>](https://github.com/pingcap/tidb/pull/13143)での`ADMIN CHECK TABLE`の実行をサポート
    -   列属性に`ON UPDATE CURRENT_TIMESTAMP`を使用し、浮動小数点精度を指定した場合、 `SHOW CREATE TABLE`などのステートメントの精度が不完全になる問題を修正[<a href="https://github.com/pingcap/tidb/pull/12462">#12462</a>](https://github.com/pingcap/tidb/pull/12462)
    -   カラム[<a href="https://github.com/pingcap/tidb/pull/14162">#14162</a>](https://github.com/pingcap/tidb/pull/14162)の削除、変更、または変更時に外部キーがチェックされないため、ステートメント`SELECT * FROM information_schema.KEY_COLUMN_USAGE`の実行時に発生したpanicを修正しました。
    -   TiDB [<a href="https://github.com/pingcap/tidb/pull/13255">#13255</a>](https://github.com/pingcap/tidb/pull/13255)で`Streaming`を有効にすると返されるデータが重複する可能性がある問題を修正
    -   夏時間によるエラー`Invalid time format`を修正[<a href="https://github.com/pingcap/tidb/pull/13624">#13624</a>](https://github.com/pingcap/tidb/pull/13624)
    -   整数を符号なし浮動小数点または 10 進数型[<a href="https://github.com/pingcap/tidb/pull/13756">#13756</a>](https://github.com/pingcap/tidb/pull/13756)に変換すると精度が失われるため、データが正しくなくなる問題を修正
    -   `Quote`関数が`NULL`値[<a href="https://github.com/pingcap/tidb/pull/13681">#13681</a>](https://github.com/pingcap/tidb/pull/13681)を処理するときに、間違ったタイプの値が返される問題を修正します。
    -   `gotime.Local` [<a href="https://github.com/pingcap/tidb/pull/13792">#13792</a>](https://github.com/pingcap/tidb/pull/13792)を使用して文字列から日付を解析した後にタイムゾーンが正しくなくなる問題を修正
    -   `builtinIntervalRealSig` [<a href="https://github.com/pingcap/tidb/pull/13768">#13768</a>](https://github.com/pingcap/tidb/pull/13768)の実装において`binSearch`関数がエラーを返さないため、結果が正しくない場合がある問題を修正
    -   `INSERT`ステートメント実行[<a href="https://github.com/pingcap/tidb/pull/14009">#14009</a>](https://github.com/pingcap/tidb/pull/14009)において文字列型から浮動小数点型への変換時にエラーが発生する場合がある問題を修正
    -   `sum(distinct)`関数[<a href="https://github.com/pingcap/tidb/pull/13041">#13041</a>](https://github.com/pingcap/tidb/pull/13041)から返される誤った結果を修正します。
    -   `CAST`同じ場所の`union`のデータをマージされた型に変換すると、 `jsonUnquoteFunction`関数の戻り値の型の長さが間違った値に指定されているため、 `data too long`返される問題を修正します[<a href="https://github.com/pingcap/tidb/pull/13645">#13645</a>](https://github.com/pingcap/tidb/pull/13645)
    -   権限チェックが厳しすぎるためパスワードが設定できない問題を修正[<a href="https://github.com/pingcap/tidb/pull/13805">#13805</a>](https://github.com/pingcap/tidb/pull/13805)
-   サーバ
    -   `KILL CONNECTION`が goroutine リークを引き起こす可能性がある問題を修正[<a href="https://github.com/pingcap/tidb/pull/13252">#13252</a>](https://github.com/pingcap/tidb/pull/13252)
    -   HTTP API の`info/all`インターフェイスを介したすべての TiDB ノードのbinlogステータスの取得をサポート[<a href="https://github.com/pingcap/tidb/pull/13188">#13188</a>](https://github.com/pingcap/tidb/pull/13188)
    -   Windows [<a href="https://github.com/pingcap/tidb/pull/13650">#13650</a>](https://github.com/pingcap/tidb/pull/13650)で TiDB プロジェクトをビルドできない問題を修正
    -   TiDBサーバー[<a href="https://github.com/pingcap/tidb/pull/13904">#13904</a>](https://github.com/pingcap/tidb/pull/13904)のバージョンを制御および変更するための`server-version`構成項目を追加します。
    -   Go1.13でコンパイルしたバイナリ`plugin`が正常に動作しない問題を修正[<a href="https://github.com/pingcap/tidb/pull/13527">#13527</a>](https://github.com/pingcap/tidb/pull/13527)
-   DDL
    -   テーブルが作成され、テーブルに`COLLATE` [<a href="https://github.com/pingcap/tidb/pull/13190">#13190</a>](https://github.com/pingcap/tidb/pull/13190)含まれている場合、列内のシステムのデフォルトの文字セットの代わりにテーブルの`COLLATE`使用します。
    -   テーブル作成時のインデックス名の長さを制限する[<a href="https://github.com/pingcap/tidb/pull/13311">#13311</a>](https://github.com/pingcap/tidb/pull/13311)
    -   テーブルの名前を変更するときにテーブル名の長さがチェックされない問題を修正[<a href="https://github.com/pingcap/tidb/pull/13345">#13345</a>](https://github.com/pingcap/tidb/pull/13345)
    -   `BIT`列[<a href="https://github.com/pingcap/tidb/pull/13511">#13511</a>](https://github.com/pingcap/tidb/pull/13511)の幅範囲を確認してください
    -   `change/modify column`で出力されるエラー情報を分かりやすくする[<a href="https://github.com/pingcap/tidb/pull/13798">#13798</a>](https://github.com/pingcap/tidb/pull/13798)
    -   ダウンストリームDrainerによってまだ処理されていない`drop column`操作を実行するときに、ダウンストリームが影響を受ける列[<a href="https://github.com/pingcap/tidb/pull/13974">#13974</a>](https://github.com/pingcap/tidb/pull/13974)なしで DML 操作を受信する可能性がある問題を修正します。

## TiKV {#tikv}

-   Raftstore
    -   TiKV の再起動時に発生したpanicを修正し、リージョンを結合してコンパクト ログを適用するプロセスで`is_merging`誤った値が与えられるようにしました[<a href="https://github.com/tikv/tikv/pull/5884">#5884</a>](https://github.com/tikv/tikv/pull/5884)
-   輸入者
    -   gRPC メッセージの長さの制限を削除します[<a href="https://github.com/tikv/tikv/pull/5809">#5809</a>](https://github.com/tikv/tikv/pull/5809)

## PD {#pd}

-   すべてのリージョン[<a href="https://github.com/pingcap/pd/pull/1988">#1988</a>](https://github.com/pingcap/pd/pull/1988)を取得するための HTTP API のパフォーマンスを向上させます。
-   etcd をアップグレードして、etcd PreVote がリーダーを選出できない問題を修正します (ダウングレードはサポートされていません) [<a href="https://github.com/pingcap/pd/pull/2052">#2052</a>](https://github.com/pingcap/pd/pull/2052)

## ツール {#tools}

-   TiDBBinlog
    -   binlogctl [<a href="https://github.com/pingcap/tidb-binlog/pull/777">#777</a>](https://github.com/pingcap/tidb-binlog/pull/777)を介して出力されるノードステータス情報を最適化します。
    -   Drainerフィルタ設定[<a href="https://github.com/pingcap/tidb-binlog/pull/802">#802</a>](https://github.com/pingcap/tidb-binlog/pull/802)の値`nil`が原因で発生したpanicを修正しました。
    -   Pump[<a href="https://github.com/pingcap/tidb-binlog/pull/825">#825</a>](https://github.com/pingcap/tidb-binlog/pull/825)の`Graceful`出口を最適化
    -   Pump がbinlogデータを書き込むときに、より詳細な監視メトリクスを追加します[<a href="https://github.com/pingcap/tidb-binlog/pull/830">#830</a>](https://github.com/pingcap/tidb-binlog/pull/830)
    -   Drainerが DDL 操作を実行した後にテーブル情報を更新するように Drainer のロジックを最適化します[<a href="https://github.com/pingcap/tidb-binlog/pull/836">#836</a>](https://github.com/pingcap/tidb-binlog/pull/836)
    -   Pumpがこのbinlog[<a href="https://github.com/pingcap/tidb-binlog/pull/855">#855</a>](https://github.com/pingcap/tidb-binlog/pull/855)を受信しない場合、DDL 操作のコミットbinlogが無視される問題を修正します。

## TiDB Ansible {#tidb-ansible}

-   TiDB サービスの`Uncommon Error OPM`監視項目の名前を`Write Binlog Error`に変更し、対応するアラート メッセージ[<a href="https://github.com/pingcap/tidb-ansible/pull/1038">#1038</a>](https://github.com/pingcap/tidb-ansible/pull/1038)を追加します。
-   TiSpark を 2.1.8 にアップグレードする[<a href="https://github.com/pingcap/tidb-ansible/pull/1063">#1063</a>](https://github.com/pingcap/tidb-ansible/pull/1063)
