---
title: TiDB 4.0.13 Release Notes
summary: TiDB 4.0.13は2021年5月28日にリリースされました。新機能には、AUTO_INCREMENT`から`AUTO_RANDOM`への変更のサポートと、`infoschema.client_errors_summary`テーブルの追加が含まれます。TiDB、TiKV、PD、 TiFlash、およびToolsの機能強化に加え、TiDB、TiKV、 TiFlash、およびToolsのバグ修正も実装され、クエリ結果、パニック、メモリ使用量などの様々な問題が修正されました。
---

# TiDB 4.0.13 リリースノート {#tidb-4-0-13-release-notes}

発売日：2021年5月28日

TiDB バージョン: 4.0.13

## 新機能 {#new-features}

-   TiDB

    -   `AUTO_INCREMENT`列を`AUTO_RANDOM` [＃24608](https://github.com/pingcap/tidb/pull/24608)に変更するサポート
    -   ユーザーがクライアントに返されたエラーを追跡できるように、 `infoschema.client_errors_summary`テーブルを追加します[＃23267](https://github.com/pingcap/tidb/pull/23267)

## 改善点 {#improvements}

-   TiDB

    -   キャッシュされた統計が最新の場合は、CPU使用率の上昇を避けるために、 `mysql.stats_histograms`テーブルを頻繁に読み取らないようにします[＃24352](https://github.com/pingcap/tidb/pull/24352)

-   TiKV

    -   `store used size`の計算プロセスをより正確にする[＃9904](https://github.com/tikv/tikv/pull/9904)
    -   `EpochNotMatch`メッセージにさらに多くのリージョンを設定すると、リージョンのミス[＃9731](https://github.com/tikv/tikv/pull/9731)が減ります。
    -   長時間稼働するクラスタに蓄積されたメモリの解放を高速化[＃10035](https://github.com/tikv/tikv/pull/10035)

-   PD

    -   TSO処理時間のメトリクスを最適化し、PD側でのTSO処理時間が長すぎるかどうかをユーザーが判断できるようにします[＃3524](https://github.com/pingcap/pd/pull/3524)
    -   ダッシュボードのバージョンをv2021.03.12.1 [＃3469](https://github.com/pingcap/pd/pull/3469)に更新します

-   TiFlash

    -   アーカイブされたデータを自動的に消去してディスク容量を解放します

-   ツール

    -   バックアップと復元 (BR)

        -   `mysql`スキーマ[＃1077](https://github.com/pingcap/br/pull/1077)で作成されたユーザー テーブルのバックアップをサポート
        -   更新`checkVersion`クラスタデータとバックアップデータ[＃1090](https://github.com/pingcap/br/pull/1090)チェックする
        -   バックアップ[＃1062](https://github.com/pingcap/br/pull/1062)中に少数のTiKVノード障害を許容する

    -   TiCDC

        -   メモリオーバーフロー（OOM）を回避するためにプロセッサフロー制御を実装する[＃1751](https://github.com/pingcap/tiflow/pull/1751)
        -   Unified Sorter 内の古い一時ファイルのクリーンアップをサポートし、複数の`cdc server`インスタンスが同じ`sort-dir`ディレクトリ[＃1741](https://github.com/pingcap/tiflow/pull/1741)を共有するのを防ぎます
        -   フェイルポイント[＃1732](https://github.com/pingcap/tiflow/pull/1732) HTTPハンドラを追加する

## バグ修正 {#bug-fixes}

-   TiDB

    -   サブクエリを含む`UPDATE`ステートメントが生成された列[＃24658](https://github.com/pingcap/tidb/pull/24658)を更新する際に発生するpanic問題を修正しました。
    -   データの読み取りにマルチカラムインデックスを使用する際に重複したクエリ結果が発生する問題を修正[＃24634](https://github.com/pingcap/tidb/pull/24634)
    -   DIV式[＃24266](https://github.com/pingcap/tidb/pull/24266)で`BIT`型定数を除数として使用した場合に間違ったクエリ結果が発生する問題を修正しました
    -   `NO_ZERO_IN_DATE` SQLモードがDDL文[＃24185](https://github.com/pingcap/tidb/pull/24185)で設定されたデフォルトの列値に反映されない問題を修正
    -   `BIT`型の列と`INTEGER`型の列の間で`UNION`使用すると間違ったクエリ結果が発生する問題を修正しました[＃24026](https://github.com/pingcap/tidb/pull/24026)
    -   `BINARY`タイプと`CHAR`タイプを比較すると`TableDual`プランが誤って作成される問題を修正しました[＃23917](https://github.com/pingcap/tidb/pull/23917)
    -   `insert ignore on duplicate`文が予期せずテーブルレコード[＃23825](https://github.com/pingcap/tidb/pull/23825)を削除する可能性がある問題を修正しました
    -   監査プラグインが TiDBpanicを引き起こす問題を修正[＃23819](https://github.com/pingcap/tidb/pull/23819)
    -   `HashJoin`演算子が照合順序[＃23812](https://github.com/pingcap/tidb/pull/23812)誤って処理する問題を修正しました
    -   `batch_point_get`悲観的トランザクション[＃23778](https://github.com/pingcap/tidb/pull/23778)で異常値を誤って処理した場合に発生する切断の問題を修正
    -   `tidb_row_format_version`設定値が`1`に設定され、 `enable_new_collation`値が`true` [＃23772](https://github.com/pingcap/tidb/pull/23772)に設定されている場合に発生する不整合なインデックスの問題を修正しました。
    -   `INTEGER`型の列と`STRING`定数値[＃23705](https://github.com/pingcap/tidb/pull/23705)比較する際に発生するバグを修正
    -   `BIT`型の列が`approx_percent`関数[＃23702](https://github.com/pingcap/tidb/pull/23702)に渡されるときに発生するエラーを修正
    -   TiFlashバッチリクエスト[＃23700](https://github.com/pingcap/tidb/pull/23700)を実行する際にTiDBが誤って`TiKV server timeout`エラーを報告するバグを修正しました
    -   プレフィックス列インデックス[＃23691](https://github.com/pingcap/tidb/pull/23691)で演算子`IndexJoin`間違った結果を返す問題を修正しました
    -   `BINARY`型列の照合順序が適切に処理されないため、間違ったクエリ結果が発生する問題を修正しました[＃23598](https://github.com/pingcap/tidb/pull/23598)
    -   `UPDATE`番目の文に`HAVING`番目の句を含む結合クエリが含まれている場合に発生するクエリpanicの問題を修正しました[＃23575](https://github.com/pingcap/tidb/pull/23575)
    -   比較式[＃23474](https://github.com/pingcap/tidb/pull/23474)で定数`NULL`使用するとTiFlashが誤った結果を返す問題を修正しました
    -   `YEAR`型の列と`STRING`定数[＃23335](https://github.com/pingcap/tidb/pull/23335)比較したときに誤った結果が出る問題を修正しました
    -   `session.group_concat_max_len`小さすぎると`group_concat`パニックになる問題を修正[＃23257](https://github.com/pingcap/tidb/pull/23257)
    -   `TIME`型の列[＃23233](https://github.com/pingcap/tidb/pull/23233)に`BETWEEN`式を使用したときに間違ったクエリ結果が発生する問題を修正しました
    -   `DELETE`文[＃23215](https://github.com/pingcap/tidb/pull/23215)の権限チェックの問題を修正
    -   `DECIMAL`型列[＃23196](https://github.com/pingcap/tidb/pull/23196)に無効な文字列を挿入してもエラーが報告されない問題を修正
    -   `DECIMAL`型列[＃23152](https://github.com/pingcap/tidb/pull/23152)にデータを挿入するときに解析エラーが発生する問題を修正しました
    -   `USE_INDEX_MERGE`ヒントが効かない問題を修正[＃22924](https://github.com/pingcap/tidb/pull/22924)
    -   `WHERE`句で`ENUM`列または`SET`列をフィルターとして使用すると、クエリが間違った結果を返すバグを修正しました[＃22814](https://github.com/pingcap/tidb/pull/22814)
    -   クラスター化インデックスと新しい照合順序を同時に使用するとクエリが間違った結果を返すバグを修正[＃21408](https://github.com/pingcap/tidb/pull/21408)
    -   `enable_new_collation`有効にした状態で`ANALYZE`実行した際に発生するpanicを修正[＃21299](https://github.com/pingcap/tidb/pull/21299)
    -   SQLビューがSQL DEFINER [＃24531](https://github.com/pingcap/tidb/pull/24531)に関連付けられたデフォルトのロールを正しく処理しない問題を修正しました。
    -   DDLジョブのキャンセルがスタックする問題を修正[＃24445](https://github.com/pingcap/tidb/pull/24445)
    -   `concat`関数が照合順序[＃24300](https://github.com/pingcap/tidb/pull/24300)誤って処理する問題を修正しました
    -   `SELECT`のフィールドに`IN`サブクエリがあり、そのサブクエリの外側に`NULL` [＃24022](https://github.com/pingcap/tidb/pull/24022)タプルが含まれている場合にクエリが間違った結果を返すバグを修正しました。
    -   `TableScan`が降順の場合にオプティマイザによってTiFlashが誤って選択されるバグを修正[＃23974](https://github.com/pingcap/tidb/pull/23974)
    -   `point_get`プランがMySQL [＃23970](https://github.com/pingcap/tidb/pull/23970)と一致しない列名を返すバグを修正しました
    -   大文字の名前を持つデータベースで`show table status`文を実行すると間違った結果が返される問題を修正しました[＃23958](https://github.com/pingcap/tidb/pull/23958)
    -   テーブルに対して同時に`INSERT`と`DELETE`権限を持たないユーザーが`REPLACE`操作[＃23938](https://github.com/pingcap/tidb/pull/23938)実行できるバグを修正しました。
    -   照合順序が正しく処理されていないため、 `concat` / `make_set` / `insert`式の結果が間違っている問題を修正しました[＃23878](https://github.com/pingcap/tidb/pull/23878)
    -   `RANGE`パーティション[＃23689](https://github.com/pingcap/tidb/pull/23689)を持つテーブルでクエリを実行するときに発生するpanicを修正しました
    -   問題を修正: 以前のバージョンのクラスターで、変数`tidb_enable_table_partition` `false`に設定されている場合、パーティションを含むテーブルは非パーティションテーブルとして扱われます。クラスターを新しいバージョンにアップグレードした後、このテーブルに対して`batch point get`クエリを実行すると、接続panicが発生します[＃23682](https://github.com/pingcap/tidb/pull/23682)
    -   TiDB が TCP および UNIX ソケットを listen するように構成されている場合、TCP 接続経由のリモート ホストが接続[＃23513](https://github.com/pingcap/tidb/pull/23513)に対して正しく検証されない問題を修正しました。
    -   デフォルト以外の照合順序で間違ったクエリ結果が発生するバグを修正[＃22923](https://github.com/pingcap/tidb/pull/22923)
    -   Grafanaの**コプロセッサー Cache**パネルが動作しないバグを修正[＃22617](https://github.com/pingcap/tidb/pull/22617)
    -   オプティマイザが統計キャッシュ[＃22565](https://github.com/pingcap/tidb/pull/22565)アクセスする際に発生するエラーを修正

-   TiKV

    -   `file_dict`ファイルが完全に書き込まれていないディスクが[＃9963](https://github.com/tikv/tikv/pull/9963)ある場合、TiKVが起動できないバグを修正しました。
    -   TiCDCのスキャン速度をデフォルトで128MB/秒に制限する[＃9983](https://github.com/tikv/tikv/pull/9983)
    -   TiCDCの初期スキャン[＃10133](https://github.com/tikv/tikv/pull/10133)のメモリ使用量を削減
    -   TiCDCのスキャン速度[＃10142](https://github.com/tikv/tikv/pull/10142)バックプレッシャーをサポート
    -   TiCDC の古い値を取得するための不要な読み取りを回避することで、潜在的な OOM 問題を修正しました[＃10031](https://github.com/tikv/tikv/pull/10031)
    -   古い値の読み取りによって引き起こされる TiCDC OOM 問題を修正[＃10197](https://github.com/tikv/tikv/pull/10197)
    -   S3 ストレージにタイムアウトメカニズムを追加して、クライアントが応答なしでハングするのを防ぎます[＃10132](https://github.com/tikv/tikv/pull/10132)

-   TiFlash

    -   `delta-merge-tasks`の数がPrometheusに報告されない問題を修正
    -   `Segment Split`中に発生するTiFlashpanic問題を修正
    -   Grafanaの`Region write Duration (write blocks)`パネルが間違った場所に表示される問題を修正しました
    -   storageエンジンがデータの削除に失敗する潜在的な問題を修正
    -   `TIME`型を`INTEGER`型にキャストしたときに結果が不正確になる問題を修正しました
    -   `bitwise`演算子の動作がTiDBと異なるバグを修正
    -   `STRING`型を`INTEGER`型にキャストしたときに結果が不正確になる問題を修正しました
    -   連続した高速書き込みによりTiFlashのメモリが不足する可能性がある問題を修正しました
    -   テーブルGC中にヌルポインタの例外が発生する可能性がある問題を修正しました
    -   ドロップされたテーブルにデータを書き込むときに発生するTiFlashpanic問題を修正しました
    -   BR復元中に発生するTiFlashpanic問題を修正
    -   一般的なCI照合順序を使用したときに一部の文字の重みが間違っているというバグを修正しました
    -   廃棄されたテーブルでデータが失われる可能性がある問題を修正
    -   ゼロバイトを含む文字列を比較するときに誤った結果が出る問題を修正しました
    -   入力列にNULL定数が含まれている場合に論理関数が間違った結果を返す問題を修正しました
    -   論理関数が数値型のみを受け入れる問題を修正
    -   タイムスタンプ値が`1970-01-01`でタイムゾーン オフセットが負の場合に誤った結果が発生する問題を修正しました
    -   ハッシュ値`Decimal256`が安定しない問題を修正

-   ツール

    -   TiCDC

        -   ソーターの入力チャネルがブロックされたときにフロー制御によって発生するデッドロックの問題を修正しました[＃1779](https://github.com/pingcap/tiflow/pull/1779)
        -   TiCDC チェンジフィード チェックポイント[＃1756](https://github.com/pingcap/tiflow/pull/1756)の停滞により TiKV GC セーフ ポイントがブロックされる問題を修正しました
        -   MySQL [＃1749](https://github.com/pingcap/tiflow/pull/1749)にデータを複製するときに`SUPER`権限を必要とする`explicit_defaults_for_timestamp`の更新を元に戻す

    -   TiDB Lightning

        -   自動コミットが無効になっていると、TiDB Lightning の TiDB バックエンドがデータをロードできないバグを修正しました。
