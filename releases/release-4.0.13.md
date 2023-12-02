---
title: TiDB 4.0.13 Release Notes
---

# TiDB 4.0.13 リリースノート {#tidb-4-0-13-release-notes}

発売日：2021年5月28日

TiDB バージョン: 4.0.13

## 新機能 {#new-features}

-   TiDB

    -   `AUTO_INCREMENT`列から`AUTO_RANDOM`列[#24608](https://github.com/pingcap/tidb/pull/24608)への変更をサポート
    -   `infoschema.client_errors_summary`テーブルを追加して、ユーザーがクライアントに返されたエラーを追跡できるようにします[#23267](https://github.com/pingcap/tidb/pull/23267)

## 改善点 {#improvements}

-   TiDB

    -   `mysql.stats_histograms`キャッシュされた統計が最新の場合は、CPU 使用率が高くなるのを避けるためにテーブルを頻繁に読み取らないようにします[#24352](https://github.com/pingcap/tidb/pull/24352)

-   TiKV

    -   `store used size`の計算処理をより正確にする[#9904](https://github.com/tikv/tikv/pull/9904)
    -   リージョンのミスを減らすために`EpochNotMatch`メッセージにさらに多くの領域を設定します[#9731](https://github.com/tikv/tikv/pull/9731)
    -   長時間実行されているクラスターに蓄積されたメモリの解放を高速化します[#10035](https://github.com/tikv/tikv/pull/10035)

-   PD

    -   TSO 処理時間のメトリクスを最適化して、PD 側の TSO 処理時間が長すぎるかどうかをユーザーが判断できるようにします[#3524](https://github.com/pingcap/pd/pull/3524)
    -   ダッシュボードのバージョンを v2021.03.12.1 に更新します[#3469](https://github.com/pingcap/pd/pull/3469)

-   TiFlash

    -   アーカイブされたデータを自動的にクリーンアップしてディスク領域を解放します

-   ツール

    -   バックアップと復元 (BR)

        -   `mysql`スキーマ[#1077](https://github.com/pingcap/br/pull/1077)で作成されたユーザー テーブルのバックアップのサポート
        -   アップデート`checkVersion`でクラスターデータとバックアップデータを確認します[#1090](https://github.com/pingcap/br/pull/1090)
        -   バックアップ中の少数の TiKV ノード障害を許容する[#1062](https://github.com/pingcap/br/pull/1062)

    -   TiCDC

        -   プロセッサ フロー制御を実装してメモリオーバーフロー (OOM) を回避します[#1751](https://github.com/pingcap/tiflow/pull/1751)
        -   統合ソーターでの古い一時ファイルのクリーンアップをサポートし、複数の`cdc server`インスタンスが`sort-dir`ディレクトリを共有するのを防ぎます[#1741](https://github.com/pingcap/tiflow/pull/1741)
        -   フェイルポイント[#1732](https://github.com/pingcap/tiflow/pull/1732)の HTTP ハンドラーを追加します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   サブクエリを含む`UPDATE`ステートメントが生成された列[#24658](https://github.com/pingcap/tidb/pull/24658)更新するときに発生するpanicの問題を修正します。
    -   データ読み取りに複数列インデックスを使用する場合に重複したクエリ結果が発生する問題を修正します[#24634](https://github.com/pingcap/tidb/pull/24634)
    -   DIV 式[#24266](https://github.com/pingcap/tidb/pull/24266)の除数として`BIT`型定数を使用すると、間違ったクエリ結果が発生する問題を修正します。
    -   `NO_ZERO_IN_DATE` SQL モードが DDL ステートメントで設定されたデフォルトの列値に対して有効にならない問題を修正します[#24185](https://github.com/pingcap/tidb/pull/24185)
    -   `BIT`タイプの列と`INTEGER`タイプの列の間で`UNION`を使用すると、間違ったクエリ結果が発生する問題を修正します[#24026](https://github.com/pingcap/tidb/pull/24026)
    -   `BINARY`タイプと`CHAR`タイプ[#23917](https://github.com/pingcap/tidb/pull/23917)を比較すると、誤って`TableDual`プランが作成されてしまう問題を修正
    -   `insert ignore on duplicate`ステートメントが予期せずテーブル レコード[#23825](https://github.com/pingcap/tidb/pull/23825)を削除する可能性がある問題を修正します。
    -   監査プラグインが TiDBpanic[#23819](https://github.com/pingcap/tidb/pull/23819)を引き起こす問題を修正
    -   `HashJoin`演算子が照合順序[#23812](https://github.com/pingcap/tidb/pull/23812)を誤って処理する問題を修正
    -   `batch_point_get`悲観的トランザクション[#23778](https://github.com/pingcap/tidb/pull/23778)で異常値を誤って処理した場合に切断が発生する問題を修正
    -   `tidb_row_format_version`構成値が`1`に設定され、 `enable_new_collation`値が`true` [#23772](https://github.com/pingcap/tidb/pull/23772)に設定されている場合に発生する不整合なインデックスの問題を修正します。
    -   `INTEGER`型の列と`STRING`定数値[#23705](https://github.com/pingcap/tidb/pull/23705)を比較するときに発生するバグを修正
    -   `BIT` type カラムが`approx_percent`関数に渡されるときに発生するエラーを修正します[#23702](https://github.com/pingcap/tidb/pull/23702)
    -   TiFlashバッチ リクエスト[#23700](https://github.com/pingcap/tidb/pull/23700)の実行時に TiDB が誤って`TiKV server timeout`エラーを報告するバグを修正しました。
    -   `IndexJoin`演算子がプレフィックス列インデックス[#23691](https://github.com/pingcap/tidb/pull/23691)で間違った結果を返す問題を修正します。
    -   `BINARY` type 列の照合順序が適切に処理されないため、間違ったクエリ結果が発生する問題を修正します[#23598](https://github.com/pingcap/tidb/pull/23598)
    -   `UPDATE`ステートメントに`HAVING`句を含む結合クエリが含まれている場合に発生するクエリpanicの問題を修正します[#23575](https://github.com/pingcap/tidb/pull/23575)
    -   比較式[#23474](https://github.com/pingcap/tidb/pull/23474)で定数`NULL`を使用すると、 TiFlashが間違った結果を返す問題を修正します。
    -   `YEAR`型列と`STRING`定数[#23335](https://github.com/pingcap/tidb/pull/23335)を比較するときに間違った結果が表示される問題を修正
    -   `session.group_concat_max_len`の設定が小さすぎると`group_concat`パニックになる問題を修正[#23257](https://github.com/pingcap/tidb/pull/23257)
    -   `TIME`タイプの列[#23233](https://github.com/pingcap/tidb/pull/23233)に`BETWEEN`式を使用すると、間違ったクエリ結果が発生する問題を修正します。
    -   `DELETE`ステートメント[#23215](https://github.com/pingcap/tidb/pull/23215)の権限チェックの問題を修正します。
    -   `DECIMAL`型列[#23196](https://github.com/pingcap/tidb/pull/23196)に無効な文字列を挿入してもエラーが報告されない問題を修正
    -   `DECIMAL`型列[#23152](https://github.com/pingcap/tidb/pull/23152)にデータを挿入すると解析エラーが発生する問題を修正
    -   `USE_INDEX_MERGE`ヒントが反映されない問題を修正[#22924](https://github.com/pingcap/tidb/pull/22924)
    -   `WHERE`句の`ENUM`または`SET`の列をフィルタとして使用すると、クエリが間違った結果を返すバグを修正[#22814](https://github.com/pingcap/tidb/pull/22814)
    -   クラスター化インデックスと新しい照合順序を同時に使用すると、クエリが間違った結果を返すバグを修正します[#21408](https://github.com/pingcap/tidb/pull/21408)
    -   `enable_new_collation`を有効にして`ANALYZE`実行すると発生するpanicを修正[#21299](https://github.com/pingcap/tidb/pull/21299)
    -   SQL ビューが SQL DEFINER [#24531](https://github.com/pingcap/tidb/pull/24531)に関連付けられたデフォルトのロールを正しく処理しない問題を修正します。
    -   DDL ジョブのキャンセルがスタックする問題を修正[#24445](https://github.com/pingcap/tidb/pull/24445)
    -   `concat`関数が照合照合順序[#24300](https://github.com/pingcap/tidb/pull/24300)を正しく処理しない問題を修正します。
    -   `SELECT`フィールドに`IN`サブクエリがあり、サブクエリの外側に`NULL`タプルが含まれる場合、クエリが間違った結果を返すバグを修正[#24022](https://github.com/pingcap/tidb/pull/24022)
    -   降順で`TableScan`が[#23974](https://github.com/pingcap/tidb/pull/23974)の場合、オプティマイザによってTiFlash が誤って選択されるバグを修正
    -   `point_get`プランが MySQL [#23970](https://github.com/pingcap/tidb/pull/23970)と一致しないカラム名を返すバグを修正
    -   大文字の名前を持つデータベースで`show table status`ステートメントを実行すると、間違った結果が返される問題を修正します[#23958](https://github.com/pingcap/tidb/pull/23958)
    -   テーブルに対する`INSERT`と`DELETE`権限を同時に持たないユーザーが`REPLACE`操作を実行できるバグを修正[#23938](https://github.com/pingcap/tidb/pull/23938)
    -   照合順序が正しく処理されないため、 `concat` / `make_set` / `insert`式の結果が間違っている問題を修正します[#23878](https://github.com/pingcap/tidb/pull/23878)
    -   `RANGE`パーティション[#23689](https://github.com/pingcap/tidb/pull/23689)を持つテーブルでクエリを実行するときに発生するpanicを修正しました。
    -   問題の修正: 以前のバージョンのクラスターでは、 `tidb_enable_table_partition`変数が`false`に設定されている場合、パーティションを含むテーブルはパーティション化されていないテーブルとして処理されます。クラスターが新しいバージョンにアップグレードされるときに、このテーブルに対して`batch point get`クエリを実行すると、接続panicが発生します。 [#23682](https://github.com/pingcap/tidb/pull/23682)
    -   TiDB が TCP および UNIX ソケットでリッスンするように構成されている場合、TCP 接続上のリモート ホストが接続[#23513](https://github.com/pingcap/tidb/pull/23513)に対して正しく検証されない問題を修正します。
    -   デフォルト以外の照合順序誤ったクエリ結果が発生するバグを修正[#22923](https://github.com/pingcap/tidb/pull/22923)
    -   Grafana の**コプロセッサー Cache**パネルが動作しないバグを修正[#22617](https://github.com/pingcap/tidb/pull/22617)
    -   オプティマイザが統計キャッシュ[#22565](https://github.com/pingcap/tidb/pull/22565)にアクセスするときに発生するエラーを修正しました。

-   TiKV

    -   `file_dict`ファイルがフルになったディスクに完全に書き込まれていない場合、TiKV が起動できないバグを修正[#9963](https://github.com/tikv/tikv/pull/9963)
    -   TiCDC のスキャン速度をデフォルトで 128MB/s に制限する[#9983](https://github.com/tikv/tikv/pull/9983)
    -   TiCDC の初期スキャン[#10133](https://github.com/tikv/tikv/pull/10133)のメモリ使用量を削減します。
    -   TiCDC のスキャン速度[#10142](https://github.com/tikv/tikv/pull/10142)のバック プレッシャーをサポート
    -   TiCDC の古い値を取得するための不必要な読み取りを回避して、潜在的な OOM 問題を修正します[#10031](https://github.com/tikv/tikv/pull/10031)
    -   古い値の読み取りによって発生する TiCDC OOM 問題を修正します[#10197](https://github.com/tikv/tikv/pull/10197)
    -   応答なしでクライアントがハングするのを避けるために、S3 ストレージにタイムアウト メカニズムを追加します[#10132](https://github.com/tikv/tikv/pull/10132)

-   TiFlash

    -   `delta-merge-tasks`の数値がPrometheusに報告されない問題を修正
    -   `Segment Split`中に発生するTiFlashpanic問題を修正
    -   Grafanaの`Region write Duration (write blocks)`パネルが間違った場所に表示される問題を修正
    -   storageエンジンがデータの削除に失敗するという潜在的な問題を修正します
    -   `TIME`型を`INTEGER`型にキャストするときに誤った結果が表示される問題を修正
    -   `bitwise`オペレーターの挙動がTiDBと異なるバグを修正
    -   `STRING`型を`INTEGER`型にキャストするときに誤った結果が表示される問題を修正
    -   連続した高速書き込みによりTiFlash がメモリ不足になる可能性がある問題を修正
    -   テーブル GC 中に null ポインターの例外が発生する可能性がある潜在的な問題を修正
    -   ドロップされたテーブルにデータを書き込むときに発生するTiFlashpanic問題を修正
    -   BR復元中に発生するTiFlashpanic問題を修正
    -   一般的なCI照合順序を使用した場合、一部の文字の重みが正しくないバグを修正
    -   トゥームストーン化されたテーブルでデータが失われるという潜在的な問題を修正
    -   ゼロバイトを含む文字列を比較すると結果が正しくなくなる問題を修正
    -   入力列に null 定数が含まれている場合、論理関数が間違った結果を返す問題を修正します。
    -   論理関数が数値型のみを受け入れる問題を修正
    -   タイムスタンプ値が`1970-01-01`で、タイムゾーン オフセットが負の場合に発生する誤った結果の問題を修正します。
    -   ハッシュ値`Decimal256`が安定しない問題を修正

-   ツール

    -   TiCDC

        -   ソーターの入力チャネルがブロックされている場合にフロー制御によって引き起こされるデッドロックの問題を修正します[#1779](https://github.com/pingcap/tiflow/pull/1779)
        -   TiCDC チェンジフィード チェックポイント[#1756](https://github.com/pingcap/tiflow/pull/1756)の停滞により TiKV GC セーフ ポイントがブロックされる問題を修正
        -   データを MySQL [#1749](https://github.com/pingcap/tiflow/pull/1749)にレプリケートするときに`SUPER`権限が必要となる`explicit_defaults_for_timestamp`の更新を元に戻します。

    -   TiDB Lightning

        -   自動コミットが無効になっている場合、TiDB Lightning の TiDB バックエンドがデータをロードできないバグを修正
