---
title: TiDB 2.1.19 Release Notes
---

# TiDB2.1.19リリースノート {#tidb-2-1-19-release-notes}

発売日：2019年12月27日

TiDBバージョン：2.1.19

TiDB Ansibleバージョン：2.1.19

## TiDB {#tidb}

-   SQLオプティマイザー
    -   全表スキャン[＃13294](https://github.com/pingcap/tidb/pull/13294)を回避するために、 `select max(_tidb_rowid) from t`のシナリオを最適化します。
    -   クエリでユーザー変数に割り当てられた誤った値と述語のプッシュダウンによって引き起こされた誤った結果を修正します[＃13230](https://github.com/pingcap/tidb/pull/13230)
    -   統計が更新されるとデータ競合が発生するため、統計が正確でない問題を修正します[＃13690](https://github.com/pingcap/tidb/pull/13690)
    -   `UPDATE`ステートメントにサブクエリと保存された生成列の両方が含まれている場合に結果が正しくないという問題を修正します。このステートメントに異なるデータベースからの2つの同じ名前のテーブルが含まれている場合の`UPDATE`ステートメントの実行エラーを修正します[＃13357](https://github.com/pingcap/tidb/pull/13357)
    -   `PhysicalUnionScan`演算子が統計を誤って設定するため、クエリプランが誤って選択される可能性がある問題を修正します[＃14134](https://github.com/pingcap/tidb/pull/14134)
    -   `minAutoAnalyzeRatio`の制約を削除して、自動`ANALYZE`をよりタイムリーに[＃14013](https://github.com/pingcap/tidb/pull/14013)にします。
    -   `WHERE`句に一意キー[＃13385](https://github.com/pingcap/tidb/pull/13385)の等しい条件が含まれている場合に、推定行数が`1`より大きい問題を修正します。
-   SQL実行エンジン
    -   `ConvertJSONToInt`の`unit64`の中間結果として`int64`を使用する場合の精度オーバーフローを修正します[＃13036](https://github.com/pingcap/tidb/pull/13036)
    -   `SLEEP`関数がクエリ（たとえば、 `select 1 from (select sleep(1)) t;)` ）にある場合、列のプルーニングによってクエリの`sleep(1)`が無効になる問題を修正します[＃13039](https://github.com/pingcap/tidb/pull/13039)
    -   `INSERT ON DUPLICATE UPDATE`ステートメント[＃12999](https://github.com/pingcap/tidb/pull/12999)で`Chunk`を再利用することにより、メモリのオーバーヘッドを削減します。
    -   `slow_query`テーブル[＃13129](https://github.com/pingcap/tidb/pull/13129)のトランザクション関連フィールドをさらに追加します。
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
    -   `UPDATE`ステートメントに含まれるサブクエリが誤って変換される問題を修正します。 `WHERE`句にサブクエリ[＃13120](https://github.com/pingcap/tidb/pull/13120)が含まれている場合の`UPDATE`実行の失敗を修正
    -   パーティションテーブル[＃13143](https://github.com/pingcap/tidb/pull/13143)での`ADMIN CHECK TABLE`の実行をサポート
    -   `ON UPDATE CURRENT_TIMESTAMP`が列属性として使用され、浮動小数点の精度が指定されている場合、 `SHOW CREATE TABLE`などのステートメントの精度が不完全になる問題を修正します[＃12462](https://github.com/pingcap/tidb/pull/12462)
    -   列[＃14162](https://github.com/pingcap/tidb/pull/14162)を削除、変更、または変更するときに外部キーがチェックされないため、 `SELECT * FROM information_schema.KEY_COLUMN_USAGE`ステートメントの実行時に発生したpanicを修正します。
    -   TiDB [＃13255](https://github.com/pingcap/tidb/pull/13255)で`Streaming`を有効にすると、返されるデータが重複する可能性がある問題を修正します。
    -   夏時間[＃13624](https://github.com/pingcap/tidb/pull/13624)によって引き起こされる`Invalid time format`のエラーを修正します
    -   整数を符号なし浮動小数点または10進型[＃13756](https://github.com/pingcap/tidb/pull/13756)に変換すると精度が失われるため、データが正しくないという問題を修正します。
    -   `Quote`関数が`NULL`値を処理するときに誤ったタイプの値が返される問題を修正します[＃13681](https://github.com/pingcap/tidb/pull/13681)
    -   `gotime.Local` [＃13792](https://github.com/pingcap/tidb/pull/13792)を使用して文字列から日付を解析した後、タイムゾーンが正しくない問題を修正します
    -   `binSearch`関数は[＃13768](https://github.com/pingcap/tidb/pull/13768)の実装でエラーを返さないため、結果が正しくない可能性があるという問題を修正し`builtinIntervalRealSig` 。
    -   `INSERT`ステートメントの実行で文字列型を浮動小数点型に変換するときにエラーが発生する可能性がある問題を修正します[＃14009](https://github.com/pingcap/tidb/pull/14009)
    -   `sum(distinct)`関数[＃13041](https://github.com/pingcap/tidb/pull/13041)から返される誤った結果を修正します
    -   同じ場所の`union`のデータをマージされた`CAST`に変換するときに`data too long`が返される問題を修正します。これは、 `jsonUnquoteFunction`関数の返された型の長さに誤った値が与えられるためです[＃13645](https://github.com/pingcap/tidb/pull/13645)
    -   特権チェックが厳しすぎるためにパスワードを設定できない問題を修正します[＃13805](https://github.com/pingcap/tidb/pull/13805)
-   サーバ
    -   `KILL CONNECTION`がゴルーチンリークを引き起こす可能性がある問題を修正します[＃13252](https://github.com/pingcap/tidb/pull/13252)
    -   HTTPAPI3の`info/all`のインターフェイスを介してすべてのTiDBノードのbinlogステータスを取得することをサポートし[＃13188](https://github.com/pingcap/tidb/pull/13188)
    -   Windows1で[＃13650](https://github.com/pingcap/tidb/pull/13650)プロジェクトをビルドできない問題を修正します
    -   `server-version`の構成アイテムを追加して、TiDBサーバー[＃13904](https://github.com/pingcap/tidb/pull/13904)のバージョンを制御および変更します。
    -   Go1.13でコンパイルされたバイナリ`plugin`が正常に実行されない問題を修正します[＃13527](https://github.com/pingcap/tidb/pull/13527)
-   DDL
    -   テーブルが作成され、テーブルに`COLLATE` [＃13190](https://github.com/pingcap/tidb/pull/13190)が含まれている場合は、列にシステムのデフォルトの文字セットの代わりにテーブルの`COLLATE`を使用します。
    -   テーブルを作成するときにインデックス名の長さを制限する[＃13311](https://github.com/pingcap/tidb/pull/13311)
    -   テーブルの名前を変更するときにテーブル名の長さがチェックされない問題を修正します[＃13345](https://github.com/pingcap/tidb/pull/13345)
    -   `BIT`列[＃13511](https://github.com/pingcap/tidb/pull/13511)の幅範囲を確認してください
    -   `change/modify column`から出力されるエラー情報をわかりやすくする[＃13798](https://github.com/pingcap/tidb/pull/13798)
    -   ダウンストリームDrainerによってまだ処理されていない`drop column`の操作を実行すると、影響を受ける列[＃13974](https://github.com/pingcap/tidb/pull/13974)なしでダウンストリームがDML操作を受け取る可能性があるという問題を修正します。

## TiKV {#tikv}

-   ラフトストア
    -   TiKVを再起動したときに発生したpanicを修正し、リージョンをマージしてコンパクトログ[＃5884](https://github.com/tikv/tikv/pull/5884)を適用するプロセスで`is_merging`に誤った値が指定された
-   輸入業者
    -   gRPCメッセージの長さ[＃5809](https://github.com/tikv/tikv/pull/5809)の制限を削除します

## PD {#pd}

-   すべてのリージョンを取得するためのHTTPAPIのパフォーマンスを改善する[＃1988](https://github.com/pingcap/pd/pull/1988)
-   etcdをアップグレードして、etcd PreVoteがリーダーを選出できない問題を修正します（ダウングレードはサポートされていません） [＃2052](https://github.com/pingcap/pd/pull/2052)

## ツール {#tools}

-   TiDB Binlog
    -   [＃777](https://github.com/pingcap/tidb-binlog/pull/777)を介して出力されるノードステータス情報を最適化します。
    -   Drainerフィルター構成[＃802](https://github.com/pingcap/tidb-binlog/pull/802)の`nil`の値が原因で発生したpanicを修正します。
    -   Pump[＃825](https://github.com/pingcap/tidb-binlog/pull/825)の`Graceful`の出口を最適化します
    -   Pumpがbinlogデータを書き込むときに、より詳細な監視メトリックを追加します[＃830](https://github.com/pingcap/tidb-binlog/pull/830)
    -   DrainerがDDL操作を実行した後にテーブル情報を更新するようにDrainerのロジックを最適化する[＃836](https://github.com/pingcap/tidb-binlog/pull/836)
    -   Pumpがこの[＃855](https://github.com/pingcap/tidb-binlog/pull/855)を受信しない場合、DDL操作のcommitbinlogが無視される問題を修正します。

## TiDB Ansible {#tidb-ansible}

-   TiDBサービスの`Uncommon Error OPM`の監視項目の名前を`Write Binlog Error`に変更し、対応するアラートメッセージを追加します[＃1038](https://github.com/pingcap/tidb-ansible/pull/1038)
-   TiSparkを2.1.81にアップグレードし[＃1063](https://github.com/pingcap/tidb-ansible/pull/1063)
