---
title: TiDB 2.1.18 Release Notes
---

# TiDB 2.1.18 リリースノート {#tidb-2-1-18-release-notes}

発売日：2019年11月4日

TiDB バージョン: 2.1.18

TiDB Ansible バージョン: 2.1.18

## TiDB {#tidb}

-   SQLオプティマイザー
    -   フィードバック[#12172](https://github.com/pingcap/tidb/pull/12172)で分割すると、無効なクエリ範囲が表示されることがある問題を修正します。
    -   ポイントゲットプラン[#12341](https://github.com/pingcap/tidb/pull/12341)の権限チェックが正しくない問題を修正
    -   Limit 演算子を`IndexLookUpReader`実行ロジックにプッシュダウンすることで、 `select ... limit ... offset …`ステートメントの実行パフォーマンスを最適化します[#12380](https://github.com/pingcap/tidb/pull/12380)
    -   `ORDER BY` 、 `GROUP BY` 、 `LIMIT OFFSET`のパラメータの使用をサポート[#12514](https://github.com/pingcap/tidb/pull/12514)
    -   パーティション テーブルの`IndexJoin`が間違った結果を返す問題を修正します[#12713](https://github.com/pingcap/tidb/pull/12713)
    -   日付文字列と形式文字列が一致しない場合、TiDB の関数`str_to_date` MySQL とは異なる結果を返す問題を修正します[#12757](https://github.com/pingcap/tidb/pull/12757)
    -   クエリ条件[#12791](https://github.com/pingcap/tidb/pull/12791)に関数`cast`が含まれる場合、外部結合が誤って内部結合に変換される問題を修正
    -   `AntiSemiJoin` [#12800](https://github.com/pingcap/tidb/pull/12800)の結合条件に渡される誤った式を修正しました。
-   SQLエンジン
    -   時刻の誤った丸めを修正します (たとえば、 `2019-09-11 11:17:47.999999666` `2019-09-11 11:17:48`に四捨五入する必要があります) [#12259](https://github.com/pingcap/tidb/pull/12259)
    -   監視レコード[#12329](https://github.com/pingcap/tidb/pull/12329)にステートメント`PREPARE`の`sql_type`による期間が表示されない問題を修正
    -   `from_unixtime`関数が null [#12572](https://github.com/pingcap/tidb/pull/12572)を処理するときのpanicの問題を修正
    -   無効な値が`YEAR`タイプとして挿入されると、結果が`0000` [#12744](https://github.com/pingcap/tidb/pull/12744)ではなく`NULL`なるという互換性の問題を修正しました。
    -   MySQL 自動インクリメント ロック ( [「連続」ロックモード](https://dev.mysql.com/doc/refman/5.7/en/innodb-auto-increment-handling.html) ) のデフォルト モードとの一貫性を維持するために、暗黙的に割り当てられたときの`AutoIncrement`カラムの動作を改善します。単一行`Insert`ステートメントでの複数の`AutoIncrement` ID の暗黙的割り当てについて、TiDB は割り当てられた値の連続性。この改善により、JDBC `getGeneratedKeys()`メソッドはどのシナリオでも正しい結果が得られるようになります[#12619](https://github.com/pingcap/tidb/pull/12619)
    -   `HashAgg` `Apply` [#12769](https://github.com/pingcap/tidb/pull/12769)の子ノードとして機能する場合にクエリがハングする問題を修正
    -   型変換[#12813](https://github.com/pingcap/tidb/pull/12813)に関して、 `AND`と`OR`の論理式が誤った結果を返す問題を修正
-   サーバ
    -   `SLEEP()`関数が`KILL TIDB QUERY`ステートメントに対して無効である問題を修正[#12159](https://github.com/pingcap/tidb/pull/12159)
    -   `AUTO_INCREMENT` `MAX int64`と`MAX uint64`誤って割り当てた場合にエラーが報告されない問題を修正[#12210](https://github.com/pingcap/tidb/pull/12210)
    -   ログレベルが`ERROR` [#12373](https://github.com/pingcap/tidb/pull/12373)の場合にスロークエリログが記録されない問題を修正
    -   TiDB がスキーマ変更および対応する変更されたテーブル情報をキャッシュする回数を 100 から 1024 まで調整し、 `tidb_max_delta_schema_count`システム変数[#12515](https://github.com/pingcap/tidb/pull/12515)を使用した変更をサポートします。
    -   SQL 統計をより正確にするために、クエリの開始時刻を「実行開始」時点から「コンパイル開始」時点に変更します[#12638](https://github.com/pingcap/tidb/pull/12638)
    -   TiDB ログ[#12568](https://github.com/pingcap/tidb/pull/12568)に`set session autocommit`のレコードを追加
    -   プランの実行中にリセットされないように、SQL クエリの開始時間を`SessionVars`に記録します[#12676](https://github.com/pingcap/tidb/pull/12676)
    -   `ORDER BY` 、 `GROUP BY` 、 `LIMIT OFFSET`で`?`プレースホルダーをサポート[#12514](https://github.com/pingcap/tidb/pull/12514)
    -   スロークエリログに`Prev_stmt`フィールドを追加して、最後のステートメントが`COMMIT` [#12724](https://github.com/pingcap/tidb/pull/12724)の場合に前のステートメントを出力します。
    -   明示的にコミットされたトランザクションで`COMMIT`失敗した場合、 `COMMIT`より前の最後のステートメントをログに記録します[#12747](https://github.com/pingcap/tidb/pull/12747)
    -   TiDBサーバーがSQL ステートメントを実行するときに前のステートメントの保存方法を最適化し、パフォーマンスを向上させます[#12751](https://github.com/pingcap/tidb/pull/12751)
    -   `skip-grant-table=true`構成[#12816](https://github.com/pingcap/tidb/pull/12816)の`FLUSH PRIVILEGES`ステートメントによって引き起こされるpanicの問題を修正
    -   短時間に多数の書き込み要求がある場合のパフォーマンスのボトルネックを回避するために、AutoID を適用するデフォルトの最小ステップを`1000`から`30000`に増やします[#12891](https://github.com/pingcap/tidb/pull/12891)
    -   TiDB パニック[#12954](https://github.com/pingcap/tidb/pull/12954)が発生したときに、失敗した`Prepared`ステートメントがエラー ログに出力されない問題を修正します。
    -   スロークエリログの`COM_STMT_FETCH`回のレコードが MySQL [#12953](https://github.com/pingcap/tidb/pull/12953)のレコードと一致しない問題を修正
    -   原因を迅速に特定するために、書き込み競合のエラー メッセージにエラー コードを追加します[#12878](https://github.com/pingcap/tidb/pull/12878)
-   DDL
    -   デフォルトでは、列の`AUTO INCREMENT`属性の削除は禁止されています。この属性を削除する必要がある場合は、変数`tidb_allow_remove_auto_inc`値を変更します。詳細については、 [システム変数](/system-variables.md#tidb_allow_remove_auto_inc-new-in-v2118-and-v304)参照してください。 [#12146](https://github.com/pingcap/tidb/pull/12146)
    -   `Create Table`ステートメントで一意のインデックスを作成するときに複数の`unique`をサポートします[#12469](https://github.com/pingcap/tidb/pull/12469)
    -   `CREATE TABLE`ステートメントの外部キー制約にスキーマがない場合、 `No Database selected`エラー[#12678](https://github.com/pingcap/tidb/pull/12678)を返す代わりに、作成されたテーブルのスキーマを使用する必要があるという互換性の問題を修正しました。
    -   `ADMIN CANCEL DDL JOBS` [#12681](https://github.com/pingcap/tidb/pull/12681)を実行すると`invalid list index`エラーが報告される問題を修正
-   モニター
    -   バックオフ監視のタイプを追加し、コミット時のバックオフ時間など、以前に記録されていないバックオフ時間を補足します[#12326](https://github.com/pingcap/tidb/pull/12326)
    -   監視する新しいメトリクスを追加`Add Index`操作の進行状況[#12389](https://github.com/pingcap/tidb/pull/12389)

## PD {#pd}

-   pd-ctl [#1772](https://github.com/pingcap/pd/pull/1772)の`--help`コマンド出力を改善

## ツール {#tools}

-   TiDBBinlog
    -   `ALTER DATABASE`関連する DDL 操作によりDrainerが異常終了する問題を修正します[#770](https://github.com/pingcap/tidb-binlog/pull/770)
    -   レプリケーション効率を向上させるために、コミットbinlogのトランザクション ステータス情報のクエリをサポートします[#761](https://github.com/pingcap/tidb-binlog/pull/761)
    -   ドレイナーの`start_ts`ポンプの最大値`commit_ts` [#759](https://github.com/pingcap/tidb-binlog/pull/759)より大きい場合にPumppanicが発生することがある問題を修正

## TiDB Ansible {#tidb-ansible}

-   TiDB Binlog [#952](https://github.com/pingcap/tidb-ansible/pull/952)に「キューサイズ」と「クエリヒストグラム」の2つの監視項目を追加
-   TiDB アラート ルールの更新[#961](https://github.com/pingcap/tidb-ansible/pull/961)
-   導入およびアップグレードの前に構成ファイルを確認する[#973](https://github.com/pingcap/tidb-ansible/pull/973)
-   TiDB [#987](https://github.com/pingcap/tidb-ansible/pull/987)のインデックス速度を監視するための新しいメトリクスを追加します
-   TiDB Binlogモニタリング ダッシュボードを更新して Grafana v4.6.3 と互換性を持たせる[#993](https://github.com/pingcap/tidb-ansible/pull/993)
