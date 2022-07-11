---
title: TiDB 4.0.13 Release Notes
---

# TiDB4.0.13リリースノート {#tidb-4-0-13-release-notes}

発売日：2021年5月28日

TiDBバージョン：4.0.13

## 新機能 {#new-features}

-   TiDB

    -   `AUTO_INCREMENT`列から`AUTO_RANDOM`列への変更をサポート[＃24608](https://github.com/pingcap/tidb/pull/24608)
    -   `infoschema.client_errors_summary`のテーブルを追加して、ユーザーがクライアントに返されたエラーを追跡できるようにします[＃23267](https://github.com/pingcap/tidb/pull/23267)

## 改善 {#improvements}

-   TiDB

    -   キャッシュされた統計が最新の場合は、CPU使用率が高くなるのを避けるために、 `mysql.stats_histograms`テーブルを頻繁に[＃24352](https://github.com/pingcap/tidb/pull/24352)ことは避けてください。

-   TiKV

    -   `store used size`の計算プロセスをより正確にします[＃9904](https://github.com/tikv/tikv/pull/9904)
    -   リージョンミスを減らすために、 `EpochNotMatch`のメッセージにさらにリージョンを設定します[＃9731](https://github.com/tikv/tikv/pull/9731)
    -   長時間実行クラスタに蓄積されたメモリの解放を高速化[＃10035](https://github.com/tikv/tikv/pull/10035)

-   PD

    -   TSO処理時間のメトリックを最適化して、ユーザーがPD側のTSO処理時間が長すぎるかどうかを判断できるようにします[＃3524](https://github.com/pingcap/pd/pull/3524)
    -   ダッシュボードのバージョンをv2021.03.12.1に更新します[＃3469](https://github.com/pingcap/pd/pull/3469)

-   TiFlash

    -   アーカイブされたデータを自動的にクリーンアップして、ディスク領域を解放します

-   ツール

    -   バックアップと復元（BR）

        -   `mysql`スキーマ[＃1077](https://github.com/pingcap/br/pull/1077)で作成されたユーザーテーブルのバックアップをサポートします。
        -   `checkVersion`を更新して、クラスタデータとバックアップデータを確認します[＃1090](https://github.com/pingcap/br/pull/1090)
        -   バックアップ中の少数のTiKVノード障害を許容する[＃1062](https://github.com/pingcap/br/pull/1062)

    -   TiCDC

        -   メモリオーバーフロー（OOM） [＃1751](https://github.com/pingcap/tiflow/pull/1751)を回避するためにプロセッサフロー制御を実装する
        -   Unified Sorterで古い一時ファイルのクリーンアップをサポートし、複数の`cdc server`インスタンスが同じ`sort-dir`ディレクトリを共有しないようにします[＃1741](https://github.com/pingcap/tiflow/pull/1741)
        -   フェイルポイント[＃1732](https://github.com/pingcap/tiflow/pull/1732)のHTTPハンドラーを追加します

## バグの修正 {#bug-fixes}

-   TiDB

    -   サブクエリを含む`UPDATE`ステートメントが生成された列[＃24658](https://github.com/pingcap/tidb/pull/24658)を更新するときに発生するpanicの問題を修正します
    -   データ読み取りに複数列のインデックスを使用すると、クエリ結果が重複する問題を修正します[＃24634](https://github.com/pingcap/tidb/pull/24634)
    -   DIV式[＃24266](https://github.com/pingcap/tidb/pull/24266)の除数として`BIT`型定数を使用すると、誤ったクエリ結果が発生する問題を修正します。
    -   `NO_ZERO_IN_DATE`モードがDDLステートメントで設定されたデフォルトの列値に対して有効にならない問題を修正します[＃24185](https://github.com/pingcap/tidb/pull/24185)
    -   `BIT`タイプの列と`INTEGER`タイプの列の間に`UNION`を使用すると、誤ったクエリ結果が発生する問題を修正します[＃24026](https://github.com/pingcap/tidb/pull/24026)
    -   `BINARY`タイプと`CHAR`タイプ[＃23917](https://github.com/pingcap/tidb/pull/23917)を比較すると、 `TableDual`のプランが誤って作成される問題を修正します。
    -   `insert ignore on duplicate`ステートメントがテーブルレコードを予期せず削除する可能性がある問題を修正します[＃23825](https://github.com/pingcap/tidb/pull/23825)
    -   監査プラグインがTiDBpanicを引き起こす問題を修正します[＃23819](https://github.com/pingcap/tidb/pull/23819)
    -   `HashJoin`オペレーターが照合順序[＃23812](https://github.com/pingcap/tidb/pull/23812)を誤って処理する問題を修正します
    -   `batch_point_get`が悲観的なトランザクション[＃23778](https://github.com/pingcap/tidb/pull/23778)で異常な値を誤って処理するときに発生する切断の問題を修正します
    -   `tidb_row_format_version`構成値が`1`に設定され、 `enable_new_collation`値が`true` [＃23772](https://github.com/pingcap/tidb/pull/23772)に設定されている場合に発生する、一貫性のないインデックスの問題を修正します。
    -   `INTEGER`タイプの列を`STRING`定数値[＃23705](https://github.com/pingcap/tidb/pull/23705)と比較するときに発生するバグを修正します
    -   `BIT`タイプの列が`approx_percent`関数に渡されたときに発生するエラーを修正します[＃23702](https://github.com/pingcap/tidb/pull/23702)
    -   TiFlashバッチリクエストの実行時にTiDBが誤って`TiKV server timeout`エラーを報告する原因となるバグを修正します[＃23700](https://github.com/pingcap/tidb/pull/23700)
    -   `IndexJoin`演算子がプレフィックス列インデックス[＃23691](https://github.com/pingcap/tidb/pull/23691)で間違った結果を返す問題を修正します
    -   `BINARY`タイプの列の照合順序が適切に処理されないために誤ったクエリ結果が発生する問題を修正します[＃23598](https://github.com/pingcap/tidb/pull/23598)
    -   `UPDATE`ステートメントに`HAVING`句[＃23575](https://github.com/pingcap/tidb/pull/23575)の結合クエリが含まれている場合に発生するクエリpanicの問題を修正します。
    -   比較式[＃23474](https://github.com/pingcap/tidb/pull/23474)で`NULL`定数を使用すると、TiFlashが誤った結果を返す原因となる問題を修正します。
    -   `YEAR`タイプの列を`STRING`定数[＃23335](https://github.com/pingcap/tidb/pull/23335)と比較するときの誤った結果の問題を修正します
    -   `session.group_concat_max_len`の設定が小さすぎると`group_concat`がパニックになる問題を修正します[＃23257](https://github.com/pingcap/tidb/pull/23257)
    -   `TIME`タイプの列[＃23233](https://github.com/pingcap/tidb/pull/23233)に`BETWEEN`式を使用したときに発生する誤ったクエリ結果の問題を修正します
    -   `DELETE`ステートメントの特権チェックの問題を修正します[＃23215](https://github.com/pingcap/tidb/pull/23215)
    -   `DECIMAL`タイプの列[＃23196](https://github.com/pingcap/tidb/pull/23196)に無効な文字列を挿入したときにエラーが報告されない問題を修正します
    -   `DECIMAL`タイプの列にデータを挿入するときに発生した解析エラーの問題を修正します[＃23152](https://github.com/pingcap/tidb/pull/23152)
    -   `USE_INDEX_MERGE`ヒントが有効にならない問題を修正します[＃22924](https://github.com/pingcap/tidb/pull/22924)
    -   `WHERE`句の`ENUM`列または`SET`列をフィルターとして使用すると、クエリが誤った結果を返すバグを修正します[＃22814](https://github.com/pingcap/tidb/pull/22814)
    -   クラスタ化されたインデックスと新しい照合順序を同時に使用すると、クエリが間違った結果を返すバグを修正します[＃21408](https://github.com/pingcap/tidb/pull/21408)
    -   `enable_new_collation`を有効にして`ANALYZE`を実行したときに発生するpanicを修正します[＃21299](https://github.com/pingcap/tidb/pull/21299)
    -   SQLビューが[＃24531](https://github.com/pingcap/tidb/pull/24531)に関連付けられたデフォルトのロールを正しく処理しない問題を修正します。
    -   DDLジョブのキャンセルがスタックする問題を修正します[＃24445](https://github.com/pingcap/tidb/pull/24445)
    -   `concat`関数が照合順序[＃24300](https://github.com/pingcap/tidb/pull/24300)を誤って処理する問題を修正します
    -   `SELECT`フィールドに`IN`のサブクエリがあり、サブクエリの外側に`NULL`のタプルが含まれている場合にクエリが誤った結果を返すバグを修正します[＃24022](https://github.com/pingcap/tidb/pull/24022)
    -   `TableScan`が降順[＃23974](https://github.com/pingcap/tidb/pull/23974)の場合に、オプティマイザによってTiFlashが誤って選択されるバグを修正します。
    -   `point_get`プランがMySQL3の列名と矛盾する列名を返すバグを修正し[＃23970](https://github.com/pingcap/tidb/pull/23970)
    -   大文字の名前のデータベースで`show table status`ステートメントを実行すると、間違った結果が返される問題を修正します[＃23958](https://github.com/pingcap/tidb/pull/23958)
    -   テーブルに対する`INSERT`と`DELETE`の特権を同時に持たないユーザーが`REPLACE`の操作を実行できるというバグを修正します[＃23938](https://github.com/pingcap/tidb/pull/23938)
    -   照合順序が正しく処理されないため、 `concat` / `make_set` / `insert`式の結果が間違っている問題を修正します[＃23878](https://github.com/pingcap/tidb/pull/23878)
    -   `RANGE`つのパーティションを持つテーブルでクエリを実行するときに発生するpanicを修正します[＃23689](https://github.com/pingcap/tidb/pull/23689)
    -   問題の修正：以前のバージョンのクラスタでは、 `tidb_enable_table_partition`変数が`false`に設定されている場合、パーティションを含むテーブルは非パーティションテーブルとして処理されます。クラスタが新しいバージョンにアップグレードされたときに、このテーブルで`batch point get`のクエリを実行すると、接続panicが発生します。 [＃23682](https://github.com/pingcap/tidb/pull/23682)
    -   TiDBがTCPおよびUNIXソケットでリッスンするように構成されている場合、TCP接続を介したリモートホストが接続[＃23513](https://github.com/pingcap/tidb/pull/23513)に対して正しく検証されない問題を修正します。
    -   デフォルト以外の照合順序が誤ったクエリ結果を引き起こすバグを修正します[＃22923](https://github.com/pingcap/tidb/pull/22923)
    -   Grafanaの**コプロセッサーキャッシュ**パネルが機能しないバグを修正します[＃22617](https://github.com/pingcap/tidb/pull/22617)
    -   オプティマイザが統計キャッシュにアクセスするときに発生するエラーを修正します[＃22565](https://github.com/pingcap/tidb/pull/22565)

-   TiKV

    -   `file_dict`のファイルがいっぱいになったディスクに完全に書き込まれていない場合にTiKVを起動できないバグを修正します[＃9963](https://github.com/tikv/tikv/pull/9963)
    -   TiCDCのスキャン速度をデフォルトで128MB/秒に制限[＃9983](https://github.com/tikv/tikv/pull/9983)
    -   TiCDCの初期スキャンのメモリ使用量を減らす[＃10133](https://github.com/tikv/tikv/pull/10133)
    -   TiCDCのスキャン速度[＃10142](https://github.com/tikv/tikv/pull/10142)の背圧をサポートする
    -   TiCDCの古い値を取得するための不要な読み取りを回避することにより、潜在的なOOMの問題を修正します[＃10031](https://github.com/tikv/tikv/pull/10031)
    -   古い値の読み取りによって引き起こされるTiCDCOOMの問題を修正します[＃10197](https://github.com/tikv/tikv/pull/10197)
    -   クライアントが応答なしでハングするのを防ぐために、S3ストレージのタイムアウトメカニズムを追加します[＃10132](https://github.com/tikv/tikv/pull/10132)

-   TiFlash

    -   番号`delta-merge-tasks`がPrometheusに報告されない問題を修正します
    -   `Segment Split`の間に発生するTiFlashpanicの問題を修正します
    -   Grafanaの`Region write Duration (write blocks)`のパネルが間違った場所に表示される問題を修正します
    -   ストレージエンジンがデータの削除に失敗するという潜在的な問題を修正します
    -   `TIME`タイプを`INTEGER`タイプにキャストするときの誤った結果の問題を修正します
    -   `bitwise`演算子の動作がTiDBの動作と異なるバグを修正します
    -   `STRING`タイプを`INTEGER`タイプにキャストするときの誤った結果の問題を修正します
    -   連続した高速書き込みによってTiFlashのメモリが不足する可能性がある問題を修正します
    -   テーブルGC中にnullポインタの例外が発生する可能性があるという潜在的な問題を修正します
    -   ドロップされたテーブルにデータを書き込むときに発生するTiFlashpanicの問題を修正します
    -   BRの復元中に発生するTiFlashpanicの問題を修正します
    -   一般的なCI照合順序を使用するときに一部の文字の重みが間違っているバグを修正します
    -   トゥームストーンされたテーブルでデータが失われるという潜在的な問題を修正します
    -   ゼロバイトを含む文字列を比較するときの誤った結果の問題を修正します
    -   入力列にnull定数が含まれている場合、論理関数が誤った結果を返す問題を修正します
    -   論理関数が数値型のみを受け入れるという問題を修正します
    -   タイムスタンプ値が`1970-01-01`で、タイムゾーンオフセットが負の場合に発生する誤った結果の問題を修正します
    -   `Decimal256`のハッシュ値が安定しない問題を修正します

-   ツール

    -   TiCDC

        -   ソーターの入力チャネルがブロックされたときにフロー制御によって引き起こされるデッドロックの問題を修正します[＃1779](https://github.com/pingcap/tiflow/pull/1779)
        -   TiCDCチェンジフィードチェックポイント[＃1756](https://github.com/pingcap/tiflow/pull/1756)の停滞により、TiKVGCセーフポイントがブロックされる問題を修正します。
        -   [＃1749](https://github.com/pingcap/tiflow/pull/1749)にデータを複製するときに`SUPER`特権を必要とする`explicit_defaults_for_timestamp`の更新を元に戻します

    -   TiDB Lightning

        -   自動コミットが無効になっている場合、TiDBLightningのTiDBバックエンドがデータをロードできないバグを修正します
