---
title: TiDB 2.1.18 Release Notes
---

# TiDB2.1.18リリースノート {#tidb-2-1-18-release-notes}

発売日：2019年11月4日

TiDBバージョン：2.1.18

TiDB Ansibleバージョン：2.1.18

## TiDB {#tidb}

-   SQLオプティマイザー
    -   フィードバックによって分割されたときに無効なクエリ範囲が表示される可能性がある問題を修正します[＃12172](https://github.com/pingcap/tidb/pull/12172)
    -   ポイント取得プラン[＃12341](https://github.com/pingcap/tidb/pull/12341)で特権チェックが正しくない問題を修正します
    -   Limit演算子を`IndexLookUpReader`実行ロジック[＃12380](https://github.com/pingcap/tidb/pull/12380)にプッシュすることにより、 `select ... limit ... offset …`ステートメントの実行パフォーマンスを最適化します。
    -   `ORDER BY` 、および`GROUP BY`での[＃12514](https://github.com/pingcap/tidb/pull/12514)の使用の`LIMIT OFFSET`
    -   パーティションテーブルの`IndexJoin`が誤った結果を返す問題を修正します[＃12713](https://github.com/pingcap/tidb/pull/12713)
    -   日付文字列とフォーマット文字列が[＃12757](https://github.com/pingcap/tidb/pull/12757)と一致しない場合、TiDBの`str_to_date`関数がMySQLとは異なる結果を返す問題を修正します。
    -   `cast`関数がクエリ条件に含まれている場合に外部結合が誤って内部結合に変換される問題を修正します[＃12791](https://github.com/pingcap/tidb/pull/12791)
    -   [＃12800](https://github.com/pingcap/tidb/pull/12800)の結合条件で渡される誤った`AntiSemiJoin`を修正しました
-   SQLエンジン
    -   時間の誤った丸めを修正します（たとえば、 `2019-09-11 11:17:47.999999666`を`2019-09-11 11:17:48`に丸める必要があります） [＃12259](https://github.com/pingcap/tidb/pull/12259)
    -   `PREPARE`ステートメントの期間が`sql_type`だけ、監視レコード[＃12329](https://github.com/pingcap/tidb/pull/12329)に表示されない問題を修正します。
    -   `from_unixtime`関数がnull3を処理するときのパニックの問題を修正し[＃12572](https://github.com/pingcap/tidb/pull/12572)
    -   無効な値が`YEAR`タイプとして挿入された場合、結果が[＃12744](https://github.com/pingcap/tidb/pull/12744)ではなく`NULL`になるという互換性の問題を修正し`0000` 。
    -   暗黙的に割り当てられた場合の`AutoIncrement`列の動作を改善し、MySQL自動インクリメントロックのデフォルトモードとの一貫性を維持します（ [「連続」ロックモード](https://dev.mysql.com/doc/refman/5.7/en/innodb-auto-increment-handling.html) ）。単一行の`Insert`ステートメントで複数の`AutoIncrement` IDを暗黙的に割り当てる場合、TiDBは割り当てられた値の連続性。この改善により、 `getGeneratedKeys()`メソッドがどのシナリオでも正しい結果を得ることが保証されます[＃12619](https://github.com/pingcap/tidb/pull/12619)
    -   `HashAgg`が[＃12769](https://github.com/pingcap/tidb/pull/12769)の子ノードとして機能するときにクエリがハングする問題を修正し`Apply`
    -   型変換[＃12813](https://github.com/pingcap/tidb/pull/12813)に関して、 `AND`と`OR`の論理式が誤った結果を返す問題を修正します。
-   サーバ
    -   `SLEEP()`の関数が`KILL TIDB QUERY`のステートメントに対して無効であるという問題を修正します[＃12159](https://github.com/pingcap/tidb/pull/12159)
    -   `AUTO_INCREMENT`が`MAX int64`と[＃12210](https://github.com/pingcap/tidb/pull/12210)を誤って割り当てたときにエラーが報告されない問題を修正し`MAX uint64` 。
    -   ログレベルが`ERROR`の場合、低速クエリログが記録されない問題を修正し[＃12373](https://github.com/pingcap/tidb/pull/12373) 。
    -   TiDBがスキーマの変更と対応する変更されたテーブル情報を100から1024にキャッシュする回数を調整し、 `tidb_max_delta_schema_count`のシステム変数[＃12515](https://github.com/pingcap/tidb/pull/12515)を使用して変更をサポートします。
    -   SQL統計をより正確にするために、クエリの開始時刻を「実行の開始」から「コンパイルの開始」に変更します[＃12638](https://github.com/pingcap/tidb/pull/12638)
    -   TiDBログ[＃12568](https://github.com/pingcap/tidb/pull/12568)に`set session autocommit`のレコードを追加します
    -   SQLクエリの開始時刻を`SessionVars`に記録して、プランの実行中にリセットされないようにします[＃12676](https://github.com/pingcap/tidb/pull/12676)
    -   `ORDER BY` 、および[＃12514](https://github.com/pingcap/tidb/pull/12514)で`?` `GROUP BY`プレースホルダーをサポートし`LIMIT OFFSET`
    -   最後のステートメントが[＃12724](https://github.com/pingcap/tidb/pull/12724)の場合に前のステートメントを出力するには、低速クエリログに`Prev_stmt`フィールドを追加し`COMMIT`
    -   明示的にコミットされたトランザクション[＃12747](https://github.com/pingcap/tidb/pull/12747)で`COMMIT`が失敗した場合、 `COMMIT`より前の最後のステートメントをログに記録します。
    -   TiDBサーバーがSQLステートメントを実行するときに、前のステートメントの保存方法を最適化して、パフォーマンスを向上させます[＃12751](https://github.com/pingcap/tidb/pull/12751)
    -   `skip-grant-table=true`の構成で`FLUSH PRIVILEGES`のステートメントによって引き起こされるパニックの問題を修正します[＃12816](https://github.com/pingcap/tidb/pull/12816)
    -   AutoIDを適用するデフォルトの最小ステップを`1000`から`30000`に増やして、短時間に多数の書き込み要求がある場合のパフォーマンスのボトルネックを回避します[＃12891](https://github.com/pingcap/tidb/pull/12891)
    -   TiDBがパニックになったときに失敗した`Prepared`ステートメントがエラーログに出力されない問題を修正します[＃12954](https://github.com/pingcap/tidb/pull/12954)
    -   遅いクエリログの`COM_STMT_FETCH`回のレコードがMySQL3のレコードと矛盾する問題を修正し[＃12953](https://github.com/pingcap/tidb/pull/12953)
    -   書き込みの競合のエラーメッセージにエラーコードを追加して、原因をすばやく特定します[＃12878](https://github.com/pingcap/tidb/pull/12878)
-   DDL
    -   デフォルトでは、列の`AUTO INCREMENT`属性の削除を禁止します。この属性を削除する必要がある場合は、 `tidb_allow_remove_auto_inc`変数の値を変更してください。詳細については、 [システム変数](/system-variables.md#tidb_allow_remove_auto_inc-new-in-v2118-and-v304)を参照してください。 [＃12146](https://github.com/pingcap/tidb/pull/12146)
    -   `Create Table`ステートメントで一意のインデックスを作成するときに複数の`unique`をサポートする[＃12469](https://github.com/pingcap/tidb/pull/12469)
    -   `CREATE TABLE`ステートメントの外部キー制約にスキーマがない場合、 `No Database selected`エラー[＃12678](https://github.com/pingcap/tidb/pull/12678)を返す代わりに、作成されたテーブルのスキーマを使用する必要があるという互換性の問題を修正します。
    -   [＃12681](https://github.com/pingcap/tidb/pull/12681)の実行時に`invalid list index`エラーが報告される問題を修正し`ADMIN CANCEL DDL JOBS`
-   モニター
    -   バックオフ監視のタイプを追加し、コミット時のバックオフ時間など、以前に記録されなかったバックオフ時間を補足します[＃12326](https://github.com/pingcap/tidb/pull/12326)
    -   新しいメトリックを追加して、 `Add Index`の操作の進行状況を監視します[＃12389](https://github.com/pingcap/tidb/pull/12389)

## PD {#pd}

-   pd- [＃1772](https://github.com/pingcap/pd/pull/1772)の`--help`コマンド出力を改善

## ツール {#tools}

-   TiDB Binlog
    -   `ALTER DATABASE`の関連するDDL操作によってDrainerが異常終了する問題を修正します[＃770](https://github.com/pingcap/tidb-binlog/pull/770)
    -   レプリケーション効率を向上させるために、コミットbinlogのトランザクションステータス情報のクエリをサポートする[＃761](https://github.com/pingcap/tidb-binlog/pull/761)
    -   [＃759](https://github.com/pingcap/tidb-binlog/pull/759)の`start_ts`がPumpの最大の35より大きい場合にPumpパニックが発生する可能性がある問題を修正し`commit_ts`

## TiDB Ansible {#tidb-ansible}

-   TiDBBinlog1の[＃952](https://github.com/pingcap/tidb-ansible/pull/952)つの監視項目「キューサイズ」と「クエリヒストグラム」を追加します。
-   TiDBアラートルールを更新する[＃961](https://github.com/pingcap/tidb-ansible/pull/961)
-   展開とアップグレードの前に構成ファイルを確認してください[＃973](https://github.com/pingcap/tidb-ansible/pull/973)
-   TiDB1のインデックス速度を監視するための新しいメトリックを追加し[＃987](https://github.com/pingcap/tidb-ansible/pull/987)
-   TiDBBinlogモニタリングダッシュボードを更新して[＃993](https://github.com/pingcap/tidb-ansible/pull/993)と互換性を持たせる
