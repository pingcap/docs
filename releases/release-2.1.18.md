---
title: TiDB 2.1.18 Release Notes
summary: TiDB 2.1.18は2019年11月4日にリリースされました。このリリースには、SQLオプティマイザー、SQLエンジン、サーバー、DDL、モニター、ツールに関する様々な修正と最適化が含まれています。注目すべき改善点としては、ORDER BY、GROUP BY、LIMIT OFFSETにおけるパラメータの使用のサポート、インデックス追加操作の進行状況を監視するための新しいメトリクスの追加などが挙げられます。TiDB Ansibleバージョン2.1.18には、TiDB Binlogの更新と新しい監視項目も含まれています。
---

# TiDB 2.1.18 リリースノート {#tidb-2-1-18-release-notes}

発売日：2019年11月4日

TiDB バージョン: 2.1.18

TiDB Ansible バージョン: 2.1.18

## TiDB {#tidb}

-   SQLオプティマイザー
    -   フィードバック[＃12172](https://github.com/pingcap/tidb/pull/12172)で分割すると無効なクエリ範囲が表示される可能性がある問題を修正しました
    -   ポイント取得プラン[＃12341](https://github.com/pingcap/tidb/pull/12341)で権限チェックが正しく行われない問題を修正
    -   Limit演算子を`IndexLookUpReader`実行ロジック[＃12380](https://github.com/pingcap/tidb/pull/12380)にプッシュすることで、 `select ... limit ... offset …`文の実行パフォーマンスを最適化します。
    -   `ORDER BY` `GROUP BY` [＃12514](https://github.com/pingcap/tidb/pull/12514) `LIMIT OFFSET`使用をサポート
    -   パーティションテーブル`IndexJoin`が誤った結果を返す問題を修正[＃12713](https://github.com/pingcap/tidb/pull/12713)
    -   日付文字列とフォーマット文字列が一致しない場合に、TiDBの`str_to_date`関数がMySQLとは異なる結果を返す問題を修正しました[＃12757](https://github.com/pingcap/tidb/pull/12757)
    -   クエリ条件に`cast`関数が含まれている場合に外部結合が誤って内部結合に変換される問題を修正しました[＃12791](https://github.com/pingcap/tidb/pull/12791)
    -   `AntiSemiJoin` [＃12800](https://github.com/pingcap/tidb/pull/12800)の結合条件で渡される誤った式を修正
-   SQLエンジン
    -   時間の丸めが間違っている問題を修正（例えば、 `2019-09-11 11:17:47.999999666` `2019-09-11 11:17:48`に丸められるべき） [＃12259](https://github.com/pingcap/tidb/pull/12259)
    -   監視レコード[＃12329](https://github.com/pingcap/tidb/pull/12329)に、ステートメント`PREPARE`の`sql_type`による期間が表示されない問題を修正しました。
    -   `from_unixtime`関数が null [＃12572](https://github.com/pingcap/tidb/pull/12572)を処理するときに発生panic問題を修正
    -   `YEAR`型として無効な値が挿入されると、結果が`0000` [＃12744](https://github.com/pingcap/tidb/pull/12744)ではなく`NULL`なるという互換性の問題を修正しました。
    -   `AutoIncrement`列が暗黙的に割り当てられた場合の動作を改善し、MySQLの自動インクリメントロックのデフォルトモード（ [「連続」ロックモード](https://dev.mysql.com/doc/refman/5.7/en/innodb-auto-increment-handling.html) ）との一貫性を保ちます。1行の`Insert`文で複数の`AutoIncrement` IDを暗黙的に割り当てる場合、TiDBは割り当てられた値の連続性を保証します。この改善により、JDBC `getGeneratedKeys()`メソッドはどのようなシナリオでも正しい結果を得ることができます[＃12619](https://github.com/pingcap/tidb/pull/12619)
    -   `HashAgg` `Apply` [＃12769](https://github.com/pingcap/tidb/pull/12769)の子ノードとして機能するときにクエリがハングする問題を修正しました
    -   型変換[＃12813](https://github.com/pingcap/tidb/pull/12813)に関して、 `AND`と`OR`論理式が誤った結果を返す問題を修正しました。
-   サーバ
    -   `SLEEP()`関数が`KILL TIDB QUERY`ステートメント[＃12159](https://github.com/pingcap/tidb/pull/12159)に対して無効であるという問題を修正
    -   `AUTO_INCREMENT` `MAX int64`と`MAX uint64`誤って割り当てた場合にエラーが報告されない問題を修正しました[＃12210](https://github.com/pingcap/tidb/pull/12210)
    -   ログレベルが`ERROR` [＃12373](https://github.com/pingcap/tidb/pull/12373)ときにスロークエリログが記録されない問題を修正しました
    -   TiDBがスキーマの変更とそれに対応する変更されたテーブル情報をキャッシュする回数を100から1024に調整し、 `tidb_max_delta_schema_count`システム変数[＃12515](https://github.com/pingcap/tidb/pull/12515)を使用して変更をサポートします。
    -   SQL統計をより正確にするために、クエリの開始時間を「実行開始」から「コンパイル開始」に変更します[＃12638](https://github.com/pingcap/tidb/pull/12638)
    -   TiDBログ[＃12568](https://github.com/pingcap/tidb/pull/12568)に`set session autocommit`のレコードを追加する
    -   プラン実行中にリセットされないようにSQLクエリの開始時刻を`SessionVars`に記録する[＃12676](https://github.com/pingcap/tidb/pull/12676)
    -   `ORDER BY` `GROUP BY` `?` [＃12514](https://github.com/pingcap/tidb/pull/12514)ホルダーをサポート`LIMIT OFFSET`
    -   最後のステートメントが`COMMIT` [＃12724](https://github.com/pingcap/tidb/pull/12724)ときに前のステートメントを出力するために、スロークエリログに`Prev_stmt`フィールドを追加します。
    -   明示的にコミットされたトランザクション[＃12747](https://github.com/pingcap/tidb/pull/12747)で`COMMIT`失敗した場合、 `COMMIT`の前の最後のステートメントをログに記録します。
    -   TiDBサーバーがSQL文を実行する際に、前の文の保存方法を最適化してパフォーマンスを向上します[＃12751](https://github.com/pingcap/tidb/pull/12751)
    -   `skip-grant-table=true`構成[＃12816](https://github.com/pingcap/tidb/pull/12816)の`FLUSH PRIVILEGES`ステートメントによって引き起こされるpanic問題を修正
    -   短時間に多数の書き込み要求があった場合にパフォーマンスのボトルネックを回避するために、AutoID を適用するデフォルトの最小ステップを`1000`から`30000`に増やします[＃12891](https://github.com/pingcap/tidb/pull/12891)
    -   TiDBがパニックになったときに失敗した`Prepared`文がエラーログに出力されない問題を修正しました[＃12954](https://github.com/pingcap/tidb/pull/12954)
    -   スロークエリログの`COM_STMT_FETCH`回限りのレコードがMySQL [＃12953](https://github.com/pingcap/tidb/pull/12953)ものと矛盾する問題を修正しました。
    -   書き込み競合のエラーメッセージにエラーコードを追加して、原因を素早く特定します[＃12878](https://github.com/pingcap/tidb/pull/12878)
-   DDL
    -   デフォルトでは、列の`AUTO INCREMENT`の属性の削除は許可されません。この属性を削除する必要がある場合は、 `tidb_allow_remove_auto_inc`の変数の値を変更してください。詳細は[システム変数](/system-variables.md#tidb_allow_remove_auto_inc-new-in-v2118-and-v304)参照してください[＃12146](https://github.com/pingcap/tidb/pull/12146)
    -   `Create Table`文[＃12469](https://github.com/pingcap/tidb/pull/12469)で一意のインデックスを作成するときに複数の`unique`をサポートする
    -   `CREATE TABLE`ステートメントの外部キー制約にスキーマがない場合、 `No Database selected`エラー[＃12678](https://github.com/pingcap/tidb/pull/12678)を返す代わりに、作成されたテーブルのスキーマを使用するという互換性の問題を修正しました。
    -   `ADMIN CANCEL DDL JOBS` [＃12681](https://github.com/pingcap/tidb/pull/12681)実行時に`invalid list index`エラーが報告される問題を修正
-   モニター
    -   バックオフ監視のタイプを追加し、コミット[＃12326](https://github.com/pingcap/tidb/pull/12326)のバックオフ時間など、これまで記録されていなかったバックオフ時間を補足します。
    -   `Add Index`操作の進行状況を監視するための新しいメトリックを追加する[＃12389](https://github.com/pingcap/tidb/pull/12389)

## PD {#pd}

-   pd-ctl [＃1772](https://github.com/pingcap/pd/pull/1772)の`--help`コマンド出力を改善する

## ツール {#tools}

-   TiDBBinlog
    -   `ALTER DATABASE`関連する DDL 操作によりDrainerが異常終了する問題を修正[＃770](https://github.com/pingcap/tidb-binlog/pull/770)
    -   レプリケーション効率を向上させるためにコミットbinlog のトランザクション ステータス情報のクエリをサポートする[＃761](https://github.com/pingcap/tidb-binlog/pull/761)
    -   ドレイナーの`start_ts`ポンプの最大値`commit_ts` [＃759](https://github.com/pingcap/tidb-binlog/pull/759)より大きい場合にPumppanicが発生する可能性がある問題を修正しました。

## TiDB アンシブル {#tidb-ansible}

-   TiDB Binlog [＃952](https://github.com/pingcap/tidb-ansible/pull/952)に「キューサイズ」と「クエリヒストグラム」の 2 つの監視項目を追加します。
-   TiDBアラートルール[＃961](https://github.com/pingcap/tidb-ansible/pull/961)を更新
-   展開およびアップグレードの前に構成ファイルを確認する[＃973](https://github.com/pingcap/tidb-ansible/pull/973)
-   TiDB [＃987](https://github.com/pingcap/tidb-ansible/pull/987)のインデックス速度を監視するための新しいメトリックを追加します
-   TiDB Binlog監視ダッシュボードを更新して、Grafana v4.6.3 [＃993](https://github.com/pingcap/tidb-ansible/pull/993)と互換性を持たせました。
