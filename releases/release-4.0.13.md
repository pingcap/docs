---
title: TiDB 4.0.13 Release Notes
---

# TiDB 4.0.13 リリースノート {#tidb-4-0-13-release-notes}

発売日：2021年5月28日

TiDB バージョン: 4.0.13

## 新機能 {#new-features}

-   TiDB

    -   `AUTO_INCREMENT`列から`AUTO_RANDOM` 1 [#24608](https://github.com/pingcap/tidb/pull/24608)への変更をサポート
    -   `infoschema.client_errors_summary`テーブルを追加して、ユーザーがクライアントに返されたエラーを追跡できるようにします[#23267](https://github.com/pingcap/tidb/pull/23267)

## 改良点 {#improvements}

-   TiDB

    -   CPU 使用率が高くならないように、キャッシュされた統計が最新の場合は`mysql.stats_histograms`テーブルを頻繁に読み取らないようにしてください[#24352](https://github.com/pingcap/tidb/pull/24352)

-   TiKV

    -   `store used size`の計算過程をより正確にする[#9904](https://github.com/tikv/tikv/pull/9904)
    -   `EpochNotMatch`メッセージでより多くのリージョンを設定して、リージョンのミスを減らします[#9731](https://github.com/tikv/tikv/pull/9731)
    -   長時間実行クラスタに蓄積されたメモリの解放を高速化する[#10035](https://github.com/tikv/tikv/pull/10035)

-   PD

    -   PD 側の TSO 処理時間が長すぎるかどうかをユーザーが判別できるように、TSO 処理時間のメトリックを最適化します[#3524](https://github.com/pingcap/pd/pull/3524)
    -   ダッシュボードのバージョンを v2021.03.12.1 に更新する[#3469](https://github.com/pingcap/pd/pull/3469)

-   TiFlash

    -   アーカイブされたデータを自動的に消去して、ディスク領域を解放します

-   ツール

    -   バックアップと復元 (BR)

        -   `mysql`スキーマで作成されたユーザー テーブルのバックアップのサポート[#1077](https://github.com/pingcap/br/pull/1077)
        -   クラスタデータとバックアップデータを確認するための更新`checkVersion` [#1090](https://github.com/pingcap/br/pull/1090)
        -   バックアップ中の少数の TiKV ノード障害を許容する[#1062](https://github.com/pingcap/br/pull/1062)

    -   TiCDC

        -   プロセッサ フロー制御を実装して、メモリオーバーフロー (OOM) を回避します[#1751](https://github.com/pingcap/tiflow/pull/1751)
        -   Unified Sorter の古い一時ファイルのクリーンアップをサポートし、複数の`cdc server`インスタンスが同じディレクトリを共有するのを防ぎます`sort-dir` [#1741](https://github.com/pingcap/tiflow/pull/1741)
        -   フェイルポイント[#1732](https://github.com/pingcap/tiflow/pull/1732)の HTTP ハンドラーを追加します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   サブクエリを含む`UPDATE`ステートメントが生成された列を更新するときに発生するpanicの問題を修正します[#24658](https://github.com/pingcap/tidb/pull/24658)
    -   データ読み取りに複数列インデックスを使用すると、クエリ結果が重複する問題を修正します[#24634](https://github.com/pingcap/tidb/pull/24634)
    -   DIV 式[#24266](https://github.com/pingcap/tidb/pull/24266)の除数として`BIT`型定数を使用すると、間違ったクエリ結果が発生する問題を修正します。
    -   1 DDL ステートメントで設定されたデフォルトのカラム値に対して`NO_ZERO_IN_DATE` SQL モードが有効にならない問題を修正します[#24185](https://github.com/pingcap/tidb/pull/24185)
    -   `BIT`型の列と`INTEGER`型の列の間で`UNION`使用すると、間違ったクエリ結果が返される問題を修正します[#24026](https://github.com/pingcap/tidb/pull/24026)
    -   `BINARY`型と`CHAR`型[#23917](https://github.com/pingcap/tidb/pull/23917)を比較する際、誤って`TableDual`型が作成される問題を修正
    -   `insert ignore on duplicate`ステートメントが予期せずテーブル レコードを削除する可能性がある問題を修正します[#23825](https://github.com/pingcap/tidb/pull/23825)
    -   Audit プラグインが TiDBpanic[#23819](https://github.com/pingcap/tidb/pull/23819)を引き起こす問題を修正
    -   `HashJoin`演算子が照合順序[#23812](https://github.com/pingcap/tidb/pull/23812)を誤って処理する問題を修正します
    -   `batch_point_get`悲観的トランザクションで異常値を誤って処理した場合に切断が発生する問題を修正[#23778](https://github.com/pingcap/tidb/pull/23778)
    -   `tidb_row_format_version`構成値が`1`に設定され、 `enable_new_collation`値が`true` [#23772](https://github.com/pingcap/tidb/pull/23772)に設定されている場合に発生する不整合なインデックスの問題を修正します。
    -   `INTEGER`型列と`STRING`型定数値[#23705](https://github.com/pingcap/tidb/pull/23705)を比較した際に発生する不具合を修正
    -   `approx_percent`関数[#23702](https://github.com/pingcap/tidb/pull/23702)に`BIT`型の列を渡すと発生するエラーを修正します。
    -   TiFlashバッチ リクエスト[#23700](https://github.com/pingcap/tidb/pull/23700)の実行時に、TiDB が誤って`TiKV server timeout`エラーを報告する原因となるバグを修正します。
    -   接頭辞列インデックス[#23691](https://github.com/pingcap/tidb/pull/23691)で`IndexJoin`演算子が間違った結果を返す問題を修正します。
    -   `BINARY`タイプ列の照合順序が適切に処理されないために、間違ったクエリ結果を引き起こす問題を修正します[#23598](https://github.com/pingcap/tidb/pull/23598)
    -   `UPDATE`ステートメントに`HAVING`句[#23575](https://github.com/pingcap/tidb/pull/23575)の結合クエリが含まれている場合に発生するクエリpanicの問題を修正します。
    -   比較式[#23474](https://github.com/pingcap/tidb/pull/23474)で定数`NULL`を使用すると、 TiFlashが間違った結果を返す問題を修正します。
    -   `YEAR`型列と`STRING`定数[#23335](https://github.com/pingcap/tidb/pull/23335)を比較すると間違った結果になる問題を修正
    -   `session.group_concat_max_len`小さすぎると`group_concat`パニックになる問題を修正[#23257](https://github.com/pingcap/tidb/pull/23257)
    -   `TIME`型列[#23233](https://github.com/pingcap/tidb/pull/23233)に`BETWEEN`式を使用した場合に発生する間違ったクエリ結果の問題を修正します。
    -   `DELETE`文の権限チェックの問題を修正[#23215](https://github.com/pingcap/tidb/pull/23215)
    -   `DECIMAL`型の列[#23196](https://github.com/pingcap/tidb/pull/23196)に無効な文字列を挿入してもエラーが報告されない問題を修正
    -   `DECIMAL`型列にデータを挿入すると解析エラーが発生する問題を修正[#23152](https://github.com/pingcap/tidb/pull/23152)
    -   `USE_INDEX_MERGE`ヒントが有効にならない問題を修正[#22924](https://github.com/pingcap/tidb/pull/22924)
    -   `WHERE`節で`ENUM`列または`SET`列をフィルターとして使用すると、クエリが間違った結果を返すというバグを修正します[#22814](https://github.com/pingcap/tidb/pull/22814)
    -   クラスター化インデックスと新しい照合順序を同時に使用すると、クエリが間違った結果を返すというバグを修正します[#21408](https://github.com/pingcap/tidb/pull/21408)
    -   `enable_new_collation`を有効にして`ANALYZE`実行するとpanicを修正[#21299](https://github.com/pingcap/tidb/pull/21299)
    -   SQL ビューが、SQL DEFINER [#24531](https://github.com/pingcap/tidb/pull/24531)に関連付けられたデフォルトのロールを正しく処理しないという問題を修正します。
    -   DDL ジョブのキャンセルがスタックする問題を修正します[#24445](https://github.com/pingcap/tidb/pull/24445)
    -   `concat`関数が照合順序[#24300](https://github.com/pingcap/tidb/pull/24300)を正しく処理しない問題を修正
    -   `SELECT`フィールドに`IN`サブクエリがあり、サブクエリの外側に`NULL`タプルが含まれている場合、クエリが間違った結果を返すというバグを修正します[#24022](https://github.com/pingcap/tidb/pull/24022)
    -   `TableScan`が降順[#23974](https://github.com/pingcap/tidb/pull/23974)の場合、オプティマイザーがTiFlash を誤って選択するバグを修正
    -   `point_get`プランがMySQL [#23970](https://github.com/pingcap/tidb/pull/23970)と矛盾するカラム名を返すバグを修正
    -   大文字の名前を持つデータベースで`show table status`ステートメントを実行すると、間違った結果が返される問題を修正します[#23958](https://github.com/pingcap/tidb/pull/23958)
    -   テーブルに対して`INSERT`と`DELETE`権限を同時に持っていないユーザーが`REPLACE`操作を実行できるというバグを修正[#23938](https://github.com/pingcap/tidb/pull/23938)
    -   照合順序が正しく処理されないため、 `concat` / `make_set` / `insert`式の結果が間違っている問題を修正します[#23878](https://github.com/pingcap/tidb/pull/23878)
    -   `RANGE`パーティション[#23689](https://github.com/pingcap/tidb/pull/23689)を持つテーブルでクエリを実行すると発生するpanicを修正します。
    -   問題を修正: 以前のバージョンのクラスターでは、変数`tidb_enable_table_partition`が`false`に設定されている場合、パーティションを含むテーブルは非パーティション テーブルとして処理されます。このテーブルで`batch point get`クエリを実行すると、クラスターが新しいバージョンにアップグレードされると、接続panicが発生します。 [#23682](https://github.com/pingcap/tidb/pull/23682)
    -   TiDB が TCP および UNIX ソケットでリッスンするように構成されている場合、TCP 接続を介したリモート ホストが接続[#23513](https://github.com/pingcap/tidb/pull/23513)に対して正しく検証されないという問題を修正します。
    -   デフォルト以外の照合順序が間違ったクエリ結果を引き起こすバグを修正します[#22923](https://github.com/pingcap/tidb/pull/22923)
    -   Grafana の**コプロセッサー Cache**パネルが動作しない不具合を修正[#22617](https://github.com/pingcap/tidb/pull/22617)
    -   オプティマイザーが統計キャッシュにアクセスするときに発生するエラーを修正します[#22565](https://github.com/pingcap/tidb/pull/22565)

-   TiKV

    -   満杯になったディスクに`file_dict`ファイルが完全に書き込まれていないとTiKVが起動できない不具合を修正[#9963](https://github.com/tikv/tikv/pull/9963)
    -   TiCDC のスキャン速度をデフォルトで 128MB/s に制限します[#9983](https://github.com/tikv/tikv/pull/9983)
    -   TiCDC の初期スキャン[#10133](https://github.com/tikv/tikv/pull/10133)のメモリ使用量を減らす
    -   TiCDC のスキャン速度[#10142](https://github.com/tikv/tikv/pull/10142)のバック プレッシャーをサポート
    -   不要な読み取りを回避して TiCDC の古い値を取得することで、潜在的な OOM の問題を修正します[#10031](https://github.com/tikv/tikv/pull/10031)
    -   古い値を読み取ることによって発生する TiCDC OOM の問題を修正します[#10197](https://github.com/tikv/tikv/pull/10197)
    -   S3 ストレージのタイムアウト メカニズムを追加して、応答なしでクライアントがハングするのを回避します[#10132](https://github.com/tikv/tikv/pull/10132)

-   TiFlash

    -   Prometheus に`delta-merge-tasks`の数が報告されない問題を修正
    -   `Segment Split`で発生するTiFlashpanicの問題を修正します。
    -   Grafana の`Region write Duration (write blocks)`パネルが間違った場所に表示される問題を修正
    -   storageエンジンがデータの削除に失敗する潜在的な問題を修正します。
    -   `TIME`型を`INTEGER`型にキャストしたときの結果が正しくない問題を修正
    -   `bitwise`オペレータの挙動がTiDBと異なる不具合を修正
    -   `STRING`型を`INTEGER`型にキャストしたときの結果が正しくない問題を修正
    -   連続した高速書き込みによってTiFlash がメモリ不足になる問題を修正
    -   テーブル GC 中に null ポインターの例外が発生する可能性がある潜在的な問題を修正します。
    -   削除されたテーブルにデータを書き込むときに発生するTiFlashpanicの問題を修正します
    -   BR復元中に発生するTiFlashpanicの問題を修正
    -   一般的な CI照合順序を使用すると、一部の文字の重みが間違っているというバグを修正します
    -   廃棄されたテーブルでデータが失われる可能性がある問題を修正します
    -   ゼロ バイトを含む文字列を比較すると、誤った結果が返される問題を修正します。
    -   入力列に null 定数が含まれている場合、論理関数が間違った結果を返す問題を修正します。
    -   論理関数が数値型しか受け付けない問題を修正
    -   タイムスタンプ値が`1970-01-01`で、タイムゾーン オフセットが負の場合に発生する誤った結果の問題を修正します。
    -   `Decimal256`のハッシュ値が安定しない問題を修正

-   ツール

    -   TiCDC

        -   ソーターの入力チャネルがブロックされている場合にフロー制御によって引き起こされるデッドロックの問題を修正します[#1779](https://github.com/pingcap/tiflow/pull/1779)
        -   TiCDC changefeed チェックポイント[#1756](https://github.com/pingcap/tiflow/pull/1756)の停滞により、TiKV GC セーフポイントがブロックされる問題を修正
        -   MySQL [#1749](https://github.com/pingcap/tiflow/pull/1749)にデータをレプリケートするときに`SUPER`権限が必要な`explicit_defaults_for_timestamp`の更新を元に戻します

    -   TiDB Lightning

        -   自動コミットが無効になっていると、TiDB Lightning の TiDB バックエンドがデータを読み込めないというバグを修正
